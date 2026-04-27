"""Generate RAFT-style training data for Cocos2d-x fine-tuning.

RAFT (Retrieval Augmented Fine-Tuning) format:
  Each example includes a doc context in the prompt so the model learns
  to USE retrieved documentation rather than pattern-match from memory.

  - 70% oracle: correct doc section included (teaches grounded answering)
  - 30% distractor: wrong doc sections (teaches robustness to bad retrieval)

Outputs: data/train-raft.jsonl

Run: python scripts/gen_raft_data.py [--limit N] [--skip-verify]
"""
import argparse
import glob
import json
import os
import random
import re
import sys

random.seed(42)

DOCS_DIR = "local-context7-cocos2d-x-only/docs"
SYMBOL_PATTERN = re.compile(r"\b((?:cc|ccui|ccs|sp)\.[A-Za-z][A-Za-z0-9_.]*)")

RAFT_ORACLE_RATIO = 0.7
NUM_DISTRACTOR_DOCS = 2

RAG_PROMPT_TMPL = (
    "Below is an instruction that describes a task. "
    "Use the provided documentation context to write an accurate response.\n\n"
    "### Documentation Context:\n{context}\n\n"
    "### Instruction:\n{instruction}\n\n"
    "### Response:\n{output}"
)

RAG_INFERENCE_TMPL = (
    "Below is an instruction that describes a task. "
    "Use the provided documentation context to write an accurate response.\n\n"
    "### Documentation Context:\n{context}\n\n"
    "### Instruction:\n{instruction}\n\n"
    "### Response:\n"
)


def load_docs():
    docs = {}
    for fpath in sorted(glob.glob(f"{DOCS_DIR}/*.md")):
        name = os.path.basename(fpath).replace(".md", "")
        docs[name] = open(fpath, encoding="utf-8").read()
    return docs


def chunk_doc(doc_text, max_chunk=1500):
    """Split a doc into sections by heading."""
    sections = re.split(r"\n(?=## )", doc_text)
    chunks = []
    for section in sections:
        if len(section) <= max_chunk:
            chunks.append(section.strip())
        else:
            # Split large sections into paragraphs
            paragraphs = re.split(r"\n{2,}", section)
            current = ""
            for para in paragraphs:
                if len(current) + len(para) > max_chunk and current:
                    chunks.append(current.strip())
                    current = para
                else:
                    current = current + "\n\n" + para if current else para
            if current.strip():
                chunks.append(current.strip())
    return [c for c in chunks if len(c) > 50]


def find_oracle_doc(instruction, output, docs):
    """Find the most relevant doc section for a given instruction+output."""
    text = instruction + " " + output
    syms = SYMBOL_PATTERN.findall(text)

    # Score each doc by symbol overlap
    doc_scores = {}
    for doc_name, doc_text in docs.items():
        score = 0
        for sym in syms:
            if sym in doc_text:
                score += 2
            elif sym.split(".")[0] in doc_name:
                score += 1
        # Keyword match fallback
        words = re.findall(r"[A-Za-z]{4,}", instruction.lower())
        for word in words:
            if word in doc_text.lower():
                score += 0.5
        doc_scores[doc_name] = score

    if not doc_scores or max(doc_scores.values()) == 0:
        return None, None

    best_doc = max(doc_scores, key=doc_scores.get)
    doc_text = docs[best_doc]

    # Find the most relevant chunk within the doc
    chunks = chunk_doc(doc_text)
    if not chunks:
        return best_doc, doc_text[:1500]

    chunk_scores = []
    for chunk in chunks:
        s = sum(2 for sym in syms if sym in chunk)
        s += sum(0.5 for w in re.findall(r"[A-Za-z]{4,}", instruction.lower())
                 if w in chunk.lower())
        chunk_scores.append(s)

    best_chunk = chunks[chunk_scores.index(max(chunk_scores))]
    return best_doc, best_chunk


