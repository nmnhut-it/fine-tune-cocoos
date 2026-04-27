"""Evaluation pipeline: fine-tuned vs RAG baseline.

Metrics:
  1. API Symbol Checker  — hallucinated vs valid vs missing symbols
  2. CodeBLEU            — syntax-aware similarity (replaces BLEU/ROUGE)
  3. Claude Judge        — semantic correctness scored 1-5 with reasoning,
                           uses prompt caching on doc sections (~$0.001/example)
"""
import glob
import json
import os
import re

import numpy as np
import torch
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

from scripts.config import (
    ALPACA_PROMPT,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DOCS_GLOB,
    DRIVE_ADAPTER,
    DRIVE_MODEL,
    EMBED_MODEL,
    EVAL_CHART_PATH,
    EVAL_REPORT_PATH,
    EVAL_RESULTS_PATH,
    MAX_NEW_TOKENS,
    MODEL_ID,
    RAG_PROMPT,
    RAG_TOP_K,
    TEMPERATURE,
    TEST_JSONL,
    TOP_P,
    USE_FULL_FINETUNE,
)

# ── Symbol whitelist ────────────────────────────────────────────────────

_SYMBOL_WHITELIST = None
_SYMBOL_PATTERN = re.compile(r"\b((?:cc|ccui|ccs|sp)\.[A-Za-z][A-Za-z0-9_.]*)")


def _load_whitelist():
    global _SYMBOL_WHITELIST
    if _SYMBOL_WHITELIST is None:
        path = "data/api_symbols.json"
        if os.path.exists(path):
            _SYMBOL_WHITELIST = set(json.load(open(path))["symbols"])
        else:
            _SYMBOL_WHITELIST = set()
            print("WARNING: data/api_symbols.json not found — run scripts/build_symbol_whitelist.py")
    return _SYMBOL_WHITELIST


def check_symbols(prediction, reference):
    """Check API symbols against whitelist; detect hallucinations and missing symbols."""
    whitelist = _load_whitelist()
    pred_syms = set(_SYMBOL_PATTERN.findall(prediction))
    ref_syms = set(_SYMBOL_PATTERN.findall(reference))
    hallucinated = pred_syms - whitelist
    valid_pred = pred_syms & whitelist
    precision = len(valid_pred) / len(pred_syms) if pred_syms else 1.0
    recall = len(ref_syms & pred_syms) / len(ref_syms) if ref_syms else None
    f1 = (2 * precision * recall / (precision + recall)
          if recall is not None and (precision + recall) > 0 else None)
    return {
        "hallucinated_symbols": sorted(hallucinated),
        "valid_symbols": sorted(valid_pred),
        "missing_symbols": sorted(ref_syms - pred_syms),
        "symbol_precision": round(precision, 4),
        "symbol_recall": round(recall, 4) if recall is not None else None,
        "symbol_f1": round(f1, 4) if f1 is not None else None,
        "has_hallucination": len(hallucinated) > 0,
    }


# ── CodeBLEU ────────────────────────────────────────────────────────────

def compute_codebleu(prediction, reference, lang="javascript"):
    """Syntax-aware code similarity. Returns None if codebleu package not installed."""
    try:
        from codebleu import calc_codebleu
        result = calc_codebleu([reference], [prediction], lang=lang,
                               weights=(0.25, 0.25, 0.25, 0.25))
        return round(result["codebleu"], 4)
    except Exception:
        return None


# ── Claude Judge ────────────────────────────────────────────────────────

_DOC_CACHE = None


def _load_docs():
    global _DOC_CACHE
    if _DOC_CACHE is None:
        _DOC_CACHE = {}
        for fpath in sorted(glob.glob(DOCS_GLOB)):
            name = os.path.basename(fpath).replace(".md", "")
            _DOC_CACHE[name] = open(fpath, encoding="utf-8").read()
    return _DOC_CACHE


