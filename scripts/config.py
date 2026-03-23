"""Central configuration — edit here, not in the notebook."""
import os

# === GitHub ===
REPO = "nmnhut-it/fine-tune-cocoos"

# === Google Drive paths ===
DRIVE_ROOT = "/content/drive/MyDrive/cocos2dx-finetune"
DRIVE_CHECKPOINTS = f"{DRIVE_ROOT}/checkpoints"
DRIVE_ADAPTER = f"{DRIVE_ROOT}/cocos2dx-lora-adapter"
EVAL_RESULTS_PATH = f"{DRIVE_ROOT}/eval_results.json"
EVAL_REPORT_PATH = f"{DRIVE_ROOT}/eval_report.json"
EVAL_CHART_PATH = f"{DRIVE_ROOT}/eval_chart.png"

# === Repo-relative data paths (set after clone) ===
TRAIN_JSONL = "data/train.jsonl"
TEST_JSONL = "data/test.jsonl"
DOCS_GLOB = "local-context7-cocos2d-x-only/docs/*.md"

# === Model ===
MODEL_ID = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

# === LoRA ===
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
LORA_TARGET_MODULES = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
]

# === Training ===
NUM_EPOCHS = 3
BATCH_SIZE = 4
GRAD_ACCUM_STEPS = 4
LEARNING_RATE = 2e-4
WARMUP_RATIO = 0.05
MAX_SEQ_LENGTH = 2048
SAVE_STEPS = 50
EVAL_STEPS = 50
SAVE_TOTAL_LIMIT = 3

# === RAG ===
CHUNK_SIZE = 800
CHUNK_OVERLAP = 200
RAG_TOP_K = 5
EMBED_MODEL = "all-MiniLM-L6-v2"

# === Generation ===
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.7
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


def ensure_drive_dirs():
    for d in [DRIVE_ROOT, DRIVE_CHECKPOINTS, DRIVE_ADAPTER]:
        os.makedirs(d, exist_ok=True)
