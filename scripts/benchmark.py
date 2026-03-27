"""
Cocos2d-x Knowledge Benchmark — auto-scored evaluation of fine-tuned model.

Runs 130 questions across 6 categories, scores each automatically, and
outputs a scorecard. Designed to test whether the model can replace
Context7 RAG for Cocos2d-x API knowledge.

Usage (from Colab after training):
    from scripts.benchmark import run_benchmark
    results = run_benchmark(model, tokenizer)
"""

import json
import os
import re
import torch
from tqdm import tqdm

from scripts.config import (
    ALPACA_PROMPT,
    DOCS_GLOB,
    DRIVE_ROOT,
    MAX_NEW_TOKENS,
    TEMPERATURE,
    TOP_P,
)
from scripts.benchmark_data import get_all_questions


# ── Generation ────────────────────────────────────────────────────────


def _generate(model, tokenizer, instruction):
    """Generate a response for a single instruction."""
    prompt = ALPACA_PROMPT.format(instruction=instruction)
    inputs = tokenizer(
        prompt, return_tensors="pt", truncation=True, max_length=2048,
    ).to(model.device)
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
        )
    return tokenizer.decode(
        out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True,
    )


# ── Scoring functions (one per category) ──────────────────────────────


def _kw_present(text, keywords):
    """Fraction of keywords found in text (case-insensitive)."""
    text_lower = text.lower()
    if not keywords:
        return 1.0
    hits = sum(1 for kw in keywords if kw.lower() in text_lower)
    return hits / len(keywords)


def _has_any(text, keywords):
    """True if any keyword is found in text."""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def score_factual(output, truth):
    """Score factual recall: keyword presence + return type match."""
    kw_score = _kw_present(output, truth.get("required_keywords", []))
    rt = truth.get("return_type", "")
    rt_score = 1.0 if rt and rt.lower() in output.lower() else 0.0
    # Weight: 60% keywords, 40% return type
    return 0.6 * kw_score + 0.4 * rt_score


def score_conceptual(output, truth):
    """Score conceptual understanding: required keywords - forbidden penalties."""
    required = truth.get("required_keywords", [])
    forbidden = truth.get("forbidden_keywords", [])
    score = _kw_present(output, required)
    # Penalize forbidden keywords
    for kw in forbidden:
        if kw.lower() in output.lower():
            score = max(0.0, score - 0.25)
    return score


def score_codegen(output, truth):
    """Score code generation: required APIs + patterns + syntax."""
    # Required API identifiers (0.4 weight)
    apis = truth.get("required_apis", [])
    api_score = _kw_present(output, apis)

    # Required patterns via regex (0.4 weight)
    patterns = truth.get("required_patterns", [])
    if patterns:
        pat_hits = sum(
            1 for p in patterns if re.search(p, output, re.IGNORECASE)
        )
        pat_score = pat_hits / len(patterns)
    else:
        pat_score = 1.0

    # Basic syntax check: balanced brackets (0.2 weight)
    opens = output.count("(") + output.count("{") + output.count("[")
    closes = output.count(")") + output.count("}") + output.count("]")
    syntax_score = 1.0 if abs(opens - closes) <= 2 else 0.5

    return 0.4 * api_score + 0.4 * pat_score + 0.2 * syntax_score


def score_hallucination(output, truth):
    """Score hallucination detection: must reject fake APIs."""
    rejection_phrases = [
        "does not exist", "doesn't exist", "not a valid",
        "no such method", "not available", "is not a method",
        "does not have", "doesn't have", "incorrect",
        "not part of", "no method", "invalid",
        "not supported", "there is no", "there's no",
        "is not defined", "not defined", "wrong",
        "not a function", "not a real",
    ]
    output_lower = output.lower()

    if truth.get("rejection_required", True):
        rejected = any(phrase in output_lower for phrase in rejection_phrases)
        if not rejected:
            return 0.0  # confidently gave a fake answer

    # Bonus for providing correction
    correction = truth.get("correction", "")
    correction_bonus = 0.0
    if correction and correction.lower() in output_lower:
        correction_bonus = 0.25

    return min(1.0, 0.75 + correction_bonus)


def score_cross_api(output, truth):
    """Score cross-API reasoning: module coverage + required keywords."""
    # Module detection by namespace
    module_patterns = {
        "sprite": r"cc\.Sprite|cc\.sprite|new cc\.Sprite",
        "audio": r"cc\.audioEngine|cc\.AudioEngine|playEffect|playMusic",
        "events": r"cc\.EventListener|cc\.eventManager|addListener|onTouch",
        "ccui": r"ccui\.",
        "actions": r"cc\.(moveTo|moveBy|scaleTo|fadeIn|fadeOut|sequence|spawn|rotateTo|rotateBy|repeat|animate|bezierTo|jumpTo)",
        "director": r"cc\.director|cc\.Director|replaceScene|pushScene",
        "spine": r"sp\.|SkeletonAnimation",
        "label": r"cc\.Label|createWithSystemFont|createWithTTF",
        "drawnode": r"cc\.DrawNode|drawRect|drawCircle|drawSegment",
        "scheduler": r"schedule\(|this\.schedule|cc\.director\.getScheduler",
        "node": r"cc\.Node|addChild|setPosition|setScale|setRotation",
        "layer": r"cc\.Layer|cc\.LayerColor",
        "sys": r"cc\.sys|localStorage",
        "particle": r"cc\.ParticleSystem|ParticleSystem",
    }

    required_modules = truth.get("required_modules", [])
    if not required_modules:
        return 1.0

    found = 0
    for mod in required_modules:
        pattern = module_patterns.get(mod, mod)
        if re.search(pattern, output, re.IGNORECASE):
            found += 1
    module_score = found / len(required_modules)

    # Required keywords bonus
    kw_score = _kw_present(output, truth.get("required_keywords", []))

    return 0.6 * module_score + 0.4 * kw_score


