"""
Generate synthetic QA training data from cocos2d-x doc files.
Reads each .md doc, extracts API methods/properties/classes,
and generates diverse QA pairs in JSONL format.
"""

import json
import re
import os
import random
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "local-context7-cocos2d-x-only" / "docs"
OUTPUT_FILE = Path(__file__).parent / "synthetic-qa.jsonl"

random.seed(42)

# Question templates for variety
WHAT_DOES_TEMPLATES = [
    "What does {api} do?",
    "Explain {api}.",
    "What is the purpose of {api}?",
    "Describe what {api} does.",
    "What is {api} used for?",
]

SIGNATURE_TEMPLATES = [
    "What is the signature of {api}?",
    "How do you call {api}?",
    "What are the parameters of {api}?",
    "What does {api} accept and return?",
    "Show the signature for {api}.",
]

EXAMPLE_TEMPLATES = [
    "Show an example of using {api}.",
    "Give me a code example for {api}.",
    "How do I use {api} in practice?",
    "Write a code snippet using {api}.",
    "Demonstrate {api} with code.",
]

PARAM_TEMPLATES = [
    "What parameters does {api} accept?",
    "What arguments does {api} take?",
    "What are the inputs to {api}?",
]

DEBUG_TEMPLATES = [
    "What are common mistakes when using {api}?",
    "What should I watch out for with {api}?",
    "How do I debug issues with {api}?",
]


def pick_template(templates, api_name):
    """Pick a random template and fill in the API name."""
    return random.choice(templates).format(api=api_name)


def parse_code_blocks(content):
    """Extract all typescript code blocks from markdown."""
    return re.findall(r"```typescript\n(.*?)```", content, re.DOTALL)


def extract_sections(content):
    """Split doc into sections by ## headers."""
    sections = []
    parts = re.split(r"^## (.+)$", content, flags=re.MULTILINE)
    # parts[0] is intro, then alternating header/body
    intro = parts[0].strip()
    if intro:
        # Extract title from # header
        title_match = re.match(r"^# (.+)$", intro, re.MULTILINE)
        title = title_match.group(1) if title_match else "Introduction"
        sections.append({"title": title, "body": intro})
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            sections.append({"title": parts[i].strip(), "body": parts[i + 1].strip()})
    return sections


def extract_api_signatures(code_block):
    """Extract individual API signatures from a code block."""
    sigs = []
    for line in code_block.split("\n"):
        line = line.strip()
        if not line or line.startswith("//") or line.startswith("*"):
            continue
        # Skip abstract/class/interface declarations
        if re.match(r"^(abstract\s+)?class\s+", line):
            continue
        if line.startswith("interface "):
            continue
        # Skip property-only lines (no parentheses, has colon)
        if "(" not in line and ":" in line and not line.startswith("new "):
            sigs.append(("property", line))
            continue
        # Method signatures
        if "(" in line:
            sigs.append(("method", line))
    return sigs


def extract_examples(section_body):
    """Extract example code blocks from a section."""
    examples = []
    # Find code blocks that follow **Example:** markers
    parts = re.split(r"\*\*Example:\*\*", section_body)
    for part in parts[1:]:
        code_match = re.search(r"```typescript\n(.*?)```", part, re.DOTALL)
        if code_match:
            examples.append(code_match.group(1).strip())
    return examples


def get_api_name(sig_line):
    """Extract a short API name from a signature line."""
    # Remove leading // comments
    sig_line = re.sub(r"//.*$", "", sig_line).strip()
    # Skip lines that look like bare parameters (no dot, end with comma)
    if sig_line.endswith(",") or sig_line.endswith("{") or sig_line.endswith("}"):
        return None
    # Must contain a dot (e.g., cc.moveTo, node.x) to be a real API
    if "." not in sig_line and not sig_line.startswith("new "):
        return None
    # Match patterns like cc.moveTo(...), node.setPosition(...), new cc.Sprite(...)
    m = re.match(r"(new\s+)?([\w.]+)\s*\(", sig_line)
    if m:
        name = m.group(2)
        # Must have a dot separator (real API, not a bare function name)
        if "." not in name and not m.group(1):
            return None
        prefix = "new " if m.group(1) else ""
        return prefix + name
    # Property: node.x: number
    m = re.match(r"([\w.]+)\s*:", sig_line)
    if m:
        name = m.group(1)
        if "." not in name:
            return None
        return name
    return None


def get_description_from_section(section):
    """Extract the textual description (non-code) from a section."""
    body = section["body"]
    # Remove code blocks
    text = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    # Remove markdown formatting
    text = re.sub(r"\*\*.*?\*\*", "", text)
    # Clean up
    lines = [l.strip() for l in text.split("\n") if l.strip() and not l.strip().startswith("#")]
    return " ".join(lines[:3])  # First few meaningful lines


def generate_param_description(sig_line):
    """Generate a parameter description from a signature."""
    m = re.search(r"\((.*?)\)", sig_line)
    if not m:
        return None
    params_str = m.group(1).strip()
    if not params_str:
        return "This method takes no parameters."
    # Parse params
    params = []
    depth = 0
    current = ""
    for ch in params_str:
        if ch in "(<[":
            depth += 1
        elif ch in ")>]":
            depth -= 1
        if ch == "," and depth == 0:
            params.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        params.append(current.strip())

    descriptions = []
    for p in params:
        p = p.strip()
        if "?" in p:
            p_clean = p.replace("?", "")
            descriptions.append(f"`{p_clean}` (optional)")
        else:
            descriptions.append(f"`{p}`")
    return "Parameters: " + ", ".join(descriptions) + "."


