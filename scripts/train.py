"""Two-phase training to embed Cocos2d-x API knowledge into the model.

Phase 1 — Continued pre-training (CPT): full-text loss on docs + QA pairs.
  The model learns API vocabulary, patterns, and associations from both
  instructions and responses. This embeds knowledge.

Phase 2 — Supervised fine-tuning (SFT): response-only loss on QA pairs.
  The model learns to follow the instruction→response format.
  Instruction tokens are masked with -100.
"""
import glob
import os
import torch
from dataclasses import dataclass
from typing import List, Dict, Any
from datasets import Dataset, load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    Trainer,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

from scripts.config import (
    BATCH_SIZE,
    CPT_EPOCHS,
    CPT_LEARNING_RATE,
    DOCS_GLOB,
    DRIVE_ADAPTER,
    DRIVE_CHECKPOINTS,
    EVAL_STEPS,
    GRAD_ACCUM_STEPS,
    LORA_ALPHA,
    LORA_DROPOUT,
    LORA_R,
    LORA_TARGET_MODULES,
    MAX_SEQ_LENGTH,
    MODEL_ID,
    NEFTUNE_NOISE_ALPHA,
    REPLAY_JSONL,
    REPLAY_RATIO,
    SAVE_STEPS,
    SAVE_TOTAL_LIMIT,
    SFT_EPOCHS,
    SFT_LEARNING_RATE,
    SYNTHETIC_QA_JSONL,
    TEST_JSONL,
    TRAIN_JSONL,
    USE_DORA,
    WARMUP_RATIO,
    WEIGHT_DECAY,
    ALPACA_PROMPT,
    ALPACA_TEMPLATE,
    ensure_drive_dirs,
)


@dataclass
class LabelPreservingCollator:
    """Pads batch to max length, preserving pre-computed labels."""

    tokenizer: Any
    max_length: int = MAX_SEQ_LENGTH

    def __call__(self, features: List[Dict]) -> Dict[str, torch.Tensor]:
        pad_id = self.tokenizer.pad_token_id
        batch = {}
        for key in ("input_ids", "attention_mask", "labels"):
            seqs = [f[key] for f in features]
            pad_val = -100 if key == "labels" else (0 if key == "attention_mask" else pad_id)
            max_len = min(max(len(s) for s in seqs), self.max_length)
            padded = []
            for s in seqs:
                diff = max_len - len(s)
                padded.append(s + [pad_val] * diff if diff > 0 else s[:max_len])
            batch[key] = torch.tensor(padded, dtype=torch.long)
        return batch


# ── Data loading ──────────────────────────────────────────────────────


def load_data():
    """Load and combine all training sources with replay mixing."""
    from datasets import concatenate_datasets
    import random

    # Core domain data (hand-crafted + augmented)
    train_ds = load_dataset("json", data_files=TRAIN_JSONL, split="train")
    test_ds = load_dataset("json", data_files=TEST_JSONL, split="train")
    print(f"Core train: {len(train_ds)}, Test: {len(test_ds)}")

    # Synthetic QA from docs
    if os.path.exists(SYNTHETIC_QA_JSONL):
        synth = load_dataset("json", data_files=SYNTHETIC_QA_JSONL, split="train")
        # Remove 'input' column if present (some generators add it)
        if "input" in synth.column_names:
            synth = synth.remove_columns("input")
        print(f"Synthetic QA: {len(synth)}")
        train_ds = concatenate_datasets([train_ds, synth])

    # General replay data to prevent catastrophic forgetting
    if os.path.exists(REPLAY_JSONL):
        replay = load_dataset("json", data_files=REPLAY_JSONL, split="train")
        # Sample to target ratio relative to domain data
        n_replay = int(len(train_ds) * REPLAY_RATIO / (1 - REPLAY_RATIO))
        n_replay = min(n_replay, len(replay))
        replay = replay.shuffle(seed=42).select(range(n_replay))
        print(f"Replay (general): {len(replay)}")
        train_ds = concatenate_datasets([train_ds, replay])

    train_ds = train_ds.shuffle(seed=42)
    print(f"Total train: {len(train_ds)}, Test: {len(test_ds)}")
    return train_ds, test_ds