def score_negative(output, truth):
    """Score negative knowledge: must correctly negate."""
    expected = truth.get("expected_answer", "no").lower()
    output_lower = output.lower()

    negation_words = [
        "no", "not", "false", "doesn't", "does not", "cannot",
        "can't", "isn't", "is not", "won't", "there is no",
    ]
    affirmation_words = [
        "yes", "true", "correct", "it does", "it can", "it is",
    ]

    has_negation = any(w in output_lower for w in negation_words)
    has_affirmation = any(w in output_lower for w in affirmation_words)

    if expected in ("no", "false"):
        base = 1.0 if has_negation and not has_affirmation else 0.0
    else:
        base = 1.0 if has_affirmation else 0.0

    # Bonus for providing correct alternative
    alt = truth.get("correct_alternative", "")
    if alt and alt.lower() in output_lower:
        base = min(1.0, base + 0.25)

    return base


# ── Scorer dispatch ───────────────────────────────────────────────────

SCORERS = {
    "factual_recall": score_factual,
    "conceptual": score_conceptual,
    "code_generation": score_codegen,
    "hallucination": score_hallucination,
    "cross_api": score_cross_api,
    "negative": score_negative,
}


# ── Main benchmark runner ─────────────────────────────────────────────


def run_benchmark(model, tokenizer, docs_glob=DOCS_GLOB, save_path=None):
    """Run the full benchmark and return results dict.

    Args:
        model: loaded model (on GPU)
        tokenizer: loaded tokenizer
        docs_glob: glob pattern for doc files
        save_path: optional path to save JSON results

    Returns:
        dict with per-question results and category summaries
    """
    questions = get_all_questions(docs_glob)
    print(f"Running benchmark: {len(questions)} questions")

    results = []
    for q in tqdm(questions, desc="Benchmarking"):
        output = _generate(model, tokenizer, q["question"])
        scorer = SCORERS[q["category"]]
        score = scorer(output, q["ground_truth"])
        results.append({
            "id": q["id"],
            "category": q["category"],
            "question": q["question"],
            "output": output,
            "score": round(score, 3),
        })

    # Aggregate by category
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = {"scores": [], "count": 0}
        categories[cat]["scores"].append(r["score"])
        categories[cat]["count"] += 1

    summary = {}
    for cat, data in categories.items():
        scores = data["scores"]
        avg = sum(scores) / len(scores) if scores else 0.0
        passed = sum(1 for s in scores if s >= 0.5)
        summary[cat] = {
            "avg_score": round(avg, 3),
            "passed": passed,
            "total": data["count"],
        }

    all_scores = [r["score"] for r in results]
    overall = sum(all_scores) / len(all_scores) if all_scores else 0.0

    # Print scorecard
    print()
    print("COCOS2D-X KNOWLEDGE BENCHMARK")
    print("=" * 52)
    cat_display = {
        "factual_recall": "Factual Recall",
        "conceptual": "Conceptual",
        "code_generation": "Code Generation",
        "hallucination": "Hallucination Det.",
        "cross_api": "Cross-API Reasoning",
        "negative": "Negative Knowledge",
    }
    for cat_key in cat_display:
        if cat_key in summary:
            s = summary[cat_key]
            label = cat_display[cat_key]
            print(f"  {label:<22} ({s['total']:>2}): "
                  f" {s['avg_score']:.2f}  [{s['passed']}/{s['total']} pass]")
    print("-" * 52)
    print(f"  {'OVERALL':<22} ({len(results):>3}):  {overall:.2f}")
    print()

    # Pass/fail thresholds
    thresholds = {
        "factual_recall": 0.80,
        "hallucination": 0.75,
    }
    overall_threshold = 0.70
    all_pass = True
    for cat_key, threshold in thresholds.items():
        if cat_key in summary and summary[cat_key]["avg_score"] < threshold:
            print(f"  FAIL: {cat_display[cat_key]} "
                  f"({summary[cat_key]['avg_score']:.2f} < {threshold})")
            all_pass = False
    if overall < overall_threshold:
        print(f"  FAIL: Overall ({overall:.2f} < {overall_threshold})")
        all_pass = False
    if all_pass:
        print("  PASS: Ready to replace Context7 RAG")
    print()

    output_data = {
        "overall_score": round(overall, 3),
        "summary": summary,
        "results": results,
    }

    # Save results
    if save_path is None:
        save_path = os.path.join(DRIVE_ROOT, "benchmark_results.json")
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"  Results saved to {save_path}")
    except OSError:
        print("  Could not save results to file (Drive not mounted?)")

    return output_data
