"""
Generate ~3000 conversational QA pairs for Cocos2d-x JS with heavy phrasing variation.
Each major API method/class gets 5-10 differently phrased questions covering:
casual, technical, goal-oriented, beginner, comparison, debugging, code review styles.
Output: data/conversational-qa.jsonl
"""

import json
import random
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "conversational-qa.jsonl")

random.seed(42)


# ---------------------------------------------------------------------------
# Knowledge base: topics with multiple QA variants
# Each topic: { "answers": {style: answer}, "questions": {style: [list]} }
# We build a flat list of (instruction, output) pairs at the end.
# ---------------------------------------------------------------------------

TOPICS = []


def topic(questions_by_style, answers_by_style):
    """Register a topic. questions_by_style and answers_by_style are dicts
    keyed by style name. Each question list is paired with its style answer."""
    TOPICS.append((questions_by_style, answers_by_style))


# ============================================================
# SPRITE
# ============================================================
topic(
    {
        "casual": [
            "hey how do I make a sprite?",
            "what's the easiest way to put an image on screen?",
            "how do i create a sprite from an image file?",
        ],
        "technical": [
            "What is the constructor signature for cc.Sprite in Cocos2d-x JS?",
            "What are the overloaded forms of cc.Sprite.create()?",
        ],
        "goal": [
            "I need to display an image on screen",
            "I want to show a character image in my scene",
        ],
        "beginner": [
            "I'm new to Cocos2d-x, how do I add a picture?",
            "explain sprites for a beginner",
        ],
        "debugging": [
            "my sprite isn't showing up on screen",
            "I created a sprite but it's invisible, what's wrong?",
        ],
    },
    {
        "casual": "Use `new cc.Sprite('res/image.png')` to create a sprite from a file. Then add it to your layer or scene with `this.addChild(sprite)` and set its position with `sprite.setPosition(x, y)`. The default anchor is center (0.5, 0.5).",
        "technical": "cc.Sprite has multiple constructor overloads:\n```js\nnew cc.Sprite(filename)\nnew cc.Sprite(texture, rect)\nnew cc.Sprite(spriteFrame)\n```\nAlternatively use the static factory: `cc.Sprite.create(filename)` or `cc.Sprite.create(filename, rect)`. The default anchor point is (0.5, 0.5).",
        "goal": "Create a `cc.Sprite` with your image path and add it to the scene:\n```js\nconst sprite = new cc.Sprite('res/hero.png')\nsprite.setPosition(240, 160)\nthis.addChild(sprite)\n```",
        "beginner": "A sprite is how you display an image in Cocos2d-x. Think of it as a picture you place on screen. Create one with `new cc.Sprite('res/myimage.png')`, set where it goes with `sprite.setPosition(x, y)`, and add it to your scene with `this.addChild(sprite)`.",
        "debugging": "If your sprite isn't showing up, check these common issues: (1) the file path is correct and the image exists in your resources, (2) the sprite is added as a child to a node that's on screen via `addChild()`, (3) the position is within the visible screen area, (4) opacity is not 0 and visible is not false, (5) the z-order isn't behind another opaque node.",
    },
)

topic(
    {
        "casual": [
            "how do I flip a sprite horizontally?",
            "can I mirror a sprite image?",
        ],
        "technical": [
            "What methods control sprite flipping in Cocos2d-x JS?",
        ],
        "goal": [
            "I need my character to face left when moving left",
        ],
        "beginner": [
            "how to make a sprite face the other direction?",
        ],
    },
    {
        "casual": "Call `sprite.setFlippedX(true)` to flip horizontally. Use `sprite.setFlippedY(true)` for vertical. These only affect the sprite image, not its children.",
        "technical": "Use `sprite.setFlippedX(flippedX: boolean)` and `sprite.setFlippedY(flippedY: boolean)`. Query state with `sprite.isFlippedX()` / `sprite.isFlippedY()`. Alternatively, use negative scaleX (`sprite.setScaleX(-1)`) which also flips children.",
        "goal": "When your character moves left, call `sprite.setFlippedX(true)`. When moving right, call `sprite.setFlippedX(false)`. This mirrors the sprite image without affecting children or collision boxes.",
        "beginner": "Use `sprite.setFlippedX(true)` to mirror your sprite horizontally. It's like flipping a picture. Set it back to `false` to return to normal.",
    },
)

topic(
    {
        "casual": [
            "how do I change a sprite's image at runtime?",
            "can I swap textures on a sprite?",
        ],
        "technical": [
            "What is the method signature for setTexture on cc.Sprite?",
            "How do I use setSpriteFrame to change a sprite's display?",
        ],
        "goal": [
            "I want to change my character's appearance during gameplay",
        ],
    },
    {
        "casual": "Call `sprite.setTexture('res/new_image.png')` to swap the entire texture, or `sprite.setSpriteFrame('frame_name.png')` if using a sprite atlas. The frame name must already be loaded in `cc.spriteFrameCache`.",
        "technical": "`sprite.setTexture(filename: string)` or `sprite.setTexture(texture: cc.Texture2D)` replaces the whole texture. For atlas-based frames: `sprite.setSpriteFrame(frameName: string)` or `sprite.setSpriteFrame(frame: cc.SpriteFrame)`. You can also use `sprite.setTextureRect(rect)` to show a sub-region of the current texture.",
        "goal": "For runtime appearance changes, use sprite frames from an atlas:\n```js\ncc.spriteFrameCache.addSpriteFrames('res/chars.plist', 'res/chars.png')\n// Later:\nsprite.setSpriteFrame('hero_powered_up.png')\n```\nOr swap the entire texture: `sprite.setTexture('res/alt_hero.png')`.",
    },
)

topic(
    {
        "casual": [
            "what's a sprite batch node for?",
            "how do batch nodes work?",
        ],
        "technical": [
            "How does cc.SpriteBatchNode optimize draw calls?",
        ],
        "goal": [
            "I have lots of sprites and my game is slow, how do I optimize?",
        ],
    },
    {
        "casual": "A `cc.SpriteBatchNode` draws many sprites in a single draw call, as long as they all share the same texture atlas. Create one with `new cc.SpriteBatchNode('res/atlas.png', capacity)` and add sprites as children of the batch node instead of the layer.",
        "technical": "`cc.SpriteBatchNode` batches all child sprites into one draw call. All children must use the same texture. Usage:\n```js\nconst batch = new cc.SpriteBatchNode('res/atlas.png', 100)\nlayer.addChild(batch)\nconst s = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('enemy.png'))\nbatch.addChild(s)\n```",
        "goal": "Use `cc.SpriteBatchNode` to reduce draw calls. Put all sprites that share the same texture atlas under one batch node:\n```js\nconst batch = new cc.SpriteBatchNode('res/atlas.png', 100)\nthis.addChild(batch)\n// Add all sprites to batch instead of layer\nfor (let i = 0; i < 50; i++) {\n    const s = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('bullet.png'))\n    batch.addChild(s)\n}\n```",
    },
)

topic(
    {
        "casual": [
            "how do I load a sprite atlas / plist?",
            "what's spriteFrameCache?",
        ],
        "technical": [
            "What are the methods on cc.spriteFrameCache?",
        ],
        "goal": [
            "I want to use a texture atlas with my sprites",
        ],
    },
    {
        "casual": "Load an atlas with `cc.spriteFrameCache.addSpriteFrames('res/ui.plist', 'res/ui.png')`. Then get frames by name: `cc.spriteFrameCache.getSpriteFrame('btn_play.png')`. You can use these frames directly in sprite constructors.",
        "technical": "cc.spriteFrameCache is a global singleton with these methods:\n- `addSpriteFrames(url, texture)` - load a plist atlas\n- `getSpriteFrame(path)` - retrieve a frame by name\n- `removeUnusedSpriteFrames()` - free unused frames\n- `removeSpriteFramesFromFile(url)` - remove frames loaded from a specific plist",
        "goal": "Load your atlas in scene init, then use frames anywhere:\n```js\ncc.spriteFrameCache.addSpriteFrames('res/ui.plist', 'res/ui.png')\nconst sprite = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('btn_play.png'))\n// Or set frame by name directly:\nsprite.setSpriteFrame('btn_play.png')\n```",
    },
)

# ============================================================
# ACTIONS - MOVE
# ============================================================
topic(
    {
        "casual": [
            "how do I move a node to a position?",
            "what's the simplest way to animate movement?",
        ],
        "technical": [
            "What is the method signature for cc.moveTo and cc.moveBy?",
        ],
        "goal": [
            "I want to smoothly move a sprite from one point to another",
            "I need to animate a character walking to a target",
        ],
        "comparison": [
            "should I use moveTo or moveBy?",
            "what's the difference between moveTo and moveBy?",
        ],
        "beginner": [
            "how do I animate movement in cocos2d-x?",
        ],
    },
    {
        "casual": "Use `node.runAction(cc.moveTo(duration, x, y))` to move to an absolute position, or `cc.moveBy(duration, dx, dy)` for relative movement. Duration is in seconds.",
        "technical": "Signatures:\n```js\ncc.moveTo(duration: number, x: number, y: number): MoveTo\ncc.moveTo(duration: number, pos: cc.Point): MoveTo\ncc.moveBy(duration: number, dx: number, dy: number): MoveBy\ncc.moveBy(duration: number, dPos: cc.Point): MoveBy\n```\nRun with `node.runAction(action)`.",
        "goal": "Animate movement like this:\n```js\n// Move to absolute position in 1 second\nnode.runAction(cc.moveTo(1.0, cc.p(300, 400)))\n// Move relative to current position\nnode.runAction(cc.moveBy(0.5, cc.p(100, 0)))\n```\nChain movements with `cc.sequence()` for multi-step paths.",
        "comparison": "`cc.moveTo` moves to an absolute position - always ends at the same point. `cc.moveBy` moves relative to the current position - the offset is added. Use moveTo when you know the destination coordinates. Use moveBy when you want a direction/distance regardless of starting position (e.g., 'jump up 50 pixels').",
        "beginner": "In Cocos2d-x, you animate things using 'actions'. To move something:\n```js\nnode.runAction(cc.moveTo(1.0, cc.p(300, 200)))\n```\nThis slides the node to position (300, 200) over 1 second. The engine handles all the in-between frames for you.",
    },
)

# ============================================================
# ACTIONS - SCALE
# ============================================================
topic(
    {
        "casual": [
            "how do I scale/resize a node with animation?",
            "how to make something grow or shrink?",
        ],
        "technical": [
            "What are the signatures for cc.scaleTo and cc.scaleBy?",
        ],
        "goal": [
            "I want a pop/bounce effect when a button is tapped",
        ],
    },
    {
        "casual": "Use `node.runAction(cc.scaleTo(duration, scale))` to animate to a target scale. For a pop effect, scale up then back down with a sequence.",
        "technical": "```js\ncc.scaleTo(duration, scale): ScaleTo\ncc.scaleTo(duration, scaleX, scaleY): ScaleTo\ncc.scaleBy(duration, scale): ScaleBy\ncc.scaleBy(duration, scaleX, scaleY): ScaleBy\n```\nscaleTo goes to absolute scale, scaleBy multiplies current scale.",
        "goal": "For a pop/bounce effect:\n```js\nnode.runAction(cc.sequence(\n    cc.scaleTo(0.15, 1.2),\n    cc.scaleTo(0.15, 1.0)\n))\n```\nAdd easing for a bouncier feel: `cc.scaleTo(0.3, 1.3).easing(cc.easeBackOut())`.",
    },
)

# ============================================================
# ACTIONS - ROTATE
# ============================================================
topic(
    {
        "casual": [
            "how do I rotate something?",
            "how to spin a node continuously?",
        ],
        "technical": [
            "What are the parameters for cc.rotateTo and cc.rotateBy?",
        ],
        "goal": [
            "I want a loading spinner that rotates forever",
        ],
    },
    {
        "casual": "Use `cc.rotateTo(duration, angle)` for absolute rotation or `cc.rotateBy(duration, angle)` for relative. Angles are in degrees, clockwise.",
        "technical": "```js\ncc.rotateTo(duration, angle): RotateTo\ncc.rotateTo(duration, angleX, angleY): RotateTo\ncc.rotateBy(duration, angle): RotateBy\ncc.rotateBy(duration, angleX, angleY): RotateBy\n```\nAngles are degrees, clockwise positive.",
        "goal": "For a continuous spinner:\n```js\nnode.runAction(cc.repeatForever(cc.rotateBy(2.0, 360)))\n```\nThis rotates 360 degrees every 2 seconds, forever.",
    },
)

# ============================================================
# ACTIONS - FADE
# ============================================================
topic(
    {
        "casual": [
            "how do I fade something in or out?",
            "how to make a node appear gradually?",
        ],
        "technical": [
            "What are cc.fadeIn, cc.fadeOut, and cc.fadeTo?",
        ],
        "goal": [
            "I want to fade out a node then remove it",
            "I need a smooth fade-in transition for a UI element",
        ],
    },
    {
        "casual": "`cc.fadeIn(duration)` fades from transparent to opaque, `cc.fadeOut(duration)` does the opposite, and `cc.fadeTo(duration, opacity)` goes to a specific opacity (0-255).",
        "technical": "```js\ncc.fadeIn(duration): FadeIn     // opacity 0 -> 255\ncc.fadeOut(duration): FadeOut   // opacity 255 -> 0\ncc.fadeTo(duration, opacity): FadeTo  // to specific value\n```\nOpacity range is 0-255.",
        "goal": "Fade out then remove:\n```js\nnode.runAction(cc.sequence(\n    cc.fadeOut(0.5),\n    cc.callFunc(() => node.removeFromParent())\n))\n```\nFor fade-in, set opacity to 0 first:\n```js\nnode.setOpacity(0)\nnode.runAction(cc.fadeIn(0.5))\n```",
    },
)

# ============================================================
# ACTIONS - SEQUENCE & SPAWN
# ============================================================
topic(
    {
        "casual": [
            "how do I chain animations one after another?",
            "how to run multiple actions at the same time?",
        ],
        "technical": [
            "What is the difference between cc.sequence and cc.spawn?",
            "How do cc.sequence and cc.spawn work?",
        ],
        "comparison": [
            "sequence vs spawn for my use case - when do I use which?",
            "should I use sequence or spawn here?",
        ],
        "goal": [
            "I want to chain animations together",
            "I need to run a move and a fade at the same time",
        ],
        "beginner": [
            "explain sequence and spawn actions",
        ],
    },
    {
        "casual": "`cc.sequence(a, b, c)` runs actions one after another. `cc.spawn(a, b)` runs them simultaneously. You can nest them for complex animations.",
        "technical": "```js\ncc.sequence(...actions: cc.FiniteTimeAction[]): Sequence\ncc.spawn(...actions: cc.FiniteTimeAction[]): Spawn\n```\nSequence runs actions serially; spawn runs them in parallel. Both accept varargs or an array. They can be nested: `cc.sequence(cc.spawn(move, fade), callback)`.",
        "comparison": "Use `cc.sequence` when actions must happen in order (move, then fade, then callback). Use `cc.spawn` when actions should happen simultaneously (move AND fade at the same time). Combine them for complex flows:\n```js\nnode.runAction(cc.sequence(\n    cc.spawn(cc.moveTo(1, cc.p(400, 300)), cc.fadeTo(1, 100)),\n    cc.callFunc(() => { /* done */ })\n))\n```",
        "goal": "Chain: `cc.sequence(action1, action2, action3)`. Parallel: `cc.spawn(action1, action2)`. Combined:\n```js\nnode.runAction(cc.sequence(\n    cc.spawn(cc.moveTo(1, cc.p(400, 300)), cc.fadeTo(1, 100)),\n    cc.callFunc(() => { /* cleanup */ })\n))\n```",
        "beginner": "Think of `cc.sequence` as a playlist - actions play one after another. `cc.spawn` is like playing multiple instruments at once - all actions run in parallel. You can combine them:\n```js\nnode.runAction(cc.sequence(\n    cc.spawn(cc.moveTo(1, cc.p(200, 200)), cc.fadeIn(1)),\n    cc.callFunc(() => console.log('done'))\n))\n```",
    },
)

# ============================================================
# ACTIONS - REPEAT
# ============================================================
topic(
    {
        "casual": [
            "how do I repeat an action?",
            "how to loop an animation forever?",
        ],
        "technical": [
            "What are cc.repeat and cc.repeatForever?",
        ],
        "goal": [
            "I want a bouncing animation that never stops",
        ],
    },
    {
        "casual": "`cc.repeat(action, times)` repeats a set number of times. `cc.repeatForever(action)` loops endlessly. You can also chain `.repeat(n)` or `.repeatForever()` on any action interval.",
        "technical": "```js\ncc.repeat(action: cc.FiniteTimeAction, times: number): Repeat\ncc.repeatForever(action: cc.FiniteTimeAction): RepeatForever\n```\nAlternatively, use method chaining: `action.repeat(5)` or `action.repeatForever()`.",
        "goal": "Infinite bounce:\n```js\nnode.runAction(cc.repeatForever(cc.sequence(\n    cc.moveBy(0.5, cc.p(0, 50)),\n    cc.moveBy(0.5, cc.p(0, -50))\n)))\n```",
    },
)

