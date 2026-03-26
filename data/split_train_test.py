"""Stratified shuffle split for train/test data.

Replaces the old sequential (first-100 / last-900) split with a proper
stratified random split that ensures every API category appears in both
train and test sets with proportional representation.
"""
import json
import os
import re
import random
from collections import defaultdict

SEED = 42
TEST_RATIO = 0.1  # 10 % for test


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def write_jsonl(path, items):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"  {path}: {len(items)} examples")


def extract_category(instruction: str) -> str:
    """Assign a coarse category based on the dominant API class mentioned."""
    inst = instruction.lower()
    # Order matters — check specific namespaces first
    if "ccui." in inst:
        return "ccui"
    for cls in [
        "cc.label", "cc.sprite", "cc.node", "cc.director", "cc.layer",
        "cc.drawnode", "cc.scheduler", "cc.eventlistener", "cc.event",
        "cc.glprogram", "cc.audioengine", "cc.animation",
        "sp.skeleton", "sp.skeletonanimation",
        "ccs.armature", "ccs.actiontimeline",
    ]:
        if cls in inst:
            return cls.replace(".", "_")
    # Fallback heuristics
    if any(w in inst for w in ["touch", "keyboard", "mouse", "listener", "event"]):
        return "events"
    if any(w in inst for w in ["action", "moveto", "fadeto", "scaleto", "rotateto",
                                "sequence", "spawn", "ease", "bezier", "spline"]):
        return "actions"
    if any(w in inst for w in ["audio", "sound", "music", "effect"]):
        return "audio"
    if any(w in inst for w in ["schedule", "update"]):
        return "scheduler"
    return "other"


def stratified_split(items, test_ratio=TEST_RATIO, seed=SEED):
    """Split items so every category is represented in both sets."""
    rng = random.Random(seed)

    # Group by category
    buckets = defaultdict(list)
    for item in items:
        cat = extract_category(item["instruction"])
        buckets[cat].append(item)

    train, test = [], []
    for cat, examples in sorted(buckets.items()):
        rng.shuffle(examples)
        n_test = max(1, round(len(examples) * test_ratio))
        test.extend(examples[:n_test])
        train.extend(examples[n_test:])

    # Final shuffle so training order is random
    rng.shuffle(train)
    rng.shuffle(test)
    return train, test


def main():
    data_dir = os.path.dirname(os.path.abspath(__file__))

    for variant, full_file in [
        ("api", "training-data.jsonl"),
        ("longform", "training-data-longform.jsonl"),
    ]:
        full_path = os.path.join(data_dir, full_file)
        if not os.path.exists(full_path):
            print(f"Skipping {variant}: {full_path} not found")
            continue

        print(f"\n{'=' * 50}")
        print(f"  Splitting: {variant} ({full_file})")
        print(f"{'=' * 50}")

        items = load_jsonl(full_path)
        train, test = stratified_split(items)

        # Verify no overlap
        train_inst = set(r["instruction"] for r in train)
        test_inst = set(r["instruction"] for r in test)
        assert not (train_inst & test_inst), "Overlap between train and test!"

        # Print category distribution
        from collections import Counter
        train_cats = Counter(extract_category(r["instruction"]) for r in train)
        test_cats = Counter(extract_category(r["instruction"]) for r in test)
        all_cats = sorted(set(train_cats) | set(test_cats))
        print(f"\n  {'Category':<25} {'Train':>6} {'Test':>6}")
        print(f"  {'-'*25} {'-'*6} {'-'*6}")
        for cat in all_cats:
            print(f"  {cat:<25} {train_cats.get(cat, 0):>6} {test_cats.get(cat, 0):>6}")
        print(f"  {'TOTAL':<25} {len(train):>6} {len(test):>6}")

        if variant == "api":
            write_jsonl(os.path.join(data_dir, "train.jsonl"), train)
            write_jsonl(os.path.join(data_dir, "test.jsonl"), test)
        else:
            write_jsonl(os.path.join(data_dir, "train-longform.jsonl"), train)
            write_jsonl(os.path.join(data_dir, "test-longform.jsonl"), test)


if __name__ == "__main__":
    main()