def _pick_relevant_doc(instruction, prediction):
    """Select the 1-2 most relevant doc sections by symbol overlap."""
    docs = _load_docs()
    text = instruction + " " + prediction
    syms = _SYMBOL_PATTERN.findall(text)
    scores = {}
    for sym in syms:
        ns = sym.split(".")[0]
        for doc_name, doc_text in docs.items():
            if sym in doc_text:
                scores[doc_name] = scores.get(doc_name, 0) + 2
            elif ns in doc_name:
                scores[doc_name] = scores.get(doc_name, 0) + 1
    if not scores:
        return "\n\n---\n\n".join(docs.values())[:3000]
    best = sorted(scores, key=scores.get, reverse=True)[:2]
    return "\n\n---\n\n".join(docs[k] for k in best)[:4000]


_JUDGE_SYSTEM = (
    "You are a Cocos2d-x JavaScript API expert and code reviewer.\n"
    "Evaluate a model-generated response to a Cocos2d-x coding question. Score 1-5.\n\n"
    "5 = Correct API usage, complete\n"
    "4 = Correct, minor omissions\n"
    "3 = Mostly correct, one meaningful error\n"
    "2 = Partially correct, wrong API calls or logic errors\n"
    "1 = Mostly wrong or hallucinated APIs\n\n"
    'Respond in JSON only: {"score": <1-5>, "verdict": "<correct|partial|incorrect>", '
    '"reason": "<one sentence>", "hallucinated_apis": [<list>]}'
)

_JUDGE_PROMPT_TMPL = (
    "### Question:\n{instruction}\n\n"
    "### Reference Answer:\n{reference}\n\n"
    "### Model Answer to Evaluate:\n{prediction}\n\n"
    "Evaluate the model answer. Respond in JSON only."
)


def judge_with_claude(instruction, reference, prediction, anthropic_client,
                      model="claude-sonnet-4-6"):
    """Score a prediction semantically using Claude with prompt-cached doc context."""
    doc_context = _pick_relevant_doc(instruction, prediction)
    response = anthropic_client.messages.create(
        model=model,
        max_tokens=256,
        system=[{"type": "text", "text": _JUDGE_SYSTEM,
                 "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": [
            {"type": "text", "text": doc_context,
             "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": _JUDGE_PROMPT_TMPL.format(
                instruction=instruction, reference=reference, prediction=prediction)},
        ]}],
    )
    raw = response.content[0].text.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if m:
            return json.loads(m.group())
        return {"score": None, "verdict": "parse_error", "reason": raw[:200],
                "hallucinated_apis": []}


# ── Chunking & RAG index ────────────────────────────────────────────────


def _chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    paragraphs = re.split(r"\n{2,}", text)
    chunks, current = [], ""
    for para in paragraphs:
        if len(current) + len(para) > chunk_size and current:
            chunks.append(current.strip())
            current = current[-overlap:] + "\n\n" + para
        else:
            current = current + "\n\n" + para if current else para
    if current.strip():
        chunks.append(current.strip())
    return chunks


def build_rag_index():
    doc_chunks, doc_sources = [], []
    for fpath in sorted(glob.glob(DOCS_GLOB)):
        with open(fpath) as f:
            text = f.read()
        fname = os.path.basename(fpath)
        chunks = _chunk_text(text)
        doc_chunks.extend(chunks)
        doc_sources.extend([fname] * len(chunks))

    print(f"RAG index: {len(doc_chunks)} chunks, avg {np.mean([len(c) for c in doc_chunks]):.0f} chars")
    embedder = SentenceTransformer(EMBED_MODEL)
    chunk_embs = embedder.encode(doc_chunks, show_progress_bar=True, convert_to_numpy=True)
    return doc_chunks, doc_sources, embedder, chunk_embs


