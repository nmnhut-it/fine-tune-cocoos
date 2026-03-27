"""Central configuration — edit here, not in the notebook."""
import os

# === GitHub ===
REPO = "nmnhut-it/fine-tune-cocoos"

# === Variant ===
# Set by notebook before importing: "longform" or "api"
# Default to "api" if not set via environment
VARIANT = os.environ.get("COCOS_VARIANT", "api")

# === Google Drive paths (variant-aware) ===
DRIVE_ROOT = f"/content/drive/MyDrive/cocos2dx-finetune-{VARIANT}"
DRIVE_CHECKPOINTS = f"{DRIVE_ROOT}/checkpoints"
DRIVE_ADAPTER = f"{DRIVE_ROOT}/cocos2dx-lora-adapter"
EVAL_RESULTS_PATH = f"{DRIVE_ROOT}/eval_results.json"
EVAL_REPORT_PATH = f"{DRIVE_ROOT}/eval_report.json"
EVAL_CHART_PATH = f"{DRIVE_ROOT}/eval_chart.png"

# === Repo-relative data paths (variant-aware) ===
if VARIANT == "longform":
    TRAIN_JSONL = "data/train-longform.jsonl"
    TEST_JSONL = "data/test-longform.jsonl"
else:
    TRAIN_JSONL = "data/train-augmented.jsonl"
    TEST_JSONL = "data/test.jsonl"
DOCS_GLOB = "local-context7-cocos2d-x-only/docs/*.md"
SYNTHETIC_QA_JSONL = "data/synthetic-qa.jsonl"
REPLAY_JSONL = "data/replay-general.jsonl"

# Data mixing ratios for SFT phase
REPLAY_RATIO = 0.15  # 15% general data to prevent catastrophic forgetting

# === Model ===
# Qwen3-8B-Base for maximum knowledge absorption on A100 40GB
# Use base (not instruct) because CPT works better without RLHF alignment
MODEL_ID = "Qwen/Qwen3-8B-Base"

# === LoRA (DoRA for better knowledge injection) ===
LORA_R = 64
LORA_ALPHA = 128
LORA_DROPOUT = 0.05
LORA_TARGET_MODULES = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
]
USE_DORA = True  # weight-decomposed LoRA — better for new knowledge

# === Phase 1: Continued pre-training (full-text loss on docs + QA) ===
# Heavy CPT to embed all Cocos2d-x API knowledge into the model weights.
# Goal: replace Context7 RAG — the model must know the APIs internally.
CPT_EPOCHS = 5
CPT_LEARNING_RATE = 2e-4

# === Phase 2: Instruction tuning (response-only loss) ===
# Teaches the model to answer questions using its embedded knowledge.
SFT_EPOCHS = 3
SFT_LEARNING_RATE = 5e-5

# === Shared training params ===
BATCH_SIZE = 2          # A100 can handle batch=2 with 8B QLoRA
GRAD_ACCUM_STEPS = 8    # effective batch = 2*8 = 16
WARMUP_RATIO = 0.06
WEIGHT_DECAY = 0.01
MAX_SEQ_LENGTH = 2048   # Qwen3 supports 32K, use 2K for training efficiency
SAVE_STEPS = 100
EVAL_STEPS = 100
SAVE_TOTAL_LIMIT = 3
NEFTUNE_NOISE_ALPHA = 5.0  # embedding noise for better generalization

# Legacy alias for notebooks that use NUM_EPOCHS
NUM_EPOCHS = SFT_EPOCHS
LEARNING_RATE = SFT_LEARNING_RATE

# === RAG (for eval comparison only) ===
CHUNK_SIZE = 800
CHUNK_OVERLAP = 200
RAG_TOP_K = 5
EMBED_MODEL = "all-MiniLM-L6-v2"

# === Generation ===
MAX_NEW_TOKENS = 256 if VARIANT == "api" else 512
TEMPERATURE = 0.3 if VARIANT == "api" else 0.7
TOP_P = 0.9

# === Prompts ===
ALPACA_TEMPLATE = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Response:
{output}"""

ALPACA_PROMPT = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Response:
"""

RAG_PROMPT = """Below is an instruction that describes a task. Use the provided documentation context to write an accurate response.

### Documentation Context:
{context}

### Instruction:
{instruction}

### Response:
"""

# RAFT: fraction of examples that include the oracle doc (rest get distractors only)
RAFT_ORACLE_RATIO = 0.7  # 70% get the relevant doc, 30% get only distractors
RAFT_NUM_DISTRACTORS = 3  # number of irrelevant doc chunks mixed in


def ensure_drive_dirs():
    for d in [DRIVE_ROOT, DRIVE_CHECKPOINTS, DRIVE_ADAPTER]:
        os.makedirs(d, exist_ok=True)