# ============================================================
# ACTIONS - EASING
# ============================================================
topic(
    {
        "casual": [
            "how do I add easing to an animation?",
            "how to make movement feel smooth and natural?",
        ],
        "technical": [
            "What easing functions are available in Cocos2d-x JS?",
            "How do I apply an ease function to an action?",
        ],
        "goal": [
            "I want a bouncy animation effect",
            "I want my movement to ease in and out smoothly",
        ],
    },
    {
        "casual": "Chain `.easing()` on any action: `cc.moveTo(1, cc.p(300, 300)).easing(cc.easeBounceOut())`. Common options: `cc.easeIn(rate)`, `cc.easeOut(rate)`, `cc.easeSineInOut()`, `cc.easeBackOut()`, `cc.easeBounceOut()`.",
        "technical": "Apply via `.easing(easeObj)` on any ActionInterval. Available functions include:\n- `cc.easeIn/Out/InOut(rate)` - polynomial\n- `cc.easeSineIn/Out/InOut()` - sinusoidal\n- `cc.easeBackIn/Out/InOut()` - overshoot\n- `cc.easeBounceIn/Out/InOut()` - bounce\n- `cc.easeElasticIn/Out/InOut(period?)` - elastic\n- `cc.easeExponentialIn/Out/InOut()` - exponential\n- `cc.easeBezierAction(p0,p1,p2,p3)` - custom bezier curve",
        "goal": "For a bouncy feel: `action.easing(cc.easeBounceOut())`. For smooth starts/stops: `action.easing(cc.easeSineInOut())`. Example:\n```js\nnode.runAction(cc.moveTo(1.0, cc.p(300, 300)).easing(cc.easeBounceOut()))\n// Or for a springy scale:\nnode.runAction(cc.scaleTo(0.3, 1.3).easing(cc.easeBackOut()))\n```",
    },
)

# ============================================================
# ACTIONS - CALLFUNC
# ============================================================
topic(
    {
        "casual": [
            "how do I run code after an action finishes?",
            "how to add a callback to an action?",
        ],
        "technical": [
            "What is cc.callFunc and how does it work?",
        ],
        "goal": [
            "I need to execute logic after an animation completes",
        ],
    },
    {
        "casual": "Use `cc.callFunc(callback)` inside a sequence:\n```js\nnode.runAction(cc.sequence(\n    cc.moveTo(1, cc.p(200, 200)),\n    cc.callFunc(() => console.log('arrived!'))\n))\n```",
        "technical": "`cc.callFunc(callback: Function): CallFunc` - an instant action that executes a function. Full signature: `cc.callFunc(callback, selectorTarget?, data?)`. The callback receives `(target, data)` as arguments when selectorTarget is provided.",
        "goal": "Place `cc.callFunc()` at the end of a `cc.sequence` to run code after animations:\n```js\nnode.runAction(cc.sequence(\n    cc.fadeOut(0.5),\n    cc.callFunc(() => {\n        node.removeFromParent()\n        this.spawnNewEnemy()\n    })\n))\n```",
    },
)

# ============================================================
# ACTIONS - JUMP & BEZIER
# ============================================================
topic(
    {
        "casual": [
            "how do I make something jump?",
            "how to create a jumping animation?",
        ],
        "technical": [
            "What are the parameters for cc.jumpTo and cc.jumpBy?",
        ],
        "goal": [
            "I want my character to do a hop/jump motion",
        ],
    },
    {
        "casual": "Use `cc.jumpTo(duration, position, height, numJumps)` or `cc.jumpBy` for relative jumps. Example: `node.runAction(cc.jumpTo(1.0, cc.p(300, 100), 80, 3))` makes 3 hops reaching 80px high.",
        "technical": "```js\ncc.jumpTo(duration, position: cc.Point, height, jumps): JumpTo\ncc.jumpTo(duration, x, y, height, jumps): JumpTo\ncc.jumpBy(duration, position: cc.Point, height, jumps): JumpBy\n```\nHeight is the peak height of each jump, jumps is the number of bounces.",
        "goal": "For a character hop:\n```js\nnode.runAction(cc.jumpTo(1.0, cc.p(300, 100), 80, 3))\n```\nFor a single relative jump: `node.runAction(cc.jumpBy(0.5, cc.p(0, 0), 60, 1))`.",
    },
)

topic(
    {
        "casual": [
            "how do I move something along a curved path?",
            "what's a bezier action?",
        ],
        "technical": [
            "How do cc.bezierTo and cc.bezierBy work?",
        ],
        "goal": [
            "I want to animate a projectile along a curved trajectory",
        ],
    },
    {
        "casual": "Use `cc.bezierTo(duration, controlPoints)` with an array of 3 control points. The curve goes from current position through the control points to the last one.",
        "technical": "```js\ncc.bezierTo(duration, points: cc.Point[]): BezierTo  // 3 control points\ncc.bezierBy(duration, points: cc.Point[]): BezierBy\n```\nThe 3 points are: first control, second control, end point. Also available: `cc.catmullRomTo`, `cc.cardinalSplineTo` for smoother multi-point curves.",
        "goal": "For a curved projectile:\n```js\nnode.runAction(cc.bezierTo(2.0, [\n    cc.p(0, 200), cc.p(200, 200), cc.p(300, 0)\n]))\n```\nFor smoother paths with multiple waypoints, use `cc.catmullRomTo(duration, points)`.",
    },
)

# ============================================================
# ACTIONS - ANIMATION (SPRITE FRAME)
# ============================================================
topic(
    {
        "casual": [
            "how do I animate a sprite with multiple frames?",
            "how to make a sprite sheet animation?",
        ],
        "technical": [
            "How does cc.animate work with cc.Animation?",
        ],
        "goal": [
            "I want my character to have a walk/run animation cycle",
        ],
        "beginner": [
            "how do sprite animations work in cocos2d-x?",
        ],
    },
    {
        "casual": "Create an `cc.Animation` from sprite frames, then run it with `cc.animate()`:\n```js\nconst frames = []\nfor (let i = 1; i <= 8; i++)\n    frames.push(cc.spriteFrameCache.getSpriteFrame(`run_0${i}.png`))\nconst anim = new cc.Animation(frames, 0.08)\nsprite.runAction(cc.repeatForever(cc.animate(anim)))\n```",
        "technical": "Create a `cc.Animation` with frames and delay:\n```js\nnew cc.Animation(frames: cc.SpriteFrame[], delay: number, loops?: number)\n```\nThen wrap with `cc.animate(animation)` to create a runnable action. Use `animation.setRestoreOriginalFrame(true)` to reset after playing. Set `loops` to 0 for infinite.",
        "goal": "Load sprite frames from your atlas, create an animation, and loop it:\n```js\ncc.spriteFrameCache.addSpriteFrames('res/hero.plist', 'res/hero.png')\nconst frames = []\nfor (let i = 1; i <= 8; i++)\n    frames.push(cc.spriteFrameCache.getSpriteFrame(`run_${String(i).padStart(2, '0')}.png`))\nconst anim = new cc.Animation(frames, 0.08, 0)\nsprite.runAction(cc.repeatForever(cc.animate(anim)))\n```",
        "beginner": "Sprite animation is like a flipbook. You have multiple images (frames) and Cocos2d-x displays them one after another quickly to create motion. Load your frames, create an animation with a delay between frames, and run it:\n```js\nconst frames = [frame1, frame2, frame3] // cc.SpriteFrame objects\nconst anim = new cc.Animation(frames, 0.1) // 0.1s per frame\nsprite.runAction(cc.animate(anim))\n```",
    },
)

# ============================================================
# ACTIONS - INSTANT ACTIONS
# ============================================================
topic(
    {
        "casual": [
            "how do I show or hide a node instantly?",
            "what instant actions are available?",
        ],
        "technical": [
            "What are the instant action types in Cocos2d-x JS?",
        ],
    },
    {
        "casual": "Use `cc.show()`, `cc.hide()`, `cc.toggleVisibility()` for visibility. `cc.place(x, y)` teleports instantly. `cc.removeSelf()` removes from parent. `cc.flipX(true)` / `cc.flipY(true)` flip instantly. All are zero-duration actions useful inside sequences.",
        "technical": "Instant actions (cc.ActionInstant subclasses):\n- `cc.show()` / `cc.hide()` / `cc.toggleVisibility()`\n- `cc.place(x, y)` or `cc.place(pos)` - instant reposition\n- `cc.removeSelf()` - remove from parent\n- `cc.flipX(flip)` / `cc.flipY(flip)`\n- `cc.callFunc(callback)` - execute code\nAll have zero duration and work in sequences.",
    },
)

# ============================================================
# ACTIONS - TINT & BLINK
# ============================================================
topic(
    {
        "casual": [
            "how to make a sprite flash or blink?",
            "how do I change a sprite's color over time?",
        ],
        "technical": [
            "What are cc.tintTo, cc.tintBy, and cc.blink?",
        ],
        "goal": [
            "I want a damage flash effect on my character",
        ],
    },
    {
        "casual": "`cc.blink(duration, blinks)` makes a node blink on/off. `cc.tintTo(duration, r, g, b)` changes color. For a damage flash, tint red then back to white.",
        "technical": "```js\ncc.blink(duration, blinks): Blink\ncc.tintTo(duration, r, g, b): TintTo\ncc.tintBy(duration, dr, dg, db): TintBy\n```\nBlink toggles visibility rapidly. TintTo/By modify the node's color channel.",
        "goal": "Damage flash effect:\n```js\nsprite.runAction(cc.sequence(\n    cc.tintTo(0.05, 255, 0, 0),  // flash red\n    cc.delayTime(0.1),\n    cc.tintTo(0.05, 255, 255, 255)  // back to normal\n))\n```\nOr use blink: `sprite.runAction(cc.blink(0.5, 5))` for 5 flashes in 0.5s.",
    },
)

# ============================================================
# ACTIONS - SPEED & FOLLOW
# ============================================================
topic(
    {
        "casual": [
            "how do I speed up or slow down an action?",
        ],
        "technical": [
            "How does cc.speed work?",
        ],
        "goal": [
            "I want to play an action at 2x speed",
        ],
    },
    {
        "casual": "Wrap any action with `cc.speed(action, speedMultiplier)`. A speed of 2.0 plays twice as fast, 0.5 plays at half speed. You can also use `action.setSpeed(2.0)` or `action.getSpeed()`.",
        "technical": "`cc.speed(action: cc.FiniteTimeAction, speed: number): Speed` - wraps an action with a speed modifier. Also available as `action.setSpeed(speed)` / `action.getSpeed()` on ActionInterval instances.",
        "goal": "Wrap your action: `node.runAction(cc.speed(cc.moveTo(2, cc.p(400, 300)), 2.0))` plays the 2-second move in 1 second. Adjust dynamically via `speedAction.setSpeed(3.0)`.",
    },
)

topic(
    {
        "casual": [
            "how do I make the camera follow a character?",
        ],
        "technical": [
            "How does cc.follow work?",
        ],
        "goal": [
            "I need a scrolling camera that tracks my player",
        ],
    },
    {
        "casual": "Use `cc.follow(targetNode, worldBoundary)` on a layer. The layer will scroll to keep the target node centered within the boundary rect.",
        "technical": "`cc.follow(followedNode: cc.Node, rect: cc.Rect): Follow` - makes the target node run this action, which causes the node (usually a layer) to move so the followed node stays visible within the boundary rect.",
        "goal": "Make a layer follow your player:\n```js\nconst follow = cc.follow(playerSprite, cc.rect(0, 0, mapWidth, mapHeight))\nthis.runAction(follow)\n```\nThe layer scrolls to keep the player centered, clamped within the map boundary.",
    },
)

# ============================================================
# AUDIO
# ============================================================
topic(
    {
        "casual": [
            "how do I play background music?",
            "how to add music to my game?",
        ],
        "technical": [
            "What is the API for cc.audioEngine music playback?",
        ],
        "goal": [
            "I want looping background music in my scene",
        ],
        "beginner": [
            "how does audio work in cocos2d-x?",
        ],
    },
    {
        "casual": "Use `cc.audioEngine.playMusic('res/audio/bgm.mp3', true)` where `true` means loop. Control volume with `cc.audioEngine.setMusicVolume(0.7)`. Pause/resume with `pauseMusic()` / `resumeMusic()`.",
        "technical": "```js\ncc.audioEngine.playMusic(url: string, loop: boolean): void\ncc.audioEngine.stopMusic(releaseData?: boolean): void\ncc.audioEngine.pauseMusic(): void\ncc.audioEngine.resumeMusic(): void\ncc.audioEngine.setMusicVolume(volume: number): void // 0.0-1.0\ncc.audioEngine.getMusicVolume(): number\ncc.audioEngine.isMusicPlaying(): boolean\n```",
        "goal": "Start looping BGM in your scene's onEnter:\n```js\ncc.audioEngine.playMusic('res/audio/bgm_main.mp3', true)\ncc.audioEngine.setMusicVolume(0.7)\n```\nPause when game pauses: `cc.audioEngine.pauseMusic()`. Resume: `cc.audioEngine.resumeMusic()`.",
        "beginner": "Cocos2d-x has a built-in audio engine accessed via `cc.audioEngine`. It handles two types of audio: background music (one track at a time) and sound effects (multiple can play simultaneously). Start music with `cc.audioEngine.playMusic('file.mp3', true)` and play effects with `cc.audioEngine.playEffect('sfx.mp3')`.",
    },
)

topic(
    {
        "casual": [
            "how do I play a sound effect?",
            "how to play a short sound?",
        ],
        "technical": [
            "What is the method signature for cc.audioEngine.playEffect?",
        ],
        "goal": [
            "I want to play a coin pickup sound",
            "I need explosion and hit sound effects",
        ],
    },
    {
        "casual": "Call `cc.audioEngine.playEffect('res/audio/sfx_coin.mp3')` for a one-shot sound. It returns an audio ID you can use to stop it later with `cc.audioEngine.stopEffect(id)`. Set volume with `setEffectsVolume(0.5)`.",
        "technical": "```js\ncc.audioEngine.playEffect(url: string, loop?: boolean, pitch?: number, pan?: number, gain?: number): number | null\ncc.audioEngine.stopEffect(audioId: number): void\ncc.audioEngine.pauseEffect(audioId: number): void\ncc.audioEngine.stopAllEffects(): void\ncc.audioEngine.setEffectsVolume(volume: number): void // 0.0-1.0\ncc.audioEngine.preloadEffect(path: string): void\n```",
        "goal": "Play and optionally track the sound:\n```js\n// One-shot\ncc.audioEngine.playEffect('res/audio/sfx_coin.mp3')\n// Looping with tracking\nconst id = cc.audioEngine.playEffect('res/audio/sfx_engine.mp3', true)\n// Stop later:\ncc.audioEngine.stopEffect(id)\n```\nPreload at startup for zero-latency playback: `cc.audioEngine.preloadEffect('res/audio/sfx_coin.mp3')`.",
    },
)

# ============================================================
# NODE - CHILDREN
# ============================================================
topic(
    {
        "casual": [
            "how do I add and remove children in cocos2d?",
            "how does the scene graph work?",
        ],
        "technical": [
            "What are the child management methods on cc.Node?",
        ],
        "goal": [
            "I want to organize my game objects in a hierarchy",
        ],
        "beginner": [
            "what is addChild and how does it work?",
        ],
    },
    {
        "casual": "Use `parent.addChild(child)` to add, optionally with z-order: `addChild(child, zOrder)`. Remove with `child.removeFromParent()` or `parent.removeChild(child)`. Find children with `getChildByName('name')` or `getChildByTag(tag)`.",
        "technical": "```js\nnode.addChild(child, localZOrder?, tag?): void\nnode.removeChild(child, cleanup?): void\nnode.removeChildByTag(tag, cleanup?): void\nnode.removeChildByName(name, cleanup?): void\nnode.removeAllChildren(cleanup?): void\nnode.removeFromParent(cleanup?): void\nnode.getChildByTag(tag): cc.Node\nnode.getChildByName(name): cc.Node\nnode.getChildren(): cc.Node[]\nnode.getChildrenCount(): number\n```\nThe `cleanup` parameter (default true) removes all running actions and scheduled callbacks.",
        "goal": "Organize your scene as a tree:\n```js\nconst bg = new cc.Sprite('bg.png')\nthis.addChild(bg, -1)  // behind everything\nconst hero = new cc.Sprite('hero.png')\nhero.setName('hero')\nthis.addChild(hero, 1)\n// Find later:\nconst h = this.getChildByName('hero')\n// Remove:\nhero.removeFromParent()\n```",
        "beginner": "`addChild` puts a node inside another node, creating a parent-child relationship. Children move, rotate, and scale with their parent. The z-order controls draw order (higher = on top). Example: `this.addChild(sprite, 1)` adds the sprite with z-order 1.",
    },
)

