"""
Benchmark questions for evaluating a fine-tuned Cocos2d-x JS API model.
Six categories: factual_recall, conceptual, code_generation, hallucination,
cross_api, and negative. All ground truth is derived from the local doc files
in local-context7-cocos2d-x-only/docs/.
"""

import glob
import random
import re
from typing import Any

# ---------------------------------------------------------------------------
# 1. generate_factual_questions — parse docs and return 30 random signature Qs
# ---------------------------------------------------------------------------

_METHOD_SIG_RE = re.compile(
    r"(\w[\w.]*)\(([^)]*)\)\s*:\s*([^\n]+)"
)


def _parse_signatures(text: str) -> list[dict[str, str]]:
    """Extract method signatures from TypeScript code blocks."""
    results: list[dict[str, str]] = []
    in_ts_block = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```typescript"):
            in_ts_block = True
            continue
        if stripped.startswith("```") and in_ts_block:
            in_ts_block = False
            continue
        if not in_ts_block:
            continue
        m = _METHOD_SIG_RE.search(stripped)
        if m:
            method_name = m.group(1)
            params = m.group(2).strip()
            return_type = m.group(3).strip()
            full_sig = f"{method_name}({params}): {return_type}"
            results.append({
                "method": method_name,
                "params": params,
                "return_type": return_type,
                "full_signature": full_sig,
            })
    return results


def _keywords_from_sig(sig: dict[str, str]) -> list[str]:
    """Derive required keywords from a parsed signature."""
    kw: list[str] = [sig["method"]]
    rt = sig["return_type"]
    if rt and rt not in ("void",):
        kw.append(rt.split("|")[0].strip())
    return kw


_QUESTION_TEMPLATES = [
    "What is the signature of {method}?",
    "What does {method} return?",
    "What are the parameters of {method}?",
    "How do you call {method}?",
]


def generate_factual_questions(
    docs_glob: str = "local-context7-cocos2d-x-only/docs/*.md",
) -> list[dict[str, Any]]:
    """Parse all doc .md files, extract signatures, return 30 random Qs."""
    all_sigs: list[dict[str, str]] = []
    for path in sorted(glob.glob(docs_glob)):
        with open(path, encoding="utf-8") as fh:
            all_sigs.extend(_parse_signatures(fh.read()))

    # De-duplicate by full_signature
    seen: set[str] = set()
    unique: list[dict[str, str]] = []
    for s in all_sigs:
        if s["full_signature"] not in seen:
            seen.add(s["full_signature"])
            unique.append(s)

    rng = random.Random(42)
    rng.shuffle(unique)
    chosen = unique[:30]

    questions: list[dict[str, Any]] = []
    for idx, sig in enumerate(chosen):
        tmpl = _QUESTION_TEMPLATES[idx % len(_QUESTION_TEMPLATES)]
        questions.append({
            "id": f"factual_{idx + 1:03d}",
            "category": "factual_recall",
            "question": tmpl.format(method=sig["method"]),
            "ground_truth": {
                "full_signature": sig["full_signature"],
                "required_keywords": _keywords_from_sig(sig),
                "return_type": sig["return_type"],
            },
        })
    return questions


# ---------------------------------------------------------------------------
# 2. CONCEPTUAL_QUESTIONS — 25 conceptual questions
# ---------------------------------------------------------------------------