def generate_common_mistakes(api_name, sig_line, section_title):
    """Generate common mistakes for an API."""
    mistakes = []

    if "opacity" in sig_line.lower() or "opacity" in api_name.lower():
        mistakes.append("Opacity values are 0-255, not 0-1. Passing a float like 0.5 won't work as expected.")
    if "color" in sig_line.lower():
        mistakes.append("Color components are 0-255 integers, not 0.0-1.0 floats.")
    if "runAction" in api_name:
        mistakes.append("An action can only run on one node at a time. If you need to reuse an action, call action.clone() first.")
    if "addChild" in api_name:
        mistakes.append("A node can only have one parent. Adding it to a second parent will silently remove it from the first.")
    if "removeFromParent" in api_name:
        mistakes.append("Calling removeFromParent(true) also stops all actions and scheduled callbacks. Use removeFromParent(false) to keep them.")
    if "schedule" in api_name.lower() and "unschedule" not in api_name.lower():
        mistakes.append("If you schedule the same callback twice without unscheduling first, it may cause unexpected behavior.")
    if "onTouchBegan" in sig_line:
        mistakes.append("onTouchBegan must return true to receive subsequent onTouchMoved and onTouchEnded callbacks.")
    if "setAnimation" in api_name and "sp." in sig_line:
        mistakes.append("Track index 0 is the base track. Using the wrong track index can cause animations to overlay unexpectedly.")
    if "localStorage" in api_name:
        mistakes.append("localStorage only stores strings. Always convert numbers with toString() and parse back with parseInt/parseFloat.")
    if "SpriteFrame" in api_name or "spriteFrameCache" in api_name:
        mistakes.append("The sprite frame must be loaded into spriteFrameCache before use, or you'll get null.")
    if "Texture" in api_name:
        mistakes.append("Make sure the texture file path is correct and the file is included in your resources. A wrong path silently returns null.")
    if "playMusic" in api_name:
        mistakes.append("Only one music track plays at a time. Calling playMusic again stops the current music.")
    if "playEffect" in api_name:
        mistakes.append("Store the returned audio ID if you need to stop or pause the effect later. Without it, you can only stop all effects.")

    if not mistakes:
        # Generic
        mistakes.append(f"Ensure the target node is added to the scene graph before calling {api_name}, or it may have no visible effect.")

    return " ".join(mistakes)


def process_doc_file(filepath):
    """Process a single doc file and generate QA pairs."""
    qa_pairs = []
    content = filepath.read_text(encoding="utf-8")
    sections = extract_sections(content)

    for section in sections:
        title = section["title"]
        body = section["body"]
        description = get_description_from_section(section)
        code_blocks = parse_code_blocks(body)
        examples = extract_examples(body)

        apis_seen = set()

        for code_block in code_blocks:
            sigs = extract_api_signatures(code_block)
            for sig_type, sig_line in sigs:
                api_name = get_api_name(sig_line)
                if not api_name or api_name in apis_seen:
                    continue
                # Skip very short/generic names
                if len(api_name) < 4:
                    continue
                apis_seen.add(api_name)

                # 1. "What does X do?" question
                qa_pairs.append({
                    "instruction": pick_template(WHAT_DOES_TEMPLATES, api_name),
                    "input": "",
                    "output": f"{sig_line.strip()}" + (f" — {description}" if description else "")
                })

                # 2. Signature question
                qa_pairs.append({
                    "instruction": pick_template(SIGNATURE_TEMPLATES, api_name),
                    "input": "",
                    "output": sig_line.strip()
                })

                # 3. Parameter question (for methods only)
                if sig_type == "method":
                    param_desc = generate_param_description(sig_line)
                    if param_desc and "no parameters" not in param_desc:
                        qa_pairs.append({
                            "instruction": pick_template(PARAM_TEMPLATES, api_name),
                            "input": "",
                            "output": f"{sig_line.strip()}\n{param_desc}"
                        })

                # 4. Example question (if examples exist for this section)
                if examples:
                    # Pick the most relevant example
                    relevant_example = None
                    for ex in examples:
                        if api_name.split(".")[-1] in ex:
                            relevant_example = ex
                            break
                    if not relevant_example:
                        relevant_example = examples[0]

                    qa_pairs.append({
                        "instruction": pick_template(EXAMPLE_TEMPLATES, api_name),
                        "input": "",
                        "output": f"```typescript\n{relevant_example}\n```"
                    })

                # 5. Common mistakes (selective - not for every API)
                mistake_text = generate_common_mistakes(api_name, sig_line, title)
                if random.random() < 0.4:  # Only generate for ~40% of APIs
                    qa_pairs.append({
                        "instruction": pick_template(DEBUG_TEMPLATES, api_name),
                        "input": "",
                        "output": mistake_text
                    })

    return qa_pairs


def main():
    all_pairs = []
    doc_files = sorted(DOCS_DIR.glob("*.md"))
    print(f"Found {len(doc_files)} doc files")

    for doc_file in doc_files:
        pairs = process_doc_file(doc_file)
        print(f"  {doc_file.name}: {len(pairs)} QA pairs")
        all_pairs.extend(pairs)

    # Shuffle for training variety
    random.shuffle(all_pairs)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for pair in all_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    print(f"\nTotal: {len(all_pairs)} QA pairs written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