# ============================================================
# NODE - POSITION / ANCHOR
# ============================================================
topic(
    {
        "casual": [
            "how do I set anchor point?",
            "what's an anchor point?",
        ],
        "technical": [
            "What methods control anchor point on cc.Node?",
        ],
        "beginner": [
            "explain anchor points in cocos2d-x",
        ],
    },
    {
        "casual": "`node.setAnchorPoint(cc.p(0.5, 0.5))` sets center anchor (default for sprites). (0,0) is bottom-left, (1,1) is top-right. The anchor is the pivot for position, rotation, and scale.",
        "technical": "```js\nnode.setAnchorPoint(point: cc.Point): void\nnode.setAnchorPoint(x, y): void\nnode.getAnchorPoint(): cc.Point         // normalized 0-1\nnode.getAnchorPointInPoints(): cc.Point  // in pixels\nnode.ignoreAnchorPointForPosition(ignore): void\n```\nAnchor affects how setPosition places the node, and is the pivot for rotation/scale.",
        "beginner": "The anchor point is the 'pin' that holds a node in place. When you set a position, the anchor point sits at that position. Default for sprites is (0.5, 0.5) meaning the center. Set (0, 0) and the bottom-left corner sits at the position instead. It also affects rotation - nodes spin around their anchor.",
    },
)

# ============================================================
# NODE - SCHEDULING
# ============================================================
topic(
    {
        "casual": [
            "how do I run code every frame?",
            "how to schedule a timer?",
        ],
        "technical": [
            "What are the scheduling methods on cc.Node?",
        ],
        "goal": [
            "I need game logic to run every frame",
            "I want to call a function every 2 seconds",
        ],
        "beginner": [
            "how does the update loop work in cocos2d-x?",
        ],
    },
    {
        "casual": "Call `this.scheduleUpdate()` then override `update(dt)` for per-frame logic. Use `this.schedule(callback, interval)` for timed callbacks. `this.scheduleOnce(cb, delay)` runs once after a delay.",
        "technical": "```js\nnode.scheduleUpdate(): void              // enables update(dt) every frame\nnode.unscheduleUpdate(): void\nnode.schedule(callback, interval?, repeat?, delay?, key?): void\nnode.scheduleOnce(callback, delay, key?): void\nnode.unschedule(callback): void\nnode.unscheduleAllCallbacks(): void\n```\nThe `update(dt)` method receives delta time in seconds.",
        "goal": "Per-frame logic:\n```js\nthis.scheduleUpdate()\n// ...\nupdate(dt) {\n    this.hero.x += this.speed * dt\n}\n```\nTimed callback:\n```js\nthis.schedule(this.spawnEnemy, 2.0) // every 2s\nthis.scheduleOnce(this.showBoss, 30.0) // once after 30s\n```",
        "beginner": "Cocos2d-x has a built-in scheduler. Call `this.scheduleUpdate()` in your onEnter, then define an `update(dt)` method. It runs every frame (usually 60 times/second). The `dt` parameter is the time since last frame in seconds, use it to keep movement smooth regardless of frame rate.",
    },
)

# ============================================================
# NODE - LIFECYCLE
# ============================================================
topic(
    {
        "casual": [
            "what are the node lifecycle callbacks?",
            "when does onEnter get called?",
        ],
        "technical": [
            "What lifecycle methods can I override on cc.Node?",
        ],
        "goal": [
            "I need to initialize things when my node enters the scene",
        ],
    },
    {
        "casual": "`onEnter()` fires when a node is added to the scene graph. `onExit()` when removed. Always call `super.onEnter()` / `super.onExit()`. Use onEnter for initialization and onExit for cleanup.",
        "technical": "Override these lifecycle callbacks:\n```js\nonEnter()                        // added to running scene\nonExit()                         // removed from scene\nonEnterTransitionDidFinish()     // after enter transition\nonExitTransitionDidStart()       // before exit transition\ncleanup()                        // stops all actions/timers\n```\nAlways call `super.onEnter()` etc. `onEnter` is the standard place to set up listeners, schedulers, and initial state.",
        "goal": "Override `onEnter()` for initialization:\n```js\nonEnter() {\n    super.onEnter()\n    this.scheduleUpdate()\n    this._listener = cc.eventManager.addListener({...}, this)\n}\nonExit() {\n    cc.eventManager.removeListener(this._listener)\n    super.onExit()\n}\n```",
    },
)

# ============================================================
# NODE - COORDINATE CONVERSION
# ============================================================
topic(
    {
        "casual": [
            "how do I convert between world and local coordinates?",
            "how to check if a touch is inside a node?",
        ],
        "technical": [
            "What coordinate conversion methods does cc.Node have?",
        ],
        "goal": [
            "I need to detect if the user tapped on my sprite",
        ],
    },
    {
        "casual": "Use `node.convertToNodeSpace(worldPoint)` to convert a world-space point to local. For touch hit testing:\n```js\nconst local = node.convertTouchToNodeSpace(touch)\nconst rect = cc.rect(0, 0, node.width, node.height)\nif (cc.rectContainsPoint(rect, local)) { /* hit! */ }\n```",
        "technical": "```js\nnode.convertToNodeSpace(worldPoint): cc.Point\nnode.convertToWorldSpace(nodePoint): cc.Point\nnode.convertToNodeSpaceAR(worldPoint): cc.Point    // anchor-relative\nnode.convertToWorldSpaceAR(nodePoint): cc.Point\nnode.convertTouchToNodeSpace(touch): cc.Point\nnode.convertTouchToNodeSpaceAR(touch): cc.Point\n```\nAR variants use the anchor point as origin instead of bottom-left.",
        "goal": "Touch hit detection:\n```js\nonTouchBegan: (touch, event) => {\n    const localPt = sprite.convertTouchToNodeSpace(touch)\n    const rect = cc.rect(0, 0, sprite.width, sprite.height)\n    if (cc.rectContainsPoint(rect, localPt)) {\n        // sprite was tapped!\n        return true\n    }\n    return false\n}\n```",
    },
)

# ============================================================
# NODE - BOUNDING BOX
# ============================================================
topic(
    {
        "casual": [
            "how do I get a node's bounding box?",
            "how to check collision between two nodes?",
        ],
        "technical": [
            "What is the difference between getBoundingBox and getBoundingBoxToWorld?",
        ],
        "goal": [
            "I need simple collision detection between sprites",
        ],
    },
    {
        "casual": "`node.getBoundingBox()` returns a rect in parent space. `node.getBoundingBoxToWorld()` returns in world space. Use `cc.rectOverlapsRect(rect1, rect2)` to check overlap.",
        "technical": "```js\nnode.getBoundingBox(): cc.Rect        // local/parent space\nnode.getBoundingBoxToWorld(): cc.Rect  // world space\n```\nUse world-space rects for cross-hierarchy collision checking with `cc.rectOverlapsRect(a, b)`.",
        "goal": "Simple AABB collision:\n```js\nconst rectA = spriteA.getBoundingBoxToWorld()\nconst rectB = spriteB.getBoundingBoxToWorld()\nif (cc.rectOverlapsRect(rectA, rectB)) {\n    // collision!\n}\n```",
    },
)

# ============================================================
# NODE - ACTIONS ON NODE
# ============================================================
topic(
    {
        "casual": [
            "how do I stop all actions on a node?",
            "how to stop a specific action?",
        ],
        "technical": [
            "What action management methods does cc.Node have?",
        ],
    },
    {
        "casual": "`node.stopAllActions()` stops everything. `node.stopAction(action)` stops a specific one. Use `node.stopActionByTag(tag)` if you tagged the action. Check running actions with `node.getNumberOfRunningActions()`.",
        "technical": "```js\nnode.runAction(action): cc.Action\nnode.stopAllActions(): void\nnode.stopAction(action): void\nnode.stopActionByTag(tag): void\nnode.getActionByTag(tag): cc.Action\nnode.getNumberOfRunningActions(): number\n```\nTag actions with `action.setTag(10)` for later retrieval or stopping.",
    },
)

# ============================================================
# NODE - ATTR
# ============================================================
topic(
    {
        "casual": [
            "how to set multiple node properties at once?",
            "what does node.attr() do?",
        ],
        "technical": [
            "How does the attr method work on cc.Node?",
        ],
    },
    {
        "casual": "Use `node.attr({x: 100, y: 200, scale: 1.5, opacity: 200})` to set multiple properties in one call. It's faster than calling individual setters.",
        "technical": "`node.attr(attrs: object): void` sets multiple properties at once. Accepts any direct property names like `x`, `y`, `scale`, `scaleX`, `scaleY`, `rotation`, `opacity`, `visible`, `width`, `height`, `anchorX`, `anchorY`, `color`, `tag`, `zIndex`.",
    },
)

# ============================================================
# LABEL
# ============================================================
topic(
    {
        "casual": [
            "how do I show text on screen?",
            "how to create a label?",
        ],
        "technical": [
            "What are the factory methods for cc.Label?",
        ],
        "goal": [
            "I need to display score text in my game",
        ],
        "beginner": [
            "how to put text on the screen in cocos2d-x?",
        ],
        "code_review": [
            "is this the right way to create a label?",
        ],
    },
    {
        "casual": "Use `cc.Label.createWithSystemFont('Hello', 'Arial', 24)` for a simple text label. Add it to your scene and set position. Update text with `label.setString('new text')`.",
        "technical": "Factory methods:\n```js\ncc.Label.createWithSystemFont(text, font, fontSize, dimensions?, hAlign?, vAlign?)\ncc.Label.createWithTTF(ttfConfig, text, hAlign?, maxLineWidth?)\ncc.Label.createWithBMFont(fntFile, text, hAlign?, maxLineWidth?)\ncc.Label.createWithCharMap(charMapFile, itemWidth, itemHeight, startChar)\n```\nSystem font is simplest, TTF is cross-platform with effects support, BMFont is fastest for bitmap fonts.",
        "goal": "Create a score label:\n```js\nconst scoreLabel = cc.Label.createWithSystemFont('Score: 0', 'Arial', 24)\nscoreLabel.setPosition(cc.director.getWinSize().width / 2, 550)\nscoreLabel.setTextColor(cc.color(255, 255, 255))\nthis.addChild(scoreLabel, 10)\n// Update:\nscoreLabel.setString('Score: ' + score)\n```",
        "beginner": "Use `cc.Label` to display text. The simplest way: `cc.Label.createWithSystemFont('Hello World', 'Arial', 24)`. This creates a label using the system font. Position it with `setPosition()` and add it to your scene with `addChild()`. Change the text anytime with `setString('new text')`.",
        "code_review": "The correct way to create a label is one of: `cc.Label.createWithSystemFont(text, font, size)` for system fonts, `cc.Label.createWithBMFont(fntPath, text)` for bitmap fonts, or `cc.Label.createWithTTF(ttfConfig, text)` for TTF. Common mistakes: using the deprecated `cc.LabelTTF` class, forgetting to add it as a child, or not setting a position.",
    },
)

topic(
    {
        "casual": [
            "how do I add outline or shadow to a label?",
            "how to make label text look fancy?",
        ],
        "technical": [
            "What text effects does cc.Label support?",
        ],
        "goal": [
            "I want outlined text for my game title",
        ],
    },
    {
        "casual": "Use `label.enableOutline(cc.color(0,0,0), 2)` for a black outline, `label.enableShadow()` for a drop shadow, or `label.enableGlow(color)` for a glow (TTF only). Remove effects with `label.disableEffect()`.",
        "technical": "```js\nlabel.enableOutline(color: cc.Color, outlineSize: number): void  // TTF/system only\nlabel.enableShadow(color?, offset?: cc.Size, blurRadius?): void\nlabel.enableGlow(color: cc.Color): void  // TTF only\nlabel.enableGradient(first, second, direction): void\nlabel.disableEffect(): void\nlabel.setTextColor(color: cc.Color): void\n```",
        "goal": "For a game title with outline and shadow:\n```js\nconst title = cc.Label.createWithSystemFont('MY GAME', 'Impact', 48)\ntitle.setTextColor(cc.color(255, 220, 0))\ntitle.enableOutline(cc.color(0, 0, 0, 255), 3)\ntitle.enableShadow(cc.color(0, 0, 0, 128), cc.size(2, -2), 0)\n```",
    },
)

topic(
    {
        "casual": [
            "how do I use a bitmap font?",
            "what's a BMFont label?",
        ],
        "technical": [
            "How do I create a label with BMFont in Cocos2d-x JS?",
        ],
    },
    {
        "casual": "Use `cc.Label.createWithBMFont('res/fonts/score.fnt', '0000')`. BMFont is fast and looks consistent across platforms since the font is pre-rendered as an image. Great for score counters and HUDs.",
        "technical": "```js\ncc.Label.createWithBMFont(fntFile: string, text: string, hAlign?, maxLineWidth?, imageOffset?): cc.Label\n```\nBMFont labels use a .fnt file and associated texture. They're faster than system/TTF labels and support per-letter animation via `label.getLetter(index)`.",
    },
)

# ============================================================
# EVENTS - TOUCH
# ============================================================
topic(
    {
        "casual": [
            "how do I handle touch input?",
            "how to detect when the user taps?",
        ],
        "technical": [
            "How do I create a touch event listener in Cocos2d-x JS?",
            "What is the TOUCH_ONE_BY_ONE event listener?",
        ],
        "goal": [
            "I need to detect taps on the screen",
            "I want drag and drop functionality",
        ],
        "debugging": [
            "touch events aren't firing",
            "my touch listener doesn't work",
        ],
        "beginner": [
            "how does touch input work in cocos2d-x?",
        ],
    },
    {
        "casual": "Use `cc.eventManager.addListener` with a touch config:\n```js\ncc.eventManager.addListener({\n    event: cc.EventListener.TOUCH_ONE_BY_ONE,\n    swallowTouches: true,\n    onTouchBegan: (touch, event) => {\n        const loc = touch.getLocation()\n        return true // must return true!\n    }\n}, this)\n```",
        "technical": "Create a TOUCH_ONE_BY_ONE listener for single-touch:\n```js\ncc.eventManager.addListener({\n    event: cc.EventListener.TOUCH_ONE_BY_ONE,\n    swallowTouches: boolean,\n    onTouchBegan: (touch: cc.Touch, event) => boolean,\n    onTouchMoved?: (touch, event) => void,\n    onTouchEnded?: (touch, event) => void,\n    onTouchCancelled?: (touch, event) => void,\n}, nodeOrPriority)\n```\n`onTouchBegan` must return `true` to receive subsequent move/end events. Use `touch.getLocation()` for world position, `touch.getDelta()` for movement.",
        "goal": "For drag and drop:\n```js\ncc.eventManager.addListener({\n    event: cc.EventListener.TOUCH_ONE_BY_ONE,\n    swallowTouches: true,\n    onTouchBegan: (touch) => {\n        const local = sprite.convertTouchToNodeSpace(touch)\n        return cc.rectContainsPoint(cc.rect(0,0,sprite.width,sprite.height), local)\n    },\n    onTouchMoved: (touch) => {\n        const delta = touch.getDelta()\n        sprite.x += delta.x\n        sprite.y += delta.y\n    }\n}, this)\n```",
        "debugging": "If touch events aren't firing, check: (1) `onTouchBegan` must return `true` or you won't get move/end events, (2) the node must be on the scene (added via addChild to a running scene), (3) if another listener has `swallowTouches: true` and higher priority, it may be consuming the events, (4) make sure you're not accidentally removing the listener, (5) verify the node passed to addListener is still alive.",
        "beginner": "Touch handling in Cocos2d-x uses event listeners. You register a listener with `cc.eventManager.addListener()`, providing callback functions for touch began/moved/ended. The key thing: `onTouchBegan` must return `true` or you won't receive the moved and ended events. Use `touch.getLocation()` to get the tap position.",
    },
)

# ============================================================
# EVENTS - KEYBOARD
# ============================================================
topic(
    {
        "casual": [
            "how do I handle keyboard input?",
            "how to detect key presses?",
        ],
        "technical": [
            "How does the keyboard event listener work?",
        ],
        "goal": [
            "I want WASD movement controls",
            "I need arrow key input for my game",
        ],
    },
    {
        "casual": "Add a keyboard listener:\n```js\ncc.eventManager.addListener({\n    event: cc.EventListener.KEYBOARD,\n    onKeyPressed: (keyCode, event) => { /* key down */ },\n    onKeyReleased: (keyCode, event) => { /* key up */ }\n}, this)\n```\nUse `cc.KEY.left`, `cc.KEY.right`, `cc.KEY.space`, `cc.KEY.a`, etc. for key codes.",
        "technical": "```js\ncc.eventManager.addListener({\n    event: cc.EventListener.KEYBOARD,\n    onKeyPressed: (keyCode: cc.KEY, event: cc.Event) => void,\n    onKeyReleased: (keyCode: cc.KEY, event: cc.Event) => void,\n}, nodeOrPriority)\n```\nKey constants: `cc.KEY.left/right/up/down` (37-40), `cc.KEY.a`-`cc.KEY.z` (65-90), `cc.KEY.space` (32), `cc.KEY.enter` (13), `cc.KEY.escape` (27).",
        "goal": "Track pressed keys for movement:\n```js\nconst keys = {}\ncc.eventManager.addListener({\n    event: cc.EventListener.KEYBOARD,\n    onKeyPressed: (k) => { keys[k] = true },\n    onKeyReleased: (k) => { keys[k] = false }\n}, this)\n// In update:\nif (keys[cc.KEY.left]) hero.x -= speed * dt\nif (keys[cc.KEY.right]) hero.x += speed * dt\n```",
    },
)

