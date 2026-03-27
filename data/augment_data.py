"""Augment training data with paraphrased, compositional, and debugging examples.

Targets:
1. Paraphrase singleton API questions (1 example → 3-4 variants)
2. Add correct-vs-wrong examples (common mistakes)
3. Add compositional/multi-step examples (combining 2+ APIs)
4. Add debugging/troubleshooting examples
"""
import json
import re
import random
from pathlib import Path

SEED = 42
random.seed(SEED)

DATA_DIR = Path(__file__).parent
TRAIN_PATH = DATA_DIR / "train.jsonl"
AUGMENTED_PATH = DATA_DIR / "augmented.jsonl"

# --- Paraphrase templates ---
# Each maps a question pattern to alternative phrasings
QUESTION_PARAPHRASES = [
    # "What is the signature of X?" variants
    (r"What is the signature of (.+?)\?",
     [
         "How do you call {0}?",
         "What parameters does {0} accept?",
         "Show the function signature for {0}.",
         "What arguments does {0} take?",
     ]),
    # "What does X return?" variants
    (r"What does (.+?) return\?",
     [
         "What is the return value of {0}?",
         "What type does {0} return?",
         "Describe the return value of {0}.",
     ]),
    # "What is X?" variants
    (r"What is (.+?)\?",
     [
         "Explain what {0} does.",
         "Describe the purpose of {0}.",
         "How does {0} work?",
     ]),
    # "How to use X" variants
    (r"How (?:do you|to) (?:use|create|make) (.+?)\??",
     [
         "Show an example of using {0}.",
         "What's the correct way to use {0}?",
         "Explain how to work with {0}.",
     ]),
]

