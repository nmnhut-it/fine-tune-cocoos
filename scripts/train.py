"""Training logic — called from the notebook."""
import glob
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

from scripts.config import (
    BATCH_SIZE,
    DRIVE_ADAPTER,
    DRIVE_CHECKPOINTS,
    EVAL_STEPS,
    GRAD_ACCUM_STEPS,
    LEARNING_RATE,
    LORA_ALPHA,
    LORA_DROPOUT,
    LORA_R,
    LORA_TARGET_MODULES,
    MAX_SEQ_LENGTH,
    MODEL_ID,
    NUM_EPOCHS,
    SAVE_STEPS,
    SAVE_TOTAL_LIMIT,
    TEST_JSONL,
    TRAIN_JSONL,
    WARMUP_RATIO,
    ALPACA_TEMPLATE,
    ensure_drive_dirs,
)


def load_data():
    train_ds = load_dataset("json", data_files=TRAIN_JSONL, split="train")
    test_ds = load_dataset("json", data_files=TEST_JSONL, split="train")
    print(f"Train: {len(train_ds)}, Test: {len(test_ds)}")
    return train_ds, test_ds


def load_model_and_tokenizer():
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        target_modules=LORA_TARGET_MODULES,
        lora_dropout=LORA_DROPOUT,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.gradient_checkpointing_enable()
    model.print_trainable_parameters()
    return model, tokenizer


def tokenize_datasets(train_ds, test_ds, tokenizer):
    def format_and_tokenize(example):
        # Build the prompt (instruction part) and full text separately
        prompt = ALPACA_PROMPT.format(instruction=example["instruction"])
        full_text = ALPACA_TEMPLATE.format(
            instruction=example["instruction"],
            output=example["output"],
        )
        tokens = tokenizer(
            full_text,
            truncation=True,
            max_length=MAX_SEQ_LENGTH,
            padding="max_length",
        )
        # Find where the response starts — mask instruction tokens with -100
        prompt_tokens = tokenizer(prompt, truncation=True, max_length=MAX_SEQ_LENGTH)
        prompt_len = len(prompt_tokens["input_ids"])
        labels = [-100] * prompt_len + tokens["input_ids"][prompt_len:]
        # Pad labels to match input length, mask padding too
        labels = labels[:len(tokens["input_ids"])]
        labels = [l if tokens["attention_mask"][i] == 1 else -100 for i, l in enumerate(labels)]
        tokens["labels"] = labels
        return tokens

    train_tok = train_ds.map(format_and_tokenize, remove_columns=train_ds.column_names)
    test_tok = test_ds.map(format_and_tokenize, remove_columns=test_ds.column_names)
    print(f"Tokenized — Train: {len(train_tok)}, Test: {len(test_tok)}")
    return train_tok, test_tok


def run_training(model, tokenizer, train_tok, test_tok):
    ensure_drive_dirs()

    training_args = TrainingArguments(
        output_dir=DRIVE_CHECKPOINTS,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM_STEPS,
        learning_rate=LEARNING_RATE,
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
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_tok,
        eval_dataset=test_tok,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    # Resume from latest checkpoint if available
    checkpoints = sorted(glob.glob(f"{DRIVE_CHECKPOINTS}/checkpoint-*"))
    resume_path = checkpoints[-1] if checkpoints else None
    if resume_path:
        print(f"Resuming from {resume_path}")
    else:
        print("Starting fresh training")

    trainer.train(resume_from_checkpoint=resume_path)
    return trainer


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