# ============================================================
# EVENTS - MOUSE
# ============================================================
topic(
    {
        "casual": [
            "how do I handle mouse events?",
            "how to detect mouse clicks and scroll?",
        ],
        "technical": [
            "What is the mouse event listener API?",
        ],
    },
    {
        "casual": "Add a mouse listener:\n```js\ncc.eventManager.addListener({\n    event: cc.EventListener.MOUSE,\n    onMouseDown: (event) => { /* click */ },\n    onMouseMove: (event) => { /* hover */ },\n    onMouseScroll: (event) => { /* scroll wheel */ }\n}, this)\n```\nUse `event.getButton()` to check left (0), right (1), middle (2). `event.getLocation()` for position.",
        "technical": "```js\ncc.eventManager.addListener({\n    event: cc.EventListener.MOUSE,\n    onMouseDown: (event: cc.EventMouse) => void,\n    onMouseUp: (event) => void,\n    onMouseMove: (event) => void,\n    onMouseScroll: (event) => void,\n}, node)\n```\nEventMouse methods: `getButton()`, `getLocation()`, `getDelta()`, `getScrollX/Y()`. Button constants: `cc.EventMouse.BUTTON_LEFT` (0), `BUTTON_RIGHT` (1), `BUTTON_MIDDLE` (2).",
    },
)

# ============================================================
# EVENTS - CUSTOM
# ============================================================
topic(
    {
        "casual": [
            "how do I create custom events?",
            "how to use pub/sub messaging in cocos2d?",
        ],
        "technical": [
            "How does custom event dispatching work in Cocos2d-x JS?",
        ],
        "goal": [
            "I want decoupled communication between game systems",
            "I need to notify multiple listeners when score changes",
        ],
    },
    {
        "casual": "Dispatch: `cc.eventManager.dispatchCustomEvent('score:update', {score: 100})`. Listen: `cc.eventManager.addCustomListener('score:update', (event) => { const data = event.getUserData() })`. Remove: `cc.eventManager.removeCustomListeners('score:update')`.",
        "technical": "```js\n// Dispatch\ncc.eventManager.dispatchCustomEvent(eventName: string, userData?: any): void\n// Listen\ncc.eventManager.addCustomListener(eventName: string, callback: (event) => void): cc.EventListener\n// Remove\ncc.eventManager.removeCustomListeners(eventName: string): void\ncc.eventManager.removeListener(listener): void\n```\nAccess data via `event.getUserData()` in the callback.",
        "goal": "Pub/sub pattern:\n```js\n// In score manager:\ncc.eventManager.dispatchCustomEvent('game:score', {score: this.score})\n// In UI layer:\ncc.eventManager.addCustomListener('game:score', (event) => {\n    const data = event.getUserData()\n    this.scoreLabel.setString('Score: ' + data.score)\n})\n```\nClean up in onExit: `cc.eventManager.removeCustomListeners('game:score')`.",
    },
)

# ============================================================
# EVENTS - REMOVE LISTENERS
# ============================================================
topic(
    {
        "casual": [
            "how do I remove event listeners?",
            "how to clean up listeners properly?",
        ],
        "technical": [
            "What are the methods for removing event listeners?",
        ],
        "debugging": [
            "I'm getting duplicate event callbacks",
            "my removed node still responds to touches",
        ],
    },
    {
        "casual": "Remove a specific listener: `cc.eventManager.removeListener(listener)`. Remove all from a node: `cc.eventManager.removeListeners(node)`. Clean up in your `onExit()` method.",
        "technical": "```js\ncc.eventManager.removeListener(listener): void\ncc.eventManager.removeListeners(nodeOrType, recursive?): void\ncc.eventManager.removeCustomListeners(eventName): void\ncc.eventManager.removeAllListeners(): void\n```\nBest practice: store listener reference in onEnter, remove in onExit.",
        "debugging": "Duplicate callbacks usually mean you're adding listeners multiple times (e.g., in a constructor that runs again). Store the listener ref and remove it in `onExit()`. If a removed node still gets events, you forgot to remove its listeners. Always do:\n```js\nonExit() {\n    cc.eventManager.removeListener(this._listener)\n    super.onExit()\n}\n```",
    },
)

# ============================================================
# DIRECTOR - SCENES
# ============================================================
topic(
    {
        "casual": [
            "how do I switch between scenes?",
            "how to change scenes?",
        ],
        "technical": [
            "What are the scene management methods on cc.director?",
        ],
        "goal": [
            "I want to transition from menu to gameplay",
            "I need to go back to the previous scene",
        ],
        "comparison": [
            "what's the difference between runScene, pushScene, and popScene?",
        ],
        "beginner": [
            "how do scenes work in cocos2d-x?",
        ],
    },
    {
        "casual": "Use `cc.director.runScene(new GameScene())` to switch scenes. For a fade transition: `cc.director.runScene(new cc.TransitionFade(0.5, new GameScene()))`. Use push/pop for overlay scenes like pause menus.",
        "technical": "```js\ncc.director.runScene(scene): void      // replace current scene\ncc.director.pushScene(scene): void     // push onto stack (overlay)\ncc.director.popScene(): void           // pop back to previous\ncc.director.popToRootScene(): void\ncc.director.getRunningScene(): cc.Scene\n```\nWrap scene in a TransitionScene subclass for animated transitions.",
        "goal": "Menu to gameplay:\n```js\ncc.director.runScene(new cc.TransitionFade(0.5, new GameScene()))\n```\nPause menu overlay:\n```js\ncc.director.pushScene(new PauseScene())\n// Resume:\ncc.director.popScene()\n```",
        "comparison": "`runScene` replaces the current scene entirely. `pushScene` pushes a new scene on a stack, keeping the old one in memory - use for pause menus, dialog overlays. `popScene` removes the top scene and returns to the one underneath. Use runScene for full scene changes, push/pop for temporary overlays.",
        "beginner": "A scene is like a screen in your game (menu screen, game screen, game over screen). Only one scene runs at a time. Use `cc.director.runScene(scene)` to switch between them. Each scene has layers and nodes as children. The director manages the lifecycle of scenes.",
    },
)

# ============================================================
# DIRECTOR - WINDOW SIZE
# ============================================================
topic(
    {
        "casual": [
            "how do I get the screen size?",
            "how to center something on screen?",
        ],
        "technical": [
            "What methods return the window/visible size in Cocos2d-x?",
        ],
        "goal": [
            "I need to position things relative to screen center",
        ],
    },
    {
        "casual": "Use `cc.director.getWinSize()` to get the design resolution as a cc.Size. Center something with:\n```js\nconst size = cc.director.getWinSize()\nnode.setPosition(size.width / 2, size.height / 2)\n```",
        "technical": "```js\ncc.director.getWinSize(): cc.Size          // design resolution in points\ncc.director.getWinSizeInPixels(): cc.Size  // actual pixel size\ncc.director.getVisibleSize(): cc.Size      // visible area (may differ with safe area)\ncc.director.getVisibleOrigin(): cc.Point   // visible area origin offset\n```\nUse `getVisibleSize()` + `getVisibleOrigin()` for safe area-aware positioning on notched devices.",
        "goal": "Center positioning:\n```js\nconst s = cc.director.getWinSize()\nconst cx = s.width / 2, cy = s.height / 2\nsprite.setPosition(cx, cy)\n```\nFor notched devices, use visible area:\n```js\nconst vs = cc.director.getVisibleSize()\nconst vo = cc.director.getVisibleOrigin()\nsprite.setPosition(vo.x + vs.width / 2, vo.y + vs.height / 2)\n```",
    },
)

# ============================================================
# DIRECTOR - TIME SCALE
# ============================================================
topic(
    {
        "casual": [
            "how do I do slow motion?",
            "how to speed up or slow down the whole game?",
        ],
        "technical": [
            "How does the scheduler time scale work?",
        ],
        "goal": [
            "I want a slow-motion effect for dramatic moments",
        ],
    },
    {
        "casual": "Set `cc.director.getScheduler().setTimeScale(0.5)` for half-speed (slow motion) or `2.0` for double speed. Reset to `1.0` for normal. This affects all scheduled callbacks and actions globally.",
        "technical": "`cc.director.getScheduler().setTimeScale(scale: number)` affects all scheduled updates and actions. 1.0 = normal, <1 = slow, >1 = fast. For per-action speed, use `cc.speed(action, multiplier)` instead.",
        "goal": "Slow motion effect:\n```js\ncc.director.getScheduler().setTimeScale(0.3)  // 30% speed\n// After dramatic moment:\ncc.director.getScheduler().setTimeScale(1.0)  // back to normal\n```\nFor action-specific speed, wrap with `cc.speed(action, 0.3)`.",
    },
)

# ============================================================
# DIRECTOR - LOADER
# ============================================================
topic(
    {
        "casual": [
            "how do I load resources at runtime?",
            "how to preload assets?",
        ],
        "technical": [
            "What methods does cc.loader provide?",
        ],
        "goal": [
            "I need to load JSON data files",
        ],
    },
    {
        "casual": "Use `cc.loader.load(['res/file.json', 'res/image.png'], callback)` to preload. Access loaded data with `cc.loader.getRes('res/file.json')`. For JSON specifically: `cc.loader.loadJson(url, callback)`.",
        "technical": "```js\ncc.loader.load(resources: string[], cb: Function): void\ncc.loader.loadJson(url, cb: (err, data) => void): void\ncc.loader.loadBinary(url, cb: (err, data) => void): void\ncc.loader.loadTxt(url, cb: (err, data) => void): void\ncc.loader.getRes(url): any\ncc.loader.release(url): void\ncc.loader.releaseAll(): void\n```",
        "goal": "Load JSON data:\n```js\ncc.loader.loadJson('res/level1.json', (err, data) => {\n    if (err) return cc.error('Load failed')\n    this.buildLevel(data)\n})\n```\nOr batch load:\n```js\ncc.loader.load(['res/level.json', 'res/tiles.png'], (err) => {\n    const data = cc.loader.getRes('res/level.json')\n})\n```",
    },
)

# ============================================================
# LAYER
# ============================================================
topic(
    {
        "casual": [
            "what's a layer and when should I use one?",
            "how do I create a colored background?",
        ],
        "technical": [
            "What are the differences between cc.Layer, cc.LayerColor, and cc.LayerGradient?",
        ],
        "goal": [
            "I need a semi-transparent overlay for my pause menu",
        ],
    },
    {
        "casual": "Use `cc.Layer` as a container for grouping nodes. `cc.LayerColor` gives you a solid color background. `cc.LayerGradient` for gradient backgrounds. For a dark overlay: `new cc.LayerColor(cc.color(0, 0, 0, 128))`.",
        "technical": "`cc.Layer` extends cc.Node - basic container with bake() for HTML5 caching. `cc.LayerColor(color?, width?, height?)` adds a solid color fill. `cc.LayerGradient(start, end, vector?)` adds gradient fill with direction vector. Methods:\n- `changeWidth/Height/WidthAndHeight` on LayerColor\n- `setStartColor/EndColor`, `setVector` on LayerGradient",
        "goal": "Semi-transparent pause overlay:\n```js\nconst overlay = new cc.LayerColor(cc.color(0, 0, 0, 128))\noverlay.setContentSize(cc.director.getWinSize())\nthis.addChild(overlay, 10)\n```\nGradient background:\n```js\nconst grad = new cc.LayerGradient(\n    cc.color(30, 100, 200, 255),\n    cc.color(5, 15, 40, 255),\n    cc.p(0, -1)\n)\nscene.addChild(grad, -1)\n```",
    },
)

topic(
    {
        "casual": [
            "how does LayerMultiplex work?",
        ],
        "technical": [
            "What is cc.LayerMultiplex and how do you switch layers?",
        ],
    },
    {
        "casual": "`cc.LayerMultiplex` holds multiple layers but shows only one at a time. Create with `new cc.LayerMultiplex(layer1, layer2)`, switch with `multiplex.switchTo(index)`. Good for tabbed UIs within a scene.",
        "technical": "```js\nnew cc.LayerMultiplex(...layers: cc.Layer[])\nmultiplex.addLayer(layer): void\nmultiplex.switchTo(n: number): void\nmultiplex.switchToAndReleaseMe(n: number): void\n```\nShows only one child layer at a time. `switchToAndReleaseMe` releases the current layer's memory.",
    },
)

# ============================================================
# DRAWNODE
# ============================================================
topic(
    {
        "casual": [
            "how do I draw shapes in cocos2d-x?",
            "how to draw lines and circles?",
        ],
        "technical": [
            "What drawing primitives does cc.DrawNode support?",
        ],
        "goal": [
            "I need to draw debug shapes for collision visualization",
            "I want to draw lines between points",
        ],
    },
    {
        "casual": "Create a `new cc.DrawNode()`, add it to your scene, then use methods like `draw.drawDot()`, `draw.drawSegment()`, `draw.drawCircle()`, `draw.drawRect()`, `draw.drawPoly()`. Call `draw.clear()` to erase.",
        "technical": "```js\nnew cc.DrawNode()\ndraw.drawDot(pos, radius, color): void\ndraw.drawSegment(from, to, lineWidth, color): void\ndraw.drawRect(origin, dest, fillColor?, lineWidth?, lineColor?): void\ndraw.drawCircle(center, radius, angle, segments, drawLineToCenter, lineWidth, color?): void\ndraw.drawPoly(verts, fillColor?, lineWidth?, lineColor?): void\ndraw.drawQuadBezier/drawCubicBezier/drawCatmullRom\ndraw.clear(): void\n```",
        "goal": "Debug collision boxes:\n```js\nconst draw = new cc.DrawNode()\nthis.addChild(draw, 100)\n// In update:\ndraw.clear()\nconst box = sprite.getBoundingBoxToWorld()\ndraw.drawRect(\n    cc.p(box.x, box.y),\n    cc.p(box.x + box.width, box.y + box.height),\n    null, 1, cc.color(255, 0, 0, 255)\n)\n```",
    },
)

# ============================================================
# CCUI - BUTTON
# ============================================================
topic(
    {
        "casual": [
            "how do I create a UI button?",
            "how to make a clickable button?",
        ],
        "technical": [
            "What is the ccui.Button constructor and click handler API?",
        ],
        "goal": [
            "I need a play button in my menu",
        ],
        "code_review": [
            "is this the right way to handle button clicks?",
        ],
    },
    {
        "casual": "Create a button with images and a click handler:\n```js\nconst btn = new ccui.Button('btn_normal.png', 'btn_pressed.png')\nbtn.setTitleText('PLAY')\nbtn.addClickEventListener(() => this.startGame())\nthis.addChild(btn)\n```",
        "technical": "```js\nnew ccui.Button(normal?, selected?, disabled?, texType?)\n// texType: ccui.Widget.LOCAL_TEXTURE or PLIST_TEXTURE\nbtn.loadTextures(normal, selected, disabled, texType?)\nbtn.setTitleText(text)\nbtn.setTitleFontSize(size)\nbtn.setTitleColor(cc.Color)\nbtn.addClickEventListener(callback)\nbtn.addTouchEventListener((sender, type) => { ... })\n// TOUCH_BEGAN, TOUCH_MOVED, TOUCH_ENDED, TOUCH_CANCELED\n```",
        "goal": "Play button:\n```js\nconst btn = new ccui.Button('btn_normal.png', 'btn_pressed.png', '', ccui.Widget.PLIST_TEXTURE)\nbtn.setTitleText('PLAY')\nbtn.setTitleFontSize(24)\nbtn.setTitleColor(cc.color.WHITE)\nbtn.setPosition(centerX, 200)\nbtn.addClickEventListener(() => this.startGame())\nthis.addChild(btn)\n```",
        "code_review": "For button clicks, `addClickEventListener` is the simplest. For more control (down/move/up states), use `addTouchEventListener` and check for `ccui.Widget.TOUCH_ENDED`. Common issue: forgetting `ccui.Widget.PLIST_TEXTURE` when using atlas frames for button images.",
    },
)

# ============================================================
# CCUI - SCROLLVIEW
# ============================================================
topic(
    {
        "casual": [
            "how do I make a scrollable list?",
            "how to create a scroll view?",
        ],
        "technical": [
            "What is the ccui.ScrollView API?",
        ],
        "goal": [
            "I need a scrollable level select screen",
        ],
    },
    {
        "casual": "Create a `ccui.ScrollView`, set its size, inner container size (must be larger), and direction:\n```js\nconst sv = new ccui.ScrollView()\nsv.setSize(cc.size(300, 400))\nsv.setInnerContainerSize(cc.size(300, 1200))\nsv.setDirection(ccui.ScrollView.DIR_VERTICAL)\nsv.setBounceEnabled(true)\n```\nAdd children to `sv.getInnerContainer()`.",
        "technical": "```js\nnew ccui.ScrollView()\nsv.setDirection(DIR_VERTICAL|DIR_HORIZONTAL|DIR_BOTH)\nsv.setInnerContainerSize(size) // must be >= scroll view size\nsv.getInnerContainer(): ccui.Layout\nsv.setBounceEnabled(bool)\nsv.setScrollBarEnabled(bool)\nsv.jumpToTop/Bottom/Left/Right()\nsv.scrollToTop/Bottom(time, attenuated)\nsv.addEventListener(callback)\n```\nDirection constants: `ccui.ScrollView.DIR_VERTICAL`, `DIR_HORIZONTAL`, `DIR_BOTH`, `DIR_NONE`.",
        "goal": "Scrollable level select:\n```js\nconst sv = new ccui.ScrollView()\nsv.setSize(cc.size(300, 400))\nsv.setInnerContainerSize(cc.size(300, 60 * levelCount))\nsv.setDirection(ccui.ScrollView.DIR_VERTICAL)\nsv.setBounceEnabled(true)\nfor (let i = 0; i < levelCount; i++) {\n    const btn = new ccui.Button('level_bg.png')\n    btn.setPosition(150, sv.getInnerContainerSize().height - 30 - i * 60)\n    sv.getInnerContainer().addChild(btn)\n}\nthis.addChild(sv)\n```",
    },
)