# --- Common mistakes for correct-vs-wrong examples ---
COMMON_MISTAKES = [
    {
        "instruction": "Is cc.Sprite.create('image.png').addTo(parent) valid in Cocos2d-x JS?",
        "output": "No, cc.Sprite.create() returns a sprite but does not have an addTo() method that can be chained directly. The correct approach is:\nvar sprite = new cc.Sprite('image.png');\nparent.addChild(sprite);\nIn Cocos2d-x JS, you typically use `new cc.Sprite(filename)` (constructor) rather than `cc.Sprite.create()`, and `addChild` is called on the parent node.",
    },
    {
        "instruction": "Why does my cc.Sequence not play all actions? I wrote: node.runAction(cc.Sequence(action1, action2))",
        "output": "cc.Sequence requires cc.sequence() (lowercase) as a helper function, or you need to use cc.Sequence.create(). The correct usage is:\nnode.runAction(cc.sequence(action1, action2));\nAlternatively: node.runAction(cc.Sequence.create(action1, action2));\nUsing cc.Sequence() directly as a constructor without create() may silently fail or only execute the first action.",
    },
    {
        "instruction": "My cc.Label text is not visible. I created it with: var label = new cc.Label('Hello'); parent.addChild(label);",
        "output": "cc.Label requires a font specification. Use one of the factory methods:\n- cc.Label.createWithSystemFont('Hello', 'Arial', 24)\n- cc.Label.createWithTTF('Hello', 'fonts/myfont.ttf', 24)\n- cc.Label.createWithBMFont('fonts/myfont.fnt', 'Hello')\nThe plain constructor without font info produces an invisible or errored label. Also ensure the label's position is set to a visible area on screen.",
    },
    {
        "instruction": "Why does cc.AudioEngine.play('sound.mp3') not play on mobile?",
        "output": "On mobile browsers, audio playback must be initiated by a user gesture (tap/click) due to autoplay policies. Common fixes:\n1. Call cc.AudioEngine.play() inside a touch event handler\n2. Use cc.AudioEngine.playEffect() for short sounds and cc.AudioEngine.playMusic() for background music\n3. Preload audio files: cc.AudioEngine.preload('sound.mp3')\nAlso verify the file path is correct relative to your resources directory and that the audio format is supported on the target platform.",
    },
    {
        "instruction": "My cc.EventListener is not receiving touch events. What could be wrong?",
        "output": "Common reasons for touch events not firing:\n1. The node must be added to the scene (not just created)\n2. The listener must be registered: cc.eventManager.addListener(listener, node)\n3. Check swallowTouches: if a higher-priority listener swallows touches, lower ones won't fire\n4. The node's contentSize must be set (for cc.EventListener.TOUCH_ONE_BY_ONE, onTouchBegan must return true)\n5. Ensure the node is visible and not scaled to 0\nExample:\nvar listener = cc.EventListener.create({\n    event: cc.EventListener.TOUCH_ONE_BY_ONE,\n    onTouchBegan: function(touch, event) { return true; },\n    onTouchMoved: function(touch, event) { /* handle */ }\n});\ncc.eventManager.addListener(listener, myNode);",
    },
    {
        "instruction": "I'm using cc.Director.runScene() but the new scene doesn't appear. The old scene stays.",
        "output": "cc.Director.runScene() should only be used for the very first scene. For subsequent scenes, use:\n- cc.director.replaceScene(newScene) — replaces current scene\n- cc.director.pushScene(newScene) — pushes onto scene stack\nAlso note the API difference: use cc.director (lowercase singleton) not cc.Director (the class).\nCorrect usage: cc.director.replaceScene(new MyScene());\nIf using transitions: cc.director.replaceScene(cc.TransitionFade.create(1.0, new MyScene()));",
    },
    {
        "instruction": "cc.Node.setPosition(100, 200) is not working. The node stays at origin.",
        "output": "In Cocos2d-x JS, setPosition takes a cc.p point or two numbers depending on the binding version. Try:\n- node.setPosition(cc.p(100, 200)); // using cc.p helper\n- node.x = 100; node.y = 200; // direct property assignment\n- node.attr({x: 100, y: 200}); // batch attribute setting\nAlso verify the node's parent anchor point and that you're calling setPosition after addChild (some layouts reset positions).",
    },
    {
        "instruction": "Why does my cc.Sprite show as a white rectangle instead of the image?",
        "output": "A white rectangle typically means the texture failed to load. Common causes:\n1. Wrong file path — paths are relative to the resources directory\n2. File not included in build — check your project.json or resource list\n3. Case sensitivity — 'Image.png' vs 'image.png' matters on some platforms\n4. Image format — use PNG or JPG; some platforms don't support WebP\n5. Image too large — check cc.sys.getMaxTextureSize()\nDebug steps:\n- Check console for loading errors\n- Verify: cc.loader.getRes('image.png') is not null\n- Try an absolute URL to rule out path issues",
    },
    {
        "instruction": "My cc.Animation plays too fast. How do I control the speed?",
        "output": "Control animation speed with:\n1. Set delay per frame: animation.setDelayPerUnit(0.1) — time in seconds between frames\n2. Wrap action in cc.speed(): node.runAction(cc.speed(cc.animate(animation), 0.5)) — 0.5 = half speed\n3. Set total duration indirectly: animation.setDelayPerUnit(totalDuration / frameCount)\nNote: cc.Animate.create(animation) creates the action from the animation. The animation object holds frame data, while cc.Animate is the runnable action.",
    },
    {
        "instruction": "cc.scheduler.schedule() crashes with 'undefined is not a function'. How to fix?",
        "output": "Use the node's scheduler via the director, not cc.scheduler directly:\nCorrect: this.schedule(callback, interval, repeat, delay)\nOr: cc.director.getScheduler().schedule(callback, target, interval, repeat, delay, paused)\n\nCommon mistakes:\n- this.schedule must be called on a cc.Node subclass (inside a layer/scene)\n- The callback must be a function, not a string\n- Make sure 'this' context is correct — use .bind(this) if needed\n\nExample:\nthis.schedule(function(dt) {\n    // runs every 0.5 seconds\n}, 0.5);",
    },
]