def retrieve_context(query, embedder, chunk_embs, doc_chunks, doc_sources, top_k=RAG_TOP_K):
    q_emb = embedder.encode([query], convert_to_numpy=True)
    scores = np.dot(chunk_embs, q_emb.T).squeeze()
    top_idx = np.argsort(scores)[-top_k:][::-1]
    return [{"text": doc_chunks[i], "source": doc_sources[i], "score": float(scores[i])} for i in top_idx]


# ── Model loading ───────────────────────────────────────────────────────


def load_models():
    compute_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=True,
    )

    if USE_FULL_FINETUNE:
        # Full fine-tuned model — load directly from Drive (quantized for eval)
        tokenizer = AutoTokenizer.from_pretrained(DRIVE_MODEL, trust_remote_code=True)
        if tokenizer.pad_token is None or tokenizer.pad_token == tokenizer.eos_token:
            tokenizer.add_special_tokens({"pad_token": "<|pad|>"})

        # Only load FT model now; base model loaded on-demand via swap
        ft_model = AutoModelForCausalLM.from_pretrained(
            DRIVE_MODEL,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=compute_dtype,
        )
        ft_model.eval()
        base_model = None  # loaded on-demand in run_evaluation
    else:
        # QLoRA — load base + adapter
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
        if tokenizer.pad_token is None or tokenizer.pad_token == tokenizer.eos_token:
            tokenizer.add_special_tokens({"pad_token": "<|pad|>"})
        base_model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=compute_dtype,
        )
        base_model.resize_token_embeddings(len(tokenizer))
        ft_model = PeftModel.from_pretrained(base_model, DRIVE_ADAPTER)
        ft_model.eval()

    print("Models loaded for evaluation.")
    return base_model, ft_model, tokenizer


# ── Generation ──────────────────────────────────────────────────────────


def _generate(model, tokenizer, prompt):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).to(model.device)
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
        )
    return tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)


def generate_finetuned(ft_model, tokenizer, instruction):
    return _generate(ft_model, tokenizer, ALPACA_PROMPT.format(instruction=instruction))


def generate_rag(base_model, tokenizer, instruction, embedder, chunk_embs, doc_chunks, doc_sources):
    chunks = retrieve_context(instruction, embedder, chunk_embs, doc_chunks, doc_sources)
    context = "\n---\n".join(c["text"] for c in chunks)
    return _generate(base_model, tokenizer, RAG_PROMPT.format(context=context, instruction=instruction))


# ── Run full evaluation (with resume) ───────────────────────────────────


def _swap_to_gpu(model, tokenizer, bnb_config, model_id, compute_dtype):
    """Unload current model, load a different one onto GPU."""
    import gc
    del model
    gc.collect()
    torch.cuda.empty_cache()
    new_model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=compute_dtype,
    )
    new_model.resize_token_embeddings(len(tokenizer))
    new_model.eval()
    return new_model