# ============================================================
# CCUI - LAYOUT
# ============================================================
topic(
    {
        "casual": [
            "how do I use layouts in ccui?",
            "how to arrange widgets automatically?",
        ],
        "technical": [
            "What layout types does ccui.Layout support?",
        ],
    },
    {
        "casual": "Use `ccui.Layout` with different types: ABSOLUTE (free positioning), LINEAR_HORIZONTAL (row), LINEAR_VERTICAL (column), RELATIVE. Set type with `layout.setLayoutType(ccui.Layout.LINEAR_VERTICAL)`. Add margin with `ccui.LinearLayoutParameter`.",
        "technical": "```js\nnew ccui.Layout()\nlayout.setLayoutType(type)  // ABSOLUTE, LINEAR_HORIZONTAL, LINEAR_VERTICAL, RELATIVE\nlayout.setClippingEnabled(bool)\nlayout.setBackGroundColorType(ccui.Layout.BG_COLOR_SOLID|GRADIENT|NONE)\nlayout.setBackGroundColor(color)\nlayout.forceDoLayout()\n```\nUse `ccui.LinearLayoutParameter` for margins: `param.setGravity(CENTER_VERTICAL)`, `param.setMargin(new ccui.Margin(l,t,r,b))`.",
    },
)

# ============================================================
# CCUI - TEXT & TEXTFIELD
# ============================================================
topic(
    {
        "casual": [
            "how do I create a text widget in ccui?",
        ],
        "technical": [
            "What is ccui.Text vs cc.Label?",
        ],
    },
    {
        "casual": "`ccui.Text` is a widget wrapper for text, useful in ccui layouts:\n```js\nconst text = new ccui.Text('Hello', 'Arial', 24)\ntext.setTextColor(cc.color(255, 255, 255))\nlayout.addChild(text)\n```\nUse `ccui.Text` when you need widget features (touch events, layout parameters). Use `cc.Label` for standalone text.",
        "technical": "`ccui.Text` extends `ccui.Widget` and wraps text rendering. It supports `setString/getString`, `setFontSize/Name`, `setTextColor`, `setTextAreaSize`, and `setTextHorizontalAlignment`. Unlike `cc.Label`, it inherits widget features like touch events, layout parameters, and size types. Prefer `cc.Label` for raw performance, `ccui.Text` for UI layouts.",
    },
)

topic(
    {
        "casual": [
            "how do I create a text input field?",
            "how to make an editable text box?",
        ],
        "technical": [
            "What is the ccui.TextField API?",
        ],
        "goal": [
            "I need a player name input field",
        ],
    },
    {
        "casual": "Use `ccui.TextField`:\n```js\nconst tf = new ccui.TextField('Enter name...', 'Arial', 20)\ntf.setMaxLength(16)\ntf.setMaxLengthEnabled(true)\ntf.setPosition(centerX, centerY)\nthis.addChild(tf)\n```\nGet the value with `tf.getString()`.",
        "technical": "```js\nnew ccui.TextField(placeholder?, fontName?, fontSize?)\ntf.setString/getString()\ntf.setPlaceHolder/getPlaceHolder()\ntf.setPasswordEnabled(bool)\ntf.setMaxLength(n)\ntf.setMaxLengthEnabled(bool)\ntf.addEventListener(callback)\n```",
        "goal": "Player name input:\n```js\nconst tf = new ccui.TextField('Enter name', 'Arial', 20)\ntf.setMaxLengthEnabled(true)\ntf.setMaxLength(16)\ntf.setPosition(centerX, centerY)\ntf.addEventListener((sender, type) => {\n    if (type === ccui.TextField.EVENT_INSERT_TEXT) {\n        // text changed\n    }\n})\nthis.addChild(tf)\n// Submit:\nconst name = tf.getString()\n```",
    },
)

# ============================================================
# CCUI - SLIDER, CHECKBOX, LOADINGBAR
# ============================================================
topic(
    {
        "casual": [
            "how do I create a slider / volume control?",
        ],
        "technical": [
            "What is the ccui.Slider API?",
        ],
        "goal": [
            "I want a volume slider in my settings",
        ],
    },
    {
        "casual": "Create a slider with bar and ball textures:\n```js\nconst slider = new ccui.Slider()\nslider.loadBarTexture('slider_bar.png')\nslider.loadSlidBallTextures('slider_ball.png', 'slider_ball_pressed.png', '')\nslider.loadProgressBarTexture('slider_progress.png')\nslider.setPercent(70)\nslider.addEventListener((sender, type) => {\n    const vol = sender.getPercent() / 100\n    cc.audioEngine.setMusicVolume(vol)\n})\n```",
        "technical": "```js\nnew ccui.Slider()\nslider.loadBarTexture(file, texType?)\nslider.loadSlidBallTextures(normal, pressed, disabled, texType?)\nslider.loadProgressBarTexture(file, texType?)\nslider.getPercent(): number\nslider.setPercent(percent: number): void\nslider.setMaxPercent(percent: number): void\nslider.addEventListener(callback)\n```",
        "goal": "Volume slider:\n```js\nconst slider = new ccui.Slider()\nslider.loadBarTexture('slider_bar.png')\nslider.loadSlidBallTextures('slider_ball.png', 'slider_ball.png', '')\nslider.loadProgressBarTexture('slider_progress.png')\nslider.setPercent(cc.audioEngine.getMusicVolume() * 100)\nslider.addEventListener((sender) => {\n    cc.audioEngine.setMusicVolume(sender.getPercent() / 100)\n})\nthis.addChild(slider)\n```",
    },
)

topic(
    {
        "casual": [
            "how do I create a checkbox?",
            "how to make a toggle switch?",
        ],
        "technical": [
            "What is ccui.CheckBox?",
        ],
    },
    {
        "casual": "Create a checkbox with background and checkmark textures:\n```js\nconst cb = new ccui.CheckBox('cb_bg.png', '', 'cb_check.png', '', '')\ncb.setSelected(true)\ncb.addEventListener((sender, type) => {\n    const isOn = sender.isSelected()\n    cc.audioEngine.setMusicVolume(isOn ? 1.0 : 0.0)\n})\n```",
        "technical": "```js\nnew ccui.CheckBox(backGround?, bgSelected?, cross?, bgDisabled?, crossDisabled?, texType?)\ncb.isSelected(): boolean\ncb.setSelected(bool): void\ncb.addEventListener(callback)\n```\nCallback receives (sender, eventType).",
    },
)

topic(
    {
        "casual": [
            "how do I show a loading/progress bar?",
        ],
        "technical": [
            "What is ccui.LoadingBar?",
        ],
        "goal": [
            "I need a health bar or loading progress indicator",
        ],
    },
    {
        "casual": "Use `ccui.LoadingBar`:\n```js\nconst bar = new ccui.LoadingBar('hp_bar.png', 100)\nbar.setPercent(75) // 75% full\n```\nUpdate with `bar.setPercent(newPercent)`. Direction can be left-to-right or right-to-left.",
        "technical": "```js\nnew ccui.LoadingBar(textureName?, percentage?)\nbar.loadTexture(fileName, texType?)\nbar.getPercent(): number\nbar.setPercent(percent: number): void\nbar.setDirection(dir) // LoadingBar.TYPE_LEFT or TYPE_RIGHT\n```",
        "goal": "Health bar:\n```js\nconst hpBar = new ccui.LoadingBar('hp_bar.png', 100)\nhpBar.setPosition(hero.x, hero.y + 40)\nthis.addChild(hpBar)\n// On damage:\nhpBar.setPercent(hero.hp / hero.maxHp * 100)\n```",
    },
)

# ============================================================
# CCUI - LISTVIEW & PAGEVIEW
# ============================================================
topic(
    {
        "casual": [
            "how do I make a list of items?",
            "how to create a scrollable item list?",
        ],
        "technical": [
            "What is ccui.ListView and how does it differ from ScrollView?",
        ],
        "goal": [
            "I need an inventory or item list UI",
        ],
    },
    {
        "casual": "Use `ccui.ListView` which extends ScrollView with item management:\n```js\nconst lv = new ccui.ListView()\nlv.setSize(cc.size(300, 400))\nlv.setDirection(ccui.ScrollView.DIR_VERTICAL)\nlv.setItemsMargin(10)\n// Add items:\nconst item = new ccui.Button('item_bg.png')\nlv.pushBackCustomItem(item)\n```",
        "technical": "```js\nnew ccui.ListView() // extends ccui.ScrollView\nlv.setItemModel(model)      // template for default items\nlv.pushBackDefaultItem()    // add clone of model\nlv.pushBackCustomItem(widget)\nlv.insertCustomItem(widget, index)\nlv.removeItem(index)\nlv.getItem(index): ccui.Widget\nlv.getItems(): ccui.Widget[]\nlv.setItemsMargin(margin)\nlv.setGravity(gravity)\nlv.addEventListener(callback)\n```",
        "goal": "Inventory list:\n```js\nconst lv = new ccui.ListView()\nlv.setSize(cc.size(300, 400))\nlv.setDirection(ccui.ScrollView.DIR_VERTICAL)\nlv.setItemsMargin(5)\nlv.setBounceEnabled(true)\nfor (const item of inventory) {\n    const row = new ccui.Layout()\n    row.setSize(cc.size(290, 50))\n    const txt = new ccui.Text(item.name, 'Arial', 18)\n    row.addChild(txt)\n    lv.pushBackCustomItem(row)\n}\nthis.addChild(lv)\n```",
    },
)

topic(
    {
        "casual": [
            "how do I create swipeable pages?",
        ],
        "technical": [
            "What is ccui.PageView?",
        ],
    },
    {
        "casual": "Use `ccui.PageView` for swipeable pages:\n```js\nconst pv = new ccui.PageView()\npv.setSize(cc.size(480, 320))\nfor (let i = 0; i < 5; i++) {\n    const page = new ccui.Layout()\n    page.setSize(cc.size(480, 320))\n    pv.addPage(page)\n}\npv.scrollToPage(0)\n```\nHandle page changes with `pv.addEventListener(callback)`.",
        "technical": "```js\nnew ccui.PageView() // extends ccui.Layout\npv.addPage(page: ccui.Layout)\npv.removePage(page)\npv.scrollToPage(idx)\npv.getCurrentPageIndex(): number\npv.addEventListener(callback)\npv.setCustomScrollThreshold(threshold)\npv.setUsingCustomScrollThreshold(flag)\n```",
    },
)

# ============================================================
# CCUI - HELPER
# ============================================================
topic(
    {
        "casual": [
            "how do I find a widget by name in a UI tree?",
        ],
        "technical": [
            "What does ccui.helper.seekWidgetByName do?",
        ],
    },
    {
        "casual": "Use `ccui.helper.seekWidgetByName(rootWidget, 'buttonName')` to recursively find a widget by its name in a UI hierarchy. Also: `ccui.helper.seekWidgetByTag(root, tag)`.",
        "technical": "```js\nccui.helper.seekWidgetByName(root: ccui.Widget, name: string): ccui.Widget\nccui.helper.seekWidgetByTag(root: ccui.Widget, tag: number): ccui.Widget\n```\nSearches the entire widget subtree recursively. Useful for finding widgets loaded from CocosStudio .csb files.",
    },
)

# ============================================================
# CCS - ARMATURE
# ============================================================
topic(
    {
        "casual": [
            "how do I use CocosStudio armature animations?",
            "how to play skeletal animations from CocosStudio?",
        ],
        "technical": [
            "What is the ccs.Armature API?",
        ],
        "goal": [
            "I have a CocosStudio exported animation and need to play it",
        ],
    },
    {
        "casual": "Load the armature data first, then create and play:\n```js\nccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson')\nconst armature = ccs.Armature.create('hero')\narmature.setPosition(240, 160)\nthis.addChild(armature)\narmature.animation.play('run', -1, -1) // name, durationTo, loop\n```",
        "technical": "```js\n// Load data\nccs.armatureDataManager.addArmatureFileInfo(configFilePath)\nccs.armatureDataManager.addArmatureFileInfo(imagePath, plistPath, configFilePath)\n// Create\nccs.Armature.create(name?, parentBone?)\n// Playback via armature.animation:\narmature.animation.play(name, durationTo?, loop?)\narmature.animation.playWithIndex(index, durationTo?, loop?)\narmature.animation.setSpeedScale(scale)\narmature.animation.pause/resume/stop()\n```\nloop: -1=forever, 0=no loop, 1+=count. durationTo: blend frames (-1=none).",
        "goal": "Play your CocosStudio animation:\n```js\nccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson')\nconst arm = ccs.Armature.create('hero')\narm.setPosition(240, 160)\nthis.addChild(arm)\narm.animation.play('idle', -1, -1)\n// Listen for completion:\narm.animation.setMovementEventCallFunc((a, type, id) => {\n    if (type === ccs.MovementEventType.COMPLETE) {\n        arm.animation.play('idle', 5, -1)\n    }\n})\n```",
    },
)

topic(
    {
        "casual": [
            "how do I listen for armature animation events?",
        ],
        "technical": [
            "What animation event callbacks does ccs.ArmatureAnimation support?",
        ],
    },
    {
        "casual": "Use `armature.animation.setMovementEventCallFunc()` for animation state changes and `setFrameEventCallFunc()` for frame events set in CocosStudio editor:\n```js\narm.animation.setMovementEventCallFunc((arm, type, id) => {\n    // type: ccs.MovementEventType.START, COMPLETE, LOOP_COMPLETE\n})\narm.animation.setFrameEventCallFunc((bone, eventName) => {\n    if (eventName === 'footstep') playSound()\n})\n```",
        "technical": "```js\narmature.animation.setMovementEventCallFunc(\n    (armature, movementType: number, movementID: string) => void\n)\n// movementType: ccs.MovementEventType.START, COMPLETE, LOOP_COMPLETE\n\narmature.animation.setFrameEventCallFunc(\n    (bone, frameEventName, originFrameIndex, currentFrameIndex) => void\n)\n```\nFrame events are triggered by keyframes set in the CocosStudio animation editor.",
    },
)

# ============================================================
# SPINE
# ============================================================
topic(
    {
        "casual": [
            "how do I use Spine animations in cocos2d-x?",
            "how to play a spine animation?",
        ],
        "technical": [
            "What is the sp.SkeletonAnimation API?",
        ],
        "goal": [
            "I have Spine exported files and need to play them",
        ],
    },
    {
        "casual": "Create a skeleton from JSON + atlas, then set animations:\n```js\nconst skel = new sp.SkeletonAnimation('res/hero.json', 'res/hero.atlas')\nskel.setPosition(240, 160)\nthis.addChild(skel)\nskel.setAnimation(0, 'run', true) // track 0, loop\n```",
        "technical": "```js\nnew sp.SkeletonAnimation(jsonFile, atlasFile, scale?)\nsp.SkeletonAnimation.createWithJsonFile(json, atlas, scale?)\n\nskel.setAnimation(trackIndex, name, loop): spine.TrackEntry\nskel.addAnimation(trackIndex, name, loop, delay): spine.TrackEntry\nskel.clearTrack(trackIndex)\nskel.clearTracks()\nskel.setMix(fromAnim, toAnim, duration)  // crossfade\nskel.setSkin(skinName)\nskel.setTimeScale(scale)\n```\nTrack 0 is the base animation layer; higher tracks overlay.",
        "goal": "Play Spine animations:\n```js\nconst hero = new sp.SkeletonAnimation('res/hero.json', 'res/hero.atlas')\nhero.setPosition(240, 160)\nthis.addChild(hero)\n// Set up crossfades:\nhero.setMix('walk', 'run', 0.3)\nhero.setMix('run', 'idle', 0.2)\n// Play:\nhero.setAnimation(0, 'idle', true)\n// Queue:\nhero.setAnimation(0, 'attack', false)\nhero.addAnimation(0, 'idle', true, 0)\n```",
    },
)

topic(
    {
        "casual": [
            "how do I listen for spine animation events?",
            "how to know when a spine animation finishes?",
        ],
        "technical": [
            "What event listeners does sp.SkeletonAnimation support?",
        ],
    },
    {
        "casual": "Use `setAnimationListener` to track animation events:\n```js\nhero.setAnimationListener(this, (track, type, event) => {\n    if (type === sp.AnimationEventType.COMPLETE) {\n        cc.log('done:', track.animation.name)\n    }\n    if (type === sp.AnimationEventType.EVENT) {\n        cc.log('event:', event.data.name)\n    }\n})\n```",
        "technical": "```js\nskel.setAnimationListener(target, (trackEntry, type, event) => void)\n// type: sp.AnimationEventType.START, END, COMPLETE, EVENT\nskel.setStartListener(listener)\nskel.setEndListener(listener)\n```\nCOMPLETE fires when an animation finishes one loop. EVENT fires for custom keyframe events. END fires when an animation is interrupted or removed.",
    },
)