# --- Compositional/multi-step examples ---
COMPOSITIONAL = [
    {
        "instruction": "How do I create a sprite that moves to position (300,400) and then fades out over 2 seconds?",
        "output": "Create the sprite, then run a sequence of moveTo and fadeOut actions:\nvar sprite = new cc.Sprite('image.png');\nsprite.setPosition(cc.p(100, 100));\nparent.addChild(sprite);\n\nvar move = cc.moveTo(1.0, cc.p(300, 400));\nvar fade = cc.fadeOut(2.0);\nsprite.runAction(cc.sequence(move, fade));",
    },
    {
        "instruction": "How to play a sound effect when a button is tapped in ccui?",
        "output": "Create a ccui.Button and add a touch event listener that plays the sound:\nvar button = new ccui.Button('btn_normal.png', 'btn_pressed.png');\nbutton.setPosition(cc.p(240, 160));\nparent.addChild(button);\n\nbutton.addTouchEventListener(function(sender, type) {\n    if (type === ccui.Widget.TOUCH_ENDED) {\n        cc.audioEngine.playEffect('click.mp3');\n    }\n});",
    },
    {
        "instruction": "How to create a scrollable list of labels using ccui.ScrollView?",
        "output": "Create a ScrollView, add labels as children, and set the inner container size:\nvar scrollView = new ccui.ScrollView();\nscrollView.setContentSize(cc.size(300, 400));\nscrollView.setDirection(ccui.ScrollView.DIR_VERTICAL);\nscrollView.setBounceEnabled(true);\nparent.addChild(scrollView);\n\nvar items = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5'];\nvar yOffset = items.length * 50;\nscrollView.setInnerContainerSize(cc.size(300, yOffset));\n\nfor (var i = 0; i < items.length; i++) {\n    var label = cc.Label.createWithSystemFont(items[i], 'Arial', 20);\n    label.setPosition(cc.p(150, yOffset - (i * 50) - 25));\n    scrollView.addChild(label);\n}",
    },
    {
        "instruction": "How to make a sprite follow a Bezier curve path while rotating?",
        "output": "Use cc.bezierTo for the path and cc.rotateBy for rotation, running them in parallel with cc.spawn:\nvar sprite = new cc.Sprite('arrow.png');\nsprite.setPosition(cc.p(50, 50));\nparent.addChild(sprite);\n\nvar bezierConfig = [\n    cc.p(150, 300),  // control point 1\n    cc.p(350, 300),  // control point 2\n    cc.p(400, 50)    // end point\n];\nvar bezierAction = cc.bezierTo(2.0, bezierConfig);\nvar rotate = cc.rotateBy(2.0, 360);\nsprite.runAction(cc.spawn(bezierAction, rotate));",
    },
    {
        "instruction": "How to create a scene transition with a fade effect and load new scene?",
        "output": "Use cc.TransitionFade with cc.director.replaceScene:\nvar newScene = new GameScene();\nvar transition = cc.TransitionFade.create(1.5, newScene, cc.color(0, 0, 0));\ncc.director.replaceScene(transition);\n\nOther transition types:\n- cc.TransitionSlideInR.create(duration, scene) — slide from right\n- cc.TransitionFlipX.create(duration, scene) — flip horizontally\n- cc.TransitionCrossFade.create(duration, scene) — cross-fade\n- cc.TransitionPageTurn.create(duration, scene, backwards) — page turn effect",
    },
    {
        "instruction": "How to animate a Spine skeleton and listen for animation completion?",
        "output": "Create a sp.SkeletonAnimation, play an animation, and set a completion listener:\nvar skeleton = sp.SkeletonAnimation.create('spine/hero.json', 'spine/hero.atlas');\nskeleton.setPosition(cc.p(240, 160));\nparent.addChild(skeleton);\n\n// Play 'run' animation on track 0, looping\nskeleton.setAnimation(0, 'run', true);\n\n// Listen for animation events\nskeleton.setAnimationListener(this, function(skeleton, trackIndex, type, event, loopCount) {\n    if (type === sp.AnimationEventType.END) {\n        cc.log('Animation ended on track ' + trackIndex);\n    } else if (type === sp.AnimationEventType.COMPLETE) {\n        cc.log('Animation loop completed: ' + loopCount);\n    }\n});",
    },
    {
        "instruction": "How to save and load game progress using cc.sys.localStorage?",
        "output": "Use cc.sys.localStorage for persistent key-value storage:\n// Save game progress\nvar saveData = {\n    level: 5,\n    score: 12500,\n    lives: 3\n};\ncc.sys.localStorage.setItem('gameProgress', JSON.stringify(saveData));\n\n// Load game progress\nvar loaded = cc.sys.localStorage.getItem('gameProgress');\nif (loaded) {\n    var data = JSON.parse(loaded);\n    cc.log('Level: ' + data.level + ', Score: ' + data.score);\n} else {\n    cc.log('No saved progress found');\n}\n\n// Remove saved data\ncc.sys.localStorage.removeItem('gameProgress');",
    },
    {
        "instruction": "How to create a particle effect at the position where the user touches?",
        "output": "Add a touch listener to the layer and create a particle system at the touch location:\nvar listener = cc.EventListener.create({\n    event: cc.EventListener.TOUCH_ONE_BY_ONE,\n    onTouchBegan: function(touch, event) {\n        var pos = touch.getLocation();\n        var particle = new cc.ParticleSystem('particles/explosion.plist');\n        particle.setPosition(pos);\n        particle.setAutoRemoveOnFinish(true);\n        this.addChild(particle);\n        return true;\n    }.bind(this)\n});\ncc.eventManager.addListener(listener, this);",
    },
    {
        "instruction": "How to create a countdown timer label that updates every second?",
        "output": "Create a label and use this.schedule to update it every second:\nvar timeLeft = 60;\nvar timerLabel = cc.Label.createWithSystemFont(timeLeft.toString(), 'Arial', 36);\ntimerLabel.setPosition(cc.p(240, 400));\nthis.addChild(timerLabel);\n\nthis.schedule(function(dt) {\n    timeLeft--;\n    timerLabel.setString(timeLeft.toString());\n    if (timeLeft <= 0) {\n        this.unschedule(arguments.callee);\n        cc.log('Time is up!');\n    }\n}.bind(this), 1.0);",
    },
    {
        "instruction": "How to draw a health bar using cc.DrawNode that updates with player HP?",
        "output": "Use cc.DrawNode to draw a filled rectangle representing the health bar:\nvar maxHP = 100;\nvar currentHP = 75;\nvar barWidth = 200;\nvar barHeight = 20;\n\nvar bgBar = new cc.DrawNode();\nvar hpBar = new cc.DrawNode();\nbgBar.setPosition(cc.p(120, 440));\nhpBar.setPosition(cc.p(120, 440));\nthis.addChild(bgBar);\nthis.addChild(hpBar);\n\nfunction updateHP(hp) {\n    currentHP = Math.max(0, Math.min(hp, maxHP));\n    var ratio = currentHP / maxHP;\n    bgBar.clear();\n    bgBar.drawRect(cc.p(0, 0), cc.p(barWidth, barHeight), cc.color(80, 80, 80), 1, cc.color(0, 0, 0));\n    hpBar.clear();\n    var color = ratio > 0.5 ? cc.color(0, 200, 0) : (ratio > 0.25 ? cc.color(255, 165, 0) : cc.color(200, 0, 0));\n    hpBar.drawRect(cc.p(0, 0), cc.p(barWidth * ratio, barHeight), color, 0, color);\n}\nupdateHP(currentHP);",
    },
]