def load_docs_as_chunks():
    """Load markdown docs and split into chunks for continued pre-training."""
    doc_files = sorted(glob.glob(DOCS_GLOB))
    chunks = []
    for fpath in doc_files:
        with open(fpath, encoding="utf-8") as f:
            text = f.read()
        # Split on double newline (section boundaries)
        sections = [s.strip() for s in text.split("\n\n") if s.strip()]
        # Merge small sections into chunks of ~800 chars
        current = ""
        for section in sections:
            if len(current) + len(section) > 800 and current:
                chunks.append(current)
                current = section
            else:
                current = current + "\n\n" + section if current else section
        if current:
            chunks.append(current)
    print(f"Loaded {len(chunks)} doc chunks from {len(doc_files)} files")
    return chunks


# ── Model loading ─────────────────────────────────────────────────────


def load_model_and_tokenizer():
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    # Dedicated pad token — never reuse eos_token
    if tokenizer.pad_token is None or tokenizer.pad_token == tokenizer.eos_token:
        tokenizer.add_special_tokens({"pad_token": "<|pad|>"})
    tokenizer.padding_side = "right"

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model.resize_token_embeddings(len(tokenizer))
    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        target_modules=LORA_TARGET_MODULES,
        lora_dropout=LORA_DROPOUT,
        bias="none",
        task_type="CAUSAL_LM",
        use_dora=USE_DORA,
    )
    model = get_peft_model(model, lora_config)
    model.gradient_checkpointing_enable()
    model.print_trainable_parameters()
    return model, tokenizer


# ── Tokenization ──────────────────────────────────────────────────────


def _tokenize_full_text(tokenizer, text):
    """Tokenize with full-text labels (for CPT). Loss on every token."""
    eos_id = tokenizer.eos_token_id
    tokens = tokenizer(
        text, truncation=True,
        max_length=MAX_SEQ_LENGTH - 1, padding=False,
    )
    tokens["input_ids"] = tokens["input_ids"] + [eos_id]
    tokens["attention_mask"] = tokens["attention_mask"] + [1]
    tokens["labels"] = list(tokens["input_ids"])
    return tokens


def _tokenize_instruction_masked(tokenizer, instruction, output):
    """Tokenize with instruction masked (for SFT). Loss only on response."""
    eos_id = tokenizer.eos_token_id
    prompt = ALPACA_PROMPT.format(instruction=instruction)
    full_text = ALPACA_TEMPLATE.format(
        instruction=instruction, output=output,
    )
    tokens = tokenizer(
        full_text, truncation=True,
        max_length=MAX_SEQ_LENGTH - 1, padding=False,
    )
    tokens["input_ids"] = tokens["input_ids"] + [eos_id]
    tokens["attention_mask"] = tokens["attention_mask"] + [1]
    prompt_tokens = tokenizer(prompt, truncation=True, max_length=MAX_SEQ_LENGTH)
    prompt_len = len(prompt_tokens["input_ids"])
    labels = [-100] * prompt_len + tokens["input_ids"][prompt_len:]
    tokens["labels"] = labels
    return tokens


def tokenize_for_cpt(train_ds, test_ds, tokenizer):
    """Phase 1 tokenization: full-text loss on QA pairs + doc chunks."""
    doc_chunks = load_docs_as_chunks()

    # QA pairs as full text (loss on everything including instruction)
    def tok_qa_full(example):
        full = ALPACA_TEMPLATE.format(
            instruction=example["instruction"],
            output=example["output"],
        )
        return _tokenize_full_text(tokenizer, full)

    # Doc chunks as plain text
    def tok_doc(chunk_text):
        return _tokenize_full_text(tokenizer, chunk_text)

    train_qa = train_ds.map(tok_qa_full, remove_columns=train_ds.column_names)
    test_tok = test_ds.map(tok_qa_full, remove_columns=test_ds.column_names)

    # Tokenize doc chunks into a Dataset
    doc_records = [tok_doc(c) for c in doc_chunks]
    if doc_records:
        doc_ds = Dataset.from_list(doc_records)
        from datasets import concatenate_datasets
        train_tok = concatenate_datasets([train_qa, doc_ds]).shuffle(seed=42)
    else:
        train_tok = train_qa

    print(f"CPT data — Train: {len(train_tok)} (QA: {len(train_qa)}, docs: {len(doc_records)}), Test: {len(test_tok)}")
    return train_tok, test_tok