topic(
    {
        "casual": [
            "how do I change spine skins or attachments?",
        ],
        "technical": [
            "What methods control spine skins and attachments?",
        ],
        "goal": [
            "I want to swap character equipment/skins in Spine",
        ],
    },
    {
        "casual": "Switch skins: `skel.setSkin('warrior')`. Change individual attachments: `skel.setAttachment('weapon_slot', 'sword')`. Set to null to hide: `skel.setAttachment('weapon_slot', null)`.",
        "technical": "```js\nskel.setSkin(skinName: string): void\nskel.setAttachment(slotName: string, attachmentName: string | null): void\nskel.findSlot(slotName): spine.Slot | null\nskel.findBone(boneName): spine.Bone | null\n```\nSkins must be defined in the Spine editor. Attachments are per-slot.",
        "goal": "Swap equipment:\n```js\n// Full skin switch\nhero.setSkin('warrior')\n// Individual slot changes\nhero.setAttachment('weapon_slot', 'sword')\nhero.setAttachment('helmet_slot', 'iron_helm')\n// Hide slot:\nhero.setAttachment('shield_slot', null)\n```",
    },
)

# ============================================================
# SYS - PLATFORM DETECTION
# ============================================================
topic(
    {
        "casual": [
            "how do I detect what platform the game is running on?",
            "how to check if we're on mobile or desktop?",
        ],
        "technical": [
            "What platform detection properties does cc.sys have?",
        ],
        "goal": [
            "I need platform-specific code for iOS vs Android vs web",
        ],
    },
    {
        "casual": "Use `cc.sys.isNative` (true for iOS/Android app), `cc.sys.isMobile`, `cc.sys.platform` (e.g. `cc.sys.ANDROID`), and `cc.sys.os` (e.g. `cc.sys.OS_IOS`).",
        "technical": "```js\ncc.sys.platform: number    // cc.sys.WIN32, ANDROID, IPHONE, MOBILE_BROWSER, etc.\ncc.sys.isNative: boolean   // true in JSB\ncc.sys.isMobile: boolean\ncc.sys.os: string          // 'iOS', 'Android', 'Windows', etc.\ncc.sys.language: number    // cc.sys.LANGUAGE_ENGLISH, etc.\ncc.sys.capabilities: { opengl, accelerometer, touches, keyboard, mouse }\ncc.sys.browserType: string // H5 only\n```",
        "goal": "Platform branching:\n```js\nif (cc.sys.isNative) {\n    // JSB (iOS/Android native)\n} else {\n    // Web browser\n}\nif (cc.sys.platform === cc.sys.ANDROID) {\n    // Android specific\n}\nif (cc.sys.isMobile) {\n    // Touch-based UI\n} else {\n    // Mouse/keyboard UI\n}\n```",
    },
)

# ============================================================
# SYS - LOCAL STORAGE
# ============================================================
topic(
    {
        "casual": [
            "how do I save data in cocos2d-x?",
            "how to persist player progress?",
        ],
        "technical": [
            "What is the localStorage API in cc.sys?",
        ],
        "goal": [
            "I need to save high scores and settings",
        ],
    },
    {
        "casual": "Use `cc.sys.localStorage`:\n```js\ncc.sys.localStorage.setItem('highscore', '100')\nconst score = cc.sys.localStorage.getItem('highscore')\n```\nValues are strings, so use `JSON.stringify/parse` for objects. Works on both native and web.",
        "technical": "```js\ncc.sys.localStorage.setItem(key: string, value: string): void\ncc.sys.localStorage.getItem(key: string): string | null\ncc.sys.localStorage.removeItem(key: string): void\ncc.sys.localStorage.clear(): void\n```\nValues must be strings. Use JSON serialization for complex data.",
        "goal": "Save/load game data:\n```js\n// Save\nconst data = { highscore: 1000, level: 5, volume: 0.8 }\ncc.sys.localStorage.setItem('save', JSON.stringify(data))\n// Load\nconst raw = cc.sys.localStorage.getItem('save')\nconst save = raw ? JSON.parse(raw) : { highscore: 0, level: 1, volume: 1.0 }\n```",
    },
)

# ============================================================
# TYPES - POINT, SIZE, RECT, COLOR
# ============================================================
topic(
    {
        "casual": [
            "what are the basic types in cocos2d-x JS?",
            "how do I create a point or size?",
        ],
        "technical": [
            "What are cc.Point, cc.Size, cc.Rect, and cc.Color?",
        ],
        "beginner": [
            "explain the basic data types in cocos2d-x",
        ],
    },
    {
        "casual": "Use factory functions: `cc.p(x, y)` for points, `cc.size(w, h)` for sizes, `cc.rect(x, y, w, h)` for rectangles, `cc.color(r, g, b, a?)` for colors. Predefined colors: `cc.color.WHITE`, `cc.color.RED`, etc.",
        "technical": "Core types:\n- `cc.Point {x, y}` - factory: `cc.p(x, y)`\n- `cc.Size {width, height}` - factory: `cc.size(w, h)`\n- `cc.Rect {x, y, width, height}` - factory: `cc.rect(x, y, w, h)`\n- `cc.Color {r, g, b, a}` - factory: `cc.color(r, g, b, a?)`\n\nRect utilities: `cc.rectContainsPoint()`, `cc.rectOverlapsRect()`, `cc.rectUnion()`, `cc.rectIntersection()`.",
        "beginner": "Cocos2d-x uses four main value types: **Point** for positions (`cc.p(100, 200)`), **Size** for dimensions (`cc.size(480, 320)`), **Rect** for rectangles (`cc.rect(0, 0, 100, 50)`), and **Color** for RGBA colors (`cc.color(255, 0, 0)` for red). These are simple objects with named properties.",
    },
)

topic(
    {
        "casual": [
            "what math utilities are available for points?",
        ],
        "technical": [
            "What are the cc.p math functions?",
        ],
    },
    {
        "casual": "Point math helpers: `cc.pAdd(a, b)`, `cc.pSub(a, b)`, `cc.pMult(p, scalar)`, `cc.pNormalize(v)`, `cc.pLength(v)`, `cc.pDistance(a, b)`, `cc.pLerp(a, b, t)`, `cc.pDot(a, b)`. Also `cc.degreesToRadians()` and `cc.radiansToDegrees()`.",
        "technical": "```js\ncc.pAdd(v1, v2): cc.Point\ncc.pSub(v1, v2): cc.Point\ncc.pMult(point, scalar): cc.Point\ncc.pNormalize(v): cc.Point\ncc.pLength(v): number\ncc.pDistance(v1, v2): number\ncc.pLerp(a, b, alpha): cc.Point\ncc.pDot(v1, v2): number\ncc.pAngle(a, b): number\ncc.pRotateByAngle(v, pivot, angle): cc.Point\ncc.clampf(value, min, max): number\n```",
    },
)

# ============================================================
# SHADERS
# ============================================================
topic(
    {
        "casual": [
            "can I use custom shaders in cocos2d-x JS?",
            "how do I apply a shader to a sprite?",
        ],
        "technical": [
            "How does cc.GLProgram work?",
        ],
    },
    {
        "casual": "Yes! Create a `cc.GLProgram`, init with vertex/fragment shader strings, then apply to a node:\n```js\nconst program = new cc.GLProgram()\nprogram.initWithString(vertSrc, fragSrc)\nprogram.addAttribute('a_position', 0)\nprogram.link()\nprogram.updateUniforms()\nsprite.setShaderProgram(program)\n```",
        "technical": "```js\nconst program = new cc.GLProgram()\nprogram.initWithString(vertShader: string, fragShader: string)\nprogram.addAttribute(name, index)\nprogram.link()\nprogram.use()\nprogram.updateUniforms()\nprogram.getUniformLocationForName(name)\nprogram.setUniformLocationWith1f/2f/4f(loc, ...values)\n```\nSimpler interface via GLProgramState:\n```js\nconst state = node.getGLProgramState()\nstate.setUniformFloat('u_time', time)\nstate.setUniformVec2('u_resolution', cc.p(w, h))\n```",
    },
)

# ============================================================
# BLEND FUNC
# ============================================================
topic(
    {
        "casual": [
            "how do I change blend mode on a sprite?",
            "how to do additive blending for particle effects?",
        ],
        "technical": [
            "What blend function constants are available?",
        ],
    },
    {
        "casual": "Set blend with `sprite.setBlendFunc(new cc.BlendFunc(src, dst))`. For additive glow: `new cc.BlendFunc(cc.ONE, cc.ONE)`. Normal alpha: `new cc.BlendFunc(cc.SRC_ALPHA, cc.ONE_MINUS_SRC_ALPHA)`.",
        "technical": "```js\nsprite.setBlendFunc(new cc.BlendFunc(src, dst))\n```\nConstants: `cc.ONE`, `cc.ZERO`, `cc.SRC_ALPHA`, `cc.ONE_MINUS_SRC_ALPHA`, `cc.DST_ALPHA`, `cc.ONE_MINUS_DST_ALPHA`, `cc.SRC_COLOR`, `cc.ONE_MINUS_SRC_COLOR`.\n\nCommon presets: Normal alpha = `(SRC_ALPHA, ONE_MINUS_SRC_ALPHA)`, Additive = `(ONE, ONE)`, Premultiplied = `(ONE, ONE_MINUS_SRC_ALPHA)`.",
    },
)

# ============================================================
# TEXTURE CACHE
# ============================================================
topic(
    {
        "casual": [
            "how does texture caching work?",
            "how to manage memory for textures?",
        ],
        "technical": [
            "What methods does cc.textureCache provide?",
        ],
        "goal": [
            "my game uses too much memory from textures",
        ],
    },
    {
        "casual": "Textures are cached automatically in `cc.textureCache`. To free memory, use `cc.textureCache.removeUnusedTextures()` or `removeTextureForKey(path)`. Preload with `cc.textureCache.addImage(path)`.",
        "technical": "```js\ncc.textureCache.addImage(path): void\ncc.textureCache.getTextureForKey(key): cc.Texture2D\ncc.textureCache.removeTextureForKey(key): void\ncc.textureCache.removeUnusedTextures(): void\ncc.textureCache.removeAllTextures(): void\n```",
        "goal": "Free texture memory between scenes:\n```js\n// In scene cleanup:\ncc.spriteFrameCache.removeUnusedSpriteFrames()\ncc.textureCache.removeUnusedTextures()\n// Or purge everything:\ncc.director.purgeCachedData()\n```",
    },
)

# ============================================================
# GRID ACTIONS
# ============================================================
topic(
    {
        "casual": [
            "what are grid/3D actions?",
            "how to do screen effects like ripple or page turn?",
        ],
        "technical": [
            "What grid effect actions are available?",
        ],
    },
    {
        "casual": "Grid actions create visual effects on the entire node: `cc.ripple3D`, `cc.waves`, `cc.liquid`, `cc.twirl`, `cc.pageTurn3D`, etc. They distort the node's rendering using a grid. Example: `node.runAction(cc.waves(5, cc.size(15, 10), 5, 20, true, true))`.",
        "technical": "Grid/3D effect actions:\n```js\ncc.flipX3D(duration)\ncc.flipY3D(duration)\ncc.shaky3D(duration, gridSize, range, shakeZ)\ncc.liquid(duration, gridSize, waves, amplitude)\ncc.waves(duration, gridSize, waves, amplitude, horizontal, vertical)\ncc.waves3D(duration, gridSize, waves, amplitude)\ncc.ripple3D(duration, gridSize, position, radius, waves, amplitude)\ncc.twirl(duration, gridSize, position, twirls, amplitude)\ncc.lens3D(duration, gridSize, position, radius)\ncc.pageTurn3D(duration, gridSize)\ncc.stopGrid()  // cleanup grid after effect\n```",
    },
)

# ============================================================
# SCENE TRANSITIONS
# ============================================================
topic(
    {
        "casual": [
            "how do I add a transition effect between scenes?",
            "what scene transitions are available?",
        ],
        "technical": [
            "How do transition scenes work in Cocos2d-x JS?",
        ],
        "goal": [
            "I want a fade transition between my menu and game",
        ],
    },
    {
        "casual": "Wrap your scene in a transition class: `cc.director.runScene(new cc.TransitionFade(0.5, new GameScene()))`. TransitionFade is the most common, but there are many others available.",
        "technical": "`cc.TransitionScene` extends `cc.Scene`, constructor: `(duration, scene)`. Subclasses include `cc.TransitionFade` and others. Usage:\n```js\ncc.director.runScene(new cc.TransitionFade(duration, targetScene))\n```\nDuration is in seconds.",
        "goal": "Fade transition from menu to game:\n```js\nconst gameScene = new GameScene()\ncc.director.runScene(new cc.TransitionFade(0.5, gameScene))\n```\nThe fade takes 0.5 seconds to complete.",
    },
)

# ============================================================
# ACTIONMANAGER
# ============================================================
topic(
    {
        "casual": [
            "how do I pause all actions in the game?",
            "how to resume paused actions?",
        ],
        "technical": [
            "What methods does cc.ActionManager provide?",
        ],
        "goal": [
            "I need to pause all gameplay when showing a pause menu",
        ],
    },
    {
        "casual": "Use `cc.director.getActionManager()` to pause/resume all actions:\n```js\nconst targets = cc.director.getActionManager().pauseAllRunningActions()\n// Later:\ncc.director.getActionManager().resumeTargets(targets)\n```",
        "technical": "```js\nconst mgr = cc.director.getActionManager()\nmgr.pauseAllRunningActions(): cc.Node[]  // returns paused targets\nmgr.pauseTarget(target)\nmgr.resumeTarget(target)\nmgr.resumeTargets(targets)\nmgr.removeAllActionsFromTarget(target, forceDelete)\nmgr.removeAction(action)\nmgr.removeActionByTag(tag, target)\nmgr.getActionByTag(tag, target)\n```",
        "goal": "Pause/resume gameplay:\n```js\n// Pause\nthis._pausedTargets = cc.director.getActionManager().pauseAllRunningActions()\ncc.director.getScheduler().setTimeScale(0)\n// Resume\ncc.director.getActionManager().resumeTargets(this._pausedTargets)\ncc.director.getScheduler().setTimeScale(1.0)\n```",
    },
)

# ============================================================
# CCS TIMELINE
# ============================================================
topic(
    {
        "casual": [
            "how do I play CocosStudio timeline animations?",
        ],
        "technical": [
            "What is ccs.ActionTimeline?",
        ],
    },
    {
        "casual": "Load a .csb file's timeline and run it:\n```js\nconst timeline = ccs.actionManager.loadAnimationActionWithFile('res/ui/dialog.csb')\nnode.runAction(timeline)\ntimeline.gotoFrameAndPlay(0, true) // from frame 0, loop\n```\nControl with `gotoFrameAndPause`, `setTimeSpeed`, `getCurrentFrame`.",
        "technical": "```js\nccs.actionManager.loadAnimationActionWithFile(file): ccs.ActionTimeline\nccs.actionManager.getAnimationActionWithName(file): ccs.ActionTimeline\ntimeline.gotoFrameAndPlay(frame, loop): void\ntimeline.gotoFrameAndPause(frame): void\ntimeline.setCurrentFrame(frame)\ntimeline.getCurrentFrame(): number\ntimeline.setTimeSpeed(speed)\ntimeline.getTimeSpeed(): number\n```",
    },
)

# ============================================================
# SCALE9SPRITE
# ============================================================
topic(
    {
        "casual": [
            "what's a 9-slice sprite and when do I use it?",
            "how do I make a resizable UI background?",
        ],
        "technical": [
            "How does ccui.Scale9Sprite work?",
        ],
    },
    {
        "casual": "A 9-slice (Scale9) sprite can be resized without stretching corners. Great for buttons and panels. Set cap insets to define the non-stretchy border:\n```js\nconst s9 = new ccui.Scale9Sprite('panel_bg.png', cc.rect(10, 10, 80, 80))\ns9.setContentSize(cc.size(300, 200)) // scales cleanly\n```",
        "technical": "```js\nnew ccui.Scale9Sprite(spriteFrame, capInsets?: cc.Rect)\ns9.setCapInsets(cc.Rect)\ns9.setInsetLeft/Right/Top/Bottom(inset: number)\ns9.setScale9Enabled(bool)\n```\nCap insets define the inner non-stretched area. On `ccui.Button`, enable with `btn.setScale9Enabled(true)` and `btn.setCapInsets(rect)`.",
    },
)

# ============================================================
# IMAGEVIEW
# ============================================================
topic(
    {
        "casual": [
            "what's ccui.ImageView for?",
        ],
        "technical": [
            "How does ccui.ImageView differ from cc.Sprite?",
        ],
    },
    {
        "casual": "`ccui.ImageView` displays an image as a widget - useful in ccui layouts. Unlike cc.Sprite, it supports Scale9 and layout parameters:\n```js\nconst img = new ccui.ImageView('avatar.png')\nimg.setScale9Enabled(true)\nimg.setCapInsets(cc.rect(5, 5, 90, 90))\nlayout.addChild(img)\n```",
        "technical": "```js\nnew ccui.ImageView(imageFileName?, texType?)\nview.loadTexture(fileName, texType?)\nview.setTextureRect(rect)\nview.setScale9Enabled(bool)\nview.setCapInsets(cc.Rect)\n```\nExtends ccui.Widget so it gets touch events, layout params, and size types. Use for UI images; use cc.Sprite for game objects.",
    },
)

