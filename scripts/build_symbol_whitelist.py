"""Build API symbol whitelist from Cocos2d-x doc files.

Parses all *.md files in the docs directory and extracts every valid
cc.X, ccui.X, ccs.X, sp.X symbol. Saves to data/api_symbols.json.

Run: python scripts/build_symbol_whitelist.py
"""
import re
import json
import glob
import os

DOCS_DIR = "local-context7-cocos2d-x-only/docs"
OUTPUT_PATH = "data/api_symbols.json"

NAMESPACES = ["cc", "ccui", "ccs", "sp"]
PATTERNS = [re.compile(rf'\b({ns}\.[A-Za-z][A-Za-z0-9_.]*)') for ns in NAMESPACES]


def extract_symbols(docs_dir: str) -> dict:
    symbols: set[str] = set()
    by_namespace: dict[str, set[str]] = {ns: set() for ns in NAMESPACES}

    for fpath in glob.glob(os.path.join(docs_dir, "*.md")):
        text = open(fpath, encoding="utf-8").read()
        for pat in PATTERNS:
            for m in pat.finditer(text):
                sym = m.group(1)
                ns = sym.split(".")[0]
                symbols.add(sym)
                by_namespace[ns].add(sym)

    return {
        "total": len(symbols),
        "by_namespace": {k: sorted(v) for k, v in by_namespace.items()},
        "symbols": sorted(symbols),
    }


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    result = extract_symbols(DOCS_DIR)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved {result['total']} symbols to {OUTPUT_PATH}")
    for ns, syms in result["by_namespace"].items():
        print(f"  {ns}: {len(syms)}")