def tokenize_for_sft(train_ds, test_ds, tokenizer):
    """Phase 2: RAFT-style SFT — train with retrieved context + distractors.

    RAFT (Retrieval-Augmented Fine-Tuning) teaches the model to:
    - Extract answers from relevant docs (oracle examples, ~70%)
    - Refuse to hallucinate when no relevant doc is provided (distractor-only, ~30%)
    This produces a model that works well both standalone and with RAG at inference.
    """
    from scripts.config import (
        RAG_PROMPT, RAFT_ORACLE_RATIO, RAFT_NUM_DISTRACTORS,
    )
    import random as _random
    _random.seed(42)

    doc_chunks = load_docs_as_chunks()

    def _find_relevant_chunk(instruction):
        """Simple keyword overlap to find the most relevant doc chunk."""
        inst_lower = instruction.lower()
        # Extract API names from instruction
        import re
        apis = re.findall(r'\b(?:cc|ccui|sp|ccs)\.[a-zA-Z_.]+', inst_lower)
        best_score, best_chunk = 0, None
        for chunk in doc_chunks:
            chunk_lower = chunk.lower()
            score = sum(1 for api in apis if api in chunk_lower)
            # Also check for keyword overlap
            words = set(inst_lower.split()) - {"the", "a", "is", "what", "how", "does", "of", "in", "to"}
            score += sum(0.1 for w in words if w in chunk_lower and len(w) > 3)
            if score > best_score:
                best_score = score
                best_chunk = chunk
        return best_chunk if best_score > 0.5 else None

    def _get_distractors(exclude_chunk, n):
        """Get n random doc chunks that aren't the oracle."""
        pool = [c for c in doc_chunks if c != exclude_chunk]
        return _random.sample(pool, min(n, len(pool)))

    def tok_raft(example, idx):
        instruction = example["instruction"]
        output = example["output"]

        oracle = _find_relevant_chunk(instruction)
        use_oracle = _random.random() < RAFT_ORACLE_RATIO and oracle

        if oracle and doc_chunks:
            distractors = _get_distractors(oracle, RAFT_NUM_DISTRACTORS)
            if use_oracle:
                # Oracle + distractors — model learns to find answer in context
                chunks = [oracle] + distractors
                _random.shuffle(chunks)
            else:
                # Distractors only — model learns to use internal knowledge
                chunks = _get_distractors(None, RAFT_NUM_DISTRACTORS + 1)

            context = "\n---\n".join(c[:300] for c in chunks)  # truncate chunks
            prompt = RAG_PROMPT.format(context=context, instruction=instruction)
            full_text = prompt + output
        else:
            # No context available — plain instruction format
            prompt = ALPACA_PROMPT.format(instruction=instruction)
            full_text = ALPACA_TEMPLATE.format(
                instruction=instruction, output=output,
            )

        # Tokenize and mask prompt
        eos_id = tokenizer.eos_token_id
        tokens = tokenizer(
            full_text, truncation=True,
            max_length=MAX_SEQ_LENGTH - 1, padding=False,
        )
        tokens["input_ids"] = tokens["input_ids"] + [eos_id]
        tokens["attention_mask"] = tokens["attention_mask"] + [1]

        prompt_tokens = tokenizer(
            prompt, truncation=True, max_length=MAX_SEQ_LENGTH,
        )
        prompt_len = len(prompt_tokens["input_ids"])
        labels = [-100] * prompt_len + tokens["input_ids"][prompt_len:]
        tokens["labels"] = labels
        return tokens

    train_tok = train_ds.map(
        tok_raft, with_indices=True,
        remove_columns=train_ds.column_names,
    )
    # Test set: plain format (no RAFT) for clean eval
    def tok_masked(example):
        return _tokenize_instruction_masked(
            tokenizer, example["instruction"], example["output"],
        )
    test_tok = test_ds.map(tok_masked, remove_columns=test_ds.column_names)
    print(f"SFT data (RAFT) — Train: {len(train_tok)}, Test: {len(test_tok)}")
    return train_tok, test_tok


# Legacy alias
def tokenize_datasets(train_ds, test_ds, tokenizer):
    return tokenize_for_sft(train_ds, test_ds, tokenizer)


# ── Training ──────────────────────────────────────────────────────────