# ============================================================
# COMMON PATTERNS / DEBUGGING / CODE REVIEW
# ============================================================
topic(
    {
        "debugging": [
            "my node isn't visible, what could be wrong?",
            "I added a child but can't see it on screen",
        ],
    },
    {
        "debugging": "Check these common causes for invisible nodes: (1) position is offscreen - verify x,y are within `cc.director.getWinSize()`, (2) opacity is 0 - check `node.getOpacity()`, (3) visible is false - check `node.isVisible()`, (4) z-order is behind an opaque layer - check local z-order, (5) parent is not on the scene graph - ensure the full chain up to the scene is connected, (6) content size is zero for non-Sprite nodes, (7) anchor point places the visual content offscreen.",
    },
)

topic(
    {
        "debugging": [
            "my game is running slow, how to debug performance?",
            "fps drops in my cocos2d-x game",
        ],
    },
    {
        "debugging": "Performance debugging: (1) Enable stats: `cc.director.setDisplayStats(true)` to see FPS and draw calls, (2) Reduce draw calls by using `cc.SpriteBatchNode` or sprite atlases, (3) Remove offscreen nodes or use culling, (4) Free unused textures: `cc.textureCache.removeUnusedTextures()`, (5) Avoid creating objects in update() - pool and reuse, (6) Profile scheduling: check if too many `schedule()` callbacks are active, (7) Use smaller textures / compressed formats.",
    },
)

topic(
    {
        "debugging": [
            "actions aren't working on my node",
            "runAction doesn't seem to do anything",
        ],
    },
    {
        "debugging": "If actions don't work: (1) Make sure the node is added to the scene graph (it must be a child of a running scene), (2) Check if `node.pause()` or `pauseSchedulerAndActions()` was called, (3) Verify the node isn't being removed before the action completes, (4) For movement actions, check if position is being overridden in `update()`, (5) Ensure you're not calling `stopAllActions()` elsewhere, (6) Try `node.getNumberOfRunningActions()` to see if any are active.",
    },
)

topic(
    {
        "code_review": [
            "is my scene setup correct? I'm extending cc.Layer",
            "is this the standard way to structure a scene?",
        ],
    },
    {
        "code_review": "Standard scene structure:\n```js\nclass GameLayer extends cc.Layer {\n    constructor() { super(); this.init() }\n    init() {\n        // create sprites, labels, etc.\n        this.scheduleUpdate()\n        return true\n    }\n    onEnter() {\n        super.onEnter()\n        // set up event listeners\n    }\n    onExit() {\n        // remove event listeners\n        super.onExit()\n    }\n    update(dt) { /* game logic */ }\n}\nconst scene = new cc.Scene()\nscene.addChild(new GameLayer())\ncc.director.runScene(scene)\n```\nAlways call `super.onEnter/onExit()`. Clean up listeners in onExit.",
    },
)

topic(
    {
        "code_review": [
            "any issues with this event listener code?",
            "what are common mistakes with event listeners?",
        ],
    },
    {
        "code_review": "Common event listener mistakes: (1) Not returning `true` from `onTouchBegan` - you won't get moved/ended events, (2) Not removing listeners in `onExit()` causing leaks or double-firing, (3) Using the same listener object on multiple nodes - create new listeners for each, (4) Forgetting `swallowTouches: true` and wondering why underlying nodes also receive the touch, (5) Adding listeners in constructor instead of `onEnter()` when the node isn't on the scene yet.",
    },
)

topic(
    {
        "comparison": [
            "cc.Label vs ccui.Text - which should I use?",
            "when to use ccui widgets vs plain cc nodes?",
        ],
    },
    {
        "comparison": "Use `cc.Label` for game-world text (HUD, floating damage numbers, dialogue) - it's lighter. Use `ccui.Text` inside ccui layouts/widgets where you need widget features (touch events, layout parameters, percentage sizing). General rule: use ccui widgets for menus and UI screens, use cc.Node/cc.Sprite/cc.Label for in-game objects.",
    },
)

topic(
    {
        "comparison": [
            "moveTo vs setPosition - when to use which?",
        ],
    },
    {
        "comparison": "`setPosition(x, y)` teleports instantly. `cc.moveTo(duration, x, y)` animates smoothly over time. Use setPosition for initial placement or when you manually update position in `update()`. Use moveTo/moveBy for animated transitions, cutscenes, or UI animations.",
    },
)

topic(
    {
        "comparison": [
            "scheduleUpdate vs schedule - what's the difference?",
        ],
    },
    {
        "comparison": "`scheduleUpdate()` calls your `update(dt)` method every frame (typically 60fps). `schedule(callback, interval)` calls a callback at a specific interval (e.g., every 2 seconds). Use scheduleUpdate for continuous game logic (movement, physics). Use schedule for periodic events (spawning enemies, checking conditions).",
    },
)

topic(
    {
        "comparison": [
            "pushScene vs runScene - when to use push?",
        ],
    },
    {
        "comparison": "`runScene` replaces the current scene completely - the old scene is released. `pushScene` stacks the new scene on top - the old scene stays in memory. Use pushScene for temporary overlays (pause menu, dialog) that you'll popScene back from. Use runScene for permanent scene changes (menu -> gameplay -> game over).",
    },
)

topic(
    {
        "goal": [
            "how do I structure a full game scene with layer, sprites, and input?",
        ],
        "beginner": [
            "can you show me a complete basic game setup?",
        ],
    },
    {
        "goal": "Complete scene structure:\n```js\nclass GameLayer extends cc.Layer {\n    onEnter() {\n        super.onEnter()\n        const size = cc.director.getWinSize()\n        // Background\n        const bg = new cc.Sprite('res/bg.png')\n        bg.setPosition(size.width/2, size.height/2)\n        this.addChild(bg, -1)\n        // Hero\n        this.hero = new cc.Sprite('res/hero.png')\n        this.hero.setPosition(100, 200)\n        this.addChild(this.hero, 1)\n        // Input\n        this._listener = cc.eventManager.addListener({\n            event: cc.EventListener.TOUCH_ONE_BY_ONE,\n            onTouchBegan: (touch) => { return true },\n            onTouchMoved: (touch) => {\n                const d = touch.getDelta()\n                this.hero.x += d.x\n                this.hero.y += d.y\n            }\n        }, this)\n        this.scheduleUpdate()\n    }\n    update(dt) { /* game logic */ }\n    onExit() {\n        cc.eventManager.removeListener(this._listener)\n        super.onExit()\n    }\n}\ncc.director.runScene(new cc.Scene().addChild(new GameLayer()))\n```",
        "beginner": "A basic Cocos2d-x game has this structure: a Scene contains Layers, Layers contain Sprites/Labels/etc. The Layer handles input and game logic. Here's the pattern:\n1. Create a class extending cc.Layer\n2. In `onEnter()`, create your sprites and add them as children\n3. Set up event listeners for input\n4. Call `scheduleUpdate()` and implement `update(dt)` for game logic\n5. Clean up listeners in `onExit()`\n6. Create a scene, add your layer, and run it with `cc.director.runScene()`",
    },
)

# ============================================================
# Additional variety topics for reaching 3000
# ============================================================

topic(
    {
        "casual": [
            "how do I use delayTime in a sequence?",
            "how to add a pause between actions?",
        ],
    },
    {
        "casual": "Use `cc.delayTime(seconds)` as an action in a sequence:\n```js\nnode.runAction(cc.sequence(\n    cc.moveTo(0.5, cc.p(200, 200)),\n    cc.delayTime(1.0),  // wait 1 second\n    cc.moveTo(0.5, cc.p(400, 200))\n))\n```",
    },
)

topic(
    {
        "casual": [
            "how do I reverse an action?",
        ],
        "technical": [
            "What is action.reverse() and cc.reverseTime?",
        ],
    },
    {
        "casual": "Call `.reverse()` on most interval actions to get the opposite: `cc.moveBy(1, cc.p(100, 0)).reverse()` moves back. Or use `cc.reverseTime(action)`. Useful for ping-pong animations.",
        "technical": "`action.reverse()` returns a new action that undoes the original. `cc.reverseTime(action)` plays an action backwards in time. Not all actions support reverse (moveTo doesn't, moveBy does). Use in sequences for back-and-forth patterns.",
    },
)

topic(
    {
        "casual": [
            "how do I use targeted actions?",
        ],
        "technical": [
            "What is cc.targetedAction?",
        ],
    },
    {
        "casual": "Use `cc.targetedAction(targetNode, action)` to run an action on a different node than the one calling runAction. Useful in sequences where you want one node's sequence to control another node.",
        "technical": "`cc.targetedAction(target: cc.Node, action: cc.FiniteTimeAction): TargetedAction` - runs the given action on the specified target node, regardless of which node runs the targeted action. Useful for coordinating multi-node animation sequences.",
    },
)

topic(
    {
        "casual": [
            "what's cc.winSize?",
        ],
    },
    {
        "casual": "`cc.winSize` is a shortcut for `cc.director.getWinSize()`. It gives you a `cc.Size` with the design resolution width and height. Common usage: `cc.winSize.width / 2` for horizontal center.",
    },
)

topic(
    {
        "casual": [
            "how do I use cc.log for debugging?",
        ],
        "technical": [
            "What logging functions does Cocos2d-x JS provide?",
        ],
    },
    {
        "casual": "Use `cc.log('message', value)` for info, `cc.warn(...)` for warnings, `cc.error(...)` for errors. They work like console.log but are cross-platform (work in JSB/native too).",
        "technical": "```js\ncc.log(...args: any[]): void     // info level\ncc.warn(...args: any[]): void    // warning level\ncc.error(...args: any[]): void   // error level\ncc.assert(...args: any[]): void  // assertion\ncc.formatStr(...args): string    // format string helper\n```",
    },
)

topic(
    {
        "casual": [
            "how do I open a URL from the game?",
        ],
    },
    {
        "casual": "Call `cc.sys.openURL('https://example.com')` to open a URL in the system browser. Works on both native (iOS/Android) and web platforms.",
    },
)

topic(
    {
        "casual": [
            "how do I set the FPS / frame rate?",
        ],
        "technical": [
            "How do I control the frame rate in Cocos2d-x?",
        ],
    },
    {
        "casual": "Set with `cc.director.setAnimationInterval(1/60)` for 60 FPS or `1/30` for 30 FPS. Check current: `cc.director.getAnimationInterval()`. Show FPS counter: `cc.director.setDisplayStats(true)`.",
        "technical": "`cc.director.setAnimationInterval(value: number)` where value is seconds per frame (e.g., 1/60 for 60 FPS). `cc.director.setDisplayStats(true)` shows an on-screen FPS counter. `cc.director.getDeltaTime()` returns seconds since last frame.",
    },
)

topic(
    {
        "casual": [
            "how do I pause and resume the game?",
        ],
        "goal": [
            "I need a full pause/resume system for my game",
        ],
    },
    {
        "casual": "Use `cc.director.pause()` and `cc.director.resume()` for a simple global pause. Check with `cc.director.isPaused()`. This pauses all scheduled updates and actions.",
        "goal": "Full pause system:\n```js\npauseGame() {\n    cc.director.pause()\n    // Or more granular:\n    this._pausedTargets = cc.director.getActionManager().pauseAllRunningActions()\n    cc.director.getScheduler().setTimeScale(0)\n    // Show pause UI\n    this.pauseOverlay.setVisible(true)\n}\nresumeGame() {\n    cc.director.resume()\n    // Or:\n    cc.director.getActionManager().resumeTargets(this._pausedTargets)\n    cc.director.getScheduler().setTimeScale(1.0)\n    this.pauseOverlay.setVisible(false)\n}\n```",
    },
)

topic(
    {
        "casual": [
            "how do I convert hex color to cc.Color?",
        ],
    },
    {
        "casual": "Use `cc.hexToColor('#FF0000')` to convert a hex string to cc.Color. Reverse: `cc.colorToHex(cc.color(255, 0, 0))` returns the hex string.",
    },
)

topic(
    {
        "casual": [
            "what's purgeCachedData do?",
        ],
        "technical": [
            "How does cc.director.purgeCachedData work?",
        ],
    },
    {
        "casual": "`cc.director.purgeCachedData()` clears the texture cache, sprite frame cache, and animation cache all at once. Use between scenes to free memory when you know old assets aren't needed.",
        "technical": "`cc.director.purgeCachedData()` purges `cc.textureCache`, `cc.spriteFrameCache`, and the animation cache. Call during scene transitions when you know the previous scene's assets aren't needed. For selective cleanup, use the individual caches' remove methods instead.",
    },
)

topic(
    {
        "casual": [
            "how do I get the delta time between frames?",
        ],
    },
    {
        "casual": "In your `update(dt)` callback, `dt` is already the delta time in seconds. You can also call `cc.director.getDeltaTime()` anywhere. Use it to make movement frame-rate independent: `node.x += speed * dt`.",
    },
)

topic(
    {
        "casual": [
            "how do I create a progress timer action?",
        ],
        "technical": [
            "What are cc.progressTo and cc.progressFromTo?",
        ],
    },
    {
        "casual": "`cc.progressTo(duration, percent)` animates a ProgressTimer node from current to target percent. `cc.progressFromTo(duration, from, to)` specifies both start and end. Use with `cc.ProgressTimer` nodes for cooldowns, loading circles, etc.",
        "technical": "```js\ncc.progressTo(duration: number, percent: number): ProgressTo\ncc.progressFromTo(duration: number, from: number, to: number): ProgressFromTo\n```\nDesigned for cc.ProgressTimer nodes. Percent ranges 0-100.",
    },
)

topic(
    {
        "casual": [
            "what is actionTween for?",
        ],
        "technical": [
            "How does cc.actionTween work?",
        ],
    },
    {
        "casual": "`cc.actionTween(duration, key, from, to)` animates any numeric property by string key. The target node must implement `updateTweenAction(value, key)`. Useful for custom properties that don't have built-in actions.",
        "technical": "```js\ncc.actionTween(duration: number, key: string, from: number, to: number): ActionTween\n```\nThe target node must implement `updateTweenAction(value: number, key: string)` or have the property accessible by key. This enables animating custom numeric properties without creating custom action classes.",
    },
)

topic(
    {
        "casual": [
            "how do I convert GL and UI coordinates?",
        ],
    },
    {
        "casual": "Use `cc.director.convertToGL(uiPoint)` to convert from UI coordinates (origin top-left) to GL coordinates (origin bottom-left). Reverse: `cc.director.convertToUI(glPoint)`. This matters when dealing with raw platform input coordinates.",
    },
)

topic(
    {
        "casual": [
            "how do I check capabilities like touch or keyboard support?",
        ],
    },
    {
        "casual": "Check `cc.sys.capabilities` which has boolean properties: `touches`, `keyboard`, `mouse`, `accelerometer`, `opengl`. Example:\n```js\nif (cc.sys.capabilities.touches) {\n    // set up touch listeners\n}\nif (cc.sys.capabilities.keyboard) {\n    // set up keyboard listeners\n}\n```",
    },
)

topic(
    {
        "casual": [
            "what is cascadeOpacity and cascadeColor?",
        ],
    },
    {
        "casual": "When `node.setCascadeOpacityEnabled(true)`, changing the parent's opacity also affects all children. Same with `setCascadeColorEnabled(true)` for color. Useful for fading out an entire UI panel by just fading the parent.",
    },
)

topic(
    {
        "casual": [
            "how do I handle the Android back button?",
        ],
        "goal": [
            "I need to handle back button on Android devices",
        ],
    },
    {
        "casual": "Listen for `cc.KEY.back` in a keyboard listener:\n```js\ncc.eventManager.addListener({\n    event: cc.EventListener.KEYBOARD,\n    onKeyPressed: (keyCode) => {\n        if (keyCode === cc.KEY.back) {\n            cc.director.popScene() // or show exit dialog\n        }\n    }\n}, this)\n```",
        "goal": "Handle Android back button:\n```js\ncc.eventManager.addListener({\n    event: cc.EventListener.KEYBOARD,\n    onKeyPressed: (keyCode) => {\n        if (keyCode === cc.KEY.back) {\n            if (this.canGoBack()) {\n                cc.director.popScene()\n            } else {\n                // Show 'press again to exit' or exit dialog\n                cc.director.end()\n            }\n        }\n    }\n}, this)\n```",
    },
)

topic(
    {
        "casual": [
            "what is node.enumerateChildren for?",
        ],
    },
    {
        "casual": "`node.enumerateChildren(pattern, callback)` searches descendants matching a name pattern. The callback receives each matching node and returns true to stop searching. Useful for finding nodes in complex hierarchies loaded from editors.",
    },
)