CONCEPTUAL_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "conceptual_001",
        "category": "conceptual",
        "question": "What is the difference between cc.sequence and cc.spawn?",
        "ground_truth": {
            "required_keywords": ["sequential", "one after", "order",
                                  "parallel", "simultaneous", "same time"],
            "forbidden_keywords": ["cc.repeat"],
        },
    },
    {
        "id": "conceptual_002",
        "category": "conceptual",
        "question": "When would you use cc.CallFunc in an action sequence?",
        "ground_truth": {
            "required_keywords": ["callback", "sequence"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_003",
        "category": "conceptual",
        "question": "What is the purpose of the anchor point on a cc.Node?",
        "ground_truth": {
            "required_keywords": ["position", "rotation", "scale",
                                  "origin", "reference"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_004",
        "category": "conceptual",
        "question": "Explain the difference between cc.Layer and cc.Scene.",
        "ground_truth": {
            "required_keywords": ["container", "scene graph", "director",
                                  "runScene"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_005",
        "category": "conceptual",
        "question": "What does cascadeOpacity do on a cc.Node?",
        "ground_truth": {
            "required_keywords": ["children", "opacity", "inherit",
                                  "propagate"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_006",
        "category": "conceptual",
        "question": "When should you use cc.SpriteBatchNode?",
        "ground_truth": {
            "required_keywords": ["draw call", "same texture", "performance"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_007",
        "category": "conceptual",
        "question": (
            "What is the difference between cc.eventManager.addListener "
            "with a node vs a priority number?"
        ),
        "ground_truth": {
            "required_keywords": ["node", "priority", "scene graph"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_008",
        "category": "conceptual",
        "question": "Why must onTouchBegan return true?",
        "ground_truth": {
            "required_keywords": ["receive", "move", "end", "claim"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_009",
        "category": "conceptual",
        "question": "What is the difference between cc.moveTo and cc.moveBy?",
        "ground_truth": {
            "required_keywords": ["absolute", "relative"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_010",
        "category": "conceptual",
        "question": (
            "Explain the difference between node.scheduleUpdate and "
            "node.schedule."
        ),
        "ground_truth": {
            "required_keywords": ["every frame", "interval", "update"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_011",
        "category": "conceptual",
        "question": "What does swallowTouches mean on a touch listener?",
        "ground_truth": {
            "required_keywords": ["prevent", "propagate", "lower", "stop"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_012",
        "category": "conceptual",
        "question": "When would you use cc.director.pushScene vs runScene?",
        "ground_truth": {
            "required_keywords": ["stack", "push", "pop", "replace"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_013",
        "category": "conceptual",
        "question": "What is the purpose of cc.spriteFrameCache?",
        "ground_truth": {
            "required_keywords": ["atlas", "plist", "sprite frame", "cache"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_014",
        "category": "conceptual",
        "question": "Explain what cc.DrawNode is used for.",
        "ground_truth": {
            "required_keywords": ["vector", "draw", "dot", "segment",
                                  "circle", "polygon"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_015",
        "category": "conceptual",
        "question": (
            "What is the difference between cc.Label.createWithSystemFont "
            "and cc.Label.createWithTTF?"
        ),
        "ground_truth": {
            "required_keywords": ["system", "TTF", "font", "platform",
                                  "FreeType"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_016",
        "category": "conceptual",
        "question": (
            "What is the difference between TOUCH_ONE_BY_ONE "
            "and TOUCH_ALL_AT_ONCE?"
        ),
        "ground_truth": {
            "required_keywords": ["single", "multi-touch", "one", "all"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_017",
        "category": "conceptual",
        "question": "When would you use cc.follow?",
        "ground_truth": {
            "required_keywords": ["camera", "follow", "node", "scroll"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_018",
        "category": "conceptual",
        "question": "What does cc.sys.isNative indicate?",
        "ground_truth": {
            "required_keywords": ["JSB", "native", "browser", "boolean"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_019",
        "category": "conceptual",
        "question": "Explain the role of trackIndex in sp.SkeletonAnimation.",
        "ground_truth": {
            "required_keywords": ["track", "animation", "overlay", "layer"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_020",
        "category": "conceptual",
        "question": "What is a cc.SpriteFrame and how does it relate to an atlas?",
        "ground_truth": {
            "required_keywords": ["region", "texture", "atlas", "rect"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_021",
        "category": "conceptual",
        "question": (
            "What is the difference between localZOrder and globalZOrder?"
        ),
        "ground_truth": {
            "required_keywords": ["local", "global", "parent", "scene"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_022",
        "category": "conceptual",
        "question": "Which API would you use to play background music that loops?",
        "ground_truth": {
            "required_keywords": ["audioEngine", "playMusic", "loop"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_023",
        "category": "conceptual",
        "question": "What does node.cleanup() do?",
        "ground_truth": {
            "required_keywords": ["actions", "timers", "stop"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_024",
        "category": "conceptual",
        "question": (
            "Explain the purpose of ccui.Layout.setClippingEnabled."
        ),
        "ground_truth": {
            "required_keywords": ["clip", "children", "bounds", "visible"],
            "forbidden_keywords": [],
        },
    },
    {
        "id": "conceptual_025",
        "category": "conceptual",
        "question": (
            "What is the difference between cc.LayerColor "
            "and cc.LayerGradient?"
        ),
        "ground_truth": {
            "required_keywords": ["solid", "gradient", "color",
                                  "start", "end"],
            "forbidden_keywords": [],
        },
    },
]

# ---------------------------------------------------------------------------
# 3. CODEGEN_QUESTIONS — 25 code generation questions
# ---------------------------------------------------------------------------

CODEGEN_QUESTIONS: list[dict[str, Any]] = [
    # --- 10 simple (single API) ---
    {
        "id": "codegen_001",
        "category": "code_generation",
        "question": "Write code to create a cc.Sprite from an image file.",
        "ground_truth": {
            "required_apis": ["cc.Sprite"],
            "required_patterns": [r"new cc\.Sprite\(|cc\.Sprite\.create\("],
            "description": "Instantiate a sprite with an image path.",
        },
    },
    {
        "id": "codegen_002",
        "category": "code_generation",
        "question": "Write code to fade out a node over 0.5 seconds.",
        "ground_truth": {
            "required_apis": ["cc.fadeOut", "runAction"],
            "required_patterns": [r"cc\.fadeOut\("],
            "description": "Run a fadeOut action on a node.",
        },
    },
    {
        "id": "codegen_003",
        "category": "code_generation",
        "question": "Write code to play background music in a loop.",
        "ground_truth": {
            "required_apis": ["cc.audioEngine.playMusic"],
            "required_patterns": [r"playMusic\(.+,\s*true\)"],
            "description": "Play looping background music via audioEngine.",
        },
    },
    {
        "id": "codegen_004",
        "category": "code_generation",
        "question": "Write code to create a system-font label that says 'Score: 0'.",
        "ground_truth": {
            "required_apis": ["cc.Label.createWithSystemFont"],
            "required_patterns": [r"createWithSystemFont\("],
            "description": "Create a label with system font.",
        },
    },
    {
        "id": "codegen_005",
        "category": "code_generation",
        "question": "Write code to draw a red dot at position (100, 100) using DrawNode.",
        "ground_truth": {
            "required_apis": ["cc.DrawNode", "drawDot"],
            "required_patterns": [r"drawDot\("],
            "description": "Create DrawNode and draw a dot.",
        },
    },
    {
        "id": "codegen_006",
        "category": "code_generation",
        "question": "Write code to save a high score to local storage.",
        "ground_truth": {
            "required_apis": ["cc.sys.localStorage.setItem"],
            "required_patterns": [r"localStorage\.setItem\("],
            "description": "Persist data with local storage.",
        },
    },
    {
        "id": "codegen_007",
        "category": "code_generation",
        "question": "Write code to schedule a callback every 2 seconds on a node.",
        "ground_truth": {
            "required_apis": ["schedule"],
            "required_patterns": [r"\.schedule\("],
            "description": "Use node.schedule with an interval.",
        },
    },
    {
        "id": "codegen_008",
        "category": "code_generation",
        "question": "Write code to move a node to position (300, 400) over 1 second.",
        "ground_truth": {
            "required_apis": ["cc.moveTo", "runAction"],
            "required_patterns": [r"cc\.moveTo\("],
            "description": "Run a moveTo action.",
        },
    },
    {
        "id": "codegen_009",
        "category": "code_generation",
        "question": "Write code to flip a sprite horizontally.",
        "ground_truth": {
            "required_apis": ["setFlippedX"],
            "required_patterns": [r"setFlippedX\(true\)"],
            "description": "Flip sprite on X axis.",
        },
    },
    {
        "id": "codegen_010",
        "category": "code_generation",
        "question": "Write code to get the window size and compute its center.",
        "ground_truth": {
            "required_apis": ["cc.director.getWinSize"],
            "required_patterns": [r"getWinSize\(\)"],
            "description": "Get window dimensions from director.",
        },
    },
    # --- 8 medium (2-3 APIs) ---
    {
        "id": "codegen_011",
        "category": "code_generation",
        "question": (
            "Write code to create a sprite, set its position to the "
            "center of the screen, and add it to a layer."
        ),
        "ground_truth": {
            "required_apis": ["cc.Sprite", "setPosition", "addChild",
                              "cc.director.getWinSize"],
            "required_patterns": [
                r"new cc\.Sprite\(|cc\.Sprite\.create\(",
                r"setPosition\(",
                r"addChild\(",
            ],
            "description": "Sprite creation, positioning, and parenting.",
        },
    },
    {
        "id": "codegen_012",
        "category": "code_generation",
        "question": (
            "Write code to fade out a node over 0.5s and then "
            "remove it from its parent."
        ),
        "ground_truth": {
            "required_apis": ["cc.fadeOut", "cc.sequence", "cc.callFunc",
                              "removeFromParent"],
            "required_patterns": [
                r"cc\.sequence\(",
                r"cc\.fadeOut\(",
                r"removeFromParent",
            ],
            "description": "Chain fadeOut with removal using sequence + callFunc.",
        },
    },
    {
        "id": "codegen_013",
        "category": "code_generation",
        "question": (
            "Write code to create a ccui.Button, set its title text, "
            "and add a click listener."
        ),
        "ground_truth": {
            "required_apis": ["ccui.Button", "setTitleText",
                              "addClickEventListener"],
            "required_patterns": [
                r"new ccui\.Button\(|ccui\.Button\.create\(",
                r"setTitleText\(",
                r"addClickEventListener\(",
            ],
            "description": "Create UI button with title and click handler.",
        },
    },
    {
        "id": "codegen_014",
        "category": "code_generation",
        "question": (
            "Write code to register a keyboard listener that logs "
            "the pressed key code."
        ),
        "ground_truth": {
            "required_apis": ["cc.eventManager.addListener",
                              "cc.EventListener.KEYBOARD"],
            "required_patterns": [
                r"EventListener\.KEYBOARD",
                r"onKeyPressed",
            ],
            "description": "Add keyboard event listener via eventManager.",
        },
    },
    {
        "id": "codegen_015",
        "category": "code_generation",
        "question": (
            "Write code to create a Spine skeleton animation, "
            "play the 'run' animation looping on track 0."
        ),
        "ground_truth": {
            "required_apis": ["sp.SkeletonAnimation", "setAnimation"],
            "required_patterns": [
                r"new sp\.SkeletonAnimation\(|createWithJsonFile\(",
                r"setAnimation\(\s*0",
            ],
            "description": "Create Spine skeleton and play animation.",
        },
    },
    {
        "id": "codegen_016",
        "category": "code_generation",
        "question": (
            "Write code to load a sprite frame atlas from a plist file "
            "and create a sprite from a frame."
        ),
        "ground_truth": {
            "required_apis": ["cc.spriteFrameCache.addSpriteFrames",
                              "cc.spriteFrameCache.getSpriteFrame",
                              "cc.Sprite"],
            "required_patterns": [
                r"addSpriteFrames\(",
                r"getSpriteFrame\(",
            ],
            "description": "Load plist atlas and use sprite frame.",
        },
    },
    {
        "id": "codegen_017",
        "category": "code_generation",
        "question": (
            "Write code to create a ccui.ScrollView with vertical "
            "scrolling and bounce enabled."
        ),
        "ground_truth": {
            "required_apis": ["ccui.ScrollView", "setDirection",
                              "setBounceEnabled"],
            "required_patterns": [
                r"new ccui\.ScrollView\(",
                r"DIR_VERTICAL",
                r"setBounceEnabled\(true\)",
            ],
            "description": "Configure a vertical ScrollView.",
        },
    },
    {
        "id": "codegen_018",
        "category": "code_generation",
        "question": (
            "Write code to draw a blue line segment and a green "
            "filled rectangle using cc.DrawNode."
        ),
        "ground_truth": {
            "required_apis": ["cc.DrawNode", "drawSegment", "drawRect"],
            "required_patterns": [
                r"drawSegment\(",
                r"drawRect\(",
            ],
            "description": "Draw two shapes with DrawNode.",
        },
    },
    # --- 7 complex (4+ APIs) ---
    {
        "id": "codegen_019",
        "category": "code_generation",
        "question": (
            "Write code for a sprite that moves to (300,300), "
            "scales up to 1.5, plays a sound effect, then fades out."
        ),
        "ground_truth": {
            "required_apis": ["cc.Sprite", "cc.sequence", "cc.spawn",
                              "cc.moveTo", "cc.scaleTo", "cc.fadeOut",
                              "cc.audioEngine.playEffect"],
            "required_patterns": [
                r"cc\.sequence\(",
                r"cc\.moveTo\(",
                r"cc\.scaleTo\(",
                r"cc\.fadeOut\(",
                r"playEffect\(",
            ],
            "description": (
                "Composite action with movement, scale, audio, and fade."
            ),
        },
    },
    {
        "id": "codegen_020",
        "category": "code_generation",
        "question": (
            "Write a complete touch listener that creates a sprite "
            "at the touch location when the user taps the screen."
        ),
        "ground_truth": {
            "required_apis": ["cc.eventManager.addListener",
                              "cc.EventListener.TOUCH_ONE_BY_ONE",
                              "cc.Sprite", "addChild", "getLocation"],
            "required_patterns": [
                r"TOUCH_ONE_BY_ONE",
                r"onTouchBegan",
                r"getLocation\(\)",
                r"new cc\.Sprite\(",
            ],
            "description": "Touch listener + sprite spawn at touch pos.",
        },
    },
    {
        "id": "codegen_021",
        "category": "code_generation",
        "question": (
            "Write code to create a sprite-frame animation that loops "
            "forever. Load 8 frames from the sprite frame cache."
        ),
        "ground_truth": {
            "required_apis": ["cc.spriteFrameCache.getSpriteFrame",
                              "cc.Animation", "cc.animate",
                              "cc.repeatForever", "runAction"],
            "required_patterns": [
                r"getSpriteFrame\(",
                r"new cc\.Animation\(",
                r"cc\.animate\(",
                r"cc\.repeatForever\(",
            ],
            "description": "Frame-by-frame sprite animation loop.",
        },
    },
    {
        "id": "codegen_022",
        "category": "code_generation",
        "question": (
            "Write code to create a game scene with a background layer, "
            "a centered label, and transition to it with a fade."
        ),
        "ground_truth": {
            "required_apis": ["cc.Scene", "cc.LayerColor", "cc.Label",
                              "cc.TransitionFade", "cc.director.runScene"],
            "required_patterns": [
                r"new cc\.Scene\(|cc\.Scene",
                r"cc\.LayerColor|new cc\.LayerColor",
                r"createWithSystemFont\(|createWithTTF\(",
                r"TransitionFade",
                r"runScene\(",
            ],
            "description": "Build scene with layer, label, and transition.",
        },
    },
    {
        "id": "codegen_023",
        "category": "code_generation",
        "question": (
            "Write code to create a ccui.ListView, set it to vertical, "
            "add 10 button items, and listen for scroll-to-bottom."
        ),
        "ground_truth": {
            "required_apis": ["ccui.ListView", "setDirection",
                              "ccui.Button", "pushBackCustomItem",
                              "addEventListener"],
            "required_patterns": [
                r"new ccui\.ListView\(",
                r"DIR_VERTICAL",
                r"pushBackCustomItem\(",
                r"EVENT_SCROLL_TO_BOTTOM",
            ],
            "description": "ListView with items and scroll event.",
        },
    },
    {
        "id": "codegen_024",
        "category": "code_generation",
        "question": (
            "Write code that pauses the director, shows a semi-transparent "
            "overlay LayerColor, and adds a resume button."
        ),
        "ground_truth": {
            "required_apis": ["cc.director.pause", "cc.LayerColor",
                              "ccui.Button", "cc.director.resume",
                              "addChild"],
            "required_patterns": [
                r"cc\.director\.pause\(",
                r"new cc\.LayerColor\(",
                r"new ccui\.Button\(",
                r"cc\.director\.resume\(",
            ],
            "description": "Pause menu overlay with resume.",
        },
    },
    {
        "id": "codegen_025",
        "category": "code_generation",
        "question": (
            "Write code to load a CocosStudio armature, play the 'idle' "
            "animation looping, listen for completion of a one-shot "
            "'attack' animation, then switch back to 'idle'."
        ),
        "ground_truth": {
            "required_apis": [
                "ccs.armatureDataManager.addArmatureFileInfo",
                "ccs.Armature.create",
                "animation.play",
                "setMovementEventCallFunc",
            ],
            "required_patterns": [
                r"addArmatureFileInfo\(",
                r"Armature\.create\(",
                r"\.play\(",
                r"setMovementEventCallFunc\(",
            ],
            "description": (
                "Armature load, play, and animation event callback."
            ),
        },
    },
]

# ---------------------------------------------------------------------------
# 4. HALLUCINATION_QUESTIONS — 20 questions about fake/wrong APIs
# ---------------------------------------------------------------------------

HALLUCINATION_QUESTIONS: list[dict[str, Any]] = [
    # --- 7 fake methods ---
    {
        "id": "hallucination_001",
        "category": "hallucination",
        "question": "What does cc.Sprite.setGravity() do?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.Sprite has no setGravity method. "
                "Gravity is not a built-in sprite feature."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_002",
        "category": "hallucination",
        "question": "What is the signature of cc.DrawNode.drawLine()?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.DrawNode has no drawLine method. "
                "Use draw.drawSegment(from, to, lineWidth, color) instead."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_003",
        "category": "hallucination",
        "question": "What does cc.Node.setVelocity(x, y) do?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.Node has no setVelocity method. "
                "Movement is done via actions or manual position updates."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_004",
        "category": "hallucination",
        "question": (
            "What is the signature of cc.audioEngine.fadeMusic()?"
        ),
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.audioEngine has no fadeMusic method. "
                "Use setMusicVolume with a scheduled callback to fade."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_005",
        "category": "hallucination",
        "question": "What does cc.DrawNode.drawEllipse() do?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.DrawNode has no drawEllipse method. "
                "Use drawCircle and set different scaleX/scaleY."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_006",
        "category": "hallucination",
        "question": "What does cc.eventManager.emit() do?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.eventManager has no emit method. "
                "Use dispatchEvent() or dispatchCustomEvent()."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_007",
        "category": "hallucination",
        "question": "What does label.setFontWeight('bold') do?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.Label has no setFontWeight method. "
                "Use a bold font file or enableOutline for emphasis."
            ),
            "rejection_required": True,
        },
    },
    # --- 5 wrong parameter order/type ---
    {
        "id": "hallucination_008",
        "category": "hallucination",
        "question": (
            "Is this correct? cc.moveTo(cc.p(300, 400), 1.0) "
            "to move to (300,400) in 1 second."
        ),
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "Wrong parameter order. "
                "Correct: cc.moveTo(1.0, cc.p(300, 400)) "
                "- duration comes first."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_009",
        "category": "hallucination",
        "question": (
            "Is this correct? cc.audioEngine.playEffect(true, 'sfx.mp3') "
            "to loop a sound effect."
        ),
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "Wrong parameter order. "
                "Correct: cc.audioEngine.playEffect('sfx.mp3', true) "
                "- url comes first, then loop."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_010",
        "category": "hallucination",
        "question": (
            "Is this correct? skel.setAnimation('run', 0, true) "
            "to play 'run' on track 0?"
        ),
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "Wrong parameter order. "
                "Correct: skel.setAnimation(0, 'run', true) "
                "- trackIndex comes first."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_011",
        "category": "hallucination",
        "question": (
            "Is this correct? cc.Label.createWithSystemFont(24, 'Arial', "
            "'Hello') to create a label?"
        ),
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "Wrong parameter order. "
                "Correct: cc.Label.createWithSystemFont('Hello', 'Arial', 24) "
                "- text, font, then fontSize."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_012",
        "category": "hallucination",
        "question": (
            "Is this correct? node.addChild(5, sprite) to add a sprite "
            "at zOrder 5?"
        ),
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "Wrong parameter order. "
                "Correct: node.addChild(sprite, 5) "
                "- child first, then zOrder."
            ),
            "rejection_required": True,
        },
    },
    # --- 4 non-existent classes ---
    {
        "id": "hallucination_013",
        "category": "hallucination",
        "question": "How do I create a cc.ParticleEmitter?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.ParticleEmitter does not exist in the Cocos2d-x JS API. "
                "The particle class is cc.ParticleSystem."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_014",
        "category": "hallucination",
        "question": "How do I use cc.TiledLayer for tile maps?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.TiledLayer is not documented in the core Cocos2d-x JS "
                "API docs. The tiled map classes are cc.TMXTiledMap and "
                "cc.TMXLayer."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_015",
        "category": "hallucination",
        "question": "What methods does cc.Camera have?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.Camera is not a documented class in the Cocos2d-x JS "
                "API. Use cc.follow for camera-like behavior or manipulate "
                "the layer/node position."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_016",
        "category": "hallucination",
        "question": "How do I create a cc.VideoPlayer?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.VideoPlayer is not documented in the Cocos2d-x JS API. "
                "Video playback depends on platform-specific extensions."
            ),
            "rejection_required": True,
        },
    },
    # --- 4 wrong namespace ---
    {
        "id": "hallucination_017",
        "category": "hallucination",
        "question": "How do I create a cc.Button?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.Button does not exist. "
                "The correct class is ccui.Button."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_018",
        "category": "hallucination",
        "question": "How do I use cc.ScrollView?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.ScrollView is not the standard UI scroll view. "
                "The correct class is ccui.ScrollView."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_019",
        "category": "hallucination",
        "question": "What is the signature of cc.Skeleton.setAnimation?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.Skeleton does not exist. "
                "The correct class is sp.SkeletonAnimation in the sp namespace."
            ),
            "rejection_required": True,
        },
    },
    {
        "id": "hallucination_020",
        "category": "hallucination",
        "question": "How do I create a cc.ListView?",
        "ground_truth": {
            "is_fake": True,
            "correction": (
                "cc.ListView does not exist. "
                "The correct class is ccui.ListView."
            ),
            "rejection_required": True,
        },
    },
]

# ---------------------------------------------------------------------------
# 5. CROSS_API_QUESTIONS — 15 cross-module questions
# ---------------------------------------------------------------------------

CROSS_API_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "cross_api_001",
        "category": "cross_api",
        "question": (
            "How do you create a sprite, animate it with a move action, "
            "and play a sound effect when it finishes?"
        ),
        "ground_truth": {
            "required_modules": ["sprite", "actions", "audio"],
            "required_apis": ["cc.Sprite", "cc.moveTo", "cc.sequence",
                              "cc.callFunc", "cc.audioEngine.playEffect"],
            "required_keywords": ["Sprite", "moveTo", "sequence",
                                  "callFunc", "playEffect"],
        },
    },
    {
        "id": "cross_api_002",
        "category": "cross_api",
        "question": (
            "How do you display a score label that updates each frame "
            "with the director's delta time?"
        ),
        "ground_truth": {
            "required_modules": ["label", "director"],
            "required_apis": ["cc.Label", "cc.director.getDeltaTime",
                              "scheduleUpdate", "setString"],
            "required_keywords": ["Label", "getDeltaTime", "setString",
                                  "update"],
        },
    },
    {
        "id": "cross_api_003",
        "category": "cross_api",
        "question": (
            "How do you handle a touch event on a sprite and run a "
            "scale action on it when tapped?"
        ),
        "ground_truth": {
            "required_modules": ["sprite", "events", "actions"],
            "required_apis": ["cc.eventManager.addListener",
                              "cc.EventListener.TOUCH_ONE_BY_ONE",
                              "cc.scaleTo", "runAction"],
            "required_keywords": ["addListener", "TOUCH_ONE_BY_ONE",
                                  "scaleTo", "runAction"],
        },
    },
    {
        "id": "cross_api_004",
        "category": "cross_api",
        "question": (
            "How do you use a Spine skeleton to play an attack animation "
            "and play a sound effect on a specific frame event?"
        ),
        "ground_truth": {
            "required_modules": ["spine", "audio"],
            "required_apis": ["sp.SkeletonAnimation", "setAnimation",
                              "setAnimationListener",
                              "cc.audioEngine.playEffect"],
            "required_keywords": ["setAnimation", "AnimationEventType",
                                  "EVENT", "playEffect"],
        },
    },
    {
        "id": "cross_api_005",
        "category": "cross_api",
        "question": (
            "How do you build a pause menu with a ccui.Button that "
            "resumes the director and fades out an overlay layer?"
        ),
        "ground_truth": {
            "required_modules": ["ccui", "director", "actions"],
            "required_apis": ["ccui.Button", "cc.director.resume",
                              "cc.fadeOut", "cc.LayerColor"],
            "required_keywords": ["Button", "resume", "fadeOut",
                                  "LayerColor"],
        },
    },
    {
        "id": "cross_api_006",
        "category": "cross_api",
        "question": (
            "How do you draw a debug bounding box around a moving "
            "sprite using cc.DrawNode?"
        ),
        "ground_truth": {
            "required_modules": ["drawnode", "sprite"],
            "required_apis": ["cc.DrawNode", "drawRect",
                              "getBoundingBoxToWorld", "clear"],
            "required_keywords": ["DrawNode", "drawRect",
                                  "getBoundingBoxToWorld", "clear"],
        },
    },
    {
        "id": "cross_api_007",
        "category": "cross_api",
        "question": (
            "How do you create a scrollable list of image items "
            "using ccui.ScrollView and ccui.ImageView?"
        ),
        "ground_truth": {
            "required_modules": ["ccui"],
            "required_apis": ["ccui.ScrollView", "ccui.ImageView",
                              "setDirection", "addChild",
                              "setInnerContainerSize"],
            "required_keywords": ["ScrollView", "ImageView",
                                  "setDirection", "setInnerContainerSize"],
        },
    },
    {
        "id": "cross_api_008",
        "category": "cross_api",
        "question": (
            "How do you transition to a new scene while stopping "
            "background music and cleaning up textures?"
        ),
        "ground_truth": {
            "required_modules": ["director", "audio"],
            "required_apis": ["cc.director.runScene", "cc.TransitionFade",
                              "cc.audioEngine.stopMusic",
                              "cc.textureCache.removeUnusedTextures"],
            "required_keywords": ["runScene", "stopMusic",
                                  "removeUnusedTextures"],
        },
    },
    {
        "id": "cross_api_009",
        "category": "cross_api",
        "question": (
            "How do you detect the platform and conditionally save "
            "data to local storage on mobile only?"
        ),
        "ground_truth": {
            "required_modules": ["sys"],
            "required_apis": ["cc.sys.isMobile",
                              "cc.sys.localStorage.setItem"],
            "required_keywords": ["isMobile", "localStorage", "setItem"],
        },
    },
    {
        "id": "cross_api_010",
        "category": "cross_api",
        "question": (
            "How do you create a gradient background and overlay "
            "a label with outline effect?"
        ),
        "ground_truth": {
            "required_modules": ["layer", "label"],
            "required_apis": ["cc.LayerGradient", "cc.Label",
                              "enableOutline"],
            "required_keywords": ["LayerGradient", "Label",
                                  "enableOutline"],
        },
    },
    {
        "id": "cross_api_011",
        "category": "cross_api",
        "question": (
            "How do you create an armature animation and trigger "
            "a custom event when it completes?"
        ),
        "ground_truth": {
            "required_modules": ["ccs", "events"],
            "required_apis": [
                "ccs.Armature.create",
                "animation.play",
                "setMovementEventCallFunc",
                "cc.eventManager.dispatchCustomEvent",
            ],
            "required_keywords": ["Armature", "play",
                                  "setMovementEventCallFunc",
                                  "dispatchCustomEvent"],
        },
    },
    {
        "id": "cross_api_012",
        "category": "cross_api",
        "question": (
            "How do you create a sprite with a custom shader program "
            "and animate it with actions?"
        ),
        "ground_truth": {
            "required_modules": ["sprite", "actions"],
            "required_apis": ["cc.Sprite", "cc.GLProgram",
                              "setShaderProgram", "runAction"],
            "required_keywords": ["Sprite", "GLProgram",
                                  "setShaderProgram", "runAction"],
        },
    },
    {
        "id": "cross_api_013",
        "category": "cross_api",
        "question": (
            "How do you compute the distance between two nodes "
            "and draw a line segment between them?"
        ),
        "ground_truth": {
            "required_modules": ["types", "drawnode"],
            "required_apis": ["cc.pDistance", "getPosition",
                              "cc.DrawNode", "drawSegment"],
            "required_keywords": ["pDistance", "getPosition",
                                  "DrawNode", "drawSegment"],
        },
    },
    {
        "id": "cross_api_014",
        "category": "cross_api",
        "question": (
            "How do you use cc.loader to load JSON data and display "
            "it in a ccui.Text widget?"
        ),
        "ground_truth": {
            "required_modules": ["director", "ccui"],
            "required_apis": ["cc.loader.loadJson", "ccui.Text",
                              "setString"],
            "required_keywords": ["loadJson", "Text", "setString"],
        },
    },
    {
        "id": "cross_api_015",
        "category": "cross_api",
        "question": (
            "How do you slow down all game actions using the scheduler "
            "time scale while keeping UI responsive?"
        ),
        "ground_truth": {
            "required_modules": ["director"],
            "required_apis": ["cc.director.getScheduler",
                              "setTimeScale"],
            "required_keywords": ["getScheduler", "setTimeScale"],
        },
    },
]

# ---------------------------------------------------------------------------
# 6. NEGATIVE_QUESTIONS — 15 questions with no/false answers
# ---------------------------------------------------------------------------

NEGATIVE_QUESTIONS: list[dict[str, Any]] = [
    # --- 5 "does X have method Y?" (no) ---
    {
        "id": "negative_001",
        "category": "negative",
        "question": "Does cc.Sprite have a setPhysicsEnabled() method?",
        "ground_truth": {
            "expected_answer": "no",
            "correct_alternative": (
                "Use node.setPhysicsBody() to attach a physics body."
            ),
            "required_keywords": ["no", "setPhysicsBody"],
        },
    },
    {
        "id": "negative_002",
        "category": "negative",
        "question": "Does cc.Label have a setFont() method?",
        "ground_truth": {
            "expected_answer": "no",
            "correct_alternative": (
                "Use setSystemFontName() for system fonts or provide "
                "a TTF config via createWithTTF."
            ),
            "required_keywords": ["no", "setSystemFontName"],
        },
    },
    {
        "id": "negative_003",
        "category": "negative",
        "question": "Does cc.audioEngine have a setVolume() method?",
        "ground_truth": {
            "expected_answer": "no",
            "correct_alternative": (
                "Use setMusicVolume() for music and setEffectsVolume() "
                "for sound effects."
            ),
            "required_keywords": ["no", "setMusicVolume",
                                  "setEffectsVolume"],
        },
    },
    {
        "id": "negative_004",
        "category": "negative",
        "question": "Does cc.Node have a getWorldPosition() method?",
        "ground_truth": {
            "expected_answer": "no",
            "correct_alternative": (
                "Use convertToWorldSpace(cc.p(0,0)) or "
                "getBoundingBoxToWorld() to get world position."
            ),
            "required_keywords": ["no", "convertToWorldSpace"],
        },
    },
    {
        "id": "negative_005",
        "category": "negative",
        "question": "Does cc.DrawNode have a drawTriangle() method?",
        "ground_truth": {
            "expected_answer": "no",
            "correct_alternative": (
                "Use drawPoly with 3 vertices to draw a triangle."
            ),
            "required_keywords": ["no", "drawPoly"],
        },
    },
    # --- 5 "can you do X?" (no / not directly) ---
    {
        "id": "negative_006",
        "category": "negative",
        "question": (
            "Can you directly set the z-index of a node relative "
            "to all other nodes in the scene using setLocalZOrder?"
        ),
        "ground_truth": {
            "expected_answer": "no",
            "correct_alternative": (
                "setLocalZOrder is relative to siblings. "
                "Use setGlobalZOrder for scene-wide ordering."
            ),
            "required_keywords": ["no", "setGlobalZOrder", "sibling"],
        },
    },
    {
        "id": "negative_007",
        "category": "negative",
        "question": (
            "Can you play two different background music tracks "
            "simultaneously with cc.audioEngine?"
        ),
        "ground_truth": {
            "expected_answer": "no",
            "correct_alternative": (
                "cc.audioEngine supports only one background music track. "
                "Use playEffect for additional audio."
            ),
            "required_keywords": ["no", "one", "playEffect"],
        },
    },
    {
        "id": "negative_008",
        "category": "negative",
        "question": (
            "Can cc.DrawNode draw text directly?"
        ),
        "ground_truth": {
            "expected_answer": "no",
            "correct_alternative": (
                "cc.DrawNode only draws shapes. "
                "Use cc.Label for text rendering."
            ),
            "required_keywords": ["no", "Label"],
        },
    },
    {
        "id": "negative_009",
        "category": "negative",
        "question": (
            "Can you use cc.eventManager.addListener to listen for "
            "network events?"
        ),
        "ground_truth": {
            "expected_answer": "no",
            "correct_alternative": (
                "cc.eventManager handles touch, keyboard, mouse, "
                "acceleration, and custom events, not network events."
            ),
            "required_keywords": ["no", "touch", "keyboard", "custom"],
        },
    },
    {
        "id": "negative_010",
        "category": "negative",
        "question": (
            "Can you render HTML content inside a ccui.Layout?"
        ),
        "ground_truth": {
            "expected_answer": "no",
            "correct_alternative": (
                "ccui.Layout only supports Cocos2d-x widgets. "
                "HTML rendering is not supported within the scene graph."
            ),
            "required_keywords": ["no", "widget"],
        },
    },
    # --- 5 true/false assertions ---
    {
        "id": "negative_011",
        "category": "negative",
        "question": (
            "True or false: cc.sys.isNative is a method that you call "
            "with parentheses."
        ),
        "ground_truth": {
            "expected_answer": "false",
            "correct_alternative": (
                "cc.sys.isNative is a boolean property, not a method."
            ),
            "required_keywords": ["false", "property", "boolean"],
        },
    },
    {
        "id": "negative_012",
        "category": "negative",
        "question": (
            "True or false: cc.Sprite default anchor point is (0, 0)."
        ),
        "ground_truth": {
            "expected_answer": "false",
            "correct_alternative": (
                "cc.Sprite default anchor point is (0.5, 0.5)."
            ),
            "required_keywords": ["false", "0.5"],
        },
    },
    {
        "id": "negative_013",
        "category": "negative",
        "question": (
            "True or false: cc.eventManager.addEventHandler is "
            "the correct method to register a touch listener."
        ),
        "ground_truth": {
            "expected_answer": "false",
            "correct_alternative": (
                "The correct method is cc.eventManager.addListener."
            ),
            "required_keywords": ["false", "addListener"],
        },
    },
    {
        "id": "negative_014",
        "category": "negative",
        "question": (
            "True or false: cc.repeatForever takes a repeat count "
            "parameter."
        ),
        "ground_truth": {
            "expected_answer": "false",
            "correct_alternative": (
                "cc.repeatForever takes only an action parameter "
                "and loops indefinitely. cc.repeat takes a count."
            ),
            "required_keywords": ["false", "action", "cc.repeat"],
        },
    },
    {
        "id": "negative_015",
        "category": "negative",
        "question": (
            "True or false: ccui.Button extends cc.Sprite."
        ),
        "ground_truth": {
            "expected_answer": "false",
            "correct_alternative": (
                "ccui.Button extends ccui.Widget, "
                "which extends cc.ProtectedNode."
            ),
            "required_keywords": ["false", "ccui.Widget"],
        },
    },
]

# ---------------------------------------------------------------------------
# 7. get_all_questions — combine all categories
# ---------------------------------------------------------------------------


def get_all_questions(
    docs_glob: str = "local-context7-cocos2d-x-only/docs/*.md",
) -> list[dict[str, Any]]:
    """Return all ~130 benchmark questions from all 6 categories."""
    questions: list[dict[str, Any]] = []
    questions.extend(generate_factual_questions(docs_glob))
    questions.extend(CONCEPTUAL_QUESTIONS)
    questions.extend(CODEGEN_QUESTIONS)
    questions.extend(HALLUCINATION_QUESTIONS)
    questions.extend(CROSS_API_QUESTIONS)
    questions.extend(NEGATIVE_QUESTIONS)
    return questions


if __name__ == "__main__":
    qs = get_all_questions()
    print(f"Total benchmark questions: {len(qs)}")
    from collections import Counter
    cats = Counter(q["category"] for q in qs)
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count}")