def run_evaluation(base_model, ft_model, tokenizer, embedder, chunk_embs, doc_chunks, doc_sources):
    from tqdm import tqdm

    test_ds = load_dataset("json", data_files=TEST_JSONL, split="train")

    if os.path.exists(EVAL_RESULTS_PATH):
        with open(EVAL_RESULTS_PATH) as f:
            results = json.load(f)
        print(f"Resuming from {len(results)} completed examples")
    else:
        results = []

    done = {r["index"] for r in results}
    pending = [i for i in range(len(test_ds)) if i not in done]

    if not pending:
        print(f"Evaluation complete: {len(results)} examples")
        return results

    compute_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True, bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype, bnb_4bit_use_double_quant=True,
    )

    if USE_FULL_FINETUNE:
        # Phase A: run all FT generations first
        print("Phase A: Generating fine-tuned responses...")
        ft_outputs = {}
        for i in tqdm(pending, desc="FT model"):
            ex = test_ds[i]
            ft_outputs[i] = generate_finetuned(ft_model, tokenizer, ex["instruction"])

        # Swap: unload FT model, load base model
        print("Swapping models: unloading FT, loading base for RAG...")
        base_model = _swap_to_gpu(ft_model, tokenizer, bnb_config, MODEL_ID, compute_dtype)
        ft_model = None

        # Phase B: run all RAG generations
        print("Phase B: Generating RAG responses...")
        for i in tqdm(pending, desc="RAG model"):
            ex = test_ds[i]
            rag_out = generate_rag(base_model, tokenizer, ex["instruction"], embedder, chunk_embs, doc_chunks, doc_sources)
            results.append({
                "index": i,
                "instruction": ex["instruction"],
                "reference": ex["output"],
                "finetuned": ft_outputs[i],
                "rag": rag_out,
            })
            if len(results) % 10 == 0:
                with open(EVAL_RESULTS_PATH, "w") as f:
                    json.dump(results, f)
    else:
        # QLoRA: both models share weights, run together
        for i in tqdm(pending, desc="Evaluating"):
            ex = test_ds[i]
            ft_out = generate_finetuned(ft_model, tokenizer, ex["instruction"])
            rag_out = generate_rag(base_model, tokenizer, ex["instruction"], embedder, chunk_embs, doc_chunks, doc_sources)
            results.append({
                "index": i,
                "instruction": ex["instruction"],
                "reference": ex["output"],
                "finetuned": ft_out,
                "rag": rag_out,
            })
            if len(results) % 10 == 0:
                with open(EVAL_RESULTS_PATH, "w") as f:
                    json.dump(results, f)

    with open(EVAL_RESULTS_PATH, "w") as f:
        json.dump(results, f)
    print(f"Evaluation complete: {len(results)} examples")
    return results


# ── Metrics ─────────────────────────────────────────────────────────────

def compute_metrics(prediction, reference, instruction="", anthropic_client=None):
    """All metrics for one pair. Pass anthropic_client to enable Claude judge."""
    sym = check_symbols(prediction, reference)
    codebleu = compute_codebleu(prediction, reference)
    judge = None
    if anthropic_client is not None and instruction:
        judge = judge_with_claude(instruction, reference, prediction, anthropic_client)
    return {
        "symbol_precision": sym["symbol_precision"],
        "symbol_recall": sym["symbol_recall"],
        "symbol_f1": sym["symbol_f1"],
        "has_hallucination": sym["has_hallucination"],
        "hallucinated_symbols": sym["hallucinated_symbols"],
        "codebleu": codebleu,
        "claude_score": judge["score"] if judge else None,
        "claude_verdict": judge["verdict"] if judge else None,
        "claude_reason": judge["reason"] if judge else None,
        "claude_hallucinated_apis": judge.get("hallucinated_apis", []) if judge else [],
    }


def compute_all_metrics(results, anthropic_client=None):
    ft_m, rag_m = [], []
    for r in results:
        ft_m.append(compute_metrics(r["finetuned"], r["reference"],
                                    r["instruction"], anthropic_client))
        rag_m.append(compute_metrics(r["rag"], r["reference"],
                                     r["instruction"], anthropic_client))
    return ft_m, rag_m


def avg(values):
    valid = [v for v in values if v is not None]
    return sum(valid) / len(valid) if valid else 0


def print_summary(metrics, label):
    has_cb = any(m["codebleu"] is not None for m in metrics)
    has_j = any(m["claude_score"] is not None for m in metrics)
    print(f'\n{"=" * 55}\n  {label}\n{"=" * 55}')
    print(f'  Symbol Precision:   {avg([m["symbol_precision"] for m in metrics]):.4f}')
    print(f'  Symbol Recall:      {avg([m["symbol_recall"] for m in metrics]):.4f}')
    print(f'  Symbol F1:          {avg([m["symbol_f1"] for m in metrics]):.4f}')
    print(f'  Hallucination %:    '
          f'{avg([1 if m["has_hallucination"] else 0 for m in metrics]) * 100:.1f}%')
    if has_cb:
        print(f'  CodeBLEU:           {avg([m["codebleu"] for m in metrics]):.4f}')
    if has_j:
        print(f'  Claude Score (1-5): {avg([m["claude_score"] for m in metrics]):.2f}')
        verdicts = [m["claude_verdict"] for m in metrics if m["claude_verdict"]]
        for v in ["correct", "partial", "incorrect"]:
            pct = verdicts.count(v) / len(verdicts) * 100 if verdicts else 0
            print(f'    {v}: {pct:.1f}%')