topic(
    {
        "casual": [
            "how does multi-touch work in cocos2d-x?",
        ],
        "technical": [
            "How do I handle multi-touch with TOUCH_ALL_AT_ONCE?",
        ],
    },
    {
        "casual": "Use `TOUCH_ALL_AT_ONCE` listener type which gives you arrays of touches:\n```js\ncc.eventManager.addListener({\n    event: cc.EventListener.TOUCH_ALL_AT_ONCE,\n    onTouchesBegan: (touches, event) => {\n        touches.forEach(t => cc.log(t.getID(), t.getLocation()))\n    },\n    onTouchesMoved: (touches, event) => { ... }\n}, this)\n```\nEach touch has a unique ID from `touch.getID()`.",
        "technical": "```js\ncc.eventManager.addListener({\n    event: cc.EventListener.TOUCH_ALL_AT_ONCE,\n    onTouchesBegan: (touches: cc.Touch[], event) => void,\n    onTouchesMoved: (touches: cc.Touch[], event) => void,\n    onTouchesEnded: (touches: cc.Touch[], event) => void,\n    onTouchesCancelled: (touches: cc.Touch[], event) => void,\n}, node)\n```\nEach `cc.Touch` has `getID()` for tracking individual fingers. `cc.EventTouch.MAX_TOUCHES` gives the maximum supported.",
    },
)

topic(
    {
        "goal": [
            "how do I make a sprite draggable?",
        ],
    },
    {
        "goal": "Make a sprite draggable:\n```js\ncc.eventManager.addListener({\n    event: cc.EventListener.TOUCH_ONE_BY_ONE,\n    swallowTouches: true,\n    onTouchBegan: (touch) => {\n        const local = sprite.convertTouchToNodeSpace(touch)\n        return cc.rectContainsPoint(cc.rect(0, 0, sprite.width, sprite.height), local)\n    },\n    onTouchMoved: (touch) => {\n        const delta = touch.getDelta()\n        sprite.x += delta.x\n        sprite.y += delta.y\n    }\n}, sprite)\n```\nReturn true in onTouchBegan only if the touch is inside the sprite.",
    },
)

topic(
    {
        "casual": [
            "what's the difference between tag and name on a node?",
        ],
    },
    {
        "casual": "Both identify nodes. `tag` is a number, `name` is a string. Use `node.setTag(1)` / `parent.getChildByTag(1)` or `node.setName('hero')` / `parent.getChildByName('hero')`. Names are more readable; tags are traditional. You can use either or both.",
    },
)

topic(
    {
        "casual": [
            "how do I make a node ignore its anchor point for positioning?",
        ],
    },
    {
        "casual": "Call `node.ignoreAnchorPointForPosition(true)`. This makes setPosition place the node's bottom-left corner at the given position, regardless of anchor point. Layers and Scenes use this by default.",
    },
)

topic(
    {
        "casual": [
            "how do I use normalized position?",
        ],
    },
    {
        "casual": "`node.setNormalizedPosition(cc.p(0.5, 0.5))` places the node at the center of its parent using 0-1 coordinates. 0 = left/bottom, 1 = right/top. Useful for resolution-independent layouts without knowing the exact pixel size.",
    },
)

topic(
    {
        "debugging": [
            "my sprite frame cache returns null",
            "getSpriteFrame returns null / undefined",
        ],
    },
    {
        "debugging": "If `cc.spriteFrameCache.getSpriteFrame()` returns null: (1) Make sure you called `addSpriteFrames(plistPath, texturePath)` first, (2) The frame name must match exactly what's in the .plist file - usually the filename without path like `'hero_01.png'`, not a full path, (3) Check for typos in the frame name, (4) Verify the plist and texture files exist and loaded without errors.",
    },
)

topic(
    {
        "debugging": [
            "my scroll view content is wrong size or not scrolling",
        ],
    },
    {
        "debugging": "If your ccui.ScrollView isn't scrolling: (1) Inner container size must be LARGER than the scroll view size in the scroll direction, (2) Set direction with `setDirection(ccui.ScrollView.DIR_VERTICAL)`, (3) Add children to `sv.getInnerContainer()`, not the scroll view directly, (4) Position children relative to the inner container's coordinate system (0,0 is bottom-left of inner container).",
    },
)

topic(
    {
        "goal": [
            "how do I create a countdown timer display?",
        ],
    },
    {
        "goal": "Countdown timer:\n```js\nthis.timeLeft = 60\nconst timerLabel = cc.Label.createWithSystemFont('60', 'Arial', 36)\nthis.addChild(timerLabel)\nthis.schedule((dt) => {\n    this.timeLeft -= dt\n    if (this.timeLeft <= 0) {\n        this.timeLeft = 0\n        this.unschedule(this.onTimerTick)\n        this.onTimeUp()\n    }\n    timerLabel.setString(Math.ceil(this.timeLeft).toString())\n}, 0, cc.REPEAT_FOREVER, 0, 'timer')\n```",
    },
)

topic(
    {
        "goal": [
            "how do I create a particle-like spawn system?",
            "I want to spawn objects at intervals",
        ],
    },
    {
        "goal": "Use schedule for periodic spawning:\n```js\nthis.schedule(() => {\n    const enemy = new cc.Sprite('res/enemy.png')\n    const x = Math.random() * cc.winSize.width\n    enemy.setPosition(x, cc.winSize.height + 50)\n    this.addChild(enemy)\n    enemy.runAction(cc.sequence(\n        cc.moveTo(3.0, cc.p(x, -50)),\n        cc.removeSelf()\n    ))\n}, 1.5)  // spawn every 1.5 seconds\n```",
    },
)

topic(
    {
        "casual": [
            "how do I check types at runtime in cocos2d-x JS?",
        ],
    },
    {
        "casual": "Use cc type checks: `cc.isFunction(obj)`, `cc.isNumber(obj)`, `cc.isString(obj)`, `cc.isArray(obj)`, `cc.isUndefined(obj)`, `cc.isObject(obj)`. Also `cc.sys.isObjectValid(obj)` checks if a native object is still alive (important in JSB).",
    },
)

topic(
    {
        "casual": [
            "how do I set texture filtering for pixel art?",
        ],
        "goal": [
            "my pixel art looks blurry",
        ],
    },
    {
        "casual": "Use `gl.NEAREST` filtering for crisp pixel art:\n```js\nconst texture = sprite.getTexture()\ntexture.setTexParameters(gl.NEAREST, gl.NEAREST, gl.CLAMP_TO_EDGE, gl.CLAMP_TO_EDGE)\n```\nDefault is `gl.LINEAR` which smooths pixels.",
        "goal": "For crisp pixel art, set NEAREST filtering on your textures:\n```js\nconst tex = sprite.getTexture()\ntex.setTexParameters(gl.NEAREST, gl.NEAREST, gl.CLAMP_TO_EDGE, gl.CLAMP_TO_EDGE)\n```\nDo this after creating the sprite. You may also want to use `gl.REPEAT` or `gl.MIRRORED_REPEAT` for tiling textures.",
    },
)

topic(
    {
        "casual": [
            "how do I create a coin collection effect?",
        ],
        "goal": [
            "I want coins to fly toward the score counter when collected",
        ],
    },
    {
        "goal": "Coin fly-to-score effect:\n```js\ncollectCoin(coinPos, scoreLabelPos) {\n    const coin = new cc.Sprite('res/coin.png')\n    coin.setPosition(coinPos)\n    this.addChild(coin, 100)\n    coin.runAction(cc.sequence(\n        cc.spawn(\n            cc.moveTo(0.5, scoreLabelPos).easing(cc.easeIn(2)),\n            cc.scaleTo(0.5, 0.3),\n            cc.fadeOut(0.5)\n        ),\n        cc.callFunc(() => {\n            coin.removeFromParent()\n            this.updateScore()\n        })\n    ))\n}\n```",
    },
)

topic(
    {
        "casual": [
            "how do I make a pulsing/breathing animation?",
        ],
    },
    {
        "casual": "Use a repeating scale sequence:\n```js\nnode.runAction(cc.repeatForever(cc.sequence(\n    cc.scaleTo(0.8, 1.1).easing(cc.easeSineInOut()),\n    cc.scaleTo(0.8, 1.0).easing(cc.easeSineInOut())\n)))\n```\nFor opacity pulse: replace scaleTo with fadeTo between two opacity values.",
    },
)

topic(
    {
        "casual": [
            "how do I make text that types out letter by letter?",
        ],
        "goal": [
            "I want a typewriter text effect for dialogue",
        ],
    },
    {
        "goal": "Typewriter effect:\n```js\ntypeText(label, fullText, charDelay) {\n    let index = 0\n    label.setString('')\n    this.schedule(() => {\n        index++\n        label.setString(fullText.substring(0, index))\n        if (index >= fullText.length) {\n            this.unschedule(this._typeTimer)\n        }\n    }, charDelay, fullText.length - 1, 0, 'typewriter')\n}\n// Usage:\nthis.typeText(dialogLabel, 'Hello adventurer!', 0.05)\n```",
    },
)

topic(
    {
        "casual": [
            "how do I make a shaking/screen shake effect?",
        ],
        "goal": [
            "I want a camera shake when the player takes damage",
        ],
    },
    {
        "goal": "Screen shake effect:\n```js\nshakeScreen(layer, intensity, duration) {\n    const shakes = Math.floor(duration / 0.05)\n    const actions = []\n    for (let i = 0; i < shakes; i++) {\n        const dx = (Math.random() - 0.5) * intensity\n        const dy = (Math.random() - 0.5) * intensity\n        actions.push(cc.moveTo(0.025, cc.p(dx, dy)))\n    }\n    actions.push(cc.moveTo(0.025, cc.p(0, 0)))  // reset\n    layer.runAction(cc.sequence(actions))\n}\n// Usage: shakeScreen(this.gameLayer, 10, 0.3)\n```",
    },
)

topic(
    {
        "casual": [
            "what is skewTo / skewBy for?",
        ],
    },
    {
        "casual": "`cc.skewTo(duration, skewX, skewY)` and `cc.skewBy` animate the skew (shear) transform. Skew distorts a node along X and Y axes. Useful for squash-and-stretch effects or italic-style animations.",
    },
)

topic(
    {
        "casual": [
            "how do I handle the accelerometer?",
        ],
    },
    {
        "casual": "Check if available with `cc.sys.capabilities.accelerometer`. Then use the acceleration event:\n```js\ncc.eventManager.addListener({\n    event: cc.EventListener.ACCELERATION,\n    callback: (accelEvent) => {\n        // accelEvent.x, .y, .z, .timestamp\n        node.x += accelEvent.x * speed\n    }\n}, this)\n```\nMostly useful on mobile devices for tilt controls.",
    },
)

topic(
    {
        "casual": [
            "how do I get label line height or kerning?",
        ],
    },
    {
        "casual": "Use `label.getLineHeight()` / `label.setLineHeight(h)` to control line spacing, and `label.getAdditionalKerning()` / `label.setAdditionalKerning(k)` for letter spacing. Note: these don't work with system fonts - only TTF and BMFont.",
    },
)

topic(
    {
        "casual": [
            "how do I animate individual letters in a label?",
        ],
    },
    {
        "casual": "Use `label.getLetter(index)` to get a sprite for each character (not available for system fonts). Then animate each letter:\n```js\nconst letter = label.getLetter(0)\nletter.runAction(cc.sequence(\n    cc.scaleTo(0.1, 1.5),\n    cc.scaleTo(0.1, 1.0)\n))\n```\nYou can create wave or bounce effects by animating each letter with a delay offset.",
    },
)


# ---------------------------------------------------------------------------
# Generation engine
# ---------------------------------------------------------------------------


def generate_pairs():
    """Generate all QA pairs from registered topics."""
    pairs = []
    for questions_by_style, answers_by_style in TOPICS:
        for style, question_list in questions_by_style.items():
            answer = answers_by_style.get(style)
            if answer is None:
                # Fall back to first available answer
                answer = next(iter(answers_by_style.values()))
            for q in question_list:
                pairs.append({"instruction": q, "output": answer})
    return pairs


def add_rephrasings(pairs):
    """Add rephrased variants to reach ~3000 total."""
    # Rephrasing templates grouped to avoid repeating any template > 3 times
    REPHRASE_TEMPLATES = [
        lambda q: f"Quick question: {q.rstrip('?.')}?",
        lambda q: f"Hey, {q[0].lower()}{q[1:]}",
        lambda q: f"Can you help me with this - {q.rstrip('?.')}?",
        lambda q: f"I was wondering, {q[0].lower()}{q[1:]}",
        lambda q: f"Could you explain {q.rstrip('?.')}?",
        lambda q: f"In Cocos2d-x JS, {q[0].lower()}{q[1:]}",
        lambda q: f"For my cocos2d game, {q[0].lower()}{q[1:]}",
        lambda q: f"Noob question but {q[0].lower()}{q[1:]}",
        lambda q: f"Working on a game and need help: {q.rstrip('?.')}",
        lambda q: f"What's the best approach to {q.rstrip('?.')}?",
        lambda q: f"Any tips on {q.rstrip('?.')}?",
        lambda q: f"Need some guidance - {q.rstrip('?.')}",
        lambda q: f"Can someone show me {q.rstrip('?.')}?",
        lambda q: f"Looking for help with {q.rstrip('?.')}",
        lambda q: f"How would I go about {q.rstrip('?.')}?",
        lambda q: f"Struggling with {q.rstrip('?.')} - any advice?",
        lambda q: f"Tell me about {q.rstrip('?.')}",
        lambda q: f"Please explain: {q}",
        lambda q: f"I'm trying to figure out {q.rstrip('?.')}",
        lambda q: f"What's the proper way to handle {q.rstrip('?.')}?",
        lambda q: f"Is there a good way to {q.rstrip('?.')}?",
        lambda q: f"New to cocos, {q[0].lower()}{q[1:]}",
        lambda q: f"So I need to {q.rstrip('?.')} - how?",
        lambda q: f"In a cocos2d-x project, {q[0].lower()}{q[1:]}",
        lambda q: f"How exactly do you {q.rstrip('?.')}?",
        lambda q: f"I've been trying to {q.rstrip('?.')} but I'm stuck",
        lambda q: f"What's the recommended way to {q.rstrip('?.')}?",
        lambda q: f"Help me understand {q.rstrip('?.')}",
        lambda q: f"Explain to me {q.rstrip('?.')}",
        lambda q: f"My question is: {q}",
        lambda q: f"How do cocos2d-x developers usually {q.rstrip('?.')}?",
        lambda q: f"Starting a new game, {q[0].lower()}{q[1:]}",
        lambda q: f"For a 2D game, {q[0].lower()}{q[1:]}",
        lambda q: f"Walk me through {q.rstrip('?.')}",
        lambda q: f"Step by step, {q[0].lower()}{q[1:]}",
        lambda q: f"Show me how to {q.rstrip('?.')}",
        lambda q: f"What do I need to know about {q.rstrip('?.')}?",
        lambda q: f"Cocos2d question: {q}",
        lambda q: f"Game dev question - {q}",
        lambda q: f"I need assistance with {q.rstrip('?.')}",
        lambda q: f"Does anyone know {q.rstrip('?.')}?",
        lambda q: f"Having trouble with {q.rstrip('?.')} - thoughts?",
        lambda q: f"Using cocos2d-x JS, {q[0].lower()}{q[1:]}",
        lambda q: f"Really need to figure out {q.rstrip('?.')}",
        lambda q: f"Wondering about {q.rstrip('?.')}",
        lambda q: f"Question about cocos2d: {q}",
        lambda q: f"How should I {q.rstrip('?.')}?",
        lambda q: f"What method do I use to {q.rstrip('?.')}?",
        lambda q: f"Is it possible to {q.rstrip('?.')}?",
        lambda q: f"What's a clean way to {q.rstrip('?.')}?",
    ]

    target = 3000
    current = len(pairs)
    if current >= target:
        return pairs

    # Track template usage count
    template_uses = [0] * len(REPHRASE_TEMPLATES)
    max_uses_per_template = 3

    extra = []
    needed = target - current

    # Shuffle original pairs for variety
    shuffled_indices = list(range(current))
    random.shuffle(shuffled_indices)

    idx = 0
    while len(extra) < needed:
        pair_idx = shuffled_indices[idx % current]
        original = pairs[pair_idx]

        # Find a template that hasn't been overused
        available = [
            i for i, count in enumerate(template_uses)
            if count < max_uses_per_template
        ]
        if not available:
            # Reset all counters (allows cycling)
            template_uses = [0] * len(REPHRASE_TEMPLATES)
            available = list(range(len(REPHRASE_TEMPLATES)))

        t_idx = random.choice(available)
        template = REPHRASE_TEMPLATES[t_idx]
        template_uses[t_idx] += 1

        try:
            new_q = template(original["instruction"])
            extra.append({"instruction": new_q, "output": original["output"]})
        except Exception:
            pass

        idx += 1

    return pairs + extra


def main():
    pairs = generate_pairs()
    print(f"Base pairs generated: {len(pairs)}")

    all_pairs = add_rephrasings(pairs)
    random.shuffle(all_pairs)

    print(f"Total pairs after rephrasings: {len(all_pairs)}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for pair in all_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    print(f"Written to {OUTPUT_PATH}")

    # Validate no template repeated > 3 times (across base questions)
    from collections import Counter
    # Count exact duplicate instructions
    instr_counts = Counter(p["instruction"] for p in all_pairs)
    dupes = {k: v for k, v in instr_counts.items() if v > 1}
    if dupes:
        print(f"WARNING: {len(dupes)} duplicate instructions found")
        for k, v in sorted(dupes.items(), key=lambda x: -x[1])[:5]:
            print(f"  '{k[:60]}...' x{v}")
    else:
        print("No duplicate instructions - good!")


if __name__ == "__main__":
    main()