def pick_distractor_docs(oracle_doc_name, docs, n=NUM_DISTRACTOR_DOCS):
    """Pick N doc sections that are NOT the oracle doc."""
    other_docs = [k for k in docs if k != oracle_doc_name]
    chosen = random.sample(other_docs, min(n, len(other_docs)))
    chunks = []
    for doc_name in chosen:
        doc_chunks = chunk_doc(docs[doc_name])
        if doc_chunks:
            chunks.append(random.choice(doc_chunks))
    return chunks


def build_context(oracle_chunk, distractor_chunks, is_oracle_example):
    """Build the context string, optionally including the oracle doc."""
    if is_oracle_example:
        all_chunks = [oracle_chunk] + distractor_chunks
    else:
        all_chunks = distractor_chunks
    random.shuffle(all_chunks)
    return "\n\n---\n\n".join(all_chunks)[:3000]


def load_source_examples():
    """Load all source training examples."""
    sources = [
        "data/train.jsonl",
        "data/code-examples-qa.jsonl",
        "data/conversational-qa.jsonl",
        "data/synthetic-qa.jsonl",
    ]
    examples = []
    for path in sources:
        if not os.path.exists(path):
            continue
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if "instruction" in obj and "output" in obj:
                examples.append({"instruction": obj["instruction"],
                                  "output": obj["output"]})
    # Dedup by output prefix
    seen = set()
    deduped = []
    for ex in examples:
        key = ex["output"].strip().lower()[:150]
        if key not in seen:
            seen.add(key)
            deduped.append(ex)
    return deduped


def generate_raft_dataset(examples, docs, limit=None):
    """Convert source examples to RAFT format."""
    if limit:
        examples = examples[:limit]

    raft_examples = []
    skipped = 0

    for i, ex in enumerate(examples):
        if i % 500 == 0:
            print(f"  Processing {i}/{len(examples)}...")

        oracle_doc_name, oracle_chunk = find_oracle_doc(
            ex["instruction"], ex["output"], docs)

        if oracle_chunk is None:
            skipped += 1
            # Fall back to full alpaca format without context
            raft_examples.append({
                "instruction": ex["instruction"],
                "context": "",
                "output": ex["output"],
                "has_oracle": False,
            })
            continue

        distractor_chunks = pick_distractor_docs(oracle_doc_name, docs)
        is_oracle = random.random() < RAFT_ORACLE_RATIO

        context = build_context(oracle_chunk, distractor_chunks, is_oracle)
        raft_examples.append({
            "instruction": ex["instruction"],
            "context": context,
            "output": ex["output"],
            "has_oracle": is_oracle,
            "oracle_doc": oracle_doc_name,
        })

    print(f"Generated {len(raft_examples)} examples ({skipped} without oracle doc)")
    oracle_count = sum(1 for e in raft_examples if e["has_oracle"])
    print(f"Oracle examples: {oracle_count} ({oracle_count/len(raft_examples)*100:.1f}%)")
    return raft_examples


def save_raft_jsonl(raft_examples, output_path):
    """Save in the training format: instruction + context -> output."""
    with open(output_path, "w", encoding="utf-8") as f:
        for ex in raft_examples:
            # Training format: context-aware prompt
            record = {
                "instruction": ex["instruction"],
                "context": ex["context"],
                "output": ex["output"],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Saved {len(raft_examples)} RAFT examples to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit number of source examples (for testing)")
    parser.add_argument("--output", default="data/train-raft.jsonl")
    args = parser.parse_args()

    os.makedirs("data", exist_ok=True)
    print("Loading docs...")
    docs = load_docs()
    print(f"  Loaded {len(docs)} doc files")

    print("Loading source examples...")
    examples = load_source_examples()
    print(f"  Loaded {len(examples)} examples (after dedup)")

    print("Generating RAFT dataset...")
    raft = generate_raft_dataset(examples, docs, limit=args.limit)

    save_raft_jsonl(raft, args.output)

    # Quick sanity check
    sample = random.choice(raft)
    print("\nSample RAFT example:")
    print(f"  Instruction: {sample['instruction'][:80]}...")
    print(f"  Context length: {len(sample['context'])} chars")
    print(f"  Has oracle: {sample.get('has_oracle', '?')}")
    print(f"  Output: {sample['output'][:80]}...")