# ── Reporting ───────────────────────────────────────────────────────────


def build_comparison_df(results, ft_metrics, rag_metrics):
    import pandas as pd

    rows = []
    for i, r in enumerate(results):
        fm, rm = ft_metrics[i], rag_metrics[i]
        ft_s = fm["claude_score"] or fm["symbol_f1"] or 0
        rag_s = rm["claude_score"] or rm["symbol_f1"] or 0
        rows.append({
            "idx": r["index"],
            "instruction": r["instruction"][:80] + "...",
            "ft_symbol_f1": fm["symbol_f1"],
            "rag_symbol_f1": rm["symbol_f1"],
            "ft_codebleu": fm["codebleu"],
            "rag_codebleu": rm["codebleu"],
            "ft_claude_score": fm["claude_score"],
            "rag_claude_score": rm["claude_score"],
            "ft_hallucinated": fm["has_hallucination"],
            "rag_hallucinated": rm["has_hallucination"],
            "winner": "FT" if ft_s > rag_s else "RAG",
        })
    df = pd.DataFrame(rows)
    ft_wr = (df["winner"] == "FT").mean() * 100
    rag_wr = (df["winner"] == "RAG").mean() * 100
    print(f"\nWin rate — FT: {ft_wr:.1f}%  RAG: {rag_wr:.1f}%")
    return df


def plot_chart(ft_metrics, rag_metrics):
    import matplotlib.pyplot as plt

    has_cb = any(m["codebleu"] is not None for m in ft_metrics)
    has_j = any(m["claude_score"] is not None for m in ft_metrics)

    names = ["Symbol Precision", "Symbol Recall", "Symbol F1", "Hallucination-free %"]
    ft_v = [avg([m["symbol_precision"] for m in ft_metrics]),
            avg([m["symbol_recall"] for m in ft_metrics]),
            avg([m["symbol_f1"] for m in ft_metrics]),
            1 - avg([1 if m["has_hallucination"] else 0 for m in ft_metrics])]
    rag_v = [avg([m["symbol_precision"] for m in rag_metrics]),
             avg([m["symbol_recall"] for m in rag_metrics]),
             avg([m["symbol_f1"] for m in rag_metrics]),
             1 - avg([1 if m["has_hallucination"] else 0 for m in rag_metrics])]

    if has_cb:
        names.append("CodeBLEU")
        ft_v.append(avg([m["codebleu"] for m in ft_metrics]))
        rag_v.append(avg([m["codebleu"] for m in rag_metrics]))
    if has_j:
        names.append("Claude Score/5")
        ft_v.append(avg([m["claude_score"] for m in ft_metrics]) / 5)
        rag_v.append(avg([m["claude_score"] for m in rag_metrics]) / 5)

    x = range(len(names))
    w = 0.35
    fig, ax = plt.subplots(figsize=(12, 5))
    b1 = ax.bar([i - w / 2 for i in x], ft_v, w, label="Fine-Tuned", color="#4CAF50")
    b2 = ax.bar([i + w / 2 for i in x], rag_v, w, label="RAG (Context7)", color="#2196F3")
    ax.set_ylabel("Score")
    ax.set_title("Fine-Tuned vs RAG — Cocos2d-x Test Set")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=15, ha="right")
    ax.legend()
    ax.set_ylim(0, 1)
    for bar in list(b1) + list(b2):
        h = bar.get_height()
        ax.annotate(f"{h:.3f}", xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(EVAL_CHART_PATH, dpi=150)
    plt.show()
    print(f"Chart saved to {EVAL_CHART_PATH}")


def save_report(results, ft_metrics, rag_metrics, df):
    report = {
        "num_examples": len(results),
        "finetuned": {
            "symbol_precision": avg([m["symbol_precision"] for m in ft_metrics]),
            "symbol_recall": avg([m["symbol_recall"] for m in ft_metrics]),
            "symbol_f1": avg([m["symbol_f1"] for m in ft_metrics]),
            "hallucination_rate": avg([1 if m["has_hallucination"] else 0
                                       for m in ft_metrics]),
            "codebleu": avg([m["codebleu"] for m in ft_metrics]),
            "claude_score_avg": avg([m["claude_score"] for m in ft_metrics]),
        },
        "rag_context7": {
            "symbol_precision": avg([m["symbol_precision"] for m in rag_metrics]),
            "symbol_recall": avg([m["symbol_recall"] for m in rag_metrics]),
            "symbol_f1": avg([m["symbol_f1"] for m in rag_metrics]),
            "hallucination_rate": avg([1 if m["has_hallucination"] else 0
                                       for m in rag_metrics]),
            "codebleu": avg([m["codebleu"] for m in rag_metrics]),
            "claude_score_avg": avg([m["claude_score"] for m in rag_metrics]),
        },
        "ft_win_rate": float((df["winner"] == "FT").mean()),
        "rag_win_rate": float((df["winner"] == "RAG").mean()),
    }
    with open(EVAL_REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))
    print(f"\nReport saved to {EVAL_REPORT_PATH}")
    return report