def _make_trainer(model, tokenizer, train_tok, test_tok, output_dir,
                  num_epochs, learning_rate):
    """Create a Trainer with the given hyperparameters."""
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM_STEPS,
        learning_rate=learning_rate,
        weight_decay=WEIGHT_DECAY,
        warmup_ratio=WARMUP_RATIO,
        lr_scheduler_type="cosine",
        fp16=True,
        gradient_checkpointing=True,
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=EVAL_STEPS,
        save_strategy="steps",
        save_steps=SAVE_STEPS,
        save_total_limit=SAVE_TOTAL_LIMIT,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        report_to="none",
        dataloader_pin_memory=False,
        neftune_noise_alpha=NEFTUNE_NOISE_ALPHA,
    )
    return Trainer(
        model=model,
        args=training_args,
        train_dataset=train_tok,
        eval_dataset=test_tok,
        data_collator=LabelPreservingCollator(tokenizer),
    )


def _resume_or_start(trainer, checkpoint_dir):
    """Resume from latest checkpoint if available."""
    checkpoints = sorted(glob.glob(f"{checkpoint_dir}/checkpoint-*"))
    resume_path = checkpoints[-1] if checkpoints else None
    if resume_path:
        print(f"  Resuming from {resume_path}")
    else:
        print("  Starting fresh")
    trainer.train(resume_from_checkpoint=resume_path)
    return trainer


def run_phase1_cpt(model, tokenizer, train_ds, test_ds):
    """Phase 1: Continued pre-training with full-text loss."""
    ensure_drive_dirs()
    cpt_dir = f"{DRIVE_CHECKPOINTS}/phase1-cpt"
    os.makedirs(cpt_dir, exist_ok=True)

    print("=" * 60)
    print("PHASE 1: Continued Pre-Training (full-text loss)")
    print("=" * 60)

    train_tok, test_tok = tokenize_for_cpt(train_ds, test_ds, tokenizer)
    trainer = _make_trainer(
        model, tokenizer, train_tok, test_tok,
        output_dir=cpt_dir,
        num_epochs=CPT_EPOCHS,
        learning_rate=CPT_LEARNING_RATE,
    )
    _resume_or_start(trainer, cpt_dir)
    return trainer


def run_phase2_sft(model, tokenizer, train_ds, test_ds):
    """Phase 2: Supervised fine-tuning with response-only loss."""
    ensure_drive_dirs()
    sft_dir = f"{DRIVE_CHECKPOINTS}/phase2-sft"
    os.makedirs(sft_dir, exist_ok=True)

    print("=" * 60)
    print("PHASE 2: Supervised Fine-Tuning (response-only loss)")
    print("=" * 60)

    train_tok, test_tok = tokenize_for_sft(train_ds, test_ds, tokenizer)
    trainer = _make_trainer(
        model, tokenizer, train_tok, test_tok,
        output_dir=sft_dir,
        num_epochs=SFT_EPOCHS,
        learning_rate=SFT_LEARNING_RATE,
    )
    _resume_or_start(trainer, sft_dir)
    return trainer


def run_two_phase_training(model, tokenizer, train_ds, test_ds):
    """Run both phases sequentially. Returns the Phase 2 trainer."""
    run_phase1_cpt(model, tokenizer, train_ds, test_ds)
    trainer = run_phase2_sft(model, tokenizer, train_ds, test_ds)
    return trainer


# Legacy single-phase entry point (backward compat)
def run_training(model, tokenizer, train_tok, test_tok):
    ensure_drive_dirs()
    trainer = _make_trainer(
        model, tokenizer, train_tok, test_tok,
        output_dir=DRIVE_CHECKPOINTS,
        num_epochs=SFT_EPOCHS,
        learning_rate=SFT_LEARNING_RATE,
    )
    _resume_or_start(trainer, DRIVE_CHECKPOINTS)
    return trainer


# ── Save / Evaluate ──────────────────────────────────────────────────


def save_adapter(model, tokenizer):
    ensure_drive_dirs()
    model.save_pretrained(DRIVE_ADAPTER)
    tokenizer.save_pretrained(DRIVE_ADAPTER)
    print(f"Adapter saved to {DRIVE_ADAPTER}")


def evaluate_loss(trainer):
    eval_results = trainer.evaluate()
    loss = eval_results["eval_loss"]
    ppl = 2 ** loss
    print(f"Test Loss: {loss:.4f}")
    print(f"Test Perplexity: {ppl:.2f}")
    return eval_results
