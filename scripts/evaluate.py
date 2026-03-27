"""Evaluation: fine-tuned vs RAG baseline — called from the notebook."""
import glob
import json
import os
import re

import nltk
import numpy as np
import torch
from datasets import load_dataset
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

from scripts.config import (
    ALPACA_PROMPT,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DOCS_GLOB,
    DRIVE_ADAPTER,
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
)

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
    print("Base + fine-tuned models loaded.")
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

    for i in tqdm(range(len(test_ds)), desc="Evaluating"):
        if i in done:
            continue
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

_scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
_smooth = SmoothingFunction().method1


def _extract_identifiers(code):
    return set(re.findall(r"\b(?:cc|ccui|sp|ccs)\.[A-Za-z_.]+\b", code))


def compute_metrics(prediction, reference):
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)

    ref_tok = nltk.word_tokenize(reference.lower())
    pred_tok = nltk.word_tokenize(prediction.lower())

    bleu = sentence_bleu([ref_tok], pred_tok, smoothing_function=_smooth)
    rouge = _scorer.score(reference, prediction)["rougeL"].fmeasure

    ref_ids = _extract_identifiers(reference)
    pred_ids = _extract_identifiers(prediction)
    if ref_ids:
        recall = len(ref_ids & pred_ids) / len(ref_ids)
        prec = len(ref_ids & pred_ids) / len(pred_ids) if pred_ids else 0
        f1 = 2 * prec * recall / (prec + recall) if (prec + recall) > 0 else 0
    else:
        recall = prec = f1 = None

    has_code = bool(re.search(r"```|\bfunction\b|\bconst\b|\bvar\b|\blet\b|=>|cc\.", prediction))

    return {"bleu": bleu, "rouge_l": rouge, "api_id_recall": recall, "api_id_f1": f1, "has_code": has_code}


def compute_all_metrics(results):
    ft_m, rag_m = [], []
    for r in results:
        ft_m.append(compute_metrics(r["finetuned"], r["reference"]))
        rag_m.append(compute_metrics(r["rag"], r["reference"]))
    return ft_m, rag_m


def avg(values):
    valid = [v for v in values if v is not None]
    return sum(valid) / len(valid) if valid else 0


def print_summary(metrics, label):
    print(f'\n{"=" * 50}')
    print(f"  {label}")
    print(f'{"=" * 50}')
    print(f'  BLEU-4:           {avg([m["bleu"] for m in metrics]):.4f}')
    print(f'  ROUGE-L:          {avg([m["rouge_l"] for m in metrics]):.4f}')
    print(f'  API ID Recall:    {avg([m["api_id_recall"] for m in metrics]):.4f}')
    print(f'  API ID F1:        {avg([m["api_id_f1"] for m in metrics]):.4f}')
    print(f'  Has Code (%):     {avg([1 if m["has_code"] else 0 for m in metrics]) * 100:.1f}%')


# ── Reporting ───────────────────────────────────────────────────────────


def build_comparison_df(results, ft_metrics, rag_metrics):
    import pandas as pd

    rows = []
    for i, r in enumerate(results):
        rows.append({
            "idx": r["index"],
            "instruction": r["instruction"][:80] + "...",
            "ft_bleu": ft_metrics[i]["bleu"],
            "rag_bleu": rag_metrics[i]["bleu"],
            "ft_rouge": ft_metrics[i]["rouge_l"],
            "rag_rouge": rag_metrics[i]["rouge_l"],
            "ft_api_f1": ft_metrics[i]["api_id_f1"] or 0,
            "rag_api_f1": rag_metrics[i]["api_id_f1"] or 0,
            "winner": "FT" if ft_metrics[i]["rouge_l"] > rag_metrics[i]["rouge_l"] else "RAG",
        })
    df = pd.DataFrame(rows)
    ft_wr = (df["winner"] == "FT").mean() * 100
    rag_wr = (df["winner"] == "RAG").mean() * 100
    print(f"\nWin rate — FT: {ft_wr:.1f}%  RAG: {rag_wr:.1f}%")
    return df


def plot_chart(ft_metrics, rag_metrics):
    import matplotlib.pyplot as plt

    names = ["BLEU-4", "ROUGE-L", "API ID Recall", "API ID F1", "Has Code %"]
    ft_v = [avg([m["bleu"] for m in ft_metrics]), avg([m["rouge_l"] for m in ft_metrics]),
            avg([m["api_id_recall"] for m in ft_metrics]), avg([m["api_id_f1"] for m in ft_metrics]),
            avg([1 if m["has_code"] else 0 for m in ft_metrics])]
    rag_v = [avg([m["bleu"] for m in rag_metrics]), avg([m["rouge_l"] for m in rag_metrics]),
             avg([m["api_id_recall"] for m in rag_metrics]), avg([m["api_id_f1"] for m in rag_metrics]),
             avg([1 if m["has_code"] else 0 for m in rag_metrics])]

    x = range(len(names))
    w = 0.35
    fig, ax = plt.subplots(figsize=(10, 5))
    b1 = ax.bar([i - w / 2 for i in x], ft_v, w, label="Fine-Tuned", color="#4CAF50")
    b2 = ax.bar([i + w / 2 for i in x], rag_v, w, label="RAG (Context7)", color="#2196F3")
    ax.set_ylabel("Score")
    ax.set_title("Fine-Tuned vs RAG (Context7 Docs) — Test Set")
    ax.set_xticks(x)
    ax.set_xticklabels(names)
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
            "bleu": avg([m["bleu"] for m in ft_metrics]),
            "rouge_l": avg([m["rouge_l"] for m in ft_metrics]),
            "api_id_recall": avg([m["api_id_recall"] for m in ft_metrics]),
            "api_id_f1": avg([m["api_id_f1"] for m in ft_metrics]),
            "has_code_pct": avg([1 if m["has_code"] else 0 for m in ft_metrics]),
        },
        "rag_context7": {
            "bleu": avg([m["bleu"] for m in rag_metrics]),
            "rouge_l": avg([m["rouge_l"] for m in rag_metrics]),
            "api_id_recall": avg([m["api_id_recall"] for m in rag_metrics]),
            "api_id_f1": avg([m["api_id_f1"] for m in rag_metrics]),
            "has_code_pct": avg([1 if m["has_code"] else 0 for m in rag_metrics]),
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
        display(HTML(f"""
        <div style='border:1px solid #ccc;padding:12px;margin:8px 0;border-radius:8px'>
        <h3>Example {r['index']}</h3>
        <p><b>Instruction:</b> {html_mod.escape(r['instruction'][:300])}</p>
        <table style='width:100%;border-collapse:collapse'>
        <tr>
          <th style='width:50%;border:1px solid #ddd;padding:8px;background:#e8f5e9'>
            Fine-Tuned (BLEU={fm['bleu']:.3f} ROUGE={fm['rouge_l']:.3f})</th>
          <th style='width:50%;border:1px solid #ddd;padding:8px;background:#e3f2fd'>
            RAG (BLEU={rm['bleu']:.3f} ROUGE={rm['rouge_l']:.3f})</th>
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

    ft_wins = df[df["winner"] == "FT"].nlargest(n, "ft_rouge").index.tolist()
    rag_wins = df[df["winner"] == "RAG"].nlargest(n, "rag_rouge").index.tolist()

    print("=== Examples where Fine-Tuned wins ===")
    for idx in ft_wins:
        _show(idx)
    print("\n=== Examples where RAG wins ===")
    for idx in rag_wins:
        _show(idx)