def show_side_by_side(results, ft_metrics, rag_metrics, df, n=5):
    from IPython.display import HTML, display
    import html as html_mod

    def _show(idx):
        r = results[idx]
        fm, rm = ft_metrics[idx], rag_metrics[idx]
        ft_sym = f"SymF1={fm['symbol_f1']:.3f}" if fm["symbol_f1"] else "SymF1=N/A"
        rag_sym = f"SymF1={rm['symbol_f1']:.3f}" if rm["symbol_f1"] else "SymF1=N/A"
        ft_j = f" Claude={fm['claude_score']}" if fm["claude_score"] else ""
        rag_j = f" Claude={rm['claude_score']}" if rm["claude_score"] else ""
        display(HTML(f"""
        <div style='border:1px solid #ccc;padding:12px;margin:8px 0;border-radius:8px'>
        <h3>Example {r['index']}</h3>
        <p><b>Instruction:</b> {html_mod.escape(r['instruction'][:300])}</p>
        <table style='width:100%;border-collapse:collapse'>
        <tr>
          <th style='width:50%;border:1px solid #ddd;padding:8px;background:#e8f5e9'>
            Fine-Tuned ({ft_sym}{ft_j})</th>
          <th style='width:50%;border:1px solid #ddd;padding:8px;background:#e3f2fd'>
            RAG ({rag_sym}{rag_j})</th>
        </tr>
        <tr>
          <td style='border:1px solid #ddd;padding:8px;vertical-align:top'>
            <pre style='white-space:pre-wrap;font-size:11px'>{html_mod.escape(r['finetuned'][:800])}</pre></td>
          <td style='border:1px solid #ddd;padding:8px;vertical-align:top'>
            <pre style='white-space:pre-wrap;font-size:11px'>{html_mod.escape(r['rag'][:800])}</pre></td>
        </tr>
        <tr><td colspan='2' style='border:1px solid #ddd;padding:8px;background:#fff3e0'>
          <b>Reference:</b>
          <pre style='white-space:pre-wrap;font-size:11px'>{html_mod.escape(r['reference'][:500])}</pre>
        </td></tr>
        </table></div>"""))

    print("=== Examples where Fine-Tuned wins ===")
    for idx in df[df["winner"] == "FT"].head(n).index.tolist():
        _show(idx)
    print("\n=== Examples where RAG wins ===")
    for idx in df[df["winner"] == "RAG"].head(n).index.tolist():
        _show(idx)