# --- Comparison examples ---
COMPARISONS = [
    {
        "instruction": "What is the difference between cc.sequence and cc.spawn?",
        "output": "cc.sequence runs actions one after another (sequentially), while cc.spawn runs actions all at the same time (in parallel).\n\n- cc.sequence(action1, action2): action2 starts only after action1 completes\n- cc.spawn(action1, action2): both actions start and run simultaneously\n\nExample:\n// Sequential: move right, then move up\nnode.runAction(cc.sequence(cc.moveBy(1, cc.p(100, 0)), cc.moveBy(1, cc.p(0, 100))));\n\n// Parallel: move right AND fade out at the same time\nnode.runAction(cc.spawn(cc.moveBy(1, cc.p(100, 0)), cc.fadeOut(1)));",
    },
    {
        "instruction": "What is the difference between cc.moveTo and cc.moveBy?",
        "output": "cc.moveTo moves a node to an absolute position, while cc.moveBy moves it by a relative offset from its current position.\n\n- cc.moveTo(duration, targetPos): final position is always targetPos regardless of starting position\n- cc.moveBy(duration, delta): moves by delta from wherever the node currently is\n\nExample: if node is at (100, 100):\n- cc.moveTo(1, cc.p(300, 200)) → ends at (300, 200)\n- cc.moveBy(1, cc.p(300, 200)) → ends at (400, 300)\n\nmoveBy is more reusable since it's relative. moveTo is better when you need exact positioning.",
    },
    {
        "instruction": "What is the difference between cc.director.replaceScene and cc.director.pushScene?",
        "output": "replaceScene destroys the current scene and replaces it with a new one. pushScene keeps the current scene on a stack and adds the new scene on top.\n\n- cc.director.replaceScene(newScene): current scene is released from memory, cannot go back\n- cc.director.pushScene(newScene): current scene pauses, can return with cc.director.popScene()\n\nUse replaceScene for normal scene changes (menu → game). Use pushScene/popScene for temporary overlays (game → pause menu → back to game) where you want to preserve the previous scene's state.",
    },
    {
        "instruction": "What is the difference between cc.Label.createWithSystemFont and cc.Label.createWithTTF?",
        "output": "createWithSystemFont uses a font installed on the device OS, while createWithTTF loads a custom .ttf font file bundled with your app.\n\n- cc.Label.createWithSystemFont('text', 'Arial', 24): uses system 'Arial', may look different across platforms\n- cc.Label.createWithTTF('text', 'fonts/custom.ttf', 24): uses your bundled font, looks identical everywhere\n\nUse SystemFont for debug/placeholder text. Use TTF for final UI where consistent appearance across iOS/Android/web matters. TTF has a small load time on first use.",
    },
    {
        "instruction": "What is the difference between cc.EventListener.TOUCH_ONE_BY_ONE and cc.EventListener.TOUCH_ALL_AT_ONCE?",
        "output": "TOUCH_ONE_BY_ONE receives individual touch events (one finger at a time), while TOUCH_ALL_AT_ONCE receives all touches in a single callback.\n\n- TOUCH_ONE_BY_ONE: onTouchBegan/Moved/Ended receive a single cc.Touch. Supports swallowTouches to prevent propagation. onTouchBegan must return true to claim the touch.\n- TOUCH_ALL_AT_ONCE: onTouchesBegan/Moved/Ended receive an array of cc.Touch objects. Better for multi-touch gestures (pinch, multi-finger swipe).\n\nUse ONE_BY_ONE for buttons and single-touch interactions. Use ALL_AT_ONCE for gesture recognition or games requiring multi-touch.",
    },
]


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def write_jsonl(path, items):
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def generate_paraphrases(train_data):
    """Generate paraphrased variants for existing examples."""
    augmented = []
    for example in train_data:
        inst = example["instruction"]
        for pattern, templates in QUESTION_PARAPHRASES:
            match = re.match(pattern, inst, re.IGNORECASE)
            if match:
                groups = match.groups()
                # Pick 1-2 random paraphrases
                chosen = random.sample(templates, min(2, len(templates)))
                for tmpl in chosen:
                    new_inst = tmpl.format(*groups)
                    augmented.append({
                        "instruction": new_inst,
                        "output": example["output"],
                    })
                break
    return augmented


def main():
    train_data = load_jsonl(TRAIN_PATH)
    print(f"Original train examples: {len(train_data)}")

    # Generate paraphrases
    paraphrases = generate_paraphrases(train_data)
    random.shuffle(paraphrases)
    # Cap at ~300 to avoid overwhelming the dataset
    paraphrases = paraphrases[:300]
    print(f"Paraphrased examples: {len(paraphrases)}")

    # Combine all augmented data
    augmented = paraphrases + COMMON_MISTAKES + COMPOSITIONAL + COMPARISONS
    random.shuffle(augmented)
    print(f"Total augmented examples: {len(augmented)}")

    write_jsonl(AUGMENTED_PATH, augmented)
    print(f"Written to {AUGMENTED_PATH}")

    # Also write a combined training file
    combined = train_data + augmented
    random.shuffle(combined)
    combined_path = DATA_DIR / "train-augmented.jsonl"
    write_jsonl(combined_path, combined)
    print(f"Combined training data: {len(combined)} -> {combined_path}")


if __name__ == "__main__":
    main()
