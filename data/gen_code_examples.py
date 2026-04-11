"""
Generate ~2000 code-focused QA pairs for Cocos2d-x JS API fine-tuning.
Categories: complete snippets (800), code completion (400), code explanation (400), refactoring (400).
Covers all 14 doc modules proportionally.
Output: data/code-examples-qa.jsonl
"""

import json
import random
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent / "code-examples-qa.jsonl"
random.seed(42)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def jl(instruction, output):
    """Return a dict for one JSONL row."""
    return {"instruction": instruction.strip(), "output": output.strip()}


def pick(lst):
    return random.choice(lst)


# ---------------------------------------------------------------------------
# 1. COMPLETE CODE SNIPPETS  (~800)
# ---------------------------------------------------------------------------

COMPLETE_SNIPPETS = []

# --- Sprite creation (module: sprite) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of creating a sprite from a PNG file and positioning it at the center of the screen.",
       """```js
// Create a sprite from a PNG file and center it on screen
var winSize = cc.director.getWinSize();
var sprite = new cc.Sprite('res/hero.png');
sprite.setPosition(winSize.width / 2, winSize.height / 2);
sprite.setAnchorPoint(cc.p(0.5, 0.5));
this.addChild(sprite, 1);
```"""),

    jl("Write a complete example of creating a sprite from a sprite frame in an atlas.",
       """```js
// Load atlas plist, then create sprite from a named frame
cc.spriteFrameCache.addSpriteFrames('res/characters.plist', 'res/characters.png');
var frame = cc.spriteFrameCache.getSpriteFrame('hero_idle_01.png');
var sprite = new cc.Sprite(frame);
sprite.setPosition(240, 160);
this.addChild(sprite);
```"""),

    jl("Write a complete example of creating a sprite with a sub-rectangle of a texture.",
       """```js
// Create sprite using only a 64x64 region starting at (128, 0)
var sprite = new cc.Sprite('res/spritesheet.png', cc.rect(128, 0, 64, 64));
sprite.setPosition(200, 300);
this.addChild(sprite);
```"""),

    jl("Write a complete example of flipping a sprite horizontally.",
       """```js
// Create a sprite and flip it to face left
var sprite = new cc.Sprite('res/hero.png');
sprite.setPosition(240, 160);
sprite.setFlippedX(true);
this.addChild(sprite);
```"""),

    jl("Write a complete example of changing a sprite's texture at runtime.",
       """```js
// Swap the sprite's texture when the player powers up
var hero = new cc.Sprite('res/hero_normal.png');
hero.setPosition(240, 160);
this.addChild(hero);

// Later, on power-up:
hero.setTexture('res/hero_powered.png');
```"""),

    jl("Write a complete example of using SpriteBatchNode for efficient rendering.",
       """```js
// Use SpriteBatchNode to draw many sprites in one draw call
cc.spriteFrameCache.addSpriteFrames('res/enemies.plist', 'res/enemies.png');
var batch = new cc.SpriteBatchNode('res/enemies.png', 50);
this.addChild(batch);

for (var i = 0; i < 20; i++) {
    var enemy = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('enemy_01.png'));
    enemy.setPosition(50 + i * 30, 200);
    batch.addChild(enemy);
}
```"""),

    jl("Write a complete example of creating a sprite and setting its opacity to 50%.",
       """```js
// Create a semi-transparent sprite
var ghost = new cc.Sprite('res/ghost.png');
ghost.setPosition(240, 160);
ghost.setOpacity(128); // 0-255, 128 is roughly 50%
this.addChild(ghost);
```"""),

    jl("Write a complete example of tinting a sprite red.",
       """```js
// Tint sprite with a red color overlay
var sprite = new cc.Sprite('res/hero.png');
sprite.setPosition(240, 160);
sprite.setColor(cc.color(255, 100, 100));
this.addChild(sprite);
```"""),

    jl("Write a complete example of preloading textures using cc.textureCache.",
       """```js
// Preload textures before creating sprites
cc.textureCache.addImage('res/hero.png');
cc.textureCache.addImage('res/enemy.png');
cc.textureCache.addImage('res/background.png');

// Later, sprites using these textures will be instant
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(240, 160);
this.addChild(hero);
```"""),

    jl("Write a complete example of switching a sprite's displayed frame by name.",
       """```js
// Switch between animation frames on a sprite
cc.spriteFrameCache.addSpriteFrames('res/hero.plist', 'res/hero.png');
var hero = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('hero_idle_01.png'));
hero.setPosition(240, 160);
this.addChild(hero);

// Change to a different frame
hero.setSpriteFrame('hero_run_01.png');
```"""),
]

# --- Animations (module: actions - animate) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of a frame-by-frame sprite animation using cc.Animation and cc.animate.",
       """```js
// Create a running animation from sprite frames
cc.spriteFrameCache.addSpriteFrames('res/hero.plist', 'res/hero.png');
var frames = [];
for (var i = 1; i <= 8; i++) {
    var name = 'run_' + (i < 10 ? '0' + i : i) + '.png';
    frames.push(cc.spriteFrameCache.getSpriteFrame(name));
}
var animation = new cc.Animation(frames, 0.08);
var hero = new cc.Sprite(frames[0]);
hero.setPosition(240, 160);
this.addChild(hero);
hero.runAction(cc.repeatForever(cc.animate(animation)));
```"""),

    jl("Write a complete example of creating a looping idle animation with cc.Animation.",
       """```js
// Build and play a looping idle animation
cc.spriteFrameCache.addSpriteFrames('res/hero.plist', 'res/hero.png');
var frames = [];
for (var i = 1; i <= 4; i++) {
    frames.push(cc.spriteFrameCache.getSpriteFrame('idle_0' + i + '.png'));
}
// 0.15s per frame, loop forever (0 loops = infinite)
var anim = new cc.Animation(frames, 0.15, 0);
var sprite = new cc.Sprite(frames[0]);
sprite.setPosition(240, 160);
this.addChild(sprite);
sprite.runAction(cc.repeatForever(cc.animate(anim)));
```"""),

    jl("Write a complete example of playing an animation once and calling a function when it finishes.",
       """```js
// Play a death animation once, then remove the sprite
cc.spriteFrameCache.addSpriteFrames('res/hero.plist', 'res/hero.png');
var frames = [];
for (var i = 1; i <= 6; i++) {
    frames.push(cc.spriteFrameCache.getSpriteFrame('death_0' + i + '.png'));
}
var anim = new cc.Animation(frames, 0.1);
anim.setRestoreOriginalFrame(false);
var sprite = new cc.Sprite(frames[0]);
sprite.setPosition(240, 160);
this.addChild(sprite);
sprite.runAction(cc.sequence(
    cc.animate(anim),
    cc.callFunc(function() {
        sprite.removeFromParent();
    })
));
```"""),
]

# --- Actions (module: actions) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of moving a node to a position over 1 second.",
       """```js
// Move a sprite to position (300, 400) over 1 second
var sprite = new cc.Sprite('res/hero.png');
sprite.setPosition(100, 100);
this.addChild(sprite);
sprite.runAction(cc.moveTo(1.0, cc.p(300, 400)));
```"""),

    jl("Write a complete example of a bounce animation using cc.sequence and cc.moveBy.",
       """```js
// Bounce a sprite up and down forever
var ball = new cc.Sprite('res/ball.png');
ball.setPosition(240, 100);
this.addChild(ball);

var bounceUp = cc.moveBy(0.4, cc.p(0, 80)).easing(cc.easeOut(2.0));
var bounceDown = cc.moveBy(0.4, cc.p(0, -80)).easing(cc.easeBounceOut());
ball.runAction(cc.repeatForever(cc.sequence(bounceUp, bounceDown)));
```"""),

    jl("Write a complete example of scaling a node up then back down (pop effect).",
       """```js
// Pop effect: scale up to 1.3x then back to 1.0x
var icon = new cc.Sprite('res/star.png');
icon.setPosition(240, 320);
this.addChild(icon);

icon.runAction(cc.sequence(
    cc.scaleTo(0.15, 1.3).easing(cc.easeBackOut()),
    cc.scaleTo(0.1, 1.0)
));
```"""),

    jl("Write a complete example of fading a node in from invisible.",
       """```js
// Fade in a title label from fully transparent
var title = cc.Label.createWithSystemFont('GAME OVER', 'Arial', 48);
title.setPosition(cc.director.getWinSize().width / 2, 300);
title.setOpacity(0);
this.addChild(title);
title.runAction(cc.fadeIn(1.0));
```"""),

    jl("Write a complete example of fading out a sprite then removing it.",
       """```js
// Fade out and auto-remove a defeated enemy
var enemy = new cc.Sprite('res/enemy.png');
enemy.setPosition(200, 300);
this.addChild(enemy);

enemy.runAction(cc.sequence(
    cc.fadeOut(0.5),
    cc.callFunc(function() {
        enemy.removeFromParent();
    })
));
```"""),

    jl("Write a complete example of running two actions simultaneously using cc.spawn.",
       """```js
// Move and rotate a coin simultaneously
var coin = new cc.Sprite('res/coin.png');
coin.setPosition(100, 100);
this.addChild(coin);

var move = cc.moveTo(1.0, cc.p(400, 300));
var rotate = cc.rotateBy(1.0, 360);
coin.runAction(cc.spawn(move, rotate));
```"""),

    jl("Write a complete example of a repeating rotation animation.",
       """```js
// Spin a gear sprite forever
var gear = new cc.Sprite('res/gear.png');
gear.setPosition(240, 240);
this.addChild(gear);
gear.runAction(cc.repeatForever(cc.rotateBy(2.0, 360)));
```"""),

    jl("Write a complete example of a jump action to make a character hop.",
       """```js
// Make a character jump to position (300, 100) with 3 hops
var character = new cc.Sprite('res/hero.png');
character.setPosition(100, 100);
this.addChild(character);
character.runAction(cc.jumpTo(1.5, cc.p(300, 100), 80, 3));
```"""),

    jl("Write a complete example of a bezier curve movement.",
       """```js
// Move a projectile along a bezier curve
var bullet = new cc.Sprite('res/bullet.png');
bullet.setPosition(50, 100);
this.addChild(bullet);

var controlPoints = [
    cc.p(100, 300),  // control point 1
    cc.p(250, 300),  // control point 2
    cc.p(400, 100)   // destination
];
bullet.runAction(cc.sequence(
    cc.bezierTo(1.5, controlPoints),
    cc.removeSelf()
));
```"""),

    jl("Write a complete example of using easing functions on a move action.",
       """```js
// Move with elastic ease-out effect
var box = new cc.Sprite('res/box.png');
box.setPosition(50, 240);
this.addChild(box);

box.runAction(
    cc.moveTo(1.5, cc.p(400, 240)).easing(cc.easeElasticOut(0.3))
);
```"""),

    jl("Write a complete example of blinking a sprite.",
       """```js
// Blink a power-up item 5 times over 2 seconds
var powerUp = new cc.Sprite('res/power_up.png');
powerUp.setPosition(240, 160);
this.addChild(powerUp);
powerUp.runAction(cc.blink(2.0, 5));
```"""),

    jl("Write a complete example of tinting a sprite from one color to another.",
       """```js
// Tint a sprite from white to red over 0.5 seconds (damage flash)
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(240, 160);
this.addChild(hero);

hero.runAction(cc.sequence(
    cc.tintTo(0.2, 255, 0, 0),
    cc.tintTo(0.3, 255, 255, 255)
));
```"""),

    jl("Write a complete example of using cc.delayTime in a sequence.",
       """```js
// Show sprite, wait 2 seconds, then fade out
var notification = new cc.Sprite('res/notification.png');
notification.setPosition(240, 400);
this.addChild(notification);

notification.runAction(cc.sequence(
    cc.delayTime(2.0),
    cc.fadeOut(0.5),
    cc.removeSelf()
));
```"""),

    jl("Write a complete example of using cc.targetedAction to run an action on a different node.",
       """```js
// When hero reaches goal, make the goal node scale up
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(50, 160);
this.addChild(hero);

var goal = new cc.Sprite('res/goal.png');
goal.setPosition(400, 160);
this.addChild(goal);

hero.runAction(cc.sequence(
    cc.moveTo(2.0, cc.p(400, 160)),
    cc.targetedAction(goal, cc.scaleTo(0.3, 1.5))
));
```"""),

    jl("Write a complete example of using cc.speed to control action playback speed.",
       """```js
// Run an action at 2x speed
var sprite = new cc.Sprite('res/hero.png');
sprite.setPosition(50, 160);
this.addChild(sprite);

var move = cc.moveTo(2.0, cc.p(400, 160));
var fast = cc.speed(move, 2.0); // plays in 1 second
sprite.runAction(fast);
```"""),

    jl("Write a complete example of using cc.follow to make the camera follow a node.",
       """```js
// Make the layer follow the hero within a bounding rect
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(100, 160);
this.addChild(hero);

// Boundary rect for the level
var levelBounds = cc.rect(0, 0, 2000, 320);
this.runAction(cc.follow(hero, levelBounds));

// Move hero so camera follows
hero.runAction(cc.moveTo(5.0, cc.p(1800, 160)));
```"""),

    jl("Write a complete example of tagging an action and stopping it later.",
       """```js
// Tag a rotation action so we can stop it later
var sprite = new cc.Sprite('res/gear.png');
sprite.setPosition(240, 160);
this.addChild(sprite);

var spin = cc.repeatForever(cc.rotateBy(1.0, 360));
spin.setTag(100);
sprite.runAction(spin);

// Later, stop the spin
sprite.stopActionByTag(100);
```"""),

    jl("Write a complete example of reversing an action.",
       """```js
// Move right, then reverse to move back left
var sprite = new cc.Sprite('res/hero.png');
sprite.setPosition(100, 160);
this.addChild(sprite);

var moveRight = cc.moveBy(1.0, cc.p(200, 0));
sprite.runAction(cc.sequence(
    moveRight,
    moveRight.reverse()
));
```"""),

    jl("Write a complete example of cc.progressTo for a progress timer.",
       """```js
// Animate a radial progress timer from 0% to 100%
var timer = new cc.ProgressTimer(new cc.Sprite('res/circle.png'));
timer.setType(cc.ProgressTimer.TYPE_RADIAL);
timer.setPosition(240, 160);
this.addChild(timer);
timer.runAction(cc.progressTo(2.0, 100));
```"""),

    jl("Write a complete example of using cc.repeatForever with cc.sequence for a patrol pattern.",
       """```js
// Patrol: move right, pause, move left, pause, repeat
var guard = new cc.Sprite('res/guard.png');
guard.setPosition(100, 160);
this.addChild(guard);

guard.runAction(cc.repeatForever(cc.sequence(
    cc.moveBy(1.5, cc.p(200, 0)),
    cc.delayTime(0.5),
    cc.moveBy(1.5, cc.p(-200, 0)),
    cc.delayTime(0.5)
)));
```"""),

    jl("Write a complete example of a card flip effect using scaleX.",
       """```js
// Card flip: scale X to 0, swap texture, scale X back
var card = new cc.Sprite('res/card_back.png');
card.setPosition(240, 240);
this.addChild(card);

card.runAction(cc.sequence(
    cc.scaleTo(0.15, 0, 1),
    cc.callFunc(function() {
        card.setTexture('res/card_front.png');
    }),
    cc.scaleTo(0.15, 1, 1)
));
```"""),

    jl("Write a complete example of a heartbeat pulse animation.",
       """```js
// Heartbeat pulse: scale up/down in a repeating pattern
var heart = new cc.Sprite('res/heart.png');
heart.setPosition(240, 300);
this.addChild(heart);

heart.runAction(cc.repeatForever(cc.sequence(
    cc.scaleTo(0.1, 1.2),
    cc.scaleTo(0.1, 1.0),
    cc.scaleTo(0.1, 1.15),
    cc.scaleTo(0.1, 1.0),
    cc.delayTime(0.6)
)));
```"""),
]

# --- UI widgets (module: ccui) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of creating a ccui.Button with a click handler.",
       """```js
// Create a UI button with normal/pressed textures and click handler
var btn = new ccui.Button('btn_normal.png', 'btn_pressed.png', '', ccui.Widget.PLIST_TEXTURE);
btn.setTitleText('PLAY');
btn.setTitleFontSize(24);
btn.setTitleColor(cc.color.WHITE);
btn.setPosition(cc.director.getWinSize().width / 2, 200);
btn.addClickEventListener(function() {
    cc.log('Play button clicked!');
});
this.addChild(btn);
```"""),

    jl("Write a complete example of creating a ccui.Button from local image files.",
       """```js
// Button using local texture files (not sprite frames)
var btn = new ccui.Button('res/btn_normal.png', 'res/btn_pressed.png', 'res/btn_disabled.png');
btn.setPosition(240, 160);
btn.setTitleText('START');
btn.setTitleFontSize(20);
btn.setScale9Enabled(true);
btn.setSize(cc.size(200, 60));
btn.addTouchEventListener(function(sender, type) {
    if (type === ccui.Widget.TOUCH_ENDED) {
        cc.log('Button tapped');
    }
}, this);
this.addChild(btn);
```"""),

    jl("Write a complete example of creating a ccui.ScrollView with vertical scrolling.",
       """```js
// Create a vertical scroll view with items
var sv = new ccui.ScrollView();
sv.setSize(cc.size(300, 400));
sv.setPosition(90, 60);
sv.setDirection(ccui.ScrollView.DIR_VERTICAL);
sv.setInnerContainerSize(cc.size(300, 1200));
sv.setBounceEnabled(true);
sv.setScrollBarEnabled(true);
this.addChild(sv);

// Populate with items
for (var i = 0; i < 20; i++) {
    var label = new ccui.Text('Item ' + (i + 1), 'Arial', 20);
    label.setPosition(150, 1180 - i * 60);
    sv.getInnerContainer().addChild(label);
}
sv.jumpToTop();
```"""),

    jl("Write a complete example of creating a ccui.Layout with a solid background color.",
       """```js
// Create a panel with a dark semi-transparent background
var panel = new ccui.Layout();
panel.setSize(cc.size(300, 200));
panel.setPosition(90, 140);
panel.setBackGroundColorType(ccui.Layout.BG_COLOR_SOLID);
panel.setBackGroundColor(cc.color(0, 0, 0));
panel.setBackGroundColorOpacity(180);
panel.setClippingEnabled(true);
this.addChild(panel);
```"""),

    jl("Write a complete example of a ccui.TextField for text input.",
       """```js
// Create a text input field with placeholder
var tf = new ccui.TextField('Enter your name...', 'Arial', 20);
tf.setPosition(240, 200);
tf.setMaxLengthEnabled(true);
tf.setMaxLength(16);
tf.setTouchAreaEnabled(true);
tf.addEventListener(function(sender, type) {
    if (type === ccui.TextField.EVENT_INSERT_TEXT) {
        cc.log('Text: ' + sender.getString());
    }
}, this);
this.addChild(tf);
```"""),

    jl("Write a complete example of creating a ccui.Slider.",
       """```js
// Volume slider
var slider = new ccui.Slider();
slider.loadBarTexture('res/slider_bar.png');
slider.loadSlidBallTextures('res/slider_ball.png', 'res/slider_ball.png', '');
slider.loadProgressBarTexture('res/slider_progress.png');
slider.setPosition(240, 200);
slider.setPercent(70);
slider.addEventListener(function(sender, type) {
    var percent = sender.getPercent();
    cc.audioEngine.setMusicVolume(percent / 100);
}, this);
this.addChild(slider);
```"""),

    jl("Write a complete example of creating a ccui.CheckBox.",
       """```js
// Sound toggle checkbox
var cb = new ccui.CheckBox(
    'res/cb_bg.png', 'res/cb_bg_selected.png',
    'res/cb_cross.png', 'res/cb_bg_disabled.png', 'res/cb_cross_disabled.png'
);
cb.setPosition(240, 200);
cb.setSelected(true);
cb.addEventListener(function(sender, type) {
    if (sender.isSelected()) {
        cc.audioEngine.resumeMusic();
    } else {
        cc.audioEngine.pauseMusic();
    }
}, this);
this.addChild(cb);
```"""),

    jl("Write a complete example of creating a ccui.LoadingBar for a health bar.",
       """```js
// Create a health bar at 100%
var hpBar = new ccui.LoadingBar('res/hp_bar.png', 100);
hpBar.setDirection(ccui.LoadingBar.TYPE_LEFT);
hpBar.setPosition(240, 440);
this.addChild(hpBar);

// Simulate taking damage
hpBar.setPercent(75);
```"""),

    jl("Write a complete example of ccui.ImageView.",
       """```js
// Display a portrait image in the UI
var portrait = new ccui.ImageView('res/portrait.png');
portrait.setPosition(80, 400);
portrait.setScale9Enabled(false);
portrait.setTouchEnabled(true);
portrait.addClickEventListener(function() {
    cc.log('Portrait tapped');
});
this.addChild(portrait);
```"""),

    jl("Write a complete example of ccui.Text for displaying styled text.",
       """```js
// Display a styled score label
var scoreText = new ccui.Text('Score: 0', 'Arial', 28);
scoreText.setPosition(240, 440);
scoreText.setTextColor(cc.color(255, 220, 0));
scoreText.setTextHorizontalAlignment(cc.TEXT_ALIGNMENT_CENTER);
this.addChild(scoreText);

// Update later:
scoreText.setString('Score: 1500');
```"""),

    jl("Write a complete example of a ccui.ListView with custom items.",
       """```js
// Create a vertical list view with text items
var lv = new ccui.ListView();
lv.setSize(cc.size(300, 400));
lv.setPosition(90, 60);
lv.setDirection(ccui.ScrollView.DIR_VERTICAL);
lv.setGravity(ccui.ListView.GRAVITY_CENTER_HORIZONTAL);
lv.setItemsMargin(10);
lv.setBounceEnabled(true);

for (var i = 0; i < 30; i++) {
    var item = new ccui.Button('res/list_item_bg.png');
    item.setTitleText('Level ' + (i + 1));
    item.setTitleFontSize(18);
    lv.pushBackCustomItem(item);
}
this.addChild(lv);
```"""),

    jl("Write a complete example of a ccui.PageView with multiple pages.",
       """```js
// Create a swipeable page view with 5 pages
var pv = new ccui.PageView();
pv.setSize(cc.size(400, 300));
pv.setPosition(40, 90);

for (var i = 0; i < 5; i++) {
    var page = new ccui.Layout();
    page.setSize(cc.size(400, 300));
    var label = new ccui.Text('Page ' + (i + 1), 'Arial', 32);
    label.setPosition(200, 150);
    page.addChild(label);
    pv.addPage(page);
}

pv.addEventListener(function(sender, type) {
    cc.log('Current page: ' + sender.getCurrentPageIndex());
}, this);
this.addChild(pv);
```"""),

    jl("Write a complete example of using ccui.LinearLayoutParameter for horizontal layout.",
       """```js
// Horizontal layout with evenly spaced buttons
var layout = new ccui.Layout();
layout.setSize(cc.size(400, 60));
layout.setPosition(40, 200);
layout.setLayoutType(ccui.Layout.LINEAR_HORIZONTAL);

var names = ['Sword', 'Shield', 'Potion'];
for (var i = 0; i < names.length; i++) {
    var btn = new ccui.Button('res/btn_bg.png');
    btn.setTitleText(names[i]);
    btn.setTitleFontSize(16);
    var param = new ccui.LinearLayoutParameter();
    param.setGravity(ccui.LinearLayoutParameter.CENTER_VERTICAL);
    param.setMargin(new ccui.Margin(10, 5, 10, 5));
    btn.setLayoutParameter(param);
    layout.addChild(btn);
}
layout.forceDoLayout();
this.addChild(layout);
```"""),

    jl("Write a complete example of using ccui.helper.seekWidgetByName to find a child widget.",
       """```js
// Find a specific widget by name in a UI tree
var root = new ccui.Layout();
root.setSize(cc.size(400, 300));
this.addChild(root);

var btn = new ccui.Button('res/btn_bg.png');
btn.setName('playButton');
btn.setTitleText('PLAY');
root.addChild(btn);

// Later, find it by name
var found = ccui.helper.seekWidgetByName(root, 'playButton');
if (found) {
    found.addClickEventListener(function() {
        cc.log('Found and clicked!');
    });
}
```"""),

    jl("Write a complete example of a scroll view that detects when user scrolls to the bottom.",
       """```js
// Detect scroll-to-bottom for infinite scroll / loading more
var sv = new ccui.ScrollView();
sv.setSize(cc.size(300, 400));
sv.setPosition(90, 60);
sv.setDirection(ccui.ScrollView.DIR_VERTICAL);
sv.setInnerContainerSize(cc.size(300, 1000));
sv.setBounceEnabled(true);
this.addChild(sv);

sv.addEventListener(function(sender, type) {
    if (type === ccui.ScrollView.EVENT_SCROLL_TO_BOTTOM) {
        cc.log('Reached bottom - load more items');
    }
}, this);
```"""),
]

# --- Touch handling (module: events) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of handling single-touch events on a layer.",
       """```js
// Handle touch began/moved/ended on a layer
var MyLayer = cc.Layer.extend({
    onEnter: function() {
        this._super();
        this._listener = cc.eventManager.addListener({
            event: cc.EventListener.TOUCH_ONE_BY_ONE,
            swallowTouches: true,
            onTouchBegan: function(touch, event) {
                var loc = touch.getLocation();
                cc.log('Touch began at:', loc.x, loc.y);
                return true; // must return true to receive move/end
            },
            onTouchMoved: function(touch, event) {
                var delta = touch.getDelta();
                cc.log('Moved by:', delta.x, delta.y);
            },
            onTouchEnded: function(touch, event) {
                cc.log('Touch ended');
            }
        }, this);
    },
    onExit: function() {
        cc.eventManager.removeListener(this._listener);
        this._super();
    }
});
```"""),

    jl("Write a complete example of dragging a sprite with touch events.",
       """```js
// Make a sprite draggable
var sprite = new cc.Sprite('res/box.png');
sprite.setPosition(240, 160);
this.addChild(sprite);

cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    swallowTouches: true,
    onTouchBegan: function(touch, event) {
        var target = event.getCurrentTarget();
        var loc = target.convertTouchToNodeSpace(touch);
        var size = target.getContentSize();
        var rect = cc.rect(0, 0, size.width, size.height);
        return cc.rectContainsPoint(rect, loc);
    },
    onTouchMoved: function(touch, event) {
        var target = event.getCurrentTarget();
        var delta = touch.getDelta();
        target.x += delta.x;
        target.y += delta.y;
    }
}, sprite);
```"""),

    jl("Write a complete example of handling keyboard input for player movement.",
       """```js
// Handle arrow keys for 4-directional movement
var GameLayer = cc.Layer.extend({
    _keys: null,
    _hero: null,
    _speed: 200,
    ctor: function() {
        this._super();
        this._keys = {};
        this._hero = new cc.Sprite('res/hero.png');
        this._hero.setPosition(240, 160);
        this.addChild(this._hero);

        cc.eventManager.addListener({
            event: cc.EventListener.KEYBOARD,
            onKeyPressed: function(key) { this._keys[key] = true; }.bind(this),
            onKeyReleased: function(key) { this._keys[key] = false; }.bind(this)
        }, this);
        this.scheduleUpdate();
    },
    update: function(dt) {
        var dx = 0, dy = 0;
        if (this._keys[cc.KEY.left])  dx -= this._speed * dt;
        if (this._keys[cc.KEY.right]) dx += this._speed * dt;
        if (this._keys[cc.KEY.up])    dy += this._speed * dt;
        if (this._keys[cc.KEY.down])  dy -= this._speed * dt;
        this._hero.x += dx;
        this._hero.y += dy;
    }
});
```"""),

    jl("Write a complete example of handling mouse events.",
       """```js
// Handle mouse click and scroll
cc.eventManager.addListener({
    event: cc.EventListener.MOUSE,
    onMouseDown: function(event) {
        if (event.getButton() === cc.EventMouse.BUTTON_LEFT) {
            var loc = event.getLocation();
            cc.log('Left click at:', loc.x, loc.y);
        }
    },
    onMouseScroll: function(event) {
        var scrollY = event.getScrollY();
        cc.log('Scroll delta:', scrollY);
    }
}, this);
```"""),

    jl("Write a complete example of custom events (pub/sub pattern) for game communication.",
       """```js
// Use custom events to decouple score updates
// In the HUD layer - listen for score changes
var listener = cc.eventManager.addCustomListener('game:score_update', function(event) {
    var data = event.getUserData();
    scoreLabel.setString('Score: ' + data.score);
});

// In the game layer - dispatch when enemy killed
function onEnemyKilled(points) {
    currentScore += points;
    cc.eventManager.dispatchCustomEvent('game:score_update', { score: currentScore });
}

// Clean up when done
cc.eventManager.removeListener(listener);
```"""),

    jl("Write a complete example of multi-touch handling.",
       """```js
// Handle multi-touch (e.g. pinch or two-finger gesture)
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ALL_AT_ONCE,
    onTouchesBegan: function(touches, event) {
        cc.log('Number of touches:', touches.length);
    },
    onTouchesMoved: function(touches, event) {
        if (touches.length === 2) {
            var t1 = touches[0].getLocation();
            var t2 = touches[1].getLocation();
            var dist = cc.pDistance(t1, t2);
            cc.log('Pinch distance:', dist);
        }
    },
    onTouchesEnded: function(touches, event) {
        cc.log('All touches ended');
    }
}, this);
```"""),

    jl("Write a complete example of checking if a touch hit a specific node.",
       """```js
// Check if a touch landed on a node using bounding box
function isTouchOnNode(touch, node) {
    var locationInNode = node.convertTouchToNodeSpace(touch);
    var size = node.getContentSize();
    var rect = cc.rect(0, 0, size.width, size.height);
    return cc.rectContainsPoint(rect, locationInNode);
}

// Usage in a touch listener:
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    swallowTouches: true,
    onTouchBegan: function(touch, event) {
        if (isTouchOnNode(touch, mySprite)) {
            cc.log('Touched the sprite!');
            return true;
        }
        return false;
    }
}, this);
```"""),

    jl("Write a complete example of handling the Android back button.",
       """```js
// Handle Android back button to go back or exit
cc.eventManager.addListener({
    event: cc.EventListener.KEYBOARD,
    onKeyPressed: function(keyCode, event) {
        if (keyCode === cc.KEY.back) {
            // Go back to previous scene or exit
            cc.director.popScene();
        }
    }
}, this);
```"""),
]

# --- Audio (module: audio) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of playing background music with volume control.",
       """```js
// Play looping background music at 70% volume
cc.audioEngine.playMusic('res/audio/bgm_main.mp3', true);
cc.audioEngine.setMusicVolume(0.7);
```"""),

    jl("Write a complete example of playing a sound effect and stopping it later.",
       """```js
// Play a looping engine sound, stop it when vehicle stops
var engineId = cc.audioEngine.playEffect('res/audio/engine_loop.mp3', true);

// Later, when vehicle stops:
cc.audioEngine.stopEffect(engineId);
```"""),

    jl("Write a complete example of preloading audio assets at game start.",
       """```js
// Preload all audio at scene init for instant playback
cc.audioEngine.preloadMusic('res/audio/bgm_battle.mp3');
cc.audioEngine.preloadEffect('res/audio/sfx_hit.mp3');
cc.audioEngine.preloadEffect('res/audio/sfx_coin.mp3');
cc.audioEngine.preloadEffect('res/audio/sfx_jump.mp3');

// Now these will play without loading delay
cc.audioEngine.playMusic('res/audio/bgm_battle.mp3', true);
```"""),

    jl("Write a complete example of pausing and resuming music when the game pauses.",
       """```js
// Pause/resume audio with game state
function onGamePause() {
    cc.audioEngine.pauseMusic();
    cc.audioEngine.pauseAllEffects();
}

function onGameResume() {
    cc.audioEngine.resumeMusic();
    cc.audioEngine.resumeAllEffects();
}
```"""),

    jl("Write a complete example of a simple sound manager class.",
       """```js
// Simple sound manager with mute support
var SoundManager = {
    _musicEnabled: true,
    _sfxEnabled: true,

    playBGM: function(path) {
        if (this._musicEnabled) {
            cc.audioEngine.playMusic(path, true);
        }
    },
    playSFX: function(path) {
        if (this._sfxEnabled) {
            return cc.audioEngine.playEffect(path);
        }
        return null;
    },
    toggleMusic: function() {
        this._musicEnabled = !this._musicEnabled;
        if (!this._musicEnabled) {
            cc.audioEngine.stopMusic();
        }
    },
    toggleSFX: function() {
        this._sfxEnabled = !this._sfxEnabled;
        if (!this._sfxEnabled) {
            cc.audioEngine.stopAllEffects();
        }
    },
    cleanup: function() {
        cc.audioEngine.stopMusic(true);
        cc.audioEngine.stopAllEffects();
    }
};
```"""),

    jl("Write a complete example of adjusting music and effects volume independently.",
       """```js
// Separate volume controls for music and effects
cc.audioEngine.setMusicVolume(0.5);   // 50% music
cc.audioEngine.setEffectsVolume(0.8); // 80% effects

// Read current volumes
var musicVol = cc.audioEngine.getMusicVolume();
var sfxVol = cc.audioEngine.getEffectsVolume();
cc.log('Music:', musicVol, 'SFX:', sfxVol);
```"""),
]

# --- Scene management (module: director) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of creating a scene with a layer and running it.",
       """```js
// Create a scene, add a layer, and run it
var GameLayer = cc.Layer.extend({
    ctor: function() {
        this._super();
        var label = cc.Label.createWithSystemFont('Hello World', 'Arial', 36);
        label.setPosition(cc.director.getWinSize().width / 2, 300);
        this.addChild(label);
    }
});

var scene = new cc.Scene();
scene.addChild(new GameLayer());
cc.director.runScene(scene);
```"""),

    jl("Write a complete example of transitioning between scenes with a fade effect.",
       """```js
// Transition to a new scene with a 0.5 second fade
var nextScene = new cc.Scene();
nextScene.addChild(new GameOverLayer());

var transition = new cc.TransitionFade(0.5, nextScene);
cc.director.runScene(transition);
```"""),

    jl("Write a complete example of using push/pop scene for a pause menu.",
       """```js
// Push pause menu on top of current scene
function showPauseMenu() {
    var pauseScene = new cc.Scene();
    pauseScene.addChild(new PauseMenuLayer());
    cc.director.pushScene(pauseScene);
}

// Pop back to the game when resume is clicked
function onResumeClicked() {
    cc.director.popScene();
}
```"""),

    jl("Write a complete example of getting the window size and centering a node.",
       """```js
// Center a node on screen using window size
var winSize = cc.director.getWinSize();
var centerX = winSize.width / 2;
var centerY = winSize.height / 2;

var logo = new cc.Sprite('res/logo.png');
logo.setPosition(centerX, centerY);
this.addChild(logo);
```"""),

    jl("Write a complete example of a scene class with onEnter lifecycle.",
       """```js
// Scene class with proper lifecycle management
var GameScene = cc.Scene.extend({
    onEnter: function() {
        this._super();
        var layer = new GameLayer();
        this.addChild(layer);
    }
});

// Run the scene
cc.director.runScene(new GameScene());
```"""),

    jl("Write a complete example of pausing and resuming the director.",
       """```js
// Pause the entire game (freezes all actions and scheduled updates)
cc.director.pause();

// Resume everything
cc.director.resume();

// Check if paused
if (cc.director.isPaused()) {
    cc.log('Game is paused');
}
```"""),

    jl("Write a complete example of changing FPS at runtime.",
       """```js
// Switch to 30 FPS for battery saving mode
cc.director.setAnimationInterval(1 / 30);

// Back to 60 FPS for smooth gameplay
cc.director.setAnimationInterval(1 / 60);

// Show FPS counter for debugging
cc.director.setDisplayStats(true);
```"""),

    jl("Write a complete example of using cc.loader to load resources asynchronously.",
       """```js
// Load multiple resources before starting the game
cc.loader.load(
    ['res/level1.json', 'res/level1_bg.png', 'res/level1_tiles.png'],
    function(err) {
        if (err) {
            cc.error('Failed to load resources:', err);
            return;
        }
        var levelData = cc.loader.getRes('res/level1.json');
        cc.log('Level loaded:', levelData.name);
        startLevel(levelData);
    }
);
```"""),
]

# --- Schedulers (module: node scheduling + director scheduler) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of using scheduleUpdate for a game loop.",
       """```js
// Use scheduleUpdate for per-frame game logic
var GameLayer = cc.Layer.extend({
    _hero: null,
    _speed: 150,
    ctor: function() {
        this._super();
        this._hero = new cc.Sprite('res/hero.png');
        this._hero.setPosition(240, 160);
        this.addChild(this._hero);
        this.scheduleUpdate();
    },
    update: function(dt) {
        // Move hero to the right every frame
        this._hero.x += this._speed * dt;
        // Wrap around screen
        if (this._hero.x > 480) {
            this._hero.x = 0;
        }
    }
});
```"""),

    jl("Write a complete example of scheduling a callback at a fixed interval.",
       """```js
// Spawn an enemy every 3 seconds
var GameLayer = cc.Layer.extend({
    onEnter: function() {
        this._super();
        this.schedule(this.spawnEnemy, 3.0);
    },
    spawnEnemy: function(dt) {
        var enemy = new cc.Sprite('res/enemy.png');
        var y = Math.random() * 320;
        enemy.setPosition(480, y);
        this.addChild(enemy);
        enemy.runAction(cc.sequence(
            cc.moveTo(4.0, cc.p(-50, y)),
            cc.removeSelf()
        ));
    }
});
```"""),

    jl("Write a complete example of scheduleOnce for a delayed callback.",
       """```js
// Show a tutorial popup after 5 seconds
this.scheduleOnce(function() {
    var popup = new cc.Sprite('res/tutorial.png');
    popup.setPosition(240, 160);
    popup.setOpacity(0);
    this.addChild(popup);
    popup.runAction(cc.fadeIn(0.5));
}, 5.0);
```"""),

    jl("Write a complete example of using setTimeScale for slow motion.",
       """```js
// Slow motion effect when boss is defeated
function startSlowMotion() {
    cc.director.getScheduler().setTimeScale(0.3);
    // Return to normal after 2 real seconds (2 / 0.3 game seconds)
}

function endSlowMotion() {
    cc.director.getScheduler().setTimeScale(1.0);
}
```"""),

    jl("Write a complete example of scheduling with repeat count and initial delay.",
       """```js
// Flash a warning 5 times, starting after 1 second delay
var warning = cc.Label.createWithSystemFont('WARNING!', 'Arial', 36);
warning.setPosition(240, 300);
warning.setTextColor(cc.color(255, 0, 0));
this.addChild(warning);

var count = 0;
this.schedule(function() {
    warning.setVisible(!warning.isVisible());
    count++;
}, 0.3, 10, 1.0); // interval=0.3s, repeat=10 times, delay=1s
```"""),

    jl("Write a complete example of unscheduling a callback.",
       """```js
// Start and stop a repeating timer
var GameLayer = cc.Layer.extend({
    _timerKey: 'myTimer',
    startTimer: function() {
        this.schedule(this.onTick, 1.0, cc.REPEAT_FOREVER, 0, this._timerKey);
    },
    stopTimer: function() {
        this.unschedule(this.onTick);
    },
    onTick: function(dt) {
        cc.log('Tick!');
    }
});
```"""),

    jl("Write a complete example of pausing and resuming a specific node's scheduler.",
       """```js
// Pause a specific node (freezes its actions and scheduled callbacks)
var enemy = new cc.Sprite('res/enemy.png');
enemy.setPosition(200, 200);
this.addChild(enemy);

// Give it a patrol action
enemy.runAction(cc.repeatForever(cc.sequence(
    cc.moveBy(1.0, cc.p(100, 0)),
    cc.moveBy(1.0, cc.p(-100, 0))
)));

// Freeze this enemy
enemy.pause();

// Unfreeze later
enemy.resume();
```"""),
]

# --- Particle effects (module: not separate doc but uses cc.Node + actions) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of creating a particle fire effect using cc.ParticleFire.",
       """```js
// Create a fire particle effect
var fire = new cc.ParticleFire();
fire.setPosition(240, 100);
fire.setTexture(cc.textureCache.addImage('res/particle_fire.png'));
this.addChild(fire, 10);
```"""),

    jl("Write a complete example of creating a particle system from a plist file.",
       """```js
// Load a custom particle effect from a plist
var particles = new cc.ParticleSystem('res/particles/explosion.plist');
particles.setPosition(240, 160);
particles.setAutoRemoveOnFinish(true);
this.addChild(particles, 10);
```"""),

    jl("Write a complete example of creating a snow particle effect.",
       """```js
// Create a snow particle effect
var snow = new cc.ParticleSnow();
snow.setPosition(240, 480);
snow.setTexture(cc.textureCache.addImage('res/particle_snow.png'));
snow.setLife(5);
snow.setSpeed(30);
this.addChild(snow, 10);
```"""),

    jl("Write a complete example of a one-shot explosion particle that auto-removes.",
       """```js
// One-shot explosion at a position
function playExplosion(parent, x, y) {
    var explosion = new cc.ParticleExplosion();
    explosion.setPosition(x, y);
    explosion.setTexture(cc.textureCache.addImage('res/particle_spark.png'));
    explosion.setAutoRemoveOnFinish(true);
    explosion.setDuration(0.1);
    parent.addChild(explosion, 10);
}
```"""),

    jl("Write a complete example of creating a custom particle system with specific properties.",
       """```js
// Custom sparkle particle system
var sparkle = new cc.ParticleSystem(50); // max 50 particles
sparkle.setTexture(cc.textureCache.addImage('res/particle_star.png'));
sparkle.setDuration(-1); // infinite
sparkle.setEmitterMode(cc.ParticleSystem.MODE_GRAVITY);
sparkle.setGravity(cc.p(0, -50));
sparkle.setLife(1.5);
sparkle.setLifeVar(0.5);
sparkle.setSpeed(60);
sparkle.setSpeedVar(20);
sparkle.setStartSize(20);
sparkle.setEndSize(5);
sparkle.setStartColor(cc.color(255, 255, 100, 255));
sparkle.setEndColor(cc.color(255, 100, 0, 0));
sparkle.setEmissionRate(30);
sparkle.setPosition(240, 160);
this.addChild(sparkle, 10);
```"""),
]

# --- Spine animations (module: spine) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of loading and playing a Spine animation.",
       """```js
// Load and play a Spine skeleton animation
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
this.addChild(hero);

// Play idle animation looping on track 0
hero.setAnimation(0, 'idle', true);
```"""),

    jl("Write a complete example of queueing Spine animations.",
       """```js
// Play attack once, then return to idle
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
this.addChild(hero);

hero.setAnimation(0, 'attack', false);
hero.addAnimation(0, 'idle', true, 0); // queue idle after attack
```"""),

    jl("Write a complete example of setting up Spine animation blending (mix).",
       """```js
// Set up smooth transitions between animations
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
this.addChild(hero);

// Define blend durations between animation pairs
hero.setMix('idle', 'walk', 0.2);
hero.setMix('walk', 'run', 0.3);
hero.setMix('run', 'idle', 0.2);
hero.setMix('idle', 'attack', 0.1);
hero.setMix('attack', 'idle', 0.2);

hero.setAnimation(0, 'idle', true);
```"""),

    jl("Write a complete example of listening for Spine animation events.",
       """```js
// Listen for animation complete and frame events
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
this.addChild(hero);

hero.setAnimationListener(this, function(track, type, event) {
    if (type === sp.AnimationEventType.COMPLETE) {
        cc.log('Animation finished:', track.animation.name);
    }
    if (type === sp.AnimationEventType.EVENT) {
        // Frame event defined in Spine editor
        if (event.data.name === 'footstep') {
            cc.audioEngine.playEffect('res/sfx_step.mp3');
        }
    }
});

hero.setAnimation(0, 'walk', true);
```"""),

    jl("Write a complete example of switching Spine skins at runtime.",
       """```js
// Switch character skin/costume
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
this.addChild(hero);
hero.setAnimation(0, 'idle', true);

// Switch to warrior skin
hero.setSkin('warrior');

// Switch to mage skin
hero.setSkin('mage');
```"""),

    jl("Write a complete example of using Spine animation with multiple tracks.",
       """```js
// Use multiple tracks: body on track 0, face on track 1
var character = new sp.SkeletonAnimation('res/char/char.json', 'res/char/char.atlas');
character.setPosition(240, 80);
this.addChild(character);

// Base body animation on track 0
character.setAnimation(0, 'walk', true);

// Overlay blink animation on track 1
character.setAnimation(1, 'blink', true);
```"""),

    jl("Write a complete example of controlling Spine animation speed.",
       """```js
// Slow down or speed up a Spine animation
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
this.addChild(hero);
hero.setAnimation(0, 'run', true);

// Half speed (slow motion)
hero.setTimeScale(0.5);

// Double speed
hero.setTimeScale(2.0);

// Normal speed
hero.setTimeScale(1.0);
```"""),

    jl("Write a complete example of showing/hiding a Spine attachment.",
       """```js
// Show and hide weapon in a Spine skeleton
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
this.addChild(hero);
hero.setAnimation(0, 'idle', true);

// Equip sword
hero.setAttachment('weapon_slot', 'sword');

// Unequip (hide weapon)
hero.setAttachment('weapon_slot', null);
```"""),
]

# --- Draw nodes (module: drawnode) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of drawing basic shapes with cc.DrawNode.",
       """```js
// Draw various shapes with DrawNode
var draw = new cc.DrawNode();
this.addChild(draw);

// Red dot
draw.drawDot(cc.p(100, 100), 10, cc.color(255, 0, 0, 255));

// Blue line
draw.drawSegment(cc.p(50, 200), cc.p(200, 200), 2, cc.color(0, 0, 255, 255));

// Green filled rectangle
draw.drawRect(
    cc.p(250, 50), cc.p(400, 150),
    cc.color(0, 200, 0, 128),
    2,
    cc.color(0, 255, 0, 255)
);
```"""),

    jl("Write a complete example of drawing a circle with cc.DrawNode.",
       """```js
// Draw a yellow hollow circle
var draw = new cc.DrawNode();
this.addChild(draw);

draw.drawCircle(
    cc.p(240, 160),  // center
    80,              // radius
    0,               // angle
    36,              // segments (smoothness)
    false,           // don't draw line to center
    2,               // line width
    cc.color(255, 255, 0, 255)
);
```"""),

    jl("Write a complete example of drawing a filled polygon with cc.DrawNode.",
       """```js
// Draw a filled triangle with a border
var draw = new cc.DrawNode();
this.addChild(draw);

var vertices = [
    cc.p(240, 300),  // top
    cc.p(140, 100),  // bottom-left
    cc.p(340, 100)   // bottom-right
];
draw.drawPoly(
    vertices,
    cc.color(100, 0, 200, 150),  // fill color
    2,                            // border width
    cc.color(200, 0, 255, 255)   // border color
);
```"""),

    jl("Write a complete example of drawing a bezier curve with cc.DrawNode.",
       """```js
// Draw a smooth cubic bezier curve
var draw = new cc.DrawNode();
this.addChild(draw);

draw.drawCubicBezier(
    cc.p(50, 100),    // start
    cc.p(150, 350),   // control 1
    cc.p(300, 50),    // control 2
    cc.p(430, 200),   // end
    40,                // segments
    2,                 // line width
    cc.color(255, 128, 0, 255)
);
```"""),

    jl("Write a complete example of using DrawNode to draw a debug bounding box that updates each frame.",
       """```js
// Debug: draw bounding box around a moving sprite each frame
var DebugLayer = cc.Layer.extend({
    _draw: null,
    _target: null,
    onEnter: function() {
        this._super();
        this._draw = new cc.DrawNode();
        this.addChild(this._draw);
        this.scheduleUpdate();
    },
    update: function(dt) {
        this._draw.clear();
        if (!this._target) return;
        var box = this._target.getBoundingBoxToWorld();
        this._draw.drawRect(
            cc.p(box.x, box.y),
            cc.p(box.x + box.width, box.y + box.height),
            null,
            1,
            cc.color(255, 0, 0, 255)
        );
    }
});
```"""),

    jl("Write a complete example of drawing a grid with cc.DrawNode.",
       """```js
// Draw a 10x10 grid
var draw = new cc.DrawNode();
this.addChild(draw);

var cellSize = 32;
var rows = 10;
var cols = 10;
var lineColor = cc.color(100, 100, 100, 128);

for (var r = 0; r <= rows; r++) {
    var y = r * cellSize;
    draw.drawSegment(cc.p(0, y), cc.p(cols * cellSize, y), 1, lineColor);
}
for (var c = 0; c <= cols; c++) {
    var x = c * cellSize;
    draw.drawSegment(cc.p(x, 0), cc.p(x, rows * cellSize), 1, lineColor);
}
```"""),
]

# --- Labels (module: label) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of creating a system font label.",
       """```js
// Create a centered system font label
var label = cc.Label.createWithSystemFont('Hello World', 'Arial', 36);
var winSize = cc.director.getWinSize();
label.setPosition(winSize.width / 2, winSize.height / 2);
this.addChild(label);
```"""),

    jl("Write a complete example of creating a BMFont label.",
       """```js
// Create a bitmap font label for the score display
var scoreLabel = cc.Label.createWithBMFont('res/fonts/score.fnt', '0000');
scoreLabel.setPosition(240, 440);
scoreLabel.setHorizontalAlignment(cc.TEXT_ALIGNMENT_RIGHT);
this.addChild(scoreLabel);

// Update score
scoreLabel.setString('1500');
```"""),

    jl("Write a complete example of a label with outline and shadow effects.",
       """```js
// Styled label with outline and shadow
var label = cc.Label.createWithSystemFont('GAME OVER', 'Impact', 48);
label.setPosition(240, 240);
label.setTextColor(cc.color(255, 50, 50));
label.enableOutline(cc.color(0, 0, 0, 255), 3);
label.enableShadow(cc.color(0, 0, 0, 128), cc.size(3, -3), 0);
this.addChild(label);
```"""),

    jl("Write a complete example of creating a TTF label.",
       """```js
// Create a label with a custom TTF font
var config = { fontFilePath: 'res/fonts/custom.ttf', fontSize: 28 };
var label = cc.Label.createWithTTF(config, 'Custom Font!');
label.setPosition(240, 200);
label.setTextColor(cc.color(255, 220, 100));
this.addChild(label);
```"""),

    jl("Write a complete example of a multi-line label with word wrapping.",
       """```js
// Multi-line label with fixed width and center alignment
var desc = cc.Label.createWithSystemFont(
    'This is a long description that should wrap to multiple lines automatically.',
    'Arial', 18
);
desc.setPosition(240, 200);
desc.setDimensions(300, 0); // width=300, height auto
desc.setHorizontalAlignment(cc.TEXT_ALIGNMENT_CENTER);
this.addChild(desc);
```"""),

    jl("Write a complete example of animating individual letters in a label.",
       """```js
// Animate each letter with a wave effect
var label = cc.Label.createWithBMFont('res/fonts/game.fnt', 'READY!');
label.setPosition(240, 240);
this.addChild(label);

for (var i = 0; i < label.getStringLength(); i++) {
    var letter = label.getLetter(i);
    if (letter) {
        letter.runAction(cc.sequence(
            cc.delayTime(i * 0.1),
            cc.moveBy(0.2, cc.p(0, 20)),
            cc.moveBy(0.2, cc.p(0, -20))
        ));
    }
}
```"""),
]

# --- Layer (module: layer) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of creating a LayerColor as a dark overlay.",
       """```js
// Dark semi-transparent overlay for pause screen
var overlay = new cc.LayerColor(cc.color(0, 0, 0, 180));
overlay.setContentSize(cc.director.getWinSize());
this.addChild(overlay, 100);
```"""),

    jl("Write a complete example of a LayerGradient background.",
       """```js
// Sky gradient background (blue to dark)
var sky = new cc.LayerGradient(
    cc.color(100, 180, 255, 255),  // top: light blue
    cc.color(10, 20, 60, 255),     // bottom: dark blue
    cc.p(0, -1)                    // direction: top to bottom
);
this.addChild(sky, -1);
```"""),

    jl("Write a complete example of cc.LayerMultiplex for switching between sub-layers.",
       """```js
// Switch between menu and settings layers
var menuLayer = new MenuLayer();
var settingsLayer = new SettingsLayer();

var multiplex = new cc.LayerMultiplex(menuLayer, settingsLayer);
this.addChild(multiplex);

// Show settings:
multiplex.switchTo(1);
// Back to menu:
multiplex.switchTo(0);
```"""),

    jl("Write a complete example of a custom Layer subclass with initialization.",
       """```js
// Custom game layer with proper initialization
var GameLayer = cc.Layer.extend({
    _score: 0,
    _scoreLabel: null,
    ctor: function() {
        this._super();
        // Background
        var bg = new cc.Sprite('res/bg.png');
        bg.setPosition(240, 160);
        this.addChild(bg, -1);
        // Score label
        this._scoreLabel = cc.Label.createWithSystemFont('Score: 0', 'Arial', 24);
        this._scoreLabel.setPosition(240, 440);
        this.addChild(this._scoreLabel, 10);
    },
    addScore: function(pts) {
        this._score += pts;
        this._scoreLabel.setString('Score: ' + this._score);
    }
});
```"""),
]

# --- Node (module: node) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of using node.attr() to set multiple properties at once.",
       """```js
// Set multiple node properties in one call
var sprite = new cc.Sprite('res/hero.png');
sprite.attr({
    x: 240,
    y: 160,
    scale: 1.5,
    opacity: 200,
    rotation: 15
});
this.addChild(sprite);
```"""),

    jl("Write a complete example of coordinate conversion from world to node space.",
       """```js
// Convert a world-space touch position to node-local coordinates
var panel = new cc.Sprite('res/panel.png');
panel.setPosition(200, 200);
this.addChild(panel);

cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    swallowTouches: true,
    onTouchBegan: function(touch, event) {
        var worldPos = touch.getLocation();
        var localPos = panel.convertToNodeSpace(worldPos);
        cc.log('Local position:', localPos.x, localPos.y);
        return true;
    }
}, this);
```"""),

    jl("Write a complete example of managing child z-order for layering.",
       """```js
// Manage draw order with z-index
var background = new cc.Sprite('res/bg.png');
background.setPosition(240, 160);
this.addChild(background, -1); // behind everything

var hero = new cc.Sprite('res/hero.png');
hero.setPosition(240, 160);
this.addChild(hero, 1); // normal layer

var hud = cc.Label.createWithSystemFont('HP: 100', 'Arial', 18);
hud.setPosition(50, 440);
this.addChild(hud, 10); // always on top
```"""),

    jl("Write a complete example of finding and removing children by tag and name.",
       """```js
// Add children with tags and names, then find/remove them
var enemy1 = new cc.Sprite('res/enemy.png');
enemy1.setTag(100);
enemy1.setName('enemy_goblin');
enemy1.setPosition(100, 200);
this.addChild(enemy1);

var enemy2 = new cc.Sprite('res/enemy.png');
enemy2.setTag(101);
enemy2.setPosition(300, 200);
this.addChild(enemy2);

// Find by tag
var found = this.getChildByTag(100);
cc.log('Found:', found.getName()); // 'enemy_goblin'

// Find by name
var goblin = this.getChildByName('enemy_goblin');

// Remove by tag
this.removeChildByTag(101, true);
```"""),

    jl("Write a complete example of using setNormalizedPosition for responsive layout.",
       """```js
// Position nodes relative to parent size (0-1 range)
var topRight = new cc.Sprite('res/icon_settings.png');
topRight.setNormalizedPosition(cc.p(0.95, 0.95)); // top-right corner
this.addChild(topRight);

var bottomLeft = new cc.Sprite('res/icon_back.png');
bottomLeft.setNormalizedPosition(cc.p(0.05, 0.05)); // bottom-left corner
this.addChild(bottomLeft);

var center = new cc.Sprite('res/logo.png');
center.setNormalizedPosition(cc.p(0.5, 0.5)); // exact center
this.addChild(center);
```"""),

    jl("Write a complete example of using cascadeOpacity to fade a parent and all children.",
       """```js
// Fade a container and all its children together
var container = new cc.Node();
container.setPosition(240, 160);
container.setCascadeOpacityEnabled(true);
this.addChild(container);

var bg = new cc.Sprite('res/dialog_bg.png');
container.addChild(bg);

var title = cc.Label.createWithSystemFont('Title', 'Arial', 24);
title.setPosition(0, 50);
container.addChild(title);

// Fading container fades all children too
container.runAction(cc.sequence(
    cc.fadeIn(0.3),
    cc.delayTime(2.0),
    cc.fadeOut(0.3)
));
```"""),
]

# --- CCS Armature (module: ccs) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of loading and playing a CocosStudio armature animation.",
       """```js
// Load and play a CocosStudio armature animation
ccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson');

var armature = ccs.Armature.create('hero');
armature.setPosition(240, 160);
this.addChild(armature);

// Play 'run' animation, loop forever
armature.animation.play('run', -1, -1);
```"""),

    jl("Write a complete example of listening for CocosStudio armature animation events.",
       """```js
// Listen for animation complete events on an armature
ccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson');
var armature = ccs.Armature.create('hero');
armature.setPosition(240, 160);
this.addChild(armature);

armature.animation.setMovementEventCallFunc(function(arm, type, id) {
    if (type === ccs.MovementEventType.COMPLETE) {
        cc.log('Animation complete:', id);
        // Return to idle after attack
        if (id === 'attack') {
            armature.animation.play('idle', 5, -1);
        }
    }
});

armature.animation.play('attack', -1, 0); // play once
```"""),

    jl("Write a complete example of using ccs.ActionTimeline to play a CocosStudio timeline animation.",
       """```js
// Load and play a CocosStudio .csb animation
var timeline = ccs.actionManager.loadAnimationActionWithFile('res/ui/intro.csb');
var node = new cc.Node();
this.addChild(node);

node.runAction(timeline);
timeline.gotoFrameAndPlay(0, true); // start from frame 0, loop
```"""),

    jl("Write a complete example of accessing a bone in a CocosStudio armature.",
       """```js
// Access a specific bone and attach a visual to it
ccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson');
var armature = ccs.Armature.create('hero');
armature.setPosition(240, 160);
this.addChild(armature);
armature.animation.play('idle', -1, -1);

// Get the hand bone
var handBone = armature.getBone('hand_r');
if (handBone) {
    cc.log('Found hand bone at:', handBone.getWorldPosition().x);
}
```"""),

    jl("Write a complete example of setting animation speed on a CocosStudio armature.",
       """```js
// Control armature animation playback speed
ccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson');
var armature = ccs.Armature.create('hero');
armature.setPosition(240, 160);
this.addChild(armature);

armature.animation.play('run', -1, -1);
// Speed up to 1.5x
armature.animation.setSpeedScale(1.5);
// Slow down to half speed
armature.animation.setSpeedScale(0.5);
```"""),

    jl("Write a complete example of listening for frame events in a CocosStudio armature.",
       """```js
// React to frame events defined in CocosStudio editor
ccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson');
var armature = ccs.Armature.create('hero');
armature.setPosition(240, 160);
this.addChild(armature);

armature.animation.setFrameEventCallFunc(function(bone, eventName, orig, cur) {
    if (eventName === 'footstep') {
        cc.audioEngine.playEffect('res/sfx_step.mp3');
    } else if (eventName === 'attack_hit') {
        cc.log('Damage frame at index:', cur);
    }
});

armature.animation.play('walk', -1, -1);
```"""),
]

# --- Types (module: types) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of using cc.Point math utilities for vector calculations.",
       """```js
// Calculate direction and distance between two nodes
var heroPos = hero.getPosition();
var enemyPos = enemy.getPosition();

var direction = cc.pNormalize(cc.pSub(enemyPos, heroPos));
var distance = cc.pDistance(heroPos, enemyPos);

// Move hero toward enemy
var speed = 100;
hero.x += direction.x * speed * dt;
hero.y += direction.y * speed * dt;

cc.log('Distance to enemy:', distance);
```"""),

    jl("Write a complete example of using cc.Rect utilities for collision detection.",
       """```js
// Simple AABB collision detection between two sprites
function checkCollision(spriteA, spriteB) {
    var boxA = spriteA.getBoundingBox();
    var boxB = spriteB.getBoundingBox();
    return cc.rectOverlapsRect(boxA, boxB);
}

// Usage in update loop:
if (checkCollision(hero, enemy)) {
    cc.log('Collision detected!');
}
```"""),

    jl("Write a complete example of using cc.color utilities including hex conversion.",
       """```js
// Color utilities
var red = cc.color(255, 0, 0, 255);
var fromHex = cc.hexToColor('#FF8800');
var hexStr = cc.colorToHex(cc.color(0, 128, 255));
cc.log('Hex:', hexStr);

// Preset colors
label.setTextColor(cc.color.WHITE);
sprite.setColor(cc.color.YELLOW);
```"""),

    jl("Write a complete example of using cc.lerp and cc.clampf for value interpolation.",
       """```js
// Smoothly interpolate a value using lerp
var current = 0;
var target = 100;
// Each frame, move 10% closer to target
current = cc.lerp(current, target, 0.1);

// Clamp health between 0 and maxHP
var hp = 120;
var maxHP = 100;
hp = cc.clampf(hp, 0, maxHP); // result: 100
```"""),

    jl("Write a complete example of additive blending for a glow effect.",
       """```js
// Additive blend for a glow/light effect
var glow = new cc.Sprite('res/glow.png');
glow.setPosition(240, 160);
glow.setBlendFunc(new cc.BlendFunc(cc.ONE, cc.ONE));
this.addChild(glow, 5);
```"""),
]

# --- Sys / platform (module: sys) ---
COMPLETE_SNIPPETS += [
    jl("Write a complete example of saving and loading game data with cc.sys.localStorage.",
       """```js
// Save player progress to local storage
function saveProgress(data) {
    var json = JSON.stringify(data);
    cc.sys.localStorage.setItem('playerProgress', json);
}

// Load player progress
function loadProgress() {
    var raw = cc.sys.localStorage.getItem('playerProgress');
    if (raw) {
        return JSON.parse(raw);
    }
    return { level: 1, score: 0, coins: 0 };
}

// Usage
var progress = loadProgress();
progress.score += 100;
saveProgress(progress);
```"""),

    jl("Write a complete example of platform detection for cross-platform code.",
       """```js
// Adjust behavior based on platform
if (cc.sys.isNative) {
    cc.log('Running on native (iOS/Android/Desktop)');
} else {
    cc.log('Running in browser');
}

if (cc.sys.isMobile) {
    // Enable touch controls
    cc.log('Mobile device detected');
} else {
    // Enable keyboard controls
    cc.log('Desktop detected');
}

if (cc.sys.platform === cc.sys.ANDROID) {
    cc.log('Android specific setup');
} else if (cc.sys.os === cc.sys.OS_IOS) {
    cc.log('iOS specific setup');
}
```"""),

    jl("Write a complete example of opening a URL from the game.",
       """```js
// Open external URL (e.g., rate the app)
function openRateDialog() {
    if (cc.sys.os === cc.sys.OS_IOS) {
        cc.sys.openURL('https://apps.apple.com/app/id123456');
    } else if (cc.sys.os === cc.sys.OS_ANDROID) {
        cc.sys.openURL('https://play.google.com/store/apps/details?id=com.mygame');
    } else {
        cc.sys.openURL('https://mygame.com');
    }
}
```"""),

    jl("Write a complete example of using cc.path for path manipulation.",
       """```js
// Path utility examples
var fullPath = cc.path.join('res', 'sprites', 'hero.png');
cc.log(fullPath); // 'res/sprites/hero.png'

var ext = cc.path.extname('hero.png');
cc.log(ext); // '.png'

var name = cc.path.basename('res/sprites/hero.png', '.png');
cc.log(name); // 'hero'

var dir = cc.path.dirname('res/sprites/hero.png');
cc.log(dir); // 'res/sprites'
```"""),

    jl("Write a complete example of detecting system language for localization.",
       """```js
// Load the correct language file based on system language
function getLocaleFile() {
    var lang = cc.sys.language;
    if (lang === cc.sys.LANGUAGE_CHINESE) {
        return 'res/i18n/zh.json';
    } else if (lang === cc.sys.LANGUAGE_JAPANESE) {
        return 'res/i18n/ja.json';
    } else if (lang === cc.sys.LANGUAGE_KOREAN) {
        return 'res/i18n/ko.json';
    }
    return 'res/i18n/en.json'; // default English
}

cc.loader.loadJson(getLocaleFile(), function(err, strings) {
    if (!err) {
        cc.log('Loaded locale:', strings);
    }
});
```"""),

    jl("Write a complete example of saving high score with local storage.",
       """```js
// Save and retrieve high score
function getHighScore() {
    var val = cc.sys.localStorage.getItem('highscore');
    return val ? parseInt(val) : 0;
}

function setHighScoreIfBetter(score) {
    var current = getHighScore();
    if (score > current) {
        cc.sys.localStorage.setItem('highscore', score.toString());
        cc.log('New high score:', score);
        return true;
    }
    return false;
}
```"""),
]

# Now let's add more to reach ~800 complete snippets with additional variations

# More complete snippet variations (mixed modules)
COMPLETE_SNIPPETS += [
    # More sprites
    jl("Write a complete example of setting a sprite's anchor point to the bottom-left corner.",
       """```js
// Set anchor to bottom-left so position refers to that corner
var sprite = new cc.Sprite('res/tile.png');
sprite.setAnchorPoint(cc.p(0, 0));
sprite.setPosition(0, 0); // tile starts at origin
this.addChild(sprite);
```"""),

    # More actions
    jl("Write a complete example of a shake effect using cc.moveBy.",
       """```js
// Screen shake effect
function shakeNode(node, intensity, duration) {
    var shakes = [];
    var steps = Math.floor(duration / 0.05);
    for (var i = 0; i < steps; i++) {
        var dx = (Math.random() - 0.5) * intensity * 2;
        var dy = (Math.random() - 0.5) * intensity * 2;
        shakes.push(cc.moveTo(0.05, cc.p(node.x + dx, node.y + dy)));
    }
    shakes.push(cc.moveTo(0.05, cc.p(node.x, node.y)));
    node.runAction(cc.sequence(shakes));
}

// Usage: shake with intensity 5 for 0.5 seconds
shakeNode(this, 5, 0.5);
```"""),

    jl("Write a complete example of a typewriter text reveal effect.",
       """```js
// Typewriter effect: reveal text one character at a time
var fullText = 'Hello, welcome to the game!';
var label = cc.Label.createWithSystemFont('', 'Arial', 20);
label.setPosition(240, 200);
label.setAnchorPoint(cc.p(0.5, 0.5));
this.addChild(label);

var charIndex = 0;
this.schedule(function() {
    charIndex++;
    label.setString(fullText.substring(0, charIndex));
    if (charIndex >= fullText.length) {
        this.unschedule(arguments.callee);
    }
}, 0.05);
```"""),

    jl("Write a complete example of using cc.actionTween to animate a custom property.",
       """```js
// Animate a custom numeric property with actionTween
var myNode = new cc.Node();
myNode.customValue = 0;
myNode.updateTweenAction = function(value, key) {
    if (key === 'customValue') {
        this.customValue = value;
        cc.log('Custom value:', value);
    }
};
this.addChild(myNode);

myNode.runAction(cc.actionTween(2.0, 'customValue', 0, 100));
```"""),

    jl("Write a complete example of a floating animation for a UI element.",
       """```js
// Floating animation: gently bob up and down
var icon = new cc.Sprite('res/floating_gem.png');
icon.setPosition(240, 200);
this.addChild(icon);

icon.runAction(cc.repeatForever(cc.sequence(
    cc.moveBy(1.0, cc.p(0, 15)).easing(cc.easeSineInOut()),
    cc.moveBy(1.0, cc.p(0, -15)).easing(cc.easeSineInOut())
)));
```"""),

    jl("Write a complete example of a coin collect animation (fly to HUD).",
       """```js
// Coin flies from pickup position to the HUD coin counter
function playCoinCollect(parent, startX, startY, hudX, hudY) {
    var coin = new cc.Sprite('res/coin.png');
    coin.setPosition(startX, startY);
    parent.addChild(coin, 10);

    coin.runAction(cc.sequence(
        cc.spawn(
            cc.moveTo(0.6, cc.p(hudX, hudY)).easing(cc.easeIn(2.0)),
            cc.scaleTo(0.6, 0.3),
            cc.fadeOut(0.6)
        ),
        cc.removeSelf()
    ));
    cc.audioEngine.playEffect('res/sfx_coin.mp3');
}
```"""),

    jl("Write a complete example of a button press animation with scale.",
       """```js
// Button with press-down and release animation
var btn = new ccui.Button('res/btn_normal.png', 'res/btn_pressed.png');
btn.setPosition(240, 160);
btn.setTitleText('TAP ME');
btn.setTitleFontSize(20);
btn.addTouchEventListener(function(sender, type) {
    if (type === ccui.Widget.TOUCH_BEGAN) {
        sender.runAction(cc.scaleTo(0.05, 0.9));
    } else if (type === ccui.Widget.TOUCH_ENDED) {
        sender.runAction(cc.scaleTo(0.1, 1.0).easing(cc.easeBackOut()));
        cc.log('Button clicked!');
    } else if (type === ccui.Widget.TOUCH_CANCELED) {
        sender.runAction(cc.scaleTo(0.1, 1.0));
    }
}, this);
this.addChild(btn);
```"""),

    # More draw node
    jl("Write a complete example of drawing multiple dots as a dotted line.",
       """```js
// Draw a dotted line using dots
var draw = new cc.DrawNode();
this.addChild(draw);

var start = cc.p(50, 200);
var end = cc.p(400, 200);
var dotSpacing = 10;
var dir = cc.pNormalize(cc.pSub(end, start));
var totalDist = cc.pDistance(start, end);

for (var d = 0; d < totalDist; d += dotSpacing) {
    var pt = cc.pAdd(start, cc.pMult(dir, d));
    draw.drawDot(pt, 2, cc.color(200, 200, 200, 255));
}
```"""),

    # More audio
    jl("Write a complete example of playing different sound effects for game events.",
       """```js
// Play appropriate sound effects for different game events
function onPlayerJump() {
    cc.audioEngine.playEffect('res/audio/sfx_jump.mp3');
}

function onCoinCollected() {
    cc.audioEngine.playEffect('res/audio/sfx_coin.mp3');
}

function onEnemyHit() {
    cc.audioEngine.playEffect('res/audio/sfx_hit.mp3');
}

function onGameOver() {
    cc.audioEngine.stopMusic();
    cc.audioEngine.playEffect('res/audio/sfx_gameover.mp3');
}
```"""),

    # More scene
    jl("Write a complete example of popToRootScene to return to the main menu.",
       """```js
// Return to the main menu from any nested scene
function goToMainMenu() {
    cc.director.popToRootScene();
}
```"""),

    # More schedulers
    jl("Write a complete example of a countdown timer using schedule.",
       """```js
// Countdown timer from 60 to 0
var GameLayer = cc.Layer.extend({
    _timeLeft: 60,
    _timerLabel: null,
    ctor: function() {
        this._super();
        this._timerLabel = cc.Label.createWithSystemFont('60', 'Arial', 36);
        this._timerLabel.setPosition(240, 440);
        this.addChild(this._timerLabel);
        this.schedule(this.onTimerTick, 1.0);
    },
    onTimerTick: function() {
        this._timeLeft--;
        this._timerLabel.setString('' + this._timeLeft);
        if (this._timeLeft <= 0) {
            this.unschedule(this.onTimerTick);
            this.onTimeUp();
        }
    },
    onTimeUp: function() {
        cc.log('Time is up!');
    }
});
```"""),

    # More labels
    jl("Write a complete example of creating a char map label for a number display.",
       """```js
// Char map label for displaying numbers (like arcade style)
var numLabel = cc.Label.createWithCharMap('res/fonts/numbers.png', 24, 32, 48);
// 48 = ASCII code for '0'
numLabel.setPosition(240, 400);
numLabel.setString('12345');
this.addChild(numLabel);
```"""),

    # More layers
    jl("Write a complete example of a dialog overlay using LayerColor and UI widgets.",
       """```js
// Modal dialog with dark overlay
var overlay = new cc.LayerColor(cc.color(0, 0, 0, 150));
this.addChild(overlay, 100);

var dialog = new ccui.Layout();
dialog.setSize(cc.size(300, 200));
dialog.setBackGroundColorType(ccui.Layout.BG_COLOR_SOLID);
dialog.setBackGroundColor(cc.color(50, 50, 70));
dialog.setBackGroundColorOpacity(230);
var winSize = cc.director.getWinSize();
dialog.setPosition(winSize.width / 2 - 150, winSize.height / 2 - 100);
overlay.addChild(dialog);

var title = new ccui.Text('Are you sure?', 'Arial', 24);
title.setPosition(150, 150);
dialog.addChild(title);

var yesBtn = new ccui.Button('res/btn_yes.png');
yesBtn.setPosition(100, 50);
yesBtn.addClickEventListener(function() {
    overlay.removeFromParent();
});
dialog.addChild(yesBtn);
```"""),

    # More node
    jl("Write a complete example of enumerateChildren to find all enemies.",
       """```js
// Find all children whose name starts with 'enemy'
this.enumerateChildren('enemy.*', function(node) {
    cc.log('Found enemy:', node.getName(), 'at', node.x, node.y);
    return false; // return false to continue searching
});
```"""),

    # More types
    jl("Write a complete example of using cc.pRotateByAngle for circular movement.",
       """```js
// Rotate a point around a center to create circular motion
var center = cc.p(240, 160);
var radius = 100;
var angle = 0;
var satellite = new cc.Sprite('res/planet.png');
this.addChild(satellite);

this.schedule(function(dt) {
    angle += dt * 2; // radians per second
    var offset = cc.p(radius, 0);
    var rotated = cc.pRotateByAngle(offset, cc.p(0, 0), angle);
    satellite.setPosition(center.x + rotated.x, center.y + rotated.y);
}, 0);
```"""),

    jl("Write a complete example of using cc.pLerp for smooth following.",
       """```js
// Smoothly follow the touch position
var follower = new cc.Sprite('res/cursor.png');
follower.setPosition(240, 160);
this.addChild(follower);

var targetPos = cc.p(240, 160);

cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    onTouchBegan: function(touch) {
        targetPos = touch.getLocation();
        return true;
    },
    onTouchMoved: function(touch) {
        targetPos = touch.getLocation();
    }
}, this);

this.schedule(function(dt) {
    var current = follower.getPosition();
    var smoothed = cc.pLerp(current, targetPos, 0.1);
    follower.setPosition(smoothed);
}, 0);
```"""),

    # More mixed examples to fill to ~160 per module
    jl("Write a complete example of a sprite with additive blending for a laser beam.",
       """```js
// Laser beam with additive blending
var laser = new cc.Sprite('res/laser.png');
laser.setPosition(240, 160);
laser.setBlendFunc(new cc.BlendFunc(cc.SRC_ALPHA, cc.ONE));
laser.setScaleX(5.0);
this.addChild(laser, 5);

// Pulse the laser
laser.runAction(cc.repeatForever(cc.sequence(
    cc.fadeTo(0.1, 255),
    cc.fadeTo(0.1, 150)
)));
```"""),

    jl("Write a complete example of removing unused textures to free memory.",
       """```js
// Clean up unused textures when transitioning scenes
function cleanupResources() {
    cc.spriteFrameCache.removeUnusedSpriteFrames();
    cc.textureCache.removeUnusedTextures();
    cc.director.purgeCachedData();
    cc.log('Resources cleaned up');
}
```"""),

    jl("Write a complete example of a health bar using DrawNode.",
       """```js
// Dynamic health bar drawn with DrawNode
var maxHP = 100;
var currentHP = 75;
var barWidth = 200;
var barHeight = 20;

var draw = new cc.DrawNode();
draw.setPosition(140, 440);
this.addChild(draw, 10);

function updateHealthBar(hp) {
    draw.clear();
    // Background (dark red)
    draw.drawRect(cc.p(0, 0), cc.p(barWidth, barHeight),
        cc.color(80, 0, 0, 200), 1, cc.color(60, 60, 60, 255));
    // Fill (green to red based on HP)
    var ratio = hp / maxHP;
    var fillW = barWidth * ratio;
    var r = Math.floor(255 * (1 - ratio));
    var g = Math.floor(255 * ratio);
    draw.drawRect(cc.p(0, 0), cc.p(fillW, barHeight),
        cc.color(r, g, 0, 220), 0, cc.color(0, 0, 0, 0));
}

updateHealthBar(currentHP);
```"""),

    jl("Write a complete example of a parallax scrolling background.",
       """```js
// Simple parallax scrolling with two layers
var bg1 = new cc.Sprite('res/bg_far.png');
var bg2 = new cc.Sprite('res/bg_near.png');
bg1.setPosition(240, 160);
bg2.setPosition(240, 160);
this.addChild(bg1, -2);
this.addChild(bg2, -1);

var scrollSpeed = 50;
this.scheduleUpdate();
this.update = function(dt) {
    // Far background scrolls slowly
    bg1.x -= scrollSpeed * 0.3 * dt;
    if (bg1.x < -bg1.width / 2) bg1.x += bg1.width;
    // Near background scrolls faster
    bg2.x -= scrollSpeed * dt;
    if (bg2.x < -bg2.width / 2) bg2.x += bg2.width;
};
```"""),

    jl("Write a complete example of a combo counter with animated text.",
       """```js
// Animated combo counter that pops and fades
function showCombo(parent, count, x, y) {
    var label = cc.Label.createWithSystemFont(count + ' COMBO!', 'Arial', 32);
    label.setPosition(x, y);
    label.setTextColor(cc.color(255, 200, 0));
    label.setScale(0.5);
    parent.addChild(label, 20);

    label.runAction(cc.sequence(
        cc.spawn(
            cc.scaleTo(0.2, 1.2).easing(cc.easeBackOut()),
            cc.moveBy(0.8, cc.p(0, 60)),
            cc.sequence(
                cc.delayTime(0.5),
                cc.fadeOut(0.3)
            )
        ),
        cc.removeSelf()
    ));
}
```"""),

    jl("Write a complete example of using cc.rectContainsPoint for simple tap detection on multiple objects.",
       """```js
// Check which of several targets was tapped
var targets = [];
for (var i = 0; i < 5; i++) {
    var t = new cc.Sprite('res/target.png');
    t.setPosition(80 + i * 80, 200);
    t.setName('target_' + i);
    this.addChild(t);
    targets.push(t);
}

cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    swallowTouches: true,
    onTouchBegan: function(touch) {
        var loc = touch.getLocation();
        for (var i = 0; i < targets.length; i++) {
            var box = targets[i].getBoundingBox();
            if (cc.rectContainsPoint(box, loc)) {
                cc.log('Hit:', targets[i].getName());
                return true;
            }
        }
        return false;
    }
}, this);
```"""),

    jl("Write a complete example of creating a minimap using a scaled-down clone of the game layer.",
       """```js
// Simple minimap: a small DrawNode that shows player position
var mapSize = 80;
var levelWidth = 2000;
var levelHeight = 600;

var minimap = new cc.DrawNode();
minimap.setPosition(380, 400);
this.addChild(minimap, 20);

function updateMinimap(heroX, heroY) {
    minimap.clear();
    // Draw border
    minimap.drawRect(cc.p(0, 0), cc.p(mapSize, mapSize * (levelHeight / levelWidth)),
        cc.color(0, 0, 0, 128), 1, cc.color(255, 255, 255, 200));
    // Draw player dot
    var px = (heroX / levelWidth) * mapSize;
    var py = (heroY / levelHeight) * mapSize * (levelHeight / levelWidth);
    minimap.drawDot(cc.p(px, py), 3, cc.color(0, 255, 0, 255));
}
```"""),

    jl("Write a complete example of creating a sprite that follows a catmull-rom spline path.",
       """```js
// Move a sprite along a smooth catmull-rom path
var sprite = new cc.Sprite('res/bird.png');
sprite.setPosition(50, 200);
this.addChild(sprite);

var waypoints = [
    cc.p(50, 200),
    cc.p(150, 350),
    cc.p(300, 100),
    cc.p(420, 280)
];
sprite.runAction(cc.catmullRomTo(3.0, waypoints));
```"""),

    jl("Write a complete example of a swipe gesture detector.",
       """```js
// Detect swipe direction from touch
var startPos = null;
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    swallowTouches: true,
    onTouchBegan: function(touch) {
        startPos = touch.getLocation();
        return true;
    },
    onTouchEnded: function(touch) {
        var endPos = touch.getLocation();
        var dx = endPos.x - startPos.x;
        var dy = endPos.y - startPos.y;
        var dist = cc.pDistance(startPos, endPos);
        if (dist < 50) return; // too short, not a swipe

        if (Math.abs(dx) > Math.abs(dy)) {
            cc.log(dx > 0 ? 'Swipe RIGHT' : 'Swipe LEFT');
        } else {
            cc.log(dy > 0 ? 'Swipe UP' : 'Swipe DOWN');
        }
    }
}, this);
```"""),

    jl("Write a complete example of object pooling for bullets.",
       """```js
// Simple object pool for bullets to avoid garbage collection
var BulletPool = {
    _pool: [],
    get: function(parent) {
        var bullet;
        if (this._pool.length > 0) {
            bullet = this._pool.pop();
            bullet.setVisible(true);
            bullet.stopAllActions();
        } else {
            bullet = new cc.Sprite('res/bullet.png');
            parent.addChild(bullet, 5);
        }
        return bullet;
    },
    put: function(bullet) {
        bullet.setVisible(false);
        bullet.stopAllActions();
        this._pool.push(bullet);
    }
};

// Usage
var b = BulletPool.get(this);
b.setPosition(hero.x, hero.y);
b.runAction(cc.sequence(
    cc.moveBy(2.0, cc.p(500, 0)),
    cc.callFunc(function() { BulletPool.put(b); })
));
```"""),

    jl("Write a complete example of a damage number popup that floats up and fades.",
       """```js
// Show floating damage number
function showDamage(parent, amount, x, y) {
    var label = cc.Label.createWithSystemFont('-' + amount, 'Arial', 28);
    label.setTextColor(cc.color(255, 50, 50));
    label.setPosition(x, y);
    label.enableOutline(cc.color(0, 0, 0, 200), 2);
    parent.addChild(label, 20);

    label.runAction(cc.sequence(
        cc.spawn(
            cc.moveBy(0.8, cc.p(0, 80)),
            cc.sequence(cc.delayTime(0.4), cc.fadeOut(0.4))
        ),
        cc.removeSelf()
    ));
}
```"""),

    jl("Write a complete example of a screen flash effect.",
       """```js
// White flash effect (e.g., on taking damage)
function screenFlash(parent) {
    var winSize = cc.director.getWinSize();
    var flash = new cc.LayerColor(cc.color(255, 255, 255, 200));
    flash.setContentSize(winSize);
    parent.addChild(flash, 100);

    flash.runAction(cc.sequence(
        cc.fadeOut(0.3),
        cc.removeSelf()
    ));
}
```"""),

    jl("Write a complete example of a scene with loading screen that preloads resources.",
       """```js
// Loading scene with progress bar
var LoadingScene = cc.Scene.extend({
    onEnter: function() {
        this._super();
        var winSize = cc.director.getWinSize();

        var label = cc.Label.createWithSystemFont('Loading...', 'Arial', 24);
        label.setPosition(winSize.width / 2, winSize.height / 2 + 30);
        this.addChild(label);

        var bar = new ccui.LoadingBar('res/loading_bar.png', 0);
        bar.setPosition(winSize.width / 2, winSize.height / 2 - 20);
        this.addChild(bar);

        var resources = ['res/bg.png', 'res/hero.png', 'res/enemy.png'];
        var loaded = 0;
        var self = this;

        cc.loader.load(resources, function(err) {
            loaded++;
            bar.setPercent(Math.floor(loaded / resources.length * 100));
            if (loaded >= resources.length) {
                cc.director.runScene(new GameScene());
            }
        });
    }
});
```"""),

    jl("Write a complete example of a trail effect behind a moving sprite.",
       """```js
// Leave fading trail sprites behind a moving object
function addTrail(parent, sourceSprite) {
    parent.schedule(function() {
        var trail = new cc.Sprite(sourceSprite.getSpriteFrame());
        trail.setPosition(sourceSprite.getPosition());
        trail.setOpacity(150);
        trail.setScale(sourceSprite.getScale());
        parent.addChild(trail, sourceSprite.getLocalZOrder() - 1);

        trail.runAction(cc.sequence(
            cc.spawn(
                cc.fadeOut(0.3),
                cc.scaleTo(0.3, 0.5)
            ),
            cc.removeSelf()
        ));
    }, 0.05);
}
```"""),
]

# Ensure we have enough - add more generic ones
_extra_complete = [
    jl("Write a complete example of a score counter that animates when the score changes.",
       """```js
// Animated score counter with rolling numbers
var ScoreDisplay = cc.Node.extend({
    _label: null,
    _displayScore: 0,
    _targetScore: 0,
    ctor: function() {
        this._super();
        this._label = cc.Label.createWithSystemFont('0', 'Arial', 32);
        this._label.setTextColor(cc.color(255, 220, 0));
        this.addChild(this._label);
        this.scheduleUpdate();
    },
    setScore: function(score) {
        this._targetScore = score;
    },
    update: function(dt) {
        if (this._displayScore < this._targetScore) {
            this._displayScore = Math.min(
                this._displayScore + Math.ceil((this._targetScore - this._displayScore) * 0.1),
                this._targetScore
            );
            this._label.setString('' + this._displayScore);
        }
    }
});
```"""),

    jl("Write a complete example of a simple state machine for character animation.",
       """```js
// Character state machine for animation switching
var STATE_IDLE = 0, STATE_WALK = 1, STATE_ATTACK = 2;

var Character = cc.Node.extend({
    _state: -1,
    _spine: null,
    ctor: function() {
        this._super();
        this._spine = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
        this.addChild(this._spine);
        this._spine.setMix('idle', 'walk', 0.2);
        this._spine.setMix('walk', 'idle', 0.2);
        this._spine.setMix('walk', 'attack', 0.1);
        this._spine.setMix('attack', 'idle', 0.2);
        this.setState(STATE_IDLE);
    },
    setState: function(state) {
        if (this._state === state) return;
        this._state = state;
        var names = ['idle', 'walk', 'attack'];
        var loop = state !== STATE_ATTACK;
        this._spine.setAnimation(0, names[state], loop);
        if (!loop) {
            this._spine.addAnimation(0, 'idle', true, 0);
        }
    }
});
```"""),

    jl("Write a complete example of a tooltip that follows the mouse cursor.",
       """```js
// Tooltip that follows mouse position
var tooltip = cc.Label.createWithSystemFont('Hover info', 'Arial', 14);
tooltip.setTextColor(cc.color(255, 255, 200));
tooltip.setVisible(false);
this.addChild(tooltip, 100);

cc.eventManager.addListener({
    event: cc.EventListener.MOUSE,
    onMouseMove: function(event) {
        var loc = event.getLocation();
        tooltip.setPosition(loc.x + 15, loc.y - 15);
    }
}, this);

// Show/hide tooltip
function showTooltip(text) {
    tooltip.setString(text);
    tooltip.setVisible(true);
}
function hideTooltip() {
    tooltip.setVisible(false);
}
```"""),

    jl("Write a complete example of a grid-based level using sprites.",
       """```js
// Render a grid-based tile map from a 2D array
var TILE_SIZE = 32;
var mapData = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 1],
    [1, 0, 0, 0, 3, 1],
    [1, 1, 1, 1, 1, 1]
];
var tileTextures = ['', 'res/floor.png', 'res/wall.png', 'res/door.png'];

for (var row = 0; row < mapData.length; row++) {
    for (var col = 0; col < mapData[row].length; col++) {
        var tileId = mapData[row][col];
        if (tileId > 0) {
            var tile = new cc.Sprite(tileTextures[tileId]);
            tile.setAnchorPoint(cc.p(0, 0));
            tile.setPosition(col * TILE_SIZE, (mapData.length - 1 - row) * TILE_SIZE);
            this.addChild(tile);
        }
    }
}
```"""),

    jl("Write a complete example of a simple game timer display showing minutes and seconds.",
       """```js
// Game timer showing MM:SS format
var totalSeconds = 0;
var timerLabel = cc.Label.createWithSystemFont('00:00', 'Arial', 28);
timerLabel.setPosition(240, 440);
timerLabel.setTextColor(cc.color.WHITE);
this.addChild(timerLabel, 10);

this.schedule(function() {
    totalSeconds++;
    var mins = Math.floor(totalSeconds / 60);
    var secs = totalSeconds % 60;
    var str = (mins < 10 ? '0' : '') + mins + ':' + (secs < 10 ? '0' : '') + secs;
    timerLabel.setString(str);
}, 1.0);
```"""),

    jl("Write a complete example of setting texture filtering for pixel art.",
       """```js
// Set nearest-neighbor filtering for crisp pixel art
var sprite = new cc.Sprite('res/pixel_hero.png');
sprite.setPosition(240, 160);
sprite.setScale(4.0); // scale up 4x
// Use GL nearest filter for sharp pixels
var tex = sprite.getTexture();
tex.setTexParameters(gl.NEAREST, gl.NEAREST, gl.CLAMP_TO_EDGE, gl.CLAMP_TO_EDGE);
this.addChild(sprite);
```"""),

    jl("Write a complete example of using cc.director.getVisibleSize for safe area layout.",
       """```js
// Layout using visible size (respects notch/safe area)
var visSize = cc.director.getVisibleSize();
var origin = cc.director.getVisibleOrigin();

// Place a back button in the top-left visible area
var backBtn = new ccui.Button('res/btn_back.png');
backBtn.setPosition(origin.x + 40, origin.y + visSize.height - 40);
backBtn.addClickEventListener(function() {
    cc.director.popScene();
});
this.addChild(backBtn, 10);
```"""),

    jl("Write a complete example of creating a 9-slice panel using ccui.Scale9Sprite.",
       """```js
// 9-slice scalable panel background
var panel = new ccui.Scale9Sprite('res/panel_bg.png');
panel.setCapInsets(cc.rect(15, 15, 2, 2)); // insets for 9-slice
panel.setContentSize(cc.size(300, 200));
panel.setPosition(240, 160);
this.addChild(panel);
```"""),

    jl("Write a complete example of a smooth camera shake using actions.",
       """```js
// Smooth camera shake by shaking the layer
function cameraShake(layer, duration, strength) {
    var originalPos = layer.getPosition();
    var shakeActions = [];
    var numShakes = Math.floor(duration / 0.05);

    for (var i = 0; i < numShakes; i++) {
        var factor = 1 - (i / numShakes); // decay
        var dx = (Math.random() * 2 - 1) * strength * factor;
        var dy = (Math.random() * 2 - 1) * strength * factor;
        shakeActions.push(cc.moveTo(0.05, cc.p(originalPos.x + dx, originalPos.y + dy)));
    }
    shakeActions.push(cc.moveTo(0.05, originalPos));
    layer.runAction(cc.sequence(shakeActions));
}
```"""),

    jl("Write a complete example of pausing all actions and resuming them later.",
       """```js
// Pause all running actions when game pauses
var pausedTargets = null;

function pauseGame() {
    pausedTargets = cc.director.getActionManager().pauseAllRunningActions();
    cc.director.getScheduler().setTimeScale(0);
}

function resumeGame() {
    if (pausedTargets) {
        cc.director.getActionManager().resumeTargets(pausedTargets);
        pausedTargets = null;
    }
    cc.director.getScheduler().setTimeScale(1.0);
}
```"""),

    jl("Write a complete example of a simple particle trail behind a moving sprite.",
       """```js
// Attach a particle trail to a moving sprite
var ship = new cc.Sprite('res/ship.png');
ship.setPosition(50, 160);
this.addChild(ship, 5);

var trail = new cc.ParticleSystem('res/particles/trail.plist');
trail.setPosition(0, 0);
ship.addChild(trail);

// Move ship across screen
ship.runAction(cc.moveTo(3.0, cc.p(430, 160)));
```"""),

    jl("Write a complete example of creating a loading spinner animation.",
       """```js
// Rotating loading spinner
var spinner = new cc.Sprite('res/spinner.png');
spinner.setPosition(240, 160);
this.addChild(spinner);
spinner.runAction(cc.repeatForever(cc.rotateBy(1.0, 360)));
```"""),

    jl("Write a complete example of interpolating colors for a health bar.",
       """```js
// Interpolate color from green to red based on health percentage
function getHealthColor(percent) {
    var r = Math.floor(255 * (1 - percent / 100));
    var g = Math.floor(255 * (percent / 100));
    return cc.color(r, g, 0);
}

// Update health bar sprite color
function updateHealthDisplay(sprite, hp, maxHP) {
    var pct = (hp / maxHP) * 100;
    sprite.setColor(getHealthColor(pct));
}
```"""),

    jl("Write a complete example of a transition with slide effect between scenes.",
       """```js
// Slide to a new scene from the right
var newScene = new cc.Scene();
newScene.addChild(new LevelSelectLayer());

var transition = new cc.TransitionSlideInR(0.5, newScene);
cc.director.runScene(transition);
```"""),

    jl("Write a complete example of removing all children from a layer and repopulating.",
       """```js
// Clear and rebuild a level
function resetLevel(layer) {
    // Remove all children and cleanup their actions
    layer.removeAllChildren(true);

    // Rebuild the level
    var bg = new cc.Sprite('res/bg.png');
    bg.setPosition(240, 160);
    layer.addChild(bg, -1);

    var hero = new cc.Sprite('res/hero.png');
    hero.setPosition(50, 160);
    layer.addChild(hero, 1);
}
```"""),

    jl("Write a complete example of a pulsing glow effect behind a sprite.",
       """```js
// Pulsing glow behind a character
var glow = new cc.Sprite('res/glow_circle.png');
glow.setPosition(240, 160);
glow.setBlendFunc(new cc.BlendFunc(cc.SRC_ALPHA, cc.ONE));
glow.setOpacity(150);
this.addChild(glow, 0);

glow.runAction(cc.repeatForever(cc.sequence(
    cc.spawn(cc.fadeTo(0.8, 200), cc.scaleTo(0.8, 1.3)),
    cc.spawn(cc.fadeTo(0.8, 100), cc.scaleTo(0.8, 1.0))
)));

// Hero on top of glow
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(240, 160);
this.addChild(hero, 1);
```"""),

    jl("Write a complete example of using cc.sys.localStorage to remember user settings.",
       """```js
// Save and load user settings
var Settings = {
    _data: null,
    load: function() {
        var raw = cc.sys.localStorage.getItem('settings');
        this._data = raw ? JSON.parse(raw) : {
            musicVolume: 0.7,
            sfxVolume: 1.0,
            language: 'en'
        };
    },
    save: function() {
        cc.sys.localStorage.setItem('settings', JSON.stringify(this._data));
    },
    get: function(key) { return this._data[key]; },
    set: function(key, val) { this._data[key] = val; this.save(); }
};

Settings.load();
cc.audioEngine.setMusicVolume(Settings.get('musicVolume'));
```"""),

    jl("Write a complete example of using cc.clampf to constrain player movement within screen bounds.",
       """```js
// Keep player within screen bounds
var winSize = cc.director.getWinSize();
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(240, 160);
this.addChild(hero);

this.scheduleUpdate();
this.update = function(dt) {
    // After applying movement...
    var hw = hero.width / 2;
    var hh = hero.height / 2;
    hero.x = cc.clampf(hero.x, hw, winSize.width - hw);
    hero.y = cc.clampf(hero.y, hh, winSize.height - hh);
};
```"""),

    jl("Write a complete example of a collectible item that spins and bobs.",
       """```js
// Animated collectible coin
var coin = new cc.Sprite('res/coin.png');
coin.setPosition(200, 200);
this.addChild(coin);

// Spin and bob simultaneously
coin.runAction(cc.repeatForever(cc.spawn(
    cc.rotateBy(1.0, 360),
    cc.sequence(
        cc.moveBy(0.5, cc.p(0, 10)).easing(cc.easeSineInOut()),
        cc.moveBy(0.5, cc.p(0, -10)).easing(cc.easeSineInOut())
    )
)));
```"""),

    jl("Write a complete example of a text field with event handling for login form.",
       """```js
// Login form with username text field
var userTF = new ccui.TextField('Username', 'Arial', 20);
userTF.setPosition(240, 250);
userTF.setMaxLengthEnabled(true);
userTF.setMaxLength(20);
userTF.setTouchAreaEnabled(true);
this.addChild(userTF);

var passTF = new ccui.TextField('Password', 'Arial', 20);
passTF.setPosition(240, 200);
passTF.setPasswordEnabled(true);
passTF.setMaxLengthEnabled(true);
passTF.setMaxLength(32);
passTF.setTouchAreaEnabled(true);
this.addChild(passTF);

var loginBtn = new ccui.Button('res/btn_login.png');
loginBtn.setPosition(240, 140);
loginBtn.setTitleText('LOGIN');
loginBtn.addClickEventListener(function() {
    var user = userTF.getString();
    var pass = passTF.getString();
    cc.log('Login:', user);
});
this.addChild(loginBtn);
```"""),

    jl("Write a complete example of CatmullRom spline drawing with DrawNode.",
       """```js
// Draw a smooth catmull-rom curve through waypoints
var draw = new cc.DrawNode();
this.addChild(draw);

var points = [
    cc.p(50, 100),
    cc.p(150, 300),
    cc.p(250, 80),
    cc.p(350, 250),
    cc.p(430, 150)
];

draw.drawCatmullRom(points, 50, 2, cc.color(0, 200, 255, 255));

// Also draw the control points as dots
for (var i = 0; i < points.length; i++) {
    draw.drawDot(points[i], 5, cc.color(255, 100, 0, 255));
}
```"""),

    jl("Write a complete example of a scene transition using pushScene with a fade.",
       """```js
// Push a settings scene with transition
function showSettings() {
    var settingsScene = new cc.Scene();
    settingsScene.addChild(new SettingsLayer());
    cc.director.pushScene(new cc.TransitionFade(0.3, settingsScene));
}

// Pop back with a different transition
function closeSettings() {
    cc.director.popScene();
}
```"""),

    jl("Write a complete example of animating a sprite sheet manually by switching frames on a timer.",
       """```js
// Manual frame animation without cc.Animation
cc.spriteFrameCache.addSpriteFrames('res/explosion.plist', 'res/explosion.png');
var frames = [];
for (var i = 0; i < 12; i++) {
    frames.push('explosion_' + (i < 10 ? '0' : '') + i + '.png');
}

var sprite = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame(frames[0]));
sprite.setPosition(240, 160);
this.addChild(sprite);

var frameIndex = 0;
this.schedule(function() {
    frameIndex++;
    if (frameIndex >= frames.length) {
        sprite.removeFromParent();
        this.unschedule(arguments.callee);
        return;
    }
    sprite.setSpriteFrame(frames[frameIndex]);
}, 0.06);
```"""),

    jl("Write a complete example of a custom shader for grayscale effect on a sprite.",
       """```js
// Apply grayscale shader to a sprite
var sprite = new cc.Sprite('res/hero.png');
sprite.setPosition(240, 160);
this.addChild(sprite);

var grayShader = new cc.GLProgram();
grayShader.initWithString(
    // Vertex shader (pass-through)
    'attribute vec4 a_position; attribute vec2 a_texCoord; attribute vec4 a_color;' +
    'varying vec2 v_texCoord; varying vec4 v_color;' +
    'void main() { gl_Position = CC_PMatrix * a_position; v_texCoord = a_texCoord; v_color = a_color; }',
    // Fragment shader (grayscale)
    'precision mediump float;' +
    'varying vec2 v_texCoord; varying vec4 v_color;' +
    'void main() { vec4 c = texture2D(CC_Texture0, v_texCoord) * v_color;' +
    'float gray = dot(c.rgb, vec3(0.299, 0.587, 0.114));' +
    'gl_FragColor = vec4(gray, gray, gray, c.a); }'
);
grayShader.addAttribute(cc.ATTRIBUTE_NAME_POSITION, cc.VERTEX_ATTRIB_POSITION);
grayShader.addAttribute(cc.ATTRIBUTE_NAME_TEX_COORD, cc.VERTEX_ATTRIB_TEX_COORDS);
grayShader.addAttribute(cc.ATTRIBUTE_NAME_COLOR, cc.VERTEX_ATTRIB_COLOR);
grayShader.link();
grayShader.updateUniforms();
sprite.setShaderProgram(grayShader);
```"""),
]

COMPLETE_SNIPPETS += _extra_complete

# ---------------------------------------------------------------------------
# 2. CODE COMPLETION  (~400)
# ---------------------------------------------------------------------------

CODE_COMPLETION = []

# Actions
CODE_COMPLETION += [
    jl("""Complete this code to make the sprite fade out after moving:
```
var sprite = new cc.Sprite('hero.png');
sprite.setPosition(cc.p(100,100));
this.addChild(sprite);
// TODO: move to (300,300) then fade out
```""",
       """```js
var sprite = new cc.Sprite('hero.png');
sprite.setPosition(cc.p(100, 100));
this.addChild(sprite);
// Move to (300,300) then fade out
sprite.runAction(cc.sequence(
    cc.moveTo(1.0, cc.p(300, 300)),
    cc.fadeOut(0.5)
));
```"""),

    jl("""Complete this code to make the sprite bounce infinitely:
```
var ball = new cc.Sprite('res/ball.png');
ball.setPosition(240, 100);
this.addChild(ball);
// TODO: bounce up 100px and back down, repeating forever
```""",
       """```js
var ball = new cc.Sprite('res/ball.png');
ball.setPosition(240, 100);
this.addChild(ball);
// Bounce up 100px and back down, repeating forever
ball.runAction(cc.repeatForever(cc.sequence(
    cc.moveBy(0.5, cc.p(0, 100)).easing(cc.easeOut(2.0)),
    cc.moveBy(0.5, cc.p(0, -100)).easing(cc.easeBounceOut())
)));
```"""),

    jl("""Complete this code to scale the button when pressed:
```
var btn = new ccui.Button('res/btn.png', 'res/btn_pressed.png');
btn.setPosition(240, 160);
btn.addTouchEventListener(function(sender, type) {
    // TODO: scale down on TOUCH_BEGAN, scale back on TOUCH_ENDED
}, this);
this.addChild(btn);
```""",
       """```js
var btn = new ccui.Button('res/btn.png', 'res/btn_pressed.png');
btn.setPosition(240, 160);
btn.addTouchEventListener(function(sender, type) {
    if (type === ccui.Widget.TOUCH_BEGAN) {
        sender.runAction(cc.scaleTo(0.05, 0.9));
    } else if (type === ccui.Widget.TOUCH_ENDED) {
        sender.runAction(cc.scaleTo(0.1, 1.0).easing(cc.easeBackOut()));
    } else if (type === ccui.Widget.TOUCH_CANCELED) {
        sender.runAction(cc.scaleTo(0.1, 1.0));
    }
}, this);
this.addChild(btn);
```"""),

    jl("""Complete this code to play a sound effect when the enemy dies:
```
var enemy = new cc.Sprite('res/enemy.png');
enemy.setPosition(300, 200);
this.addChild(enemy);
// TODO: fade out, play death sound, then remove from parent
```""",
       """```js
var enemy = new cc.Sprite('res/enemy.png');
enemy.setPosition(300, 200);
this.addChild(enemy);
// Fade out, play death sound, then remove from parent
enemy.runAction(cc.sequence(
    cc.callFunc(function() {
        cc.audioEngine.playEffect('res/audio/sfx_enemy_die.mp3');
    }),
    cc.fadeOut(0.5),
    cc.callFunc(function() {
        enemy.removeFromParent();
    })
));
```"""),

    jl("""Complete this code to schedule enemy spawning every 2 seconds:
```
var GameLayer = cc.Layer.extend({
    ctor: function() {
        this._super();
        // TODO: schedule spawnEnemy every 2 seconds
    },
    spawnEnemy: function() {
        var enemy = new cc.Sprite('res/enemy.png');
        enemy.setPosition(480, Math.random() * 320);
        this.addChild(enemy);
    }
});
```""",
       """```js
var GameLayer = cc.Layer.extend({
    ctor: function() {
        this._super();
        // Schedule spawnEnemy every 2 seconds
        this.schedule(this.spawnEnemy, 2.0);
    },
    spawnEnemy: function() {
        var enemy = new cc.Sprite('res/enemy.png');
        enemy.setPosition(480, Math.random() * 320);
        this.addChild(enemy);
    }
});
```"""),

    jl("""Complete this code to create a touch listener that drags the sprite:
```
var box = new cc.Sprite('res/box.png');
box.setPosition(240, 160);
this.addChild(box);
// TODO: add a touch listener that lets user drag the box
```""",
       """```js
var box = new cc.Sprite('res/box.png');
box.setPosition(240, 160);
this.addChild(box);
// Add a touch listener that lets user drag the box
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    swallowTouches: true,
    onTouchBegan: function(touch, event) {
        var target = event.getCurrentTarget();
        var loc = target.convertTouchToNodeSpace(touch);
        var rect = cc.rect(0, 0, target.width, target.height);
        return cc.rectContainsPoint(rect, loc);
    },
    onTouchMoved: function(touch, event) {
        var target = event.getCurrentTarget();
        var delta = touch.getDelta();
        target.x += delta.x;
        target.y += delta.y;
    }
}, box);
```"""),

    jl("""Complete this code to transition to a new scene with a fade:
```
var GameOverLayer = cc.Layer.extend({
    ctor: function() {
        this._super();
        var label = cc.Label.createWithSystemFont('GAME OVER', 'Arial', 48);
        label.setPosition(240, 240);
        this.addChild(label);
    }
});
// TODO: create scene with GameOverLayer and transition to it with fade
```""",
       """```js
var GameOverLayer = cc.Layer.extend({
    ctor: function() {
        this._super();
        var label = cc.Label.createWithSystemFont('GAME OVER', 'Arial', 48);
        label.setPosition(240, 240);
        this.addChild(label);
    }
});
// Create scene with GameOverLayer and transition to it with fade
var scene = new cc.Scene();
scene.addChild(new GameOverLayer());
cc.director.runScene(new cc.TransitionFade(0.5, scene));
```"""),

    jl("""Complete this code to make the label display the current score:
```
var score = 0;
var label = cc.Label.createWithSystemFont('Score: 0', 'Arial', 24);
label.setPosition(240, 440);
this.addChild(label);

function addPoints(pts) {
    // TODO: update score and label
}
```""",
       """```js
var score = 0;
var label = cc.Label.createWithSystemFont('Score: 0', 'Arial', 24);
label.setPosition(240, 440);
this.addChild(label);

function addPoints(pts) {
    score += pts;
    label.setString('Score: ' + score);
}
```"""),

    jl("""Complete this code to run both actions at the same time:
```
var sprite = new cc.Sprite('res/coin.png');
sprite.setPosition(100, 100);
this.addChild(sprite);
var move = cc.moveTo(1.0, cc.p(400, 300));
var rotate = cc.rotateBy(1.0, 360);
// TODO: run both simultaneously
```""",
       """```js
var sprite = new cc.Sprite('res/coin.png');
sprite.setPosition(100, 100);
this.addChild(sprite);
var move = cc.moveTo(1.0, cc.p(400, 300));
var rotate = cc.rotateBy(1.0, 360);
// Run both simultaneously using cc.spawn
sprite.runAction(cc.spawn(move, rotate));
```"""),

    jl("""Complete this code to add keyboard controls:
```
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(240, 160);
this.addChild(hero);
// TODO: add keyboard listener - space to jump
```""",
       """```js
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(240, 160);
this.addChild(hero);
// Add keyboard listener - space to jump
cc.eventManager.addListener({
    event: cc.EventListener.KEYBOARD,
    onKeyPressed: function(keyCode, event) {
        if (keyCode === cc.KEY.space) {
            hero.runAction(cc.sequence(
                cc.moveBy(0.3, cc.p(0, 100)).easing(cc.easeOut(2.0)),
                cc.moveBy(0.3, cc.p(0, -100)).easing(cc.easeIn(2.0))
            ));
        }
    }
}, this);
```"""),

    jl("""Complete this code to draw a health bar:
```
var draw = new cc.DrawNode();
this.addChild(draw);
var hp = 75;
var maxHP = 100;
// TODO: draw a health bar that's green when full, red when low
```""",
       """```js
var draw = new cc.DrawNode();
this.addChild(draw);
var hp = 75;
var maxHP = 100;
// Draw health bar: green when full, red when low
var barWidth = 200;
var barHeight = 16;
var ratio = hp / maxHP;
var fillWidth = barWidth * ratio;
var r = Math.floor(255 * (1 - ratio));
var g = Math.floor(255 * ratio);

// Background
draw.drawRect(cc.p(20, 440), cc.p(20 + barWidth, 440 + barHeight),
    cc.color(50, 50, 50, 200), 1, cc.color(100, 100, 100, 255));
// Fill
draw.drawRect(cc.p(20, 440), cc.p(20 + fillWidth, 440 + barHeight),
    cc.color(r, g, 0, 220), 0, cc.color(0, 0, 0, 0));
```"""),

    jl("""Complete this code to add a vertical scroll view with list items:
```
var sv = new ccui.ScrollView();
sv.setSize(cc.size(300, 400));
sv.setPosition(90, 60);
// TODO: configure vertical scrolling and add 15 text items
this.addChild(sv);
```""",
       """```js
var sv = new ccui.ScrollView();
sv.setSize(cc.size(300, 400));
sv.setPosition(90, 60);
// Configure vertical scrolling and add 15 text items
sv.setDirection(ccui.ScrollView.DIR_VERTICAL);
sv.setInnerContainerSize(cc.size(300, 15 * 50));
sv.setBounceEnabled(true);
sv.setScrollBarEnabled(true);

for (var i = 0; i < 15; i++) {
    var item = new ccui.Text('Item ' + (i + 1), 'Arial', 18);
    item.setPosition(150, 15 * 50 - 25 - i * 50);
    sv.getInnerContainer().addChild(item);
}
sv.jumpToTop();
this.addChild(sv);
```"""),

    jl("""Complete this code to save and load the high score:
```
// TODO: load saved high score, or default to 0
var highscore = ???;

function checkHighScore(newScore) {
    // TODO: save if newScore is higher
}
```""",
       """```js
// Load saved high score, or default to 0
var saved = cc.sys.localStorage.getItem('highscore');
var highscore = saved ? parseInt(saved) : 0;

function checkHighScore(newScore) {
    if (newScore > highscore) {
        highscore = newScore;
        cc.sys.localStorage.setItem('highscore', highscore.toString());
        cc.log('New high score: ' + highscore);
    }
}
```"""),

    jl("""Complete this code to play a Spine animation and switch on completion:
```
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
this.addChild(hero);
// TODO: play 'attack' once, then go back to 'idle' looping
```""",
       """```js
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
this.addChild(hero);
// Play 'attack' once, then go back to 'idle' looping
hero.setAnimation(0, 'attack', false);
hero.addAnimation(0, 'idle', true, 0);
```"""),

    jl("""Complete this code to create a frame animation from a sprite sheet:
```
cc.spriteFrameCache.addSpriteFrames('res/hero.plist', 'res/hero.png');
// TODO: build animation from frames hero_01.png to hero_08.png and play it looping
var hero = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('hero_01.png'));
hero.setPosition(240, 160);
this.addChild(hero);
```""",
       """```js
cc.spriteFrameCache.addSpriteFrames('res/hero.plist', 'res/hero.png');
// Build animation from frames hero_01.png to hero_08.png and play looping
var frames = [];
for (var i = 1; i <= 8; i++) {
    frames.push(cc.spriteFrameCache.getSpriteFrame('hero_0' + i + '.png'));
}
var anim = new cc.Animation(frames, 0.1);
var hero = new cc.Sprite(frames[0]);
hero.setPosition(240, 160);
this.addChild(hero);
hero.runAction(cc.repeatForever(cc.animate(anim)));
```"""),

    jl("""Complete this code to handle the Android back button:
```
// TODO: listen for back button, pop scene when pressed
```""",
       """```js
// Listen for back button, pop scene when pressed
cc.eventManager.addListener({
    event: cc.EventListener.KEYBOARD,
    onKeyPressed: function(keyCode, event) {
        if (keyCode === cc.KEY.back) {
            cc.director.popScene();
        }
    }
}, this);
```"""),

    jl("""Complete this code to add easing to the move action:
```
var sprite = new cc.Sprite('res/box.png');
sprite.setPosition(50, 160);
this.addChild(sprite);
var move = cc.moveTo(1.0, cc.p(400, 160));
// TODO: apply a bounce easing and run the action
```""",
       """```js
var sprite = new cc.Sprite('res/box.png');
sprite.setPosition(50, 160);
this.addChild(sprite);
var move = cc.moveTo(1.0, cc.p(400, 160));
// Apply bounce easing and run the action
sprite.runAction(move.easing(cc.easeBounceOut()));
```"""),

    jl("""Complete this code to create a custom event system for player death:
```
// In HUD layer:
// TODO: listen for 'player:died' custom event and show game over

// In game layer:
function onPlayerDied() {
    // TODO: dispatch the custom event
}
```""",
       """```js
// In HUD layer:
// Listen for 'player:died' custom event and show game over
cc.eventManager.addCustomListener('player:died', function(event) {
    var data = event.getUserData();
    cc.log('Player died with score:', data.score);
    showGameOverScreen(data.score);
});

// In game layer:
function onPlayerDied() {
    // Dispatch the custom event
    cc.eventManager.dispatchCustomEvent('player:died', { score: currentScore });
}
```"""),

    jl("""Complete this code to make a label with outline and shadow:
```
var label = cc.Label.createWithSystemFont('VICTORY', 'Impact', 48);
label.setPosition(240, 240);
// TODO: set gold text color, black outline, and drop shadow
this.addChild(label);
```""",
       """```js
var label = cc.Label.createWithSystemFont('VICTORY', 'Impact', 48);
label.setPosition(240, 240);
// Set gold text color, black outline, and drop shadow
label.setTextColor(cc.color(255, 215, 0));
label.enableOutline(cc.color(0, 0, 0, 255), 3);
label.enableShadow(cc.color(0, 0, 0, 150), cc.size(2, -2), 0);
this.addChild(label);
```"""),

    jl("""Complete this code to create an armature animation and play it:
```
// TODO: load armature data and create an armature
// Play the 'idle' animation looping
```""",
       """```js
// Load armature data and create an armature
ccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson');
var armature = ccs.Armature.create('hero');
armature.setPosition(240, 160);
this.addChild(armature);

// Play the 'idle' animation looping
armature.animation.play('idle', -1, -1);
```"""),

    jl("""Complete this code to make a slider control the music volume:
```
var slider = new ccui.Slider();
slider.loadBarTexture('res/slider_bar.png');
slider.loadSlidBallTextures('res/slider_ball.png', 'res/slider_ball.png', '');
slider.loadProgressBarTexture('res/slider_progress.png');
slider.setPosition(240, 200);
slider.setPercent(70);
// TODO: add event listener to update music volume
this.addChild(slider);
```""",
       """```js
var slider = new ccui.Slider();
slider.loadBarTexture('res/slider_bar.png');
slider.loadSlidBallTextures('res/slider_ball.png', 'res/slider_ball.png', '');
slider.loadProgressBarTexture('res/slider_progress.png');
slider.setPosition(240, 200);
slider.setPercent(70);
// Add event listener to update music volume
slider.addEventListener(function(sender, type) {
    var vol = sender.getPercent() / 100;
    cc.audioEngine.setMusicVolume(vol);
}, this);
this.addChild(slider);
```"""),

    jl("""Complete this code to detect when user scrolls to the bottom:
```
var sv = new ccui.ScrollView();
sv.setSize(cc.size(300, 400));
sv.setDirection(ccui.ScrollView.DIR_VERTICAL);
sv.setInnerContainerSize(cc.size(300, 1500));
// TODO: add event listener to detect scroll-to-bottom
this.addChild(sv);
```""",
       """```js
var sv = new ccui.ScrollView();
sv.setSize(cc.size(300, 400));
sv.setDirection(ccui.ScrollView.DIR_VERTICAL);
sv.setInnerContainerSize(cc.size(300, 1500));
// Add event listener to detect scroll-to-bottom
sv.addEventListener(function(sender, type) {
    if (type === ccui.ScrollView.EVENT_SCROLL_TO_BOTTOM) {
        cc.log('Reached bottom, load more content');
    }
}, this);
this.addChild(sv);
```"""),

    jl("""Complete this code to draw a dashed circle using DrawNode:
```
var draw = new cc.DrawNode();
this.addChild(draw);
var center = cc.p(240, 160);
var radius = 80;
// TODO: draw dots around the circle to create a dashed effect
```""",
       """```js
var draw = new cc.DrawNode();
this.addChild(draw);
var center = cc.p(240, 160);
var radius = 80;
// Draw dots around the circle to create a dashed effect
var numDots = 36;
for (var i = 0; i < numDots; i++) {
    var angle = (i / numDots) * Math.PI * 2;
    var x = center.x + Math.cos(angle) * radius;
    var y = center.y + Math.sin(angle) * radius;
    draw.drawDot(cc.p(x, y), 2, cc.color(255, 255, 255, 200));
}
```"""),

    jl("""Complete this code to create a parallax background:
```
var bg_far = new cc.Sprite('res/bg_mountains.png');
var bg_near = new cc.Sprite('res/bg_trees.png');
// TODO: set up scrolling parallax with different speeds
```""",
       """```js
var bg_far = new cc.Sprite('res/bg_mountains.png');
var bg_near = new cc.Sprite('res/bg_trees.png');
bg_far.setPosition(240, 160);
bg_near.setPosition(240, 160);
this.addChild(bg_far, -2);
this.addChild(bg_near, -1);

// Set up scrolling parallax with different speeds
var speed = 60;
this.scheduleUpdate();
this.update = function(dt) {
    bg_far.x -= speed * 0.3 * dt;  // slow
    bg_near.x -= speed * 0.8 * dt; // fast
    // Wrap around
    if (bg_far.x < -bg_far.width / 2) bg_far.x += bg_far.width;
    if (bg_near.x < -bg_near.width / 2) bg_near.x += bg_near.width;
};
```"""),

    jl("""Complete this code to detect swipe direction:
```
var startPos = null;
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    onTouchBegan: function(touch) {
        startPos = touch.getLocation();
        return true;
    },
    onTouchEnded: function(touch) {
        var endPos = touch.getLocation();
        // TODO: determine swipe direction (up/down/left/right)
    }
}, this);
```""",
       """```js
var startPos = null;
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    onTouchBegan: function(touch) {
        startPos = touch.getLocation();
        return true;
    },
    onTouchEnded: function(touch) {
        var endPos = touch.getLocation();
        var dx = endPos.x - startPos.x;
        var dy = endPos.y - startPos.y;
        if (cc.pDistance(startPos, endPos) < 30) return; // too short

        if (Math.abs(dx) > Math.abs(dy)) {
            cc.log(dx > 0 ? 'Swipe RIGHT' : 'Swipe LEFT');
        } else {
            cc.log(dy > 0 ? 'Swipe UP' : 'Swipe DOWN');
        }
    }
}, this);
```"""),

    jl("""Complete this code to make an armature animation trigger a sound on a frame event:
```
ccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson');
var armature = ccs.Armature.create('hero');
armature.setPosition(240, 160);
this.addChild(armature);
armature.animation.play('walk', -1, -1);
// TODO: listen for frame events and play footstep sound
```""",
       """```js
ccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson');
var armature = ccs.Armature.create('hero');
armature.setPosition(240, 160);
this.addChild(armature);
armature.animation.play('walk', -1, -1);
// Listen for frame events and play footstep sound
armature.animation.setFrameEventCallFunc(function(bone, eventName, orig, cur) {
    if (eventName === 'footstep') {
        cc.audioEngine.playEffect('res/sfx_step.mp3');
    }
});
```"""),

    jl("""Complete this code to make a checkbox toggle sound on/off:
```
var cb = new ccui.CheckBox('res/cb_bg.png', 'res/cb_bg_sel.png', 'res/cb_cross.png', '', '');
cb.setPosition(240, 200);
cb.setSelected(true);
// TODO: toggle music on/off based on checkbox state
this.addChild(cb);
```""",
       """```js
var cb = new ccui.CheckBox('res/cb_bg.png', 'res/cb_bg_sel.png', 'res/cb_cross.png', '', '');
cb.setPosition(240, 200);
cb.setSelected(true);
// Toggle music on/off based on checkbox state
cb.addEventListener(function(sender, type) {
    if (sender.isSelected()) {
        cc.audioEngine.resumeMusic();
    } else {
        cc.audioEngine.pauseMusic();
    }
}, this);
this.addChild(cb);
```"""),

    jl("""Complete this code to set up Spine animation blending:
```
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
this.addChild(hero);
// TODO: set up smooth transitions between idle, walk, and run
hero.setAnimation(0, 'idle', true);
```""",
       """```js
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
this.addChild(hero);
// Set up smooth transitions between idle, walk, and run
hero.setMix('idle', 'walk', 0.2);
hero.setMix('walk', 'idle', 0.2);
hero.setMix('walk', 'run', 0.3);
hero.setMix('run', 'walk', 0.3);
hero.setMix('run', 'idle', 0.2);
hero.setAnimation(0, 'idle', true);
```"""),

    jl("""Complete this code to load JSON data asynchronously:
```
// TODO: load level data from 'res/level.json' and start the level
```""",
       """```js
// Load level data from 'res/level.json' and start the level
cc.loader.loadJson('res/level.json', function(err, data) {
    if (err) {
        cc.error('Failed to load level:', err);
        return;
    }
    cc.log('Level name:', data.name);
    startLevel(data);
});
```"""),

    jl("""Complete this code to make a node follow the player:
```
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(100, 160);
this.addChild(hero);
// TODO: make this layer follow the hero within level bounds (0,0 to 2000,320)
// Then move hero to the end of the level
```""",
       """```js
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(100, 160);
this.addChild(hero);
// Make this layer follow the hero within level bounds
this.runAction(cc.follow(hero, cc.rect(0, 0, 2000, 320)));
// Move hero to the end of the level
hero.runAction(cc.moveTo(8.0, cc.p(1900, 160)));
```"""),

    jl("""Complete this code to create a gradient background:
```
// TODO: create a gradient from sky blue (top) to dark blue (bottom)
```""",
       """```js
// Create a gradient from sky blue (top) to dark blue (bottom)
var gradient = new cc.LayerGradient(
    cc.color(135, 206, 235, 255),  // sky blue at top
    cc.color(10, 20, 60, 255),     // dark blue at bottom
    cc.p(0, -1)                    // direction: downward
);
this.addChild(gradient, -1);
```"""),

    jl("""Complete this code to use platform detection for cross-platform behavior:
```
// TODO: check if running on mobile and enable appropriate controls
```""",
       """```js
// Check if running on mobile and enable appropriate controls
if (cc.sys.isMobile) {
    // Enable touch controls / virtual joystick
    cc.log('Mobile platform - using touch controls');
    this.enableTouchControls();
} else {
    // Enable keyboard and mouse controls
    cc.log('Desktop platform - using keyboard/mouse');
    this.enableKeyboardControls();
}

if (cc.sys.platform === cc.sys.ANDROID) {
    // Handle Android back button
    cc.eventManager.addListener({
        event: cc.EventListener.KEYBOARD,
        onKeyPressed: function(key) {
            if (key === cc.KEY.back) cc.director.popScene();
        }
    }, this);
}
```"""),
]

# Add more code completion to reach ~400
_extra_completion = [
    jl("""Complete this code to create a BMFont label for the score:
```
// TODO: create a bitmap font label centered at top of screen
```""",
       """```js
// Create a bitmap font label centered at top of screen
var winSize = cc.director.getWinSize();
var scoreLabel = cc.Label.createWithBMFont('res/fonts/score.fnt', '0');
scoreLabel.setPosition(winSize.width / 2, winSize.height - 30);
scoreLabel.setHorizontalAlignment(cc.TEXT_ALIGNMENT_CENTER);
this.addChild(scoreLabel, 10);
```"""),

    jl("""Complete this code to add a particle explosion at the enemy's position:
```
var enemyPos = enemy.getPosition();
enemy.removeFromParent();
// TODO: add explosion particle effect at enemyPos
```""",
       """```js
var enemyPos = enemy.getPosition();
enemy.removeFromParent();
// Add explosion particle effect at enemyPos
var explosion = new cc.ParticleExplosion();
explosion.setTexture(cc.textureCache.addImage('res/particle_spark.png'));
explosion.setPosition(enemyPos);
explosion.setAutoRemoveOnFinish(true);
this.addChild(explosion, 10);
```"""),

    jl("""Complete this code to set the sprite to pixel-perfect rendering:
```
var sprite = new cc.Sprite('res/pixel_art.png');
sprite.setPosition(240, 160);
sprite.setScale(4.0);
// TODO: set nearest-neighbor filtering so pixels stay sharp
this.addChild(sprite);
```""",
       """```js
var sprite = new cc.Sprite('res/pixel_art.png');
sprite.setPosition(240, 160);
sprite.setScale(4.0);
// Set nearest-neighbor filtering so pixels stay sharp
var tex = sprite.getTexture();
tex.setTexParameters(gl.NEAREST, gl.NEAREST, gl.CLAMP_TO_EDGE, gl.CLAMP_TO_EDGE);
this.addChild(sprite);
```"""),

    jl("""Complete this code to make a label appear letter by letter (typewriter):
```
var fullText = 'Once upon a time...';
var label = cc.Label.createWithSystemFont('', 'Arial', 18);
label.setPosition(240, 200);
this.addChild(label);
// TODO: reveal one character at a time every 0.05 seconds
```""",
       """```js
var fullText = 'Once upon a time...';
var label = cc.Label.createWithSystemFont('', 'Arial', 18);
label.setPosition(240, 200);
this.addChild(label);
// Reveal one character at a time every 0.05 seconds
var idx = 0;
this.schedule(function() {
    idx++;
    label.setString(fullText.substring(0, idx));
    if (idx >= fullText.length) {
        this.unschedule(arguments.callee);
    }
}, 0.05);
```"""),

    jl("""Complete this code to implement slow motion when boss is hit:
```
function onBossHit() {
    // TODO: slow time to 30% for 1 second, then restore normal speed
}
```""",
       """```js
function onBossHit() {
    // Slow time to 30% for 1 second, then restore normal speed
    cc.director.getScheduler().setTimeScale(0.3);
    // Use a real-time delay (not affected by time scale)
    setTimeout(function() {
        cc.director.getScheduler().setTimeScale(1.0);
    }, 1000);
}
```"""),

    jl("""Complete this code to create a loading bar that fills from 0 to 100:
```
var bar = new ccui.LoadingBar('res/loading_bar.png', 0);
bar.setPosition(240, 160);
this.addChild(bar);
// TODO: animate the bar from 0% to 100% over 3 seconds
```""",
       """```js
var bar = new ccui.LoadingBar('res/loading_bar.png', 0);
bar.setPosition(240, 160);
this.addChild(bar);
// Animate the bar from 0% to 100% over 3 seconds
var percent = 0;
this.schedule(function(dt) {
    percent += (100 / 3.0) * dt;
    if (percent >= 100) {
        percent = 100;
        this.unschedule(arguments.callee);
        cc.log('Loading complete!');
    }
    bar.setPercent(percent);
}, 0);
```"""),

    jl("""Complete this code to flip the hero sprite based on movement direction:
```
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(240, 160);
this.addChild(hero);
// TODO: in the update loop, flip sprite based on horizontal velocity
var velocityX = 0;
```""",
       """```js
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(240, 160);
this.addChild(hero);
// In the update loop, flip sprite based on horizontal velocity
var velocityX = 0;
this.scheduleUpdate();
this.update = function(dt) {
    if (velocityX > 0) {
        hero.setFlippedX(false); // facing right (default)
    } else if (velocityX < 0) {
        hero.setFlippedX(true);  // facing left
    }
    hero.x += velocityX * dt;
};
```"""),

    jl("""Complete this code to localize text based on system language:
```
// TODO: detect system language and load appropriate strings
```""",
       """```js
// Detect system language and load appropriate strings
var langFile;
switch (cc.sys.language) {
    case cc.sys.LANGUAGE_CHINESE:  langFile = 'res/i18n/zh.json'; break;
    case cc.sys.LANGUAGE_JAPANESE: langFile = 'res/i18n/ja.json'; break;
    case cc.sys.LANGUAGE_KOREAN:   langFile = 'res/i18n/ko.json'; break;
    default:                       langFile = 'res/i18n/en.json'; break;
}
cc.loader.loadJson(langFile, function(err, strings) {
    if (!err) {
        window.i18n = strings;
        cc.log('Loaded language:', langFile);
    }
});
```"""),

    jl("""Complete this code to make the Spine character switch to a different skin:
```
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
hero.setAnimation(0, 'idle', true);
this.addChild(hero);
// TODO: switch to 'warrior' skin, then later to 'mage' skin
```""",
       """```js
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setPosition(240, 80);
hero.setAnimation(0, 'idle', true);
this.addChild(hero);
// Switch to 'warrior' skin
hero.setSkin('warrior');

// Later, switch to 'mage' skin
// hero.setSkin('mage');
```"""),

    jl("""Complete this code to clean up resources when leaving a scene:
```
var MyScene = cc.Scene.extend({
    onExit: function() {
        // TODO: clean up audio, textures, and sprite frames
        this._super();
    }
});
```""",
       """```js
var MyScene = cc.Scene.extend({
    onExit: function() {
        // Clean up audio, textures, and sprite frames
        cc.audioEngine.stopMusic(true);
        cc.audioEngine.stopAllEffects();
        cc.spriteFrameCache.removeUnusedSpriteFrames();
        cc.textureCache.removeUnusedTextures();
        this._super();
    }
});
```"""),

    jl("""Complete this code to create a page view with 3 tutorial pages:
```
var pv = new ccui.PageView();
pv.setSize(cc.size(400, 300));
pv.setPosition(40, 90);
// TODO: add 3 pages with different tutorial images
this.addChild(pv);
```""",
       """```js
var pv = new ccui.PageView();
pv.setSize(cc.size(400, 300));
pv.setPosition(40, 90);
// Add 3 pages with different tutorial images
var tutorials = ['res/tutorial_1.png', 'res/tutorial_2.png', 'res/tutorial_3.png'];
for (var i = 0; i < tutorials.length; i++) {
    var page = new ccui.Layout();
    page.setSize(cc.size(400, 300));
    var img = new ccui.ImageView(tutorials[i]);
    img.setPosition(200, 150);
    page.addChild(img);
    pv.addPage(page);
}
pv.addEventListener(function(sender, type) {
    cc.log('Page:', sender.getCurrentPageIndex());
}, this);
this.addChild(pv);
```"""),

    jl("""Complete this code to find a widget by name in a UI tree:
```
var root = loadUIFromCSB('res/ui/main_menu.csb');
this.addChild(root);
// TODO: find the 'playButton' widget and add a click handler
```""",
       """```js
var root = loadUIFromCSB('res/ui/main_menu.csb');
this.addChild(root);
// Find the 'playButton' widget and add a click handler
var playBtn = ccui.helper.seekWidgetByName(root, 'playButton');
if (playBtn) {
    playBtn.addClickEventListener(function() {
        cc.log('Play button clicked!');
        cc.director.runScene(new GameScene());
    });
}
```"""),

    jl("""Complete this code to use cc.pLerp for smooth camera following:
```
var camera = this;
var target = hero.getPosition();
// TODO: smoothly interpolate camera position toward target each frame
```""",
       """```js
var camera = this;
var target = hero.getPosition();
// Smoothly interpolate camera position toward target each frame
this.scheduleUpdate();
this.update = function(dt) {
    target = hero.getPosition();
    var current = camera.getPosition();
    var smoothed = cc.pLerp(current, cc.p(-target.x + 240, -target.y + 160), 0.05);
    camera.setPosition(smoothed);
};
```"""),

    jl("""Complete this code to draw a minimap dot for each enemy:
```
var minimap = new cc.DrawNode();
minimap.setPosition(380, 380);
this.addChild(minimap, 20);
var enemies = [/* array of enemy sprites */];
// TODO: draw a red dot for each enemy scaled to minimap coordinates
```""",
       """```js
var minimap = new cc.DrawNode();
minimap.setPosition(380, 380);
this.addChild(minimap, 20);
var enemies = [/* array of enemy sprites */];
var levelW = 2000, levelH = 600, mapW = 80, mapH = 24;

function updateMinimap() {
    minimap.clear();
    // Border
    minimap.drawRect(cc.p(0, 0), cc.p(mapW, mapH), null, 1, cc.color(255, 255, 255, 150));
    // Enemy dots
    for (var i = 0; i < enemies.length; i++) {
        var ex = (enemies[i].x / levelW) * mapW;
        var ey = (enemies[i].y / levelH) * mapH;
        minimap.drawDot(cc.p(ex, ey), 2, cc.color(255, 0, 0, 255));
    }
}
```"""),

    jl("""Complete this code to create an additive blend glow sprite:
```
var glow = new cc.Sprite('res/glow.png');
glow.setPosition(240, 160);
// TODO: set additive blending and add a pulsing opacity animation
this.addChild(glow, 5);
```""",
       """```js
var glow = new cc.Sprite('res/glow.png');
glow.setPosition(240, 160);
// Set additive blending and add a pulsing opacity animation
glow.setBlendFunc(new cc.BlendFunc(cc.SRC_ALPHA, cc.ONE));
glow.runAction(cc.repeatForever(cc.sequence(
    cc.fadeTo(0.6, 220),
    cc.fadeTo(0.6, 100)
)));
this.addChild(glow, 5);
```"""),
]

CODE_COMPLETION += _extra_completion

# ---------------------------------------------------------------------------
# 3. CODE EXPLANATION  (~400)
# ---------------------------------------------------------------------------

CODE_EXPLANATION = []

CODE_EXPLANATION += [
    jl("""What does this code do?
```
var action = cc.sequence(cc.moveBy(1, cc.p(100,0)), cc.callFunc(function(){ cc.log('done'); }));
node.runAction(action);
```""",
       """This code creates a sequence of two actions on `node`:

1. **`cc.moveBy(1, cc.p(100, 0))`** moves the node 100 pixels to the right over 1 second (relative movement).
2. **`cc.callFunc(...)`** is an instant action that executes a callback logging `'done'` to the console.

The `cc.sequence` wraps them so they run one after the other: first the move completes, then the callback fires. The node will shift right by 100px and print "done" when finished."""),

    jl("""What does this code do?
```
node.runAction(cc.repeatForever(cc.sequence(
    cc.moveBy(0.5, cc.p(0, 50)),
    cc.moveBy(0.5, cc.p(0, -50))
)));
```""",
       """This code makes `node` bounce up and down forever. The sequence moves the node up 50 pixels over 0.5 seconds, then back down 50 pixels over 0.5 seconds. `cc.repeatForever` wraps this sequence to loop indefinitely, creating a continuous bouncing animation."""),

    jl("""What does this code do?
```
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    swallowTouches: true,
    onTouchBegan: function(touch, event) {
        var loc = touch.getLocation();
        return true;
    },
    onTouchMoved: function(touch, event) {
        var delta = touch.getDelta();
        node.x += delta.x;
        node.y += delta.y;
    }
}, node);
```""",
       """This code makes `node` draggable by touch. It registers a touch listener that:

1. **`onTouchBegan`**: Gets the touch world position and returns `true` to claim the touch (required to receive move/end events).
2. **`onTouchMoved`**: Gets the movement delta since the last frame and applies it to the node's position, making the node follow the finger.
3. **`swallowTouches: true`**: Prevents the touch from propagating to nodes below, so only this node responds.

The listener is attached to `node`, so it has the same lifecycle (removed when `node` is removed from the scene)."""),

    jl("""What does this code do?
```
var frames = [];
for (var i = 1; i <= 8; i++) {
    frames.push(cc.spriteFrameCache.getSpriteFrame('run_' + (i < 10 ? '0' + i : i) + '.png'));
}
var anim = new cc.Animation(frames, 0.08, 0);
sprite.runAction(cc.repeatForever(cc.animate(anim)));
```""",
       """This code creates a looping frame-by-frame animation on `sprite`:

1. It builds an array of 8 sprite frames named `run_01.png` through `run_08.png` from the sprite frame cache (they must be pre-loaded from a plist).
2. Creates a `cc.Animation` with those frames, 0.08 seconds per frame (12.5 FPS), and `0` loops (which means infinite loops in the Animation constructor).
3. Wraps it in `cc.animate` to create an action, then `cc.repeatForever` to loop it endlessly.

This is the standard pattern for sprite sheet animation, like a character running."""),

    jl("""What does this code do?
```
cc.audioEngine.playMusic('res/audio/bgm.mp3', true);
cc.audioEngine.setMusicVolume(0.7);
var id = cc.audioEngine.playEffect('res/audio/sfx_hit.mp3', false);
```""",
       """This code plays audio using the Cocos2d-x audio engine:

1. **`playMusic`**: Starts background music from the file `bgm.mp3`, looping (`true`).
2. **`setMusicVolume(0.7)`**: Sets the music volume to 70%.
3. **`playEffect`**: Plays a one-shot (`false` = no loop) sound effect `sfx_hit.mp3` and stores the returned audio ID in `id`.

The audio ID can be used later to stop or pause that specific sound effect instance with `cc.audioEngine.stopEffect(id)`."""),

    jl("""What does this code do?
```
var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');
hero.setMix('idle', 'walk', 0.2);
hero.setMix('walk', 'run', 0.3);
hero.setAnimation(0, 'idle', true);
```""",
       """This code sets up a Spine skeletal animation:

1. Creates a `SkeletonAnimation` from a Spine JSON file and its texture atlas.
2. **`setMix`** defines smooth cross-fade transitions between animations: 0.2 seconds when blending from 'idle' to 'walk', and 0.3 seconds from 'walk' to 'run'. Without mix, transitions would be abrupt.
3. **`setAnimation(0, 'idle', true)`**: Plays the 'idle' animation on track 0, looping. Track 0 is the base animation track.

When you later call `hero.setAnimation(0, 'walk', true)`, it will smoothly blend from idle to walk over 0.2 seconds."""),

    jl("""What does this code do?
```
var draw = new cc.DrawNode();
this.addChild(draw);
draw.drawPoly(
    [cc.p(100, 0), cc.p(200, 150), cc.p(0, 150)],
    cc.color(0, 255, 0, 100),
    1,
    cc.color(0, 200, 0, 255)
);
```""",
       """This code draws a filled triangle using `cc.DrawNode`:

1. Creates a new `DrawNode` (a node for immediate-mode vector graphics) and adds it to the scene.
2. **`drawPoly`** draws a polygon with:
   - **Vertices**: Three points forming a triangle: bottom-center (100,0), top-right (200,150), top-left (0,150).
   - **Fill color**: Semi-transparent green (RGBA: 0, 255, 0, 100).
   - **Border width**: 1 pixel.
   - **Border color**: Opaque darker green (RGBA: 0, 200, 0, 255).

The result is a green filled triangle with a slightly darker green outline."""),

    jl("""What does this code do?
```
cc.director.pushScene(new cc.TransitionFade(0.5, pauseScene));
```""",
       """This code pushes a new scene onto the scene stack with a fade transition:

1. **`cc.TransitionFade(0.5, pauseScene)`** creates a 0.5-second fade transition to `pauseScene`.
2. **`cc.director.pushScene`** pushes it onto the stack instead of replacing the current scene. The current scene is preserved underneath.

This is commonly used for pause menus or modal dialogs. Later, calling `cc.director.popScene()` will remove the pause scene and return to the previous one, which is still in memory and retains its state."""),

    jl("""What does this code do?
```
node.runAction(cc.moveTo(1.0, cc.p(300, 300)).easing(cc.easeBounceOut()));
```""",
       """This code moves `node` to position (300, 300) over 1 second with a bounce easing effect. The `cc.easeBounceOut()` easing function makes the node overshoot the target and bounce back a few times before settling, like a ball hitting the ground. Without the easing, the movement would be linear (constant speed)."""),

    jl("""What does this code do?
```
cc.eventManager.dispatchCustomEvent('game:score_update', { score: 100 });
```""",
       """This code dispatches a custom event named `'game:score_update'` with user data `{ score: 100 }`. Any listener registered with `cc.eventManager.addCustomListener('game:score_update', callback)` will receive this event and can access the score via `event.getUserData()`. This is a pub/sub pattern used to decouple game systems (e.g., the game logic notifies the HUD of score changes without direct references)."""),

    jl("""What does this code do?
```
cc.sys.localStorage.setItem('playerData', JSON.stringify({ name: 'Alice', level: 5 }));
var raw = cc.sys.localStorage.getItem('playerData');
var player = raw ? JSON.parse(raw) : {};
```""",
       """This code persists player data using local storage:

1. **Saves**: Serializes a JavaScript object `{ name: 'Alice', level: 5 }` to a JSON string and stores it under the key `'playerData'`.
2. **Loads**: Retrieves the stored string, and if it exists (not null/undefined), parses it back into a JavaScript object. If nothing was saved, defaults to an empty object `{}`.

`cc.sys.localStorage` works like browser `localStorage` and persists across sessions on both native and web platforms."""),

    jl("""What does this code do?
```
cc.director.getScheduler().setTimeScale(0.3);
```""",
       """This code sets the global time scale to 0.3 (30% of normal speed), creating a slow-motion effect. All scheduled callbacks, actions, and animations will run at 30% speed. The scheduler controls the `dt` (delta time) passed to `update()` and all time-based systems. To return to normal speed, call `setTimeScale(1.0)`. A value of 2.0 would double the speed."""),

    jl("""What does this code do?
```
var overlay = new cc.LayerColor(cc.color(0, 0, 0, 128));
overlay.setContentSize(cc.director.getWinSize());
this.addChild(overlay, 100);
```""",
       """This code creates a semi-transparent black overlay covering the entire screen:

1. **`cc.LayerColor`** creates a solid color layer with RGBA (0, 0, 0, 128) - black at 50% opacity.
2. **`setContentSize`** sizes it to match the window.
3. **`addChild(overlay, 100)`** adds it at z-order 100, ensuring it draws on top of most other content.

This is a common pattern for pause screens, dialog backgrounds, or modal overlays that dim the game content behind them."""),

    jl("""What does this code do?
```
node.attr({
    x: 100, y: 200,
    scale: 1.5, opacity: 200,
    visible: true
});
```""",
       """This code sets multiple properties on `node` in a single call using `attr()`:

- **x: 100, y: 200**: Positions the node at (100, 200).
- **scale: 1.5**: Scales to 150% size.
- **opacity: 200**: Sets opacity to ~78% (200 out of 255).
- **visible: true**: Makes the node visible.

`attr()` is a convenience method that avoids multiple setter calls. It sets each property directly, which is faster than calling individual setter methods in JavaScript."""),

    jl("""What does this code do?
```
this.schedule(this.spawnEnemy, 3.0);
```""",
       """This code schedules the method `this.spawnEnemy` to be called every 3 seconds. The scheduler will invoke `spawnEnemy` on `this` (typically a Layer or Node subclass) repeatedly with a 3-second interval until it's unscheduled with `this.unschedule(this.spawnEnemy)`. The callback receives `dt` (time since last call) as a parameter."""),

    jl("""What does this code do?
```
ccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson');
var armature = ccs.Armature.create('hero');
armature.animation.play('run', -1, 1);
armature.animation.setSpeedScale(1.5);
```""",
       """This code loads and plays a CocosStudio armature animation:

1. **`addArmatureFileInfo`**: Loads the armature data (bones, animations, textures) from an ExportJson file created in CocosStudio.
2. **`ccs.Armature.create('hero')`**: Creates an armature instance named 'hero'.
3. **`play('run', -1, 1)`**: Plays the 'run' animation with no blending (-1 = instant transition) and loop count 1 (play once). Use -1 for infinite loop.
4. **`setSpeedScale(1.5)`**: Plays at 1.5x normal speed.

The armature extends cc.Node so it can be positioned, scaled, and added to the scene like any other node."""),

    jl("""What does this code do?
```
var localPt = node.convertTouchToNodeSpace(touch);
var nodeRect = cc.rect(0, 0, node.width, node.height);
if (cc.rectContainsPoint(nodeRect, localPt)) {
    cc.log('hit');
}
```""",
       """This code performs hit testing to check if a touch landed on a node:

1. **`convertTouchToNodeSpace`**: Converts the touch's world-space position into the node's local coordinate system (accounting for position, rotation, scale, and parent transforms).
2. Creates a rectangle from (0,0) to (width, height) representing the node's content area in local space.
3. **`cc.rectContainsPoint`**: Checks if the local touch point falls within that rectangle.

This is the standard pattern for detecting taps on specific nodes in Cocos2d-x JS."""),

    jl("""What does this code do?
```
sprite.setBlendFunc(new cc.BlendFunc(cc.ONE, cc.ONE));
```""",
       """This code sets the sprite's blend function to **additive blending** (source: ONE, destination: ONE). Instead of the default alpha blending (where transparent pixels hide what's behind), additive blending adds the sprite's pixel colors to whatever is already drawn on screen. This creates a glow or light effect, commonly used for particles, lasers, fire, and other luminous effects. Overlapping additive sprites become brighter."""),

    jl("""What does this code do?
```
var batch = new cc.SpriteBatchNode('res/atlas.png', 100);
layer.addChild(batch);
for (var i = 0; i < 50; i++) {
    var s = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('enemy.png'));
    batch.addChild(s);
}
```""",
       """This code uses a `SpriteBatchNode` to render 50 sprites in a single draw call for better performance:

1. Creates a batch node bound to the texture `atlas.png`, with capacity for 100 sprites.
2. Creates 50 sprites from the sprite frame `'enemy.png'` (which must be a frame within `atlas.png`).
3. Adds each sprite as a child of the batch node instead of the layer.

All children of a batch node must share the same texture. The GPU renders them all in one draw call instead of 50 separate calls, which significantly improves performance for many similar sprites."""),

    jl("""What does this code do?
```
hero.setAnimation(0, 'attack', false);
hero.addAnimation(0, 'run', true, 0);
```""",
       """This code queues two Spine animations on track 0:

1. **`setAnimation(0, 'attack', false)`**: Immediately plays the 'attack' animation on track 0 without looping (plays once).
2. **`addAnimation(0, 'run', true, 0)`**: Queues 'run' to play after 'attack' finishes, with looping enabled and 0 seconds extra delay.

The result is: the character attacks once, then seamlessly transitions to the running animation and keeps running. `addAnimation` queues without interrupting the current animation, unlike `setAnimation` which replaces immediately."""),

    jl("""What does this code do?
```
this.scheduleOnce(function() {
    cc.log('delayed!');
}, 3.0);
```""",
       """This code schedules a one-time callback that fires after a 3-second delay. Unlike `schedule()` which repeats, `scheduleOnce` executes the function exactly once after the specified delay, then automatically unschedules itself. It's useful for delayed events like showing a tutorial popup, triggering a cutscene, or any one-shot timed event."""),

    jl("""What does this code do?
```
var pausedTargets = cc.director.getActionManager().pauseAllRunningActions();
```""",
       """This code pauses all currently running actions across all nodes in the scene. It returns an array of all targets (nodes) that were paused. You can later resume them with `cc.director.getActionManager().resumeTargets(pausedTargets)`. This is useful for implementing a global game pause that freezes all animations and movements without stopping the scheduler."""),

    jl("""What does this code do?
```
var sv = new ccui.ScrollView();
sv.setDirection(ccui.ScrollView.DIR_VERTICAL);
sv.setInnerContainerSize(cc.size(300, 1200));
sv.setBounceEnabled(true);
```""",
       """This code creates a vertical scroll view widget:

1. **`setDirection(DIR_VERTICAL)`**: Only allows vertical scrolling.
2. **`setInnerContainerSize(300, 1200)`**: The scrollable content area is 1200px tall (larger than the visible area), enabling scrolling.
3. **`setBounceEnabled(true)`**: Adds an elastic bounce effect when scrolling past the edges, like iOS scroll views.

Children are added to the inner container via `sv.getInnerContainer().addChild(...)`. The scroll view must also have its own size set with `sv.setSize()` to define the visible viewport."""),

    jl("""What does this code do?
```
hero.setCascadeOpacityEnabled(true);
hero.runAction(cc.fadeOut(0.5));
```""",
       """This code fades out the `hero` node and all its children together over 0.5 seconds. `setCascadeOpacityEnabled(true)` makes the node's opacity propagate to all descendant nodes. Without it, only the hero itself would fade, while its children (like a weapon sprite, health bar, or name label attached to it) would remain fully visible. With cascade enabled, the entire hierarchy fades as one unit."""),

    jl("""What does this code do?
```
cc.spriteFrameCache.addSpriteFrames('res/ui.plist', 'res/ui.png');
var btn = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('btn_play.png'));
```""",
       """This code loads a texture atlas and creates a sprite from one of its frames:

1. **`addSpriteFrames`**: Loads a plist file (which contains frame definitions - names, positions, sizes, rotations within the atlas) paired with its texture image `ui.png`. All frame definitions are registered in the global sprite frame cache.
2. **`getSpriteFrame('btn_play.png')`**: Retrieves the sprite frame named `btn_play.png` from the cache - this is a reference to a sub-rectangle of the atlas texture.
3. Creates a sprite using that frame, so only the `btn_play.png` region of the atlas is displayed.

This is the standard texture atlas workflow: one draw call for all sprites sharing the atlas."""),

    jl("""What does this code do?
```
node.setNormalizedPosition(cc.p(0.5, 0.5));
```""",
       """This code positions the node at exactly the center of its parent, using normalized coordinates (0 to 1 range). `(0.5, 0.5)` means 50% of the parent's width and 50% of its height. Unlike `setPosition` which uses absolute pixel values, `setNormalizedPosition` is relative to the parent's content size, making layouts responsive to different screen sizes. `(0, 0)` would be bottom-left, `(1, 1)` would be top-right."""),

    jl("""What does this code do?
```
var timeline = ccs.actionManager.loadAnimationActionWithFile('res/ui/dialog.csb');
dialogNode.runAction(timeline);
timeline.gotoFrameAndPlay(0, true);
```""",
       """This code loads and plays a CocosStudio timeline animation from a .csb binary file:

1. **`loadAnimationActionWithFile`**: Loads a timeline action from a CocosStudio exported binary file. The timeline contains keyframe animations for position, scale, rotation, opacity etc.
2. **`runAction(timeline)`**: Attaches the timeline to `dialogNode`.
3. **`gotoFrameAndPlay(0, true)`**: Starts playback from frame 0, looping (`true`). Use `false` for one-shot playback.

This is the CocosStudio workflow for UI animations - designers create animations visually, export as .csb, and code plays them."""),

    jl("""What does this code do?
```
var dir = cc.pNormalize(cc.pSub(target, source));
var dist = cc.pDistance(source, target);
```""",
       """This code calculates the direction and distance between two points:

1. **`cc.pSub(target, source)`**: Subtracts the source point from the target point, giving a vector pointing from source to target.
2. **`cc.pNormalize(...)`**: Normalizes that vector to unit length (magnitude 1), giving just the direction.
3. **`cc.pDistance(source, target)`**: Calculates the Euclidean distance between the two points.

This is commonly used in game AI: `dir` tells which way to move, `dist` tells how far away the target is. To move toward the target: `node.x += dir.x * speed * dt`."""),

    jl("""What does this code do?
```
widget.addTouchEventListener(function(sender, type) {
    if (type === ccui.Widget.TOUCH_ENDED) {
        cc.log('tapped');
    }
}, this);
```""",
       """This code adds a touch event listener to a ccui widget (button, image, etc.). The callback receives:
- **sender**: The widget that was touched.
- **type**: The touch phase - `TOUCH_BEGAN`, `TOUCH_MOVED`, `TOUCH_ENDED`, or `TOUCH_CANCELED`.

The code only responds to `TOUCH_ENDED`, which fires when the user lifts their finger while still on the widget (a successful tap). `TOUCH_CANCELED` would fire if the finger moved off the widget before lifting. The `this` parameter binds the callback's context."""),

    jl("""What does this code do?
```
draw.drawCircle(cc.p(160, 240), 80, 0, 32, false, 2, cc.color(255, 255, 0, 255));
```""",
       """This code draws a yellow hollow circle using a DrawNode:

- **center**: (160, 240)
- **radius**: 80 pixels
- **angle**: 0 radians (starting angle for the line-to-center)
- **segments**: 32 (number of line segments approximating the circle - higher = smoother)
- **drawLineToCenter**: `false` (don't draw a line from the edge to the center)
- **lineWidth**: 2 pixels
- **color**: Fully opaque yellow

With 32 segments the circle will appear smooth. The `drawLineToCenter` parameter, when true, would draw a radius line like a clock hand."""),

    jl("""What does this code do?
```
sprite.setFlippedX(true);
```""",
       """This code flips the sprite horizontally (mirrors it along the Y axis). The sprite's image is reversed left-to-right, but its position, anchor point, and children are unaffected. This is commonly used to make a character face left instead of right without needing a separate texture. To undo, call `setFlippedX(false)`. There is also `setFlippedY` for vertical flipping."""),

    jl("""What does this code do?
```
label.enableOutline(cc.color(0, 0, 0, 255), 2);
label.enableShadow(cc.color(0, 0, 0, 128), cc.size(2, -2), 0);
```""",
       """This code adds text effects to a label:

1. **`enableOutline`**: Adds a 2-pixel black opaque outline around each character. Works with TTF and system fonts.
2. **`enableShadow`**: Adds a drop shadow with semi-transparent black color, offset 2px right and 2px down (`cc.size(2, -2)`), and blur radius 0 (sharp shadow).

These effects improve text readability over busy backgrounds and are commonly used for game HUD text, titles, and score displays."""),

    jl("""What does this code do?
```
this.runAction(cc.follow(hero, cc.rect(0, 0, 2000, 320)));
```""",
       """This code makes the current node (typically a layer) follow the `hero` node as it moves, creating a camera-follow effect. The `cc.rect(0, 0, 2000, 320)` defines the boundary rectangle for the level - the camera won't scroll beyond these bounds. This means:

- The view stays centered on `hero` as it moves.
- The camera stops at the edges of the 2000x320 level so you never see outside the level boundaries.

This is the standard way to implement a scrolling camera in Cocos2d-x side-scrollers or top-down games."""),
]

# Add more explanations to get closer to 400
_extra_explanations = [
    jl("""What does this code do?
```
cc.textureCache.addImage('res/hero.png');
```""",
       """This code preloads the image `res/hero.png` into the texture cache. The texture is loaded into GPU memory so that when a sprite later uses this texture, it won't need to load from disk (avoiding a frame hitch). This is typically called during a loading screen to prepare assets before gameplay starts. The loaded texture can also be retrieved later with `cc.textureCache.getTextureForKey('res/hero.png')`."""),

    jl("""What does this code do?
```
node.pause();
```""",
       """This code pauses the node, which stops all of its scheduled callbacks (including `update`) and all running actions. The node remains visible and its children continue running unless they are also paused. Call `node.resume()` to restart the node's actions and scheduling. This is useful for freezing individual game objects, like pausing a specific enemy while the rest of the game continues."""),

    jl("""What does this code do?
```
cc.director.purgeCachedData();
```""",
       """This code purges all cached data managed by the director, including the texture cache, sprite frame cache, and animation cache. All textures are removed from GPU memory. This is a memory cleanup operation typically used during scene transitions when the next scene uses completely different assets. After purging, any sprites still referencing the old textures will display incorrectly until reloaded."""),

    jl("""What does this code do?
```
var track = hero.setAnimation(0, 'attack', false);
if (track) {
    track.timeScale = 2.0;
}
```""",
       """This code plays the 'attack' Spine animation once on track 0 and doubles its playback speed. `setAnimation` returns a `spine.TrackEntry` object that controls the specific animation instance. Setting `track.timeScale = 2.0` makes only this specific animation play at 2x speed, without affecting other tracks or the global time scale. If `setAnimation` returns null (e.g., animation name not found), the null check prevents an error."""),

    jl("""What does this code do?
```
node.enumerateChildren('enemy.*', function(child) {
    child.removeFromParent();
    return false;
});
```""",
       """This code finds and removes all children whose name matches the pattern `'enemy.*'` (names starting with 'enemy'). The `enumerateChildren` method searches the node's children using a name pattern with wildcard support. The callback receives each matching child and should return `false` to continue searching or `true` to stop. Here it removes each matched enemy node from its parent and continues until all matches are processed."""),

    jl("""What does this code do?
```
var gradient = new cc.LayerGradient(
    cc.color(30, 100, 200, 255),
    cc.color(5, 15, 40, 255),
    cc.p(0, -1)
);
```""",
       """This code creates a gradient background layer. The first color (light blue) is the start color, the second (dark blue) is the end color. The vector `cc.p(0, -1)` defines the gradient direction - pointing downward, so the gradient goes from light blue at the top to dark blue at the bottom. `cc.LayerGradient` extends `cc.LayerColor` which extends `cc.Layer`, so it fills the entire screen by default."""),

    jl("""What does this code do?
```
cc.spriteFrameCache.removeUnusedSpriteFrames();
cc.textureCache.removeUnusedTextures();
```""",
       """This code performs memory cleanup by removing cached assets that are no longer referenced:

1. **`removeUnusedSpriteFrames`**: Removes sprite frame definitions from the cache that have a reference count of 1 (only the cache itself holds them - no sprites are using them).
2. **`removeUnusedTextures`**: Removes GPU textures that are no longer referenced by any sprite or sprite frame.

This is a safe cleanup operation typically called during scene transitions to free memory from the previous scene's assets without removing still-in-use resources."""),

    jl("""What does this code do?
```
var multiplex = new cc.LayerMultiplex(menuLayer, settingsLayer);
scene.addChild(multiplex);
multiplex.switchTo(1);
```""",
       """This code creates a layer multiplexer that manages two layers but shows only one at a time:

1. Creates a `LayerMultiplex` with `menuLayer` (index 0) and `settingsLayer` (index 1).
2. Adds it to the scene.
3. **`switchTo(1)`** shows `settingsLayer` and removes `menuLayer` from the display.

Only the active layer is rendered and receives updates. Call `switchTo(0)` to switch back to the menu. `switchToAndReleaseMe(n)` would also release the current layer's memory."""),

    jl("""What does this code do?
```
hero.setAttachment('weapon_slot', 'sword');
```""",
       """This code shows the 'sword' attachment in the 'weapon_slot' slot of a Spine skeleton. Spine skeletons have named slots that can display different attachments (images/meshes). By setting the attachment to 'sword', the character visually equips a sword. Calling `hero.setAttachment('weapon_slot', null)` would hide the attachment (unequip). The slot name and attachment name must match what was defined in the Spine editor."""),

    jl("""What does this code do?
```
btn.setScale9Enabled(true);
btn.setSize(cc.size(200, 60));
btn.setCapInsets(cc.rect(10, 10, 2, 2));
```""",
       """This code enables 9-slice scaling on a button widget:

1. **`setScale9Enabled(true)`**: Enables 9-slice rendering so the button texture can stretch without distorting corners.
2. **`setSize(200, 60)`**: Sets the button to 200x60 pixels - it will scale using 9-slice rules.
3. **`setCapInsets(cc.rect(10, 10, 2, 2))`**: Defines the non-stretching border: 10px from left, 10px from top, 2px wide center, 2px tall center. The corners (10x10) stay fixed, edges stretch in one direction, and the center stretches both ways.

This is essential for UI buttons that need to work at different sizes without distorted corners."""),

    jl("""What does this code do?
```
cc.sys.openURL('https://example.com');
```""",
       """This code opens the URL `https://example.com` in the system's default browser. On mobile (iOS/Android), it switches to the browser app. On desktop, it opens the default web browser. On HTML5, it opens in a new tab. This is commonly used for "Rate Us" links, privacy policy pages, or external website links within the game."""),

    jl("""What does this code do?
```
var tex = sprite.getTexture();
tex.setTexParameters(gl.NEAREST, gl.NEAREST, gl.CLAMP_TO_EDGE, gl.CLAMP_TO_EDGE);
```""",
       """This code changes the texture filtering for a sprite to nearest-neighbor (point) sampling:

- **`gl.NEAREST`** (for both min and mag filters): Disables bilinear filtering, so when the texture is scaled up, pixels remain sharp and blocky instead of blurry. This is essential for pixel art games.
- **`gl.CLAMP_TO_EDGE`** (for both S and T wrap modes): Prevents texture coordinates outside [0,1] from wrapping/repeating - edge pixels are extended instead.

Without this, scaled pixel art looks blurry due to the default `gl.LINEAR` filtering."""),
]

CODE_EXPLANATION += _extra_explanations

# ---------------------------------------------------------------------------
# 4. REFACTORING / IMPROVEMENT  (~400)
# ---------------------------------------------------------------------------

REFACTORING = []

REFACTORING += [
    jl("""This works but can be improved:
```
node.runAction(cc.moveTo(1, cc.p(100,100)));
node.runAction(cc.scaleTo(1, 2.0));
```
How can I run these simultaneously?""",
       """Use `cc.spawn` to run actions in parallel instead of calling `runAction` twice:

```js
node.runAction(cc.spawn(
    cc.moveTo(1, cc.p(100, 100)),
    cc.scaleTo(1, 2.0)
));
```

Calling `runAction` twice creates two independent actions that happen to start at the same time but are managed separately. `cc.spawn` explicitly combines them into a single composite action that guarantees they run in parallel and finish together. This is cleaner, easier to chain in sequences, and the intent is clearer."""),

    jl("""This works but can be improved:
```
var label = cc.Label.createWithSystemFont('Score: 0', 'Arial', 24);
label.setPosition(240, 440);
label.setColor(cc.color(255, 220, 0));
label.setScale(1.0);
label.setOpacity(255);
label.setVisible(true);
this.addChild(label);
```
How can this be simplified?""",
       """Remove redundant calls (the defaults are already scale=1.0, opacity=255, visible=true) and use `setTextColor` instead of `setColor` for labels:

```js
var label = cc.Label.createWithSystemFont('Score: 0', 'Arial', 24);
label.setPosition(240, 440);
label.setTextColor(cc.color(255, 220, 0));
this.addChild(label);
```

For labels, `setTextColor` is preferred over `setColor` because it sets the text fill color directly. `setColor` tints the entire node including any effects. Also, you never need to set scale, opacity, or visibility to their default values."""),

    jl("""This works but can be improved:
```
if (cc.sys.platform === cc.sys.IPHONE || cc.sys.platform === cc.sys.IPAD || cc.sys.platform === cc.sys.ANDROID || cc.sys.platform === cc.sys.MOBILE_BROWSER) {
    enableTouchControls();
}
```
How can this be simplified?""",
       """Use `cc.sys.isMobile` which covers all mobile platforms:

```js
if (cc.sys.isMobile) {
    enableTouchControls();
}
```

`cc.sys.isMobile` returns `true` for iPhone, iPad, Android, and mobile browsers, making the check much simpler and more maintainable. It also handles any future mobile platforms automatically."""),

    jl("""This works but is verbose:
```
var sprite = new cc.Sprite('res/hero.png');
sprite.setPositionX(100);
sprite.setPositionY(200);
sprite.setScaleX(1.5);
sprite.setScaleY(1.5);
sprite.setOpacity(200);
this.addChild(sprite);
```
How can this be more concise?""",
       """Use `attr()` for batch property setting, and combined setters:

```js
var sprite = new cc.Sprite('res/hero.png');
sprite.attr({
    x: 100,
    y: 200,
    scale: 1.5,
    opacity: 200
});
this.addChild(sprite);
```

`attr()` sets multiple properties in one call. Also, `scale` sets both X and Y uniformly, and `setPosition(100, 200)` combines X and Y into one call. Direct property access (`sprite.x`, `sprite.scale`) is also faster than setter methods in JS."""),

    jl("""This works but leaks memory:
```
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    onTouchBegan: function(touch) { return true; }
}, this);
```
What's the problem and how to fix it?""",
       """The listener is never removed, which can cause a memory leak and receive events after the node is gone. Store the listener reference and remove it in `onExit`:

```js
var MyLayer = cc.Layer.extend({
    _touchListener: null,
    onEnter: function() {
        this._super();
        this._touchListener = cc.eventManager.addListener({
            event: cc.EventListener.TOUCH_ONE_BY_ONE,
            swallowTouches: true,
            onTouchBegan: function(touch) { return true; }
        }, this);
    },
    onExit: function() {
        cc.eventManager.removeListener(this._touchListener);
        this._super();
    }
});
```

When the listener is attached to a node (second param), Cocos2d-x auto-removes it when the node is removed from the scene. But explicitly removing it in `onExit` is the safest pattern."""),

    jl("""This code creates sprites inefficiently:
```
for (var i = 0; i < 100; i++) {
    var s = new cc.Sprite('res/bullet.png');
    s.setPosition(Math.random() * 480, Math.random() * 320);
    this.addChild(s);
}
```
How can this be optimized?""",
       """Use a `SpriteBatchNode` to render all sprites in a single draw call:

```js
var batch = new cc.SpriteBatchNode('res/bullet.png', 100);
this.addChild(batch);

for (var i = 0; i < 100; i++) {
    var s = new cc.Sprite('res/bullet.png');
    s.setPosition(Math.random() * 480, Math.random() * 320);
    batch.addChild(s);
}
```

With 100 individual sprites, you'd have 100 draw calls. A batch node renders all children sharing the same texture in a single draw call, which is dramatically faster. For even more sprites, consider also using an object pool to reuse sprites instead of creating new ones."""),

    jl("""This works but the transitions are jarring:
```
hero.setAnimation(0, 'idle', true);
// Later:
hero.setAnimation(0, 'walk', true);
// Later:
hero.setAnimation(0, 'run', true);
```
How can I make animation transitions smoother?""",
       """Use `setMix` to define blend durations between animation pairs:

```js
// Set up blending once at initialization
hero.setMix('idle', 'walk', 0.2);
hero.setMix('walk', 'idle', 0.2);
hero.setMix('walk', 'run', 0.3);
hero.setMix('run', 'walk', 0.3);
hero.setMix('run', 'idle', 0.2);

hero.setAnimation(0, 'idle', true);
// Later transitions will blend smoothly:
hero.setAnimation(0, 'walk', true); // 0.2s blend
hero.setAnimation(0, 'run', true);  // 0.3s blend
```

`setMix` tells Spine to cross-fade between the two animations over the specified duration instead of switching instantly, resulting in smooth natural transitions."""),

    jl("""This works but duplicates the centering logic:
```
var sprite1 = new cc.Sprite('res/a.png');
sprite1.setPosition(cc.director.getWinSize().width / 2, cc.director.getWinSize().height / 2);
this.addChild(sprite1);

var sprite2 = new cc.Sprite('res/b.png');
sprite2.setPosition(cc.director.getWinSize().width / 2, cc.director.getWinSize().height / 2);
this.addChild(sprite2);
```
How can this be improved?""",
       """Cache the window size and center coordinates:

```js
var winSize = cc.director.getWinSize();
var cx = winSize.width / 2;
var cy = winSize.height / 2;

var sprite1 = new cc.Sprite('res/a.png');
sprite1.setPosition(cx, cy);
this.addChild(sprite1);

var sprite2 = new cc.Sprite('res/b.png');
sprite2.setPosition(cx, cy);
this.addChild(sprite2);
```

`cc.director.getWinSize()` creates a new `cc.Size` object each call. Caching it avoids redundant object creation and makes the code cleaner. You could also use `setNormalizedPosition(cc.p(0.5, 0.5))` for truly responsive centering."""),

    jl("""This sound code is messy:
```
cc.audioEngine.playEffect('res/audio/sfx_hit.mp3');
cc.audioEngine.playEffect('res/audio/sfx_hit.mp3');
cc.audioEngine.playEffect('res/audio/sfx_coin.mp3');
cc.audioEngine.setEffectsVolume(0.5);
```
How should this be organized?""",
       """Create a sound manager with constants and preloading:

```js
var SFX = {
    HIT: 'res/audio/sfx_hit.mp3',
    COIN: 'res/audio/sfx_coin.mp3'
};

// Preload at startup
function preloadAudio() {
    for (var key in SFX) {
        cc.audioEngine.preloadEffect(SFX[key]);
    }
}

// Set volume once
cc.audioEngine.setEffectsVolume(0.5);

// Play by name
cc.audioEngine.playEffect(SFX.HIT);
cc.audioEngine.playEffect(SFX.COIN);
```

This avoids string duplication, makes it easy to rename files, ensures preloading for instant playback, and sets the volume once instead of implicitly relying on default state."""),

    jl("""This code updates the score label every frame even when it hasn't changed:
```
update: function(dt) {
    this._scoreLabel.setString('Score: ' + this._score);
}
```
How can this be improved?""",
       """Only update the label when the score actually changes:

```js
addScore: function(pts) {
    this._score += pts;
    this._scoreLabel.setString('Score: ' + this._score);
},
update: function(dt) {
    // Game logic only - no label update needed
}
```

`setString` triggers text re-rendering (glyph layout, texture generation for TTF fonts) which is expensive. Updating it every frame (60 times/second) wastes CPU/GPU time when the score rarely changes. Instead, update the label only when the score changes in the setter method."""),

    jl("""This uses separate variables for each UI element:
```
var btn1 = new ccui.Button('res/btn.png');
btn1.setPosition(100, 200);
btn1.setTitleText('Option 1');
btn1.addClickEventListener(function() { selectOption(1); });
this.addChild(btn1);

var btn2 = new ccui.Button('res/btn.png');
btn2.setPosition(200, 200);
btn2.setTitleText('Option 2');
btn2.addClickEventListener(function() { selectOption(2); });
this.addChild(btn2);

var btn3 = new ccui.Button('res/btn.png');
btn3.setPosition(300, 200);
btn3.setTitleText('Option 3');
btn3.addClickEventListener(function() { selectOption(3); });
this.addChild(btn3);
```
How can this be refactored?""",
       """Use a loop with a data array to eliminate repetition:

```js
var options = ['Option 1', 'Option 2', 'Option 3'];
var buttons = [];

for (var i = 0; i < options.length; i++) {
    var btn = new ccui.Button('res/btn.png');
    btn.setPosition(100 + i * 100, 200);
    btn.setTitleText(options[i]);
    btn.addClickEventListener((function(idx) {
        return function() { selectOption(idx + 1); };
    })(i));
    this.addChild(btn);
    buttons.push(btn);
}
```

This scales to any number of options, avoids code duplication, and uses a closure to capture the correct index for each button's callback. Adding a new option only requires adding a string to the array."""),

    jl("""This code manually checks collision with each enemy:
```
if (cc.rectOverlapsRect(hero.getBoundingBox(), enemy1.getBoundingBox())) handleHit(enemy1);
if (cc.rectOverlapsRect(hero.getBoundingBox(), enemy2.getBoundingBox())) handleHit(enemy2);
if (cc.rectOverlapsRect(hero.getBoundingBox(), enemy3.getBoundingBox())) handleHit(enemy3);
```
How can this be improved?""",
       """Use an array and loop, and cache the hero's bounding box:

```js
var enemies = [enemy1, enemy2, enemy3]; // or build dynamically
var heroBox = hero.getBoundingBox();

for (var i = 0; i < enemies.length; i++) {
    if (cc.rectOverlapsRect(heroBox, enemies[i].getBoundingBox())) {
        handleHit(enemies[i]);
    }
}
```

Key improvements: (1) Cache `hero.getBoundingBox()` since it recalculates each call. (2) Use an array for scalability - works with any number of enemies. (3) When enemies are added/removed dynamically, just manage the array instead of adding new if-statements."""),

    jl("""This creates actions repeatedly in the update loop:
```
update: function(dt) {
    if (this._isMoving) {
        this._hero.runAction(cc.moveBy(dt, cc.p(100 * dt, 0)));
    }
}
```
How should continuous movement be done?""",
       """Move the node directly instead of creating a new action every frame:

```js
update: function(dt) {
    if (this._isMoving) {
        this._hero.x += 100 * dt;
    }
}
```

Creating a new `cc.moveBy` action every frame is wasteful - it allocates a new object 60 times/second and the action manager must manage each one. For continuous movement in an update loop, directly modify the position property. Actions are better for fire-and-forget animations (move to X over 1 second), not for per-frame position updates."""),

    jl("""This code loads resources synchronously at the start of a scene:
```
var GameLayer = cc.Layer.extend({
    ctor: function() {
        this._super();
        // This blocks until loaded
        cc.spriteFrameCache.addSpriteFrames('res/game.plist', 'res/game.png');
        this.startGame();
    }
});
```
How can this be improved with a loading screen?""",
       """Add a loading scene that preloads resources before transitioning:

```js
var LoadingScene = cc.Scene.extend({
    onEnter: function() {
        this._super();
        var label = cc.Label.createWithSystemFont('Loading...', 'Arial', 24);
        label.setPosition(cc.director.getWinSize().width / 2, 160);
        this.addChild(label);

        // Preload asynchronously
        cc.loader.load(['res/game.plist', 'res/game.png'], function(err) {
            cc.spriteFrameCache.addSpriteFrames('res/game.plist', 'res/game.png');
            cc.director.runScene(new GameScene());
        });
    }
});
```

This shows a loading screen while resources load, preventing the app from appearing frozen. The game scene constructor can then assume all assets are ready."""),

    jl("""This timer code uses a raw counter:
```
var elapsed = 0;
this.schedule(function(dt) {
    elapsed += dt;
    if (elapsed >= 5.0) {
        doSomething();
        elapsed = 0;
    }
}, 0);
```
How can this be simplified?""",
       """Use the built-in interval parameter of `schedule`:

```js
this.schedule(function(dt) {
    doSomething();
}, 5.0);
```

The `schedule` method's second parameter is the interval in seconds. The scheduler handles the timing internally, which is more efficient than checking elapsed time every frame. For a one-shot delay, use `scheduleOnce`:

```js
this.scheduleOnce(function() {
    doSomething();
}, 5.0);
```"""),

    jl("""This code stores game state with multiple localStorage calls:
```
cc.sys.localStorage.setItem('name', 'Alice');
cc.sys.localStorage.setItem('level', '5');
cc.sys.localStorage.setItem('score', '1000');
cc.sys.localStorage.setItem('coins', '50');
```
How can this be improved?""",
       """Store all data as a single JSON object:

```js
var gameData = {
    name: 'Alice',
    level: 5,
    score: 1000,
    coins: 50
};
cc.sys.localStorage.setItem('gameData', JSON.stringify(gameData));

// Load:
var raw = cc.sys.localStorage.getItem('gameData');
var data = raw ? JSON.parse(raw) : { name: '', level: 1, score: 0, coins: 0 };
```

Benefits: (1) One I/O operation instead of four. (2) Atomic save - all data is consistent. (3) Easy to add new fields. (4) Numbers stay typed after parsing (no need to parseInt each value)."""),

    jl("""This code creates a new sprite every time an enemy dies for the death effect:
```
function onEnemyDied(enemy) {
    var explosion = new cc.Sprite('res/explosion.png');
    explosion.setPosition(enemy.getPosition());
    this.addChild(explosion);
    explosion.runAction(cc.sequence(cc.fadeOut(0.5), cc.removeSelf()));
}
```
How can this be optimized for many deaths?""",
       """Use an object pool to recycle explosion sprites:

```js
var ExplosionPool = {
    _pool: [],
    get: function(parent) {
        var sprite;
        if (this._pool.length > 0) {
            sprite = this._pool.pop();
            sprite.setVisible(true);
            sprite.setOpacity(255);
            sprite.stopAllActions();
        } else {
            sprite = new cc.Sprite('res/explosion.png');
            parent.addChild(sprite);
        }
        return sprite;
    },
    recycle: function(sprite) {
        sprite.setVisible(false);
        sprite.stopAllActions();
        this._pool.push(sprite);
    }
};

function onEnemyDied(enemy) {
    var fx = ExplosionPool.get(this);
    fx.setPosition(enemy.getPosition());
    fx.runAction(cc.sequence(
        cc.fadeOut(0.5),
        cc.callFunc(function() { ExplosionPool.recycle(fx); })
    ));
}
```

Object pooling avoids garbage collection spikes from constantly creating and destroying nodes, which is critical for smooth gameplay during intense combat."""),

    jl("""This hard-codes screen positions:
```
btn.setPosition(240, 400);
title.setPosition(240, 300);
```
How can this be more responsive?""",
       """Use the window size for relative positioning:

```js
var ws = cc.director.getWinSize();

// Center horizontally, near top
btn.setPosition(ws.width / 2, ws.height * 0.83);
title.setPosition(ws.width / 2, ws.height * 0.625);
```

Or use normalized positions for fully responsive layout:

```js
btn.setNormalizedPosition(cc.p(0.5, 0.83));
title.setNormalizedPosition(cc.p(0.5, 0.625));
```

Hard-coded positions break on different screen sizes. Using ratios of the window size ensures the layout adapts to any resolution. `setNormalizedPosition` is the cleanest approach when the parent size is known."""),

    jl("""This code has many magic numbers:
```
sprite.setPosition(240, 160);
sprite.setScale(1.5);
enemy.setPosition(400, 280);
this.schedule(this.spawn, 3.0);
label.setFontSize(24);
```
How should this be refactored?""",
       """Extract magic numbers to named constants:

```js
var SCREEN_CENTER_X = cc.director.getWinSize().width / 2;
var SCREEN_CENTER_Y = cc.director.getWinSize().height / 2;
var HERO_SCALE = 1.5;
var ENEMY_SPAWN_X = 400;
var ENEMY_SPAWN_Y = 280;
var SPAWN_INTERVAL = 3.0;
var HUD_FONT_SIZE = 24;

sprite.setPosition(SCREEN_CENTER_X, SCREEN_CENTER_Y);
sprite.setScale(HERO_SCALE);
enemy.setPosition(ENEMY_SPAWN_X, ENEMY_SPAWN_Y);
this.schedule(this.spawn, SPAWN_INTERVAL);
label.setFontSize(HUD_FONT_SIZE);
```

Named constants make the code self-documenting, easy to tune, and prevent errors from changing a number in one place but not another."""),

    jl("""This code checks collisions between all pairs of enemies:
```
for (var i = 0; i < enemies.length; i++) {
    for (var j = 0; j < enemies.length; j++) {
        if (i !== j) {
            if (cc.rectOverlapsRect(enemies[i].getBoundingBox(), enemies[j].getBoundingBox())) {
                handleCollision(enemies[i], enemies[j]);
            }
        }
    }
}
```
How can this be improved?""",
       """Start the inner loop from `i + 1` to avoid checking each pair twice:

```js
for (var i = 0; i < enemies.length; i++) {
    var boxA = enemies[i].getBoundingBox();
    for (var j = i + 1; j < enemies.length; j++) {
        if (cc.rectOverlapsRect(boxA, enemies[j].getBoundingBox())) {
            handleCollision(enemies[i], enemies[j]);
        }
    }
}
```

This halves the number of checks (from N*N to N*(N-1)/2) by only checking each pair once, and caches `boxA` to avoid recalculating it for every inner iteration. For large numbers of enemies, consider spatial partitioning (grid-based) for further optimization."""),

    jl("""This code creates identical buttons with slightly different positions:
```
var btn1 = new ccui.Button('res/btn.png');
btn1.setPosition(80, 200);
btn1.setTitleText('Easy');
btn1.setTitleFontSize(18);
btn1.addClickEventListener(function() { startGame('easy'); });
this.addChild(btn1);
// ... repeat for Medium, Hard
```
How can this be refactored using a helper function?""",
       """Extract a factory function:

```js
function createMenuButton(parent, text, x, y, callback) {
    var btn = new ccui.Button('res/btn.png');
    btn.setPosition(x, y);
    btn.setTitleText(text);
    btn.setTitleFontSize(18);
    btn.addClickEventListener(callback);
    parent.addChild(btn);
    return btn;
}

var difficulties = [
    { text: 'Easy',   x: 80,  mode: 'easy'   },
    { text: 'Medium', x: 200, mode: 'medium' },
    { text: 'Hard',   x: 320, mode: 'hard'   }
];

difficulties.forEach(function(d) {
    createMenuButton(this, d.text, d.x, 200, function() {
        startGame(d.mode);
    });
}, this);
```

The factory function eliminates duplication, and the data-driven approach makes it trivial to add or modify difficulty options."""),
]

# Add more refactoring to reach ~400
_extra_refactoring = [
    jl("""This code uses string concatenation for the score:
```
label.setString('Score: ' + score + ' / Level: ' + level + ' / Lives: ' + lives);
```
How can this be cleaner?""",
       """Use template-style formatting or separate labels:

```js
// Option 1: cc.formatStr (if available) or simple template
label.setString('Score: ' + score + '  |  Level: ' + level + '  |  Lives: ' + lives);

// Option 2 (recommended): Separate labels for separate concerns
scoreLabel.setString('Score: ' + score);
levelLabel.setString('Level: ' + level);
livesLabel.setString('Lives: ' + lives);
```

Separate labels are better because: (1) each can be positioned and styled independently, (2) updating one value doesn't re-render the entire string, and (3) it's easier to animate individual values (e.g., flash the lives label red when hit)."""),

    jl("""This code checks for null before every operation:
```
if (hero !== null) {
    if (hero.getPosition() !== null) {
        var pos = hero.getPosition();
        if (pos.x !== null && pos.y !== null) {
            hero.setPosition(pos.x + 10, pos.y);
        }
    }
}
```
How can this be simplified?""",
       """Most of these null checks are unnecessary in Cocos2d-x:

```js
if (hero) {
    hero.x += 10;
}
```

`getPosition()` always returns a valid `cc.Point`, and `x`/`y` are always numbers (never null). The only check needed is whether `hero` itself exists. Using the direct `x` property is also faster than calling `getPosition()` and then `setPosition()`. Defensive programming is good, but checking for impossible null states adds noise and hides real logic."""),

    jl("""This animation code repeats the same pattern:
```
cc.spriteFrameCache.addSpriteFrames('res/hero.plist', 'res/hero.png');
var runFrames = [];
for (var i = 1; i <= 8; i++) runFrames.push(cc.spriteFrameCache.getSpriteFrame('run_0' + i + '.png'));
var runAnim = new cc.Animation(runFrames, 0.08);

var idleFrames = [];
for (var i = 1; i <= 4; i++) idleFrames.push(cc.spriteFrameCache.getSpriteFrame('idle_0' + i + '.png'));
var idleAnim = new cc.Animation(idleFrames, 0.12);
```
How can this be refactored?""",
       """Extract a reusable animation builder:

```js
function buildAnimation(prefix, count, delay) {
    var frames = [];
    for (var i = 1; i <= count; i++) {
        var name = prefix + (i < 10 ? '0' : '') + i + '.png';
        frames.push(cc.spriteFrameCache.getSpriteFrame(name));
    }
    return new cc.Animation(frames, delay);
}

cc.spriteFrameCache.addSpriteFrames('res/hero.plist', 'res/hero.png');
var runAnim  = buildAnimation('run_',  8, 0.08);
var idleAnim = buildAnimation('idle_', 4, 0.12);
var jumpAnim = buildAnimation('jump_', 6, 0.10);
```

The helper function eliminates duplicated frame-loading logic and makes it trivial to add new animations in one line each."""),

    jl("""This touch handler doesn't properly handle multiple UI elements:
```
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    onTouchBegan: function(touch) {
        var loc = touch.getLocation();
        if (cc.rectContainsPoint(btn1.getBoundingBox(), loc)) handleBtn1();
        if (cc.rectContainsPoint(btn2.getBoundingBox(), loc)) handleBtn2();
        if (cc.rectContainsPoint(btn3.getBoundingBox(), loc)) handleBtn3();
        return true;
    }
}, this);
```
What's wrong and how to fix it?""",
       """Problems: (1) A single touch could hit overlapping buttons simultaneously. (2) Manual hit testing on raw nodes - should use ccui widgets. (3) The listener always returns true, swallowing all touches.

Use `ccui.Button` widgets instead, which handle hit testing, visual feedback, and touch exclusivity automatically:

```js
var buttons = [
    { name: 'btn1', handler: handleBtn1 },
    { name: 'btn2', handler: handleBtn2 },
    { name: 'btn3', handler: handleBtn3 }
];

buttons.forEach(function(b) {
    var btn = new ccui.Button('res/' + b.name + '.png');
    btn.addClickEventListener(b.handler);
    this.addChild(btn);
}, this);
```

ccui widgets have built-in touch handling with proper event swallowing - only one button responds per touch."""),

    jl("""This code nests too many callbacks:
```
hero.runAction(cc.sequence(
    cc.moveTo(1, cc.p(200, 200)),
    cc.callFunc(function() {
        hero.runAction(cc.sequence(
            cc.scaleTo(0.3, 1.5),
            cc.callFunc(function() {
                hero.runAction(cc.sequence(
                    cc.fadeOut(0.5),
                    cc.removeSelf()
                ));
            })
        ));
    })
));
```
How can this be flattened?""",
       """Flatten the nested sequences into a single sequence:

```js
hero.runAction(cc.sequence(
    cc.moveTo(1, cc.p(200, 200)),
    cc.scaleTo(0.3, 1.5),
    cc.fadeOut(0.5),
    cc.removeSelf()
));
```

`cc.sequence` can take any number of actions and runs them one after another. There's no need to nest sequences inside callFunc callbacks - that defeats the purpose of the action sequencing system. The flattened version is cleaner, more readable, and easier to modify."""),

    jl("""This code schedules an update but doesn't unschedule when done:
```
var GameLayer = cc.Layer.extend({
    ctor: function() {
        this._super();
        this.scheduleUpdate();
    },
    update: function(dt) {
        // game logic
    }
});
```
Is there anything wrong?""",
       """For most cases this is fine - `scheduleUpdate` is automatically cleaned up when the node is removed from the scene. However, if you need to stop the update earlier (e.g., game over), explicitly unschedule:

```js
var GameLayer = cc.Layer.extend({
    ctor: function() {
        this._super();
        this.scheduleUpdate();
    },
    update: function(dt) {
        if (this._gameOver) return; // guard clause
        // game logic
    },
    onGameOver: function() {
        this._gameOver = true;
        this.unscheduleUpdate(); // stop the update loop
    }
});
```

The improvement here is the cleanup pattern: stop the update when game logic no longer needs it. A guard clause alone wastes cycles calling an empty function 60 times/second."""),

    jl("""This code re-creates the DrawNode every frame:
```
update: function(dt) {
    var draw = new cc.DrawNode();
    this.addChild(draw);
    draw.drawCircle(cc.p(240, 160), 50, 0, 32, false, 2, cc.color.RED);
}
```
What's wrong?""",
       """This creates a new DrawNode and adds it as a child every single frame (60 times/second), causing massive node accumulation and memory leaks. Instead, create the DrawNode once and use `clear()` to redraw:

```js
onEnter: function() {
    this._super();
    this._draw = new cc.DrawNode();
    this.addChild(this._draw);
    this.scheduleUpdate();
},
update: function(dt) {
    this._draw.clear(); // erase previous frame's drawings
    this._draw.drawCircle(cc.p(240, 160), 50, 0, 32, false, 2, cc.color.RED);
}
```

Create the DrawNode once in `onEnter`, then call `clear()` each frame before redrawing. This is the correct pattern for dynamic DrawNode content."""),

    jl("""This uses setInterval for game timing:
```
setInterval(function() {
    spawnEnemy();
}, 3000);
```
What's wrong with this approach?""",
       """Using JavaScript's `setInterval` bypasses the Cocos2d-x scheduler system:

1. It doesn't respect `cc.director.pause()` or time scale changes.
2. It continues running after the scene is removed, causing errors.
3. It doesn't synchronize with the game loop frame timing.

Use the node's scheduler instead:

```js
this.schedule(function() {
    spawnEnemy();
}, 3.0);
```

The Cocos2d-x scheduler automatically pauses when the director pauses, respects `setTimeScale` for slow motion effects, and cleans up when the node is removed from the scene."""),

    jl("""This code uses numbers for tags:
```
sprite.setTag(1);
label.setTag(2);
enemy.setTag(3);
var found = this.getChildByTag(2);
```
How can this be more readable?""",
       """Use named constants or the `setName`/`getChildByName` API:

```js
// Option 1: Named constants for tags
var TAG = { HERO: 1, SCORE_LABEL: 2, ENEMY: 3 };
sprite.setTag(TAG.HERO);
label.setTag(TAG.SCORE_LABEL);
var found = this.getChildByTag(TAG.SCORE_LABEL);

// Option 2 (preferred): Use string names instead of numeric tags
sprite.setName('hero');
label.setName('scoreLabel');
enemy.setName('enemy');
var found = this.getChildByName('scoreLabel');
```

String names are self-documenting and don't require maintaining a separate constant table. `getChildByName` is the modern preferred approach over numeric tags."""),

    jl("""This creates separate listeners for each enemy:
```
for (var i = 0; i < enemies.length; i++) {
    cc.eventManager.addListener({
        event: cc.EventListener.TOUCH_ONE_BY_ONE,
        swallowTouches: true,
        onTouchBegan: function(touch, event) {
            return true;
        }
    }, enemies[i]);
}
```
What's the issue?""",
       """Each listener added via `addListener` with the same listener config object reuses the same internal listener. After the first `addListener`, subsequent calls fail silently or clone. Also, having many individual touch listeners is expensive.

Use a single listener with hit-testing:

```js
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    swallowTouches: true,
    onTouchBegan: function(touch) {
        var loc = touch.getLocation();
        for (var i = 0; i < enemies.length; i++) {
            if (cc.rectContainsPoint(enemies[i].getBoundingBox(), loc)) {
                handleEnemyTap(enemies[i]);
                return true;
            }
        }
        return false;
    }
}, this);
```

One listener checking all enemies is more efficient than N separate listeners, and the priority/swallowing behavior is clearer."""),

    jl("""This code has a long initialization method:
```
ctor: function() {
    this._super();
    var bg = new cc.Sprite('res/bg.png');
    bg.setPosition(240, 160);
    this.addChild(bg, -1);
    var hero = new cc.Sprite('res/hero.png');
    hero.setPosition(100, 160);
    this.addChild(hero, 1);
    var enemy1 = new cc.Sprite('res/enemy.png');
    enemy1.setPosition(350, 200);
    this.addChild(enemy1, 1);
    var label = cc.Label.createWithSystemFont('Score: 0', 'Arial', 24);
    label.setPosition(240, 440);
    this.addChild(label, 10);
    // ... 30 more lines
}
```
How can this be improved?""",
       """Break the initialization into focused helper methods:

```js
ctor: function() {
    this._super();
    this.initBackground();
    this.initPlayer();
    this.initEnemies();
    this.initHUD();
},
initBackground: function() {
    var bg = new cc.Sprite('res/bg.png');
    bg.setPosition(240, 160);
    this.addChild(bg, -1);
},
initPlayer: function() {
    this._hero = new cc.Sprite('res/hero.png');
    this._hero.setPosition(100, 160);
    this.addChild(this._hero, 1);
},
initEnemies: function() {
    this._enemies = [];
    // spawn initial enemies
},
initHUD: function() {
    this._scoreLabel = cc.Label.createWithSystemFont('Score: 0', 'Arial', 24);
    this._scoreLabel.setPosition(240, 440);
    this.addChild(this._scoreLabel, 10);
}
```

Each method is under 10 lines, has a clear responsibility, and the constructor reads like a high-level outline. This follows the single responsibility principle and keeps methods under 30 lines."""),
]

REFACTORING += _extra_refactoring


# ---------------------------------------------------------------------------
# PROGRAMMATIC GENERATORS — produce parameterized variations to reach ~2000
# ---------------------------------------------------------------------------

def gen_complete_snippets_parametric():
    """Generate complete snippet variations programmatically."""
    results = []

    # --- Action variations ---
    move_targets = [
        ("100, 200", "100", "200"), ("300, 400", "300", "400"),
        ("50, 50", "50", "50"), ("400, 100", "400", "100"),
        ("240, 320", "240", "320"), ("160, 240", "160", "240"),
        ("350, 150", "350", "150"), ("200, 400", "200", "400"),
    ]
    durations = ["0.3", "0.5", "0.8", "1.0", "1.5", "2.0"]
    easings = [
        ("cc.easeBounceOut()", "bounce ease-out"),
        ("cc.easeBackOut()", "back ease-out"),
        ("cc.easeElasticOut()", "elastic ease-out"),
        ("cc.easeSineInOut()", "sine ease-in-out"),
        ("cc.easeExponentialOut()", "exponential ease-out"),
        ("cc.easeQuadraticActionOut()", "quadratic ease-out"),
        ("cc.easeCubicActionOut()", "cubic ease-out"),
        ("cc.easeIn(2.0)", "ease-in with rate 2"),
        ("cc.easeOut(3.0)", "ease-out with rate 3"),
    ]

    for tx, ty_name, _ in move_targets[:6]:
        dur = pick(durations)
        ease_code, ease_name = pick(easings)
        results.append(jl(
            f"Write a complete example of moving a sprite to ({tx}) over {dur} seconds with {ease_name} easing.",
            f"""```js
// Move sprite to ({tx}) with {ease_name} easing
var sprite = new cc.Sprite('res/hero.png');
sprite.setPosition(240, 160);
this.addChild(sprite);
sprite.runAction(cc.moveTo({dur}, cc.p({tx})).easing({ease_code}));
```"""))

    # --- Scale + fade combos ---
    scale_vals = ["0.5", "1.2", "1.5", "2.0", "0.8", "1.8", "3.0"]
    fade_vals = ["0", "50", "100", "150", "200", "255"]
    for sv in scale_vals:
        fv = pick(fade_vals)
        dur = pick(durations)
        results.append(jl(
            f"Write a complete example of scaling a sprite to {sv}x and fading to opacity {fv} simultaneously over {dur} seconds.",
            f"""```js
// Scale and fade simultaneously
var sprite = new cc.Sprite('res/icon.png');
sprite.setPosition(240, 160);
this.addChild(sprite);

sprite.runAction(cc.spawn(
    cc.scaleTo({dur}, {sv}),
    cc.fadeTo({dur}, {fv})
));
```"""))

    # --- Rotate variations ---
    angles = ["45", "90", "180", "270", "360", "720"]
    for angle in angles:
        dur = pick(durations)
        results.append(jl(
            f"Write a complete example of rotating a sprite by {angle} degrees over {dur} seconds.",
            f"""```js
// Rotate sprite by {angle} degrees
var sprite = new cc.Sprite('res/gear.png');
sprite.setPosition(240, 160);
this.addChild(sprite);
sprite.runAction(cc.rotateBy({dur}, {angle}));
```"""))

    # --- Jump variations ---
    heights = ["50", "80", "100", "120", "150"]
    jumps = ["1", "2", "3", "4", "5"]
    for h in heights:
        j = pick(jumps)
        results.append(jl(
            f"Write a complete example of making a sprite jump with height {h} and {j} bounces.",
            f"""```js
// Character jumps with height {h} and {j} bounces
var hero = new cc.Sprite('res/hero.png');
hero.setPosition(100, 100);
this.addChild(hero);
hero.runAction(cc.jumpTo(1.5, cc.p(300, 100), {h}, {j}));
```"""))

    # --- Blink variations ---
    blink_counts = ["3", "5", "7", "10"]
    for bc in blink_counts:
        dur = pick(durations)
        results.append(jl(
            f"Write a complete example of blinking a sprite {bc} times over {dur} seconds.",
            f"""```js
// Blink a sprite {bc} times
var sprite = new cc.Sprite('res/powerup.png');
sprite.setPosition(240, 200);
this.addChild(sprite);
sprite.runAction(cc.blink({dur}, {bc}));
```"""))

    # --- Tint variations ---
    colors = [
        ("255, 0, 0", "red"), ("0, 255, 0", "green"), ("0, 0, 255", "blue"),
        ("255, 255, 0", "yellow"), ("255, 0, 255", "magenta"), ("0, 255, 255", "cyan"),
        ("255, 128, 0", "orange"), ("128, 0, 255", "purple"),
    ]
    for rgb, name in colors:
        dur = pick(durations)
        results.append(jl(
            f"Write a complete example of tinting a sprite to {name} over {dur} seconds.",
            f"""```js
// Tint sprite to {name}
var sprite = new cc.Sprite('res/hero.png');
sprite.setPosition(240, 160);
this.addChild(sprite);
sprite.runAction(cc.tintTo({dur}, {rgb}));
```"""))

    # --- Label style variations ---
    fonts = ["Arial", "Impact", "Helvetica", "Times New Roman", "Verdana"]
    sizes = ["18", "24", "32", "36", "48"]
    texts = ["SCORE", "GAME OVER", "READY?", "LEVEL UP!", "VICTORY!", "PAUSED",
             "COMBO!", "NEW HIGH SCORE!", "TAP TO START", "LOADING..."]
    outline_sizes = ["1", "2", "3", "4"]
    for text in texts:
        font = pick(fonts)
        size = pick(sizes)
        cr, cg, cb = random.randint(100, 255), random.randint(100, 255), random.randint(0, 255)
        os = pick(outline_sizes)
        results.append(jl(
            f"Write a complete example of creating a label showing '{text}' with {font} font, size {size}, colored and outlined.",
            f"""```js
// Styled label: '{text}'
var label = cc.Label.createWithSystemFont('{text}', '{font}', {size});
label.setPosition(cc.director.getWinSize().width / 2, 240);
label.setTextColor(cc.color({cr}, {cg}, {cb}));
label.enableOutline(cc.color(0, 0, 0, 255), {os});
this.addChild(label);
```"""))

    # --- Audio variations ---
    sfx_files = ["sfx_jump.mp3", "sfx_coin.mp3", "sfx_hit.mp3", "sfx_explosion.mp3",
                 "sfx_powerup.mp3", "sfx_click.mp3", "sfx_death.mp3", "sfx_win.mp3"]
    bgm_files = ["bgm_menu.mp3", "bgm_battle.mp3", "bgm_boss.mp3", "bgm_peaceful.mp3",
                 "bgm_victory.mp3", "bgm_credits.mp3"]
    volumes = ["0.3", "0.5", "0.7", "0.8", "1.0"]
    for bgm in bgm_files:
        vol = pick(volumes)
        results.append(jl(
            f"Write a complete example of playing background music '{bgm}' at volume {vol}.",
            f"""```js
// Play background music at volume {vol}
cc.audioEngine.playMusic('res/audio/{bgm}', true);
cc.audioEngine.setMusicVolume({vol});
```"""))
    for sfx in sfx_files:
        results.append(jl(
            f"Write a complete example of preloading and playing the sound effect '{sfx}'.",
            f"""```js
// Preload and play sound effect
cc.audioEngine.preloadEffect('res/audio/{sfx}');
// Later, play it:
cc.audioEngine.playEffect('res/audio/{sfx}');
```"""))

    # --- DrawNode shape variations ---
    draw_colors = [
        ("255, 0, 0, 255", "red"), ("0, 255, 0, 255", "green"),
        ("0, 0, 255, 255", "blue"), ("255, 255, 0, 255", "yellow"),
        ("255, 128, 0, 255", "orange"), ("200, 0, 255, 255", "purple"),
    ]
    radii = ["30", "50", "80", "100", "120"]
    for r in radii:
        col_code, col_name = pick(draw_colors)
        results.append(jl(
            f"Write a complete example of drawing a {col_name} circle with radius {r} using DrawNode.",
            f"""```js
// Draw a {col_name} circle with radius {r}
var draw = new cc.DrawNode();
this.addChild(draw);
draw.drawCircle(
    cc.p(240, 160), {r}, 0, 36, false, 2,
    cc.color({col_code})
);
```"""))

    # --- Spine skin variations ---
    skins = ["default", "warrior", "mage", "archer", "knight", "thief", "healer"]
    anims = ["idle", "walk", "run", "attack", "jump", "die", "cast", "block"]
    for skin in skins:
        anim = pick(anims)
        results.append(jl(
            f"Write a complete example of loading a Spine skeleton, setting '{skin}' skin and playing '{anim}' animation.",
            f"""```js
// Spine skeleton with '{skin}' skin playing '{anim}'
var skel = new sp.SkeletonAnimation('res/char/char.json', 'res/char/char.atlas');
skel.setPosition(240, 80);
skel.setSkin('{skin}');
skel.setAnimation(0, '{anim}', true);
this.addChild(skel);
```"""))

    # --- Scene transition variations ---
    transitions = [
        ("cc.TransitionFade", "fade"),
        ("cc.TransitionSlideInR", "slide-in from right"),
        ("cc.TransitionSlideInL", "slide-in from left"),
        ("cc.TransitionSlideInT", "slide-in from top"),
        ("cc.TransitionSlideInB", "slide-in from bottom"),
    ]
    scenes = ["GameScene", "MenuScene", "LevelSelectScene", "ShopScene", "SettingsScene"]
    for tr_cls, tr_name in transitions:
        scene = pick(scenes)
        dur = pick(["0.3", "0.5", "0.8"])
        results.append(jl(
            f"Write a complete example of transitioning to {scene} with a {tr_name} effect over {dur} seconds.",
            f"""```js
// Transition to {scene} with {tr_name}
var scene = new cc.Scene();
scene.addChild(new {scene}Layer());
cc.director.runScene(new {tr_cls}({dur}, scene));
```"""))

    # --- Schedule interval variations ---
    intervals = ["0.5", "1.0", "2.0", "3.0", "5.0", "10.0"]
    tasks = [
        ("spawn an enemy", "spawnEnemy", "var e = new cc.Sprite('res/enemy.png');\n        e.setPosition(480, Math.random() * 320);\n        this.addChild(e);"),
        ("spawn a coin", "spawnCoin", "var c = new cc.Sprite('res/coin.png');\n        c.setPosition(Math.random() * 480, 320);\n        this.addChild(c);"),
        ("increase difficulty", "rampDifficulty", "this._speed += 10;\n        cc.log('Speed increased to:', this._speed);"),
        ("check game state", "checkState", "if (this._enemies.length === 0) {\n            this.onWaveComplete();\n        }"),
    ]
    for interval in intervals[:4]:
        task_desc, task_fn, task_code = pick(tasks)
        results.append(jl(
            f"Write a complete example of scheduling a callback to {task_desc} every {interval} seconds.",
            f"""```js
// Schedule to {task_desc} every {interval} seconds
this.schedule(this.{task_fn}, {interval});

// The callback:
{task_fn}: function(dt) {{
    {task_code}
}}
```"""))

    # --- ccui Button variations ---
    btn_labels = ["PLAY", "RESTART", "QUIT", "SETTINGS", "SHOP", "NEXT LEVEL",
                  "RETRY", "CONTINUE", "PAUSE", "BACK", "OK", "CANCEL"]
    for label in btn_labels:
        sz = pick(sizes)
        results.append(jl(
            f"Write a complete example of creating a UI button labeled '{label}' with font size {sz}.",
            f"""```js
// UI button: '{label}'
var btn = new ccui.Button('res/btn_normal.png', 'res/btn_pressed.png');
btn.setTitleText('{label}');
btn.setTitleFontSize({sz});
btn.setTitleColor(cc.color.WHITE);
btn.setPosition(cc.director.getWinSize().width / 2, 200);
btn.addClickEventListener(function() {{
    cc.log('{label} button clicked');
}});
this.addChild(btn);
```"""))

    # --- localStorage variations ---
    data_keys = [
        ("highscore", "12500", "parseInt"),
        ("playerName", "'Hero'", ""),
        ("musicVolume", "0.7", "parseFloat"),
        ("currentLevel", "5", "parseInt"),
        ("totalCoins", "350", "parseInt"),
        ("soundEnabled", "true", ""),
    ]
    for key, default_val, parser in data_keys:
        parse_expr = f"{parser}(val)" if parser else "val"
        results.append(jl(
            f"Write a complete example of saving and loading '{key}' from local storage.",
            f"""```js
// Save '{key}' to local storage
cc.sys.localStorage.setItem('{key}', String({default_val}));

// Load '{key}' from local storage
var val = cc.sys.localStorage.getItem('{key}');
var {key} = val ? {parse_expr} : {default_val};
cc.log('{key}:', {key});
```"""))

    # --- Particle type variations ---
    particle_types = [
        ("cc.ParticleFire", "fire"),
        ("cc.ParticleExplosion", "explosion"),
        ("cc.ParticleSnow", "snow"),
        ("cc.ParticleSmoke", "smoke"),
        ("cc.ParticleRain", "rain"),
        ("cc.ParticleSun", "sun"),
        ("cc.ParticleGalaxy", "galaxy"),
        ("cc.ParticleFlower", "flower"),
        ("cc.ParticleSpiral", "spiral"),
        ("cc.ParticleMeteor", "meteor"),
    ]
    for pcls, pname in particle_types:
        results.append(jl(
            f"Write a complete example of creating a {pname} particle effect.",
            f"""```js
// Create a {pname} particle effect
var particles = new {pcls}();
particles.setPosition(240, 160);
particles.setTexture(cc.textureCache.addImage('res/particle_{pname}.png'));
this.addChild(particles, 10);
```"""))

    # --- CCS armature animation variations ---
    ccs_anims = ["idle", "walk", "run", "attack", "jump", "die", "skill", "hit"]
    for anim_name in ccs_anims:
        loop = "-1" if anim_name in ["idle", "walk", "run"] else "0"
        loop_desc = "looping" if loop == "-1" else "once"
        results.append(jl(
            f"Write a complete example of playing the '{anim_name}' armature animation ({loop_desc}).",
            f"""```js
// Play '{anim_name}' armature animation {loop_desc}
ccs.armatureDataManager.addArmatureFileInfo('res/character/character.ExportJson');
var armature = ccs.Armature.create('character');
armature.setPosition(240, 160);
this.addChild(armature);
armature.animation.play('{anim_name}', -1, {loop});
```"""))

    # --- Sequence/spawn combo variations ---
    action_combos = [
        ("move then scale", "cc.moveTo(1.0, cc.p(300, 200))", "cc.scaleTo(0.3, 1.5)"),
        ("fade in then move", "cc.fadeIn(0.5)", "cc.moveTo(1.0, cc.p(240, 300))"),
        ("scale then rotate", "cc.scaleTo(0.5, 2.0)", "cc.rotateBy(1.0, 360)"),
        ("move then blink then fade out", "cc.moveTo(1.0, cc.p(200, 200))", "cc.blink(1.0, 5)"),
        ("jump then scale down", "cc.jumpBy(1.0, cc.p(0, 0), 80, 2)", "cc.scaleTo(0.3, 0.5)"),
    ]
    for desc, a1, a2 in action_combos:
        results.append(jl(
            f"Write a complete example of a sprite that runs a sequence: {desc}.",
            f"""```js
// Sequence: {desc}
var sprite = new cc.Sprite('res/item.png');
sprite.setPosition(100, 100);
this.addChild(sprite);
sprite.runAction(cc.sequence(
    {a1},
    {a2}
));
```"""))

    # --- Grid/3D effect variations ---
    grid_effects = [
        ("cc.shaky3D(2.0, cc.size(15, 10), 5, false)", "shaky 3D"),
        ("cc.waves(3.0, cc.size(15, 10), 5, 20, true, true)", "wave distortion"),
        ("cc.flipX3D(1.0)", "3D X flip"),
        ("cc.flipY3D(1.0)", "3D Y flip"),
        ("cc.liquid(3.0, cc.size(15, 10), 4, 20)", "liquid distortion"),
        ("cc.lens3D(3.0, cc.size(15, 10), cc.p(240, 160), 150)", "lens effect"),
        ("cc.ripple3D(3.0, cc.size(15, 10), cc.p(240, 160), 200, 5, 40)", "ripple effect"),
        ("cc.twirl(3.0, cc.size(15, 10), cc.p(240, 160), 2, 5)", "twirl effect"),
    ]
    for effect_code, effect_name in grid_effects:
        results.append(jl(
            f"Write a complete example of applying a {effect_name} grid action to a node.",
            f"""```js
// Apply {effect_name} grid action
var sprite = new cc.Sprite('res/background.png');
sprite.setPosition(240, 160);
this.addChild(sprite);
sprite.runAction({effect_code});
```"""))

    # --- Keyboard key handling variations ---
    key_actions = [
        ("cc.KEY.space", "jump", "hero.runAction(cc.jumpBy(0.5, cc.p(0, 0), 80, 1));"),
        ("cc.KEY.enter", "confirm selection", "this.confirmSelection();"),
        ("cc.KEY.escape", "open pause menu", "this.showPauseMenu();"),
        ("cc.KEY.a", "move left", "hero.x -= 10;"),
        ("cc.KEY.d", "move right", "hero.x += 10;"),
        ("cc.KEY.w", "move up", "hero.y += 10;"),
        ("cc.KEY.s", "move down", "hero.y -= 10;"),
    ]
    for key_code, key_desc, action_code in key_actions:
        results.append(jl(
            f"Write a complete example of handling a keyboard press to {key_desc}.",
            f"""```js
// Handle keyboard press to {key_desc}
cc.eventManager.addListener({{
    event: cc.EventListener.KEYBOARD,
    onKeyPressed: function(keyCode, event) {{
        if (keyCode === {key_code}) {{
            {action_code}
        }}
    }}
}}, this);
```"""))

    # --- Widget event type variations ---
    widget_types = [
        ("ccui.ImageView", "ccui.ImageView('res/portrait.png')", "image view"),
        ("ccui.Text", "ccui.Text('Tap me', 'Arial', 20)", "text widget"),
    ]
    for cls, ctor, desc in widget_types:
        results.append(jl(
            f"Write a complete example of creating a touchable {desc} with click handling.",
            f"""```js
// Touchable {desc}
var widget = new {ctor};
widget.setPosition(240, 200);
widget.setTouchEnabled(true);
widget.addClickEventListener(function() {{
    cc.log('{desc} tapped!');
}});
this.addChild(widget);
```"""))

    # --- Color presets usage ---
    color_presets = [
        "cc.color.WHITE", "cc.color.BLACK", "cc.color.RED",
        "cc.color.GREEN", "cc.color.BLUE", "cc.color.YELLOW",
    ]
    for cp in color_presets:
        results.append(jl(
            f"Write a complete example of setting a sprite's color to {cp}.",
            f"""```js
// Set sprite color to {cp}
var sprite = new cc.Sprite('res/icon.png');
sprite.setPosition(240, 160);
sprite.setColor({cp});
this.addChild(sprite);
```"""))

    # --- Node property batch set ---
    prop_combos = [
        {"x": 100, "y": 300, "scale": 2.0, "rotation": 45},
        {"x": 50, "y": 50, "opacity": 128, "visible": True},
        {"x": 400, "y": 200, "scaleX": -1, "scaleY": 1},
        {"x": 240, "y": 160, "anchorX": 0, "anchorY": 0},
    ]
    for props in prop_combos:
        props_str = ", ".join(f"{k}: {v}" for k, v in props.items())
        results.append(jl(
            f"Write a complete example of using node.attr() to set {{{props_str}}}.",
            f"""```js
// Set multiple properties with attr()
var sprite = new cc.Sprite('res/hero.png');
sprite.attr({{ {props_str} }});
this.addChild(sprite);
```"""))

    return results


def gen_completion_parametric():
    """Generate code completion variations."""
    results = []

    # --- Action completion templates ---
    action_templates = [
        {
            "setup": "var sprite = new cc.Sprite('res/star.png');\nsprite.setPosition(240, 160);\nthis.addChild(sprite);",
            "todo": "rotate 360 degrees and then remove itself",
            "solution": "sprite.runAction(cc.sequence(\n    cc.rotateBy(1.0, 360),\n    cc.removeSelf()\n));"
        },
        {
            "setup": "var label = cc.Label.createWithSystemFont('0', 'Arial', 36);\nlabel.setPosition(240, 400);\nlabel.setOpacity(0);\nthis.addChild(label);",
            "todo": "fade in the label over 0.5 seconds",
            "solution": "label.runAction(cc.fadeIn(0.5));"
        },
        {
            "setup": "var bg = new cc.Sprite('res/bg.png');\nbg.setPosition(240, 160);\nthis.addChild(bg);",
            "todo": "add a pulsing scale animation that loops forever",
            "solution": "bg.runAction(cc.repeatForever(cc.sequence(\n    cc.scaleTo(1.0, 1.05).easing(cc.easeSineInOut()),\n    cc.scaleTo(1.0, 1.0).easing(cc.easeSineInOut())\n)));"
        },
        {
            "setup": "var coin = new cc.Sprite('res/coin.png');\ncoin.setPosition(100, 300);\nthis.addChild(coin);",
            "todo": "move to (400, 300) while spinning 720 degrees",
            "solution": "coin.runAction(cc.spawn(\n    cc.moveTo(1.5, cc.p(400, 300)),\n    cc.rotateBy(1.5, 720)\n));"
        },
        {
            "setup": "var enemy = new cc.Sprite('res/enemy.png');\nenemy.setPosition(480, 200);\nthis.addChild(enemy);",
            "todo": "move left to x=-50 over 3 seconds then remove itself",
            "solution": "enemy.runAction(cc.sequence(\n    cc.moveTo(3.0, cc.p(-50, 200)),\n    cc.removeSelf()\n));"
        },
        {
            "setup": "var sprite = new cc.Sprite('res/ship.png');\nsprite.setPosition(240, 50);\nthis.addChild(sprite);",
            "todo": "jump to position (240, 50) with height 100 and 2 jumps",
            "solution": "sprite.runAction(cc.jumpTo(1.0, cc.p(240, 50), 100, 2));"
        },
        {
            "setup": "var title = cc.Label.createWithSystemFont('GAME OVER', 'Arial', 48);\ntitle.setPosition(240, 300);\ntitle.setScale(0);\nthis.addChild(title);",
            "todo": "scale up from 0 to 1.0 with a back ease-out effect",
            "solution": "title.runAction(cc.scaleTo(0.5, 1.0).easing(cc.easeBackOut()));"
        },
        {
            "setup": "var hero = new cc.Sprite('res/hero.png');\nhero.setPosition(240, 160);\nthis.addChild(hero);",
            "todo": "tint to red (damage), wait 0.2s, tint back to white",
            "solution": "hero.runAction(cc.sequence(\n    cc.tintTo(0.1, 255, 0, 0),\n    cc.delayTime(0.2),\n    cc.tintTo(0.1, 255, 255, 255)\n));"
        },
    ]

    for tmpl in action_templates:
        results.append(jl(
            f"""Complete this code to {tmpl['todo']}:
```
{tmpl['setup']}
// TODO: {tmpl['todo']}
```""",
            f"""```js
{tmpl['setup']}
// {tmpl['todo'].capitalize()}
{tmpl['solution']}
```"""))

    # --- UI completion templates ---
    ui_templates = [
        {
            "setup": "var panel = new ccui.Layout();\npanel.setSize(cc.size(300, 200));\npanel.setPosition(90, 140);",
            "todo": "add a solid dark background with 80% opacity",
            "solution": "panel.setBackGroundColorType(ccui.Layout.BG_COLOR_SOLID);\npanel.setBackGroundColor(cc.color(0, 0, 0));\npanel.setBackGroundColorOpacity(200);\nthis.addChild(panel);"
        },
        {
            "setup": "var tf = new ccui.TextField('Enter name...', 'Arial', 18);\ntf.setPosition(240, 200);",
            "todo": "enable password mode and set max length to 20",
            "solution": "tf.setPasswordEnabled(true);\ntf.setMaxLengthEnabled(true);\ntf.setMaxLength(20);\nthis.addChild(tf);"
        },
        {
            "setup": "var bar = new ccui.LoadingBar('res/hp_bar.png', 100);\nbar.setPosition(240, 440);",
            "todo": "set bar to 60% and make it fill from left to right",
            "solution": "bar.setPercent(60);\nbar.setDirection(ccui.LoadingBar.TYPE_LEFT);\nthis.addChild(bar);"
        },
    ]
    for tmpl in ui_templates:
        results.append(jl(
            f"""Complete this code to {tmpl['todo']}:
```
{tmpl['setup']}
// TODO: {tmpl['todo']}
```""",
            f"""```js
{tmpl['setup']}
// {tmpl['todo'].capitalize()}
{tmpl['solution']}
```"""))

    # --- Audio completion ---
    audio_templates = [
        {
            "setup": "// Music is playing",
            "todo": "pause all audio when game pauses, resume when unpaused",
            "solution": "function onPause() {\n    cc.audioEngine.pauseMusic();\n    cc.audioEngine.pauseAllEffects();\n}\nfunction onResume() {\n    cc.audioEngine.resumeMusic();\n    cc.audioEngine.resumeAllEffects();\n}"
        },
        {
            "setup": "// About to load level assets",
            "todo": "preload 3 sound effects for the level",
            "solution": "cc.audioEngine.preloadEffect('res/audio/sfx_jump.mp3');\ncc.audioEngine.preloadEffect('res/audio/sfx_coin.mp3');\ncc.audioEngine.preloadEffect('res/audio/sfx_hit.mp3');"
        },
    ]
    for tmpl in audio_templates:
        results.append(jl(
            f"""Complete this code to {tmpl['todo']}:
```
{tmpl['setup']}
// TODO: {tmpl['todo']}
```""",
            f"""```js
{tmpl['setup']}
// {tmpl['todo'].capitalize()}
{tmpl['solution']}
```"""))

    # --- Scene/Director completion ---
    scene_templates = [
        {
            "setup": "var scene = new cc.Scene();\nscene.addChild(new GameLayer());",
            "todo": "run this scene with a fade transition of 0.5 seconds",
            "solution": "cc.director.runScene(new cc.TransitionFade(0.5, scene));"
        },
        {
            "setup": "// Game is running",
            "todo": "pause the director and show 'PAUSED' label",
            "solution": "cc.director.pause();\nvar pauseLabel = cc.Label.createWithSystemFont('PAUSED', 'Arial', 48);\npauseLabel.setPosition(cc.director.getWinSize().width / 2, cc.director.getWinSize().height / 2);\nthis.addChild(pauseLabel, 100);"
        },
    ]
    for tmpl in scene_templates:
        results.append(jl(
            f"""Complete this code to {tmpl['todo']}:
```
{tmpl['setup']}
// TODO: {tmpl['todo']}
```""",
            f"""```js
{tmpl['setup']}
// {tmpl['todo'].capitalize()}
{tmpl['solution']}
```"""))

    # --- Spine completion ---
    spine_templates = [
        {
            "setup": "var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');\nhero.setPosition(240, 80);\nthis.addChild(hero);",
            "todo": "play 'attack' once then queue 'idle' to loop",
            "solution": "hero.setAnimation(0, 'attack', false);\nhero.addAnimation(0, 'idle', true, 0);"
        },
        {
            "setup": "var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');\nhero.setPosition(240, 80);\nthis.addChild(hero);",
            "todo": "set time scale to half speed for slow motion",
            "solution": "hero.setTimeScale(0.5);"
        },
        {
            "setup": "var hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas');\nhero.setPosition(240, 80);\nthis.addChild(hero);\nhero.setAnimation(0, 'idle', true);",
            "todo": "listen for animation complete events",
            "solution": "hero.setAnimationListener(this, function(track, type, event) {\n    if (type === sp.AnimationEventType.COMPLETE) {\n        cc.log('Animation complete:', track.animation.name);\n    }\n});"
        },
    ]
    for tmpl in spine_templates:
        results.append(jl(
            f"""Complete this code to {tmpl['todo']}:
```
{tmpl['setup']}
// TODO: {tmpl['todo']}
```""",
            f"""```js
{tmpl['setup']}
// {tmpl['todo'].capitalize()}
{tmpl['solution']}
```"""))

    # --- DrawNode completion ---
    draw_templates = [
        {
            "setup": "var draw = new cc.DrawNode();\nthis.addChild(draw);",
            "todo": "draw a filled red rectangle from (50,50) to (200,150)",
            "solution": "draw.drawRect(\n    cc.p(50, 50), cc.p(200, 150),\n    cc.color(255, 0, 0, 200),\n    2, cc.color(200, 0, 0, 255)\n);"
        },
        {
            "setup": "var draw = new cc.DrawNode();\nthis.addChild(draw);",
            "todo": "draw a green line from (0,0) to (480,320)",
            "solution": "draw.drawSegment(\n    cc.p(0, 0), cc.p(480, 320),\n    2, cc.color(0, 255, 0, 255)\n);"
        },
        {
            "setup": "var draw = new cc.DrawNode();\nthis.addChild(draw);",
            "todo": "draw a blue quadratic bezier from (50,100) through control (240,300) to (430,100)",
            "solution": "draw.drawQuadBezier(\n    cc.p(50, 100), cc.p(240, 300), cc.p(430, 100),\n    30, 2, cc.color(0, 100, 255, 255)\n);"
        },
    ]
    for tmpl in draw_templates:
        results.append(jl(
            f"""Complete this code to {tmpl['todo']}:
```
{tmpl['setup']}
// TODO: {tmpl['todo']}
```""",
            f"""```js
{tmpl['setup']}
// {tmpl['todo'].capitalize()}
{tmpl['solution']}
```"""))

    # --- Node lifecycle completion ---
    lifecycle_templates = [
        {
            "setup": "var MyLayer = cc.Layer.extend({\n    ctor: function() {\n        this._super();\n    }",
            "todo": "add onEnter that schedules update, and update that moves hero right",
            "solution": "var MyLayer = cc.Layer.extend({\n    ctor: function() {\n        this._super();\n        this._hero = new cc.Sprite('res/hero.png');\n        this._hero.setPosition(50, 160);\n        this.addChild(this._hero);\n    },\n    onEnter: function() {\n        this._super();\n        this.scheduleUpdate();\n    },\n    update: function(dt) {\n        this._hero.x += 100 * dt;\n        if (this._hero.x > 500) this._hero.x = -20;\n    }\n});"
        },
    ]
    for tmpl in lifecycle_templates:
        results.append(jl(
            f"""Complete this code to {tmpl['todo']}:
```
{tmpl['setup']}
// TODO: {tmpl['todo']}
```""",
            f"""```js
{tmpl['solution']}
```"""))

    # --- Parametric completion: various easing combinations ---
    easing_names = [
        ("cc.easeSineIn()", "sine ease-in"),
        ("cc.easeSineOut()", "sine ease-out"),
        ("cc.easeBackIn()", "back ease-in"),
        ("cc.easeBackOut()", "back ease-out"),
        ("cc.easeBounceOut()", "bounce ease-out"),
        ("cc.easeBounceIn()", "bounce ease-in"),
        ("cc.easeElasticOut(0.3)", "elastic ease-out"),
        ("cc.easeExponentialIn()", "exponential ease-in"),
        ("cc.easeExponentialOut()", "exponential ease-out"),
    ]
    for ease_code, ease_name in easing_names:
        results.append(jl(
            f"""Complete this code to apply {ease_name} to the move action:
```
var sprite = new cc.Sprite('res/box.png');
sprite.setPosition(50, 160);
this.addChild(sprite);
var move = cc.moveTo(1.0, cc.p(400, 160));
// TODO: apply {ease_name} and run
```""",
            f"""```js
var sprite = new cc.Sprite('res/box.png');
sprite.setPosition(50, 160);
this.addChild(sprite);
var move = cc.moveTo(1.0, cc.p(400, 160));
// Apply {ease_name} and run
sprite.runAction(move.easing({ease_code}));
```"""))

    # --- Parametric: create various widget types ---
    widget_creates = [
        ("ccui.CheckBox", "new ccui.CheckBox('res/cb_bg.png', 'res/cb_bg_sel.png', 'res/cb_cross.png', '', '')", "checkbox", "cb.addEventListener(function(sender) {\n    cc.log('Checked:', sender.isSelected());\n}, this);"),
        ("ccui.Slider", "new ccui.Slider()", "slider", "slider.loadBarTexture('res/slider_bar.png');\nslider.loadSlidBallTextures('res/slider_ball.png', 'res/slider_ball.png', '');\nslider.loadProgressBarTexture('res/slider_progress.png');\nslider.setPercent(50);\nslider.addEventListener(function(sender) {\n    cc.log('Percent:', sender.getPercent());\n}, this);"),
    ]
    for cls, ctor, desc, event_code in widget_creates:
        results.append(jl(
            f"""Complete this code to create a {desc} and handle its events:
```
// TODO: create a {desc} at (240, 200) and add event listener
```""",
            f"""```js
// Create a {desc} at (240, 200) and add event listener
var widget = {ctor};
widget.setPosition(240, 200);
{event_code}
this.addChild(widget);
```"""))

    return results


def gen_explanation_parametric():
    """Generate code explanation variations."""
    results = []

    # --- Simple action explanations ---
    action_explanations = [
        {
            "code": "node.runAction(cc.repeat(cc.rotateBy(1.0, 360), 3));",
            "explanation": "This code rotates `node` by 360 degrees (one full spin) over 1 second, and repeats that spin exactly 3 times. After 3 rotations (3 seconds total), the action completes. Unlike `cc.repeatForever`, `cc.repeat` runs a finite number of times."
        },
        {
            "code": "node.runAction(cc.reverseTime(cc.moveBy(1.0, cc.p(100, 0))));",
            "explanation": "This code plays the move action in reverse - instead of moving right 100px, the node starts at the end position and moves back to its starting position over 1 second. `cc.reverseTime` reverses the time progression of any finite-time action."
        },
        {
            "code": "sprite.setDisplayFrameWithAnimationName('run', 3);",
            "explanation": "This code sets the sprite's display to the 4th frame (index 3, zero-based) of the animation named 'run'. The animation must have been previously added to the animation cache. This is useful for showing a specific frame without playing the full animation."
        },
        {
            "code": "var s9 = new ccui.Scale9Sprite('res/panel.png');\ns9.setCapInsets(cc.rect(10, 10, 2, 2));\ns9.setContentSize(cc.size(300, 200));",
            "explanation": "This creates a 9-slice scalable sprite from 'panel.png'. The cap insets define a 10px border on each side that won't stretch. When setContentSize resizes it to 300x200, the corners stay pixel-perfect while the edges and center stretch to fill. This is the standard approach for scalable UI panels and buttons."
        },
        {
            "code": "cc.director.convertToGL(cc.p(100, 50));",
            "explanation": "This converts a UI coordinate point (100, 50) to OpenGL coordinate space. In Cocos2d-x, the GL coordinate system has the origin at bottom-left with Y going up, while UI coordinates (as from browser events) have origin at top-left with Y going down. This method flips the Y axis for proper positioning."
        },
        {
            "code": "var result = cc.pMidpoint(cc.p(100, 200), cc.p(300, 400));",
            "explanation": "This calculates the midpoint between two points (100,200) and (300,400), resulting in cc.p(200, 300). `cc.pMidpoint` is a vector math utility that returns the average of two points - useful for finding the center between two objects, or the middle of a line segment."
        },
        {
            "code": "node.scheduleUpdateWithPriority(10);",
            "explanation": "This schedules the node's `update(dt)` method to be called every frame, with a priority of 10. Lower priority numbers execute first. The default priority for `scheduleUpdate()` is 0. Higher priority (like 10) means this node's update runs after nodes with lower priority values, useful for ordering physics before rendering."
        },
        {
            "code": "var frame = cc.spriteFrameCache.getSpriteFrame('hero_01.png');\nvar newFrame = new cc.SpriteFrame(frame.getTexture(), cc.rect(0, 0, 32, 32));",
            "explanation": "This retrieves a sprite frame from the cache, then creates a new SpriteFrame using the same texture but with a custom rectangle (0,0,32,32). The new frame references only a 32x32 pixel region of the original texture. This is useful for manually defining sub-regions of a texture without a plist file."
        },
        {
            "code": "cc.loader.loadJson('res/config.json', function(err, data) {\n    if (!err) cc.log(data.version);\n});",
            "explanation": "This asynchronously loads and parses a JSON file at 'res/config.json'. When loading completes, the callback receives an error (null on success) and the parsed JSON data as a JavaScript object. This is used for loading configuration files, level data, or localization strings at runtime."
        },
        {
            "code": "armature.animation.playWithNames(['idle', 'walk', 'run'], 5, true);",
            "explanation": "This plays a sequence of CocosStudio armature animations in order: 'idle', then 'walk', then 'run'. The `5` is the durationTo parameter (5 frames of blending between each animation), and `true` means loop the entire sequence. When 'run' finishes, it blends back to 'idle' and repeats."
        },
        {
            "code": "var letter = label.getLetter(0);\nletter.runAction(cc.scaleTo(0.1, 1.5));",
            "explanation": "This gets the first character (index 0) of a BMFont or TTF label as an individual cc.Sprite, then runs a scale action on it. Each letter in a non-system-font label can be individually animated. This enables effects like wave animations, per-character color changes, or drop-in letter reveals."
        },
        {
            "code": "label.enableCubicBezierCurves(\n    cc.p(0, 0), cc.p(100, 200), cc.p(200, 200), cc.p(300, 0), 1, 50\n);",
            "explanation": "This arranges the label's text along a cubic bezier curve path. The four points define the curve: start(0,0), control1(100,200), control2(200,200), end(300,0). The `1` is center alignment along the curve, and `50` is the number of segments for smoothness. Each character is positioned and rotated to follow the curve."
        },
    ]
    for item in action_explanations:
        results.append(jl(
            f"""What does this code do?
```
{item['code']}
```""",
            item['explanation']))

    # --- Parametric: simple one-liner explanations ---
    one_liners = [
        ("node.stopAllActions();", "This immediately stops and removes all actions currently running on the node. Any in-progress movements, fades, rotations, etc. are halted at their current state. The node remains at whatever position/scale/opacity it had when the actions were stopped."),
        ("node.cleanup();", "This stops all actions and unschedules all callbacks on this node and all its children recursively. It's called automatically when a node is removed from its parent with cleanup=true (the default). Manually calling it prepares a node for reuse or disposal."),
        ("node.removeFromParent();", "This removes the node from its parent's children list, with cleanup enabled by default (stops all actions and schedules). After this call, the node is no longer part of the scene graph and won't be rendered or updated."),
        ("cc.director.popToRootScene();", "This pops all scenes from the scene stack until only the root (first) scene remains, and makes it the active scene. Used to return directly to the main menu from any depth of nested pushed scenes."),
        ("cc.audioEngine.end();", "This completely shuts down the audio engine - stops all music and sound effects, releases all audio resources from memory. Typically called when the game exits or when performing a full audio system reset."),
        ("cc.sys.garbageCollect();", "This forces a JavaScript garbage collection cycle. Only works in JSB (native) builds, not in HTML5. Useful after releasing many large resources (textures, audio) to immediately reclaim memory rather than waiting for automatic GC."),
        ("sprite.setBatchNode(batch);", "This assigns the sprite to a SpriteBatchNode. Once assigned, the sprite must share the same texture as the batch node and will be rendered in the batch's single draw call. The sprite becomes a child of the batch node for rendering purposes."),
        ("node.setGlobalZOrder(100);", "This sets the node's global Z-order to 100, which overrides the local Z-order for rendering. Nodes with higher global Z-order are drawn on top regardless of their parent hierarchy. A value of 0 (default) means the local Z-order is used instead."),
        ("cc.rectIntersection(rectA, rectB);", "This returns a new cc.Rect representing the overlapping area between two rectangles. If the rectangles don't overlap, the result has zero width and height. Useful for calculating the exact collision area between two axis-aligned bounding boxes."),
        ("cc.degreesToRadians(90);", "This converts 90 degrees to radians (approximately 1.5708). Cocos2d-x uses degrees for most rotation APIs, but some math functions and trigonometry require radians. The equivalent formula is `90 * Math.PI / 180`."),
    ]
    for code, expl in one_liners:
        results.append(jl(
            f"""What does this code do?
```
{code}
```""",
            expl))

    # --- Parametric: pattern explanations ---
    patterns = [
        {
            "code": "this.scheduleOnce(function() {\n    this.loadNextLevel();\n}.bind(this), 3.0);",
            "explanation": "This schedules `loadNextLevel()` to be called once after a 3-second delay. The `.bind(this)` ensures that `this` inside the callback refers to the layer/node, not the global scope. `scheduleOnce` automatically unschedules itself after firing, unlike `schedule` which repeats. This is commonly used for delayed transitions or timed events."
        },
        {
            "code": "var size = cc.director.getWinSize();\nvar safe = cc.director.getSafeAreaRect();\nvar btn = new ccui.Button('res/btn.png');\nbtn.setPosition(safe.x + safe.width - 40, safe.y + safe.height - 40);",
            "explanation": "This positions a button in the top-right corner of the safe area, accounting for notched/cutout devices. `getWinSize()` returns the full window, while `getSafeAreaRect()` returns the rectangle that avoids the device notch, rounded corners, and system UI bars. The button is placed 40px from the right and top edges of the safe area."
        },
        {
            "code": "var blend = new cc.BlendFunc(cc.SRC_ALPHA, cc.ONE_MINUS_SRC_ALPHA);\nsprite.setBlendFunc(blend);",
            "explanation": "This sets the sprite's blend function to standard alpha blending (the default). Source pixels are multiplied by their alpha, and destination pixels are multiplied by (1 - source alpha). This is normal transparency: a pixel with 50% alpha shows half the sprite color and half the background color. Setting this explicitly is useful after changing to additive blending to restore normal transparency."
        },
    ]
    for item in patterns:
        results.append(jl(
            f"""What does this code do?
```
{item['code']}
```""",
            item['explanation']))

    return results


def gen_refactoring_parametric():
    """Generate refactoring/improvement variations."""
    results = []

    refactoring_items = [
        {
            "code": "node.setPosition(240, 160);\nnode.setScale(1.0);\nnode.setRotation(0);\nnode.setOpacity(255);\nnode.setVisible(true);",
            "problem": "This sets properties to their default values unnecessarily",
            "improved": "node.setPosition(240, 160);\n// scale=1, rotation=0, opacity=255, visible=true are all defaults - no need to set them",
            "explanation": "Remove all calls that set properties to their default values. New nodes already have scale=1, rotation=0, opacity=255, and visible=true. Setting defaults wastes CPU cycles and clutters the code."
        },
        {
            "code": "sprite.runAction(cc.moveTo(1, cc.p(200, 200)));\nsprite.runAction(cc.fadeOut(1));\nsprite.runAction(cc.scaleTo(1, 2));",
            "problem": "Three separate runAction calls for simultaneous actions",
            "improved": "sprite.runAction(cc.spawn(\n    cc.moveTo(1, cc.p(200, 200)),\n    cc.fadeOut(1),\n    cc.scaleTo(1, 2)\n));",
            "explanation": "Use `cc.spawn` to run all three actions as a single composite action. This is semantically clearer (explicitly parallel) and easier to wrap in sequences or other composites."
        },
        {
            "code": "var x = cc.director.getWinSize().width;\nvar y = cc.director.getWinSize().height;\nvar cx = cc.director.getWinSize().width / 2;\nvar cy = cc.director.getWinSize().height / 2;",
            "problem": "getWinSize() called 4 times creating 4 temporary objects",
            "improved": "var ws = cc.director.getWinSize();\nvar x = ws.width;\nvar y = ws.height;\nvar cx = ws.width / 2;\nvar cy = ws.height / 2;",
            "explanation": "Cache the result of `getWinSize()` in a local variable. Each call creates a new cc.Size object. Calling it once and reusing the reference is cleaner and avoids unnecessary object creation."
        },
        {
            "code": "if (hp > 0) {\n    if (hp > 50) {\n        bar.setColor(cc.color(0, 255, 0));\n    } else if (hp > 25) {\n        bar.setColor(cc.color(255, 255, 0));\n    } else {\n        bar.setColor(cc.color(255, 0, 0));\n    }\n}",
            "problem": "Deeply nested conditionals for health bar color",
            "improved": "if (hp > 0) {\n    var ratio = hp / maxHP;\n    var r = Math.floor(255 * (1 - ratio));\n    var g = Math.floor(255 * ratio);\n    bar.setColor(cc.color(r, g, 0));\n}",
            "explanation": "Replace the discrete color thresholds with a continuous interpolation based on the HP ratio. This produces a smooth color gradient from green (full health) through yellow (half) to red (low), is more concise, and automatically handles any HP value without needing new threshold branches."
        },
        {
            "code": "setTimeout(function() {\n    spawnEnemy();\n}, 3000);\nsetInterval(function() {\n    updateScore();\n}, 1000);",
            "problem": "Using JavaScript timers instead of Cocos2d-x scheduler",
            "improved": "this.scheduleOnce(function() {\n    spawnEnemy();\n}, 3.0);\nthis.schedule(function() {\n    updateScore();\n}, 1.0);",
            "explanation": "Use the Cocos2d-x scheduler instead of `setTimeout`/`setInterval`. The scheduler: (1) respects `cc.director.pause()`, (2) respects `setTimeScale` for slow motion, (3) auto-cleans when the node is removed, (4) syncs with the game loop. JavaScript timers continue running even when the game is paused or the scene is removed."
        },
        {
            "code": "for (var i = 0; i < 10; i++) {\n    var s = new cc.Sprite('res/particle.png');\n    s.setPosition(x + Math.random() * 50, y + Math.random() * 50);\n    this.addChild(s);\n    s.runAction(cc.sequence(cc.fadeOut(1.0), cc.removeSelf()));\n}",
            "problem": "Manually creating particle-like effects with sprites",
            "improved": "var particles = new cc.ParticleSystem('res/particles/burst.plist');\nparticles.setPosition(x, y);\nparticles.setAutoRemoveOnFinish(true);\nparticles.setDuration(0.1);\nthis.addChild(particles);",
            "explanation": "Use the built-in particle system instead of manually managing individual sprites. A ParticleSystem is GPU-accelerated, handles hundreds of particles efficiently, supports complex behaviors (gravity, wind, size/color changes), and auto-cleans when finished. Manual sprite particles are slow and limited."
        },
        {
            "code": "cc.log('x=' + hero.x + ' y=' + hero.y + ' hp=' + hp + ' score=' + score + ' level=' + level);",
            "problem": "Verbose string concatenation for debug logging",
            "improved": "cc.log('hero:', hero.x, hero.y, 'hp:', hp, 'score:', score, 'level:', level);",
            "explanation": "`cc.log` accepts multiple arguments like `console.log`, automatically separated by spaces. This is cleaner than manual string concatenation and handles non-string types (numbers, objects) without explicit conversion."
        },
        {
            "code": "node.setPosition(node.getPositionX() + 5, node.getPositionY() + 3);",
            "problem": "Verbose getter/setter for position modification",
            "improved": "node.x += 5;\nnode.y += 3;",
            "explanation": "Use direct property access (`node.x`, `node.y`) instead of getter/setter methods. Direct property access is not only shorter but also faster in JavaScript. The `.x` and `.y` properties are fully supported read/write properties on all cc.Node subclasses."
        },
        {
            "code": "var visible = node.isVisible();\nif (visible === true) {\n    node.setVisible(false);\n} else if (visible === false) {\n    node.setVisible(true);\n}",
            "problem": "Verbose visibility toggle",
            "improved": "node.setVisible(!node.isVisible());",
            "explanation": "A boolean toggle is simply `!currentValue`. The verbose version with explicit `=== true` and `=== false` comparisons is unnecessarily long. Alternatively, use the instant action: `node.runAction(cc.toggleVisibility())`."
        },
        {
            "code": "var data = cc.sys.localStorage.getItem('save');\nif (data !== null && data !== undefined && data !== '') {\n    var parsed = JSON.parse(data);\n}",
            "problem": "Overly defensive null/undefined/empty checking",
            "improved": "var data = cc.sys.localStorage.getItem('save');\nvar parsed = data ? JSON.parse(data) : null;",
            "explanation": "JavaScript's truthiness check handles null, undefined, and empty string in one expression. `data ? ... : null` returns null for all falsy values and parses only when valid data exists. This is the idiomatic JavaScript pattern for optional parsing."
        },
    ]

    for item in refactoring_items:
        results.append(jl(
            f"""This works but can be improved:
```
{item['code']}
```
{item['problem']}. How can this be improved?""",
            f"""{item['explanation']}

```js
{item['improved']}
```"""))

    # --- Parametric refactoring: repeated patterns ---
    repeated_patterns = [
        {
            "bad_code": "enemy1.runAction(cc.moveBy(2, cc.p(-400, 0)));\nenemy1.runAction(cc.sequence(cc.delayTime(2), cc.removeSelf()));\nenemy2.runAction(cc.moveBy(2, cc.p(-400, 0)));\nenemy2.runAction(cc.sequence(cc.delayTime(2), cc.removeSelf()));",
            "problem": "Duplicated action setup for multiple enemies",
            "fix": "function setupEnemyMovement(enemy) {\n    enemy.runAction(cc.sequence(\n        cc.moveBy(2, cc.p(-400, 0)),\n        cc.removeSelf()\n    ));\n}\nsetupEnemyMovement(enemy1);\nsetupEnemyMovement(enemy2);",
            "why": "Extract the repeated action setup into a reusable function. The move and remove can also be combined into a single sequence instead of two separate `runAction` calls."
        },
        {
            "bad_code": "cc.spriteFrameCache.addSpriteFrames('res/a.plist', 'res/a.png');\ncc.spriteFrameCache.addSpriteFrames('res/b.plist', 'res/b.png');\ncc.spriteFrameCache.addSpriteFrames('res/c.plist', 'res/c.png');\ncc.spriteFrameCache.addSpriteFrames('res/d.plist', 'res/d.png');",
            "problem": "Repetitive resource loading calls",
            "fix": "var atlases = ['a', 'b', 'c', 'd'];\natlases.forEach(function(name) {\n    cc.spriteFrameCache.addSpriteFrames('res/' + name + '.plist', 'res/' + name + '.png');\n});",
            "why": "Use a data-driven approach with an array and loop. Adding a new atlas only requires adding one string to the array. This pattern is especially powerful when the atlas list is loaded from a config file."
        },
        {
            "bad_code": "this.schedule(function() {\n    var e = new cc.Sprite('res/enemy.png');\n    e.setPosition(500, Math.random() * 320);\n    this.addChild(e);\n    e.runAction(cc.sequence(\n        cc.moveTo(4, cc.p(-50, e.y)),\n        cc.removeSelf()\n    ));\n}.bind(this), 2.0);",
            "problem": "Creating new sprites without recycling - causes GC spikes",
            "fix": "var EnemyPool = { _pool: [], get: function(p) {\n    if (this._pool.length > 0) { var e = this._pool.pop(); e.setVisible(true); e.stopAllActions(); return e; }\n    var e = new cc.Sprite('res/enemy.png'); p.addChild(e); return e;\n}, recycle: function(e) { e.setVisible(false); e.stopAllActions(); this._pool.push(e); } };\n\nthis.schedule(function() {\n    var e = EnemyPool.get(this);\n    e.setPosition(500, Math.random() * 320);\n    e.runAction(cc.sequence(\n        cc.moveTo(4, cc.p(-50, e.y)),\n        cc.callFunc(function() { EnemyPool.recycle(e); })\n    ));\n}.bind(this), 2.0);",
            "why": "Object pooling reuses sprite instances instead of creating and destroying them. This prevents garbage collection spikes that cause frame drops, especially on mobile devices with frequent enemy spawning."
        },
    ]

    for item in repeated_patterns:
        results.append(jl(
            f"""This code has a pattern that should be improved:
```
{item['bad_code']}
```
{item['problem']}. How can this be refactored?""",
            f"""{item['why']}

```js
{item['fix']}
```"""))

    return results


# ---------------------------------------------------------------------------
# BULK GENERATORS — cross-product approach for high volume
# ---------------------------------------------------------------------------

def gen_bulk_complete():
    """Generate many more complete snippets via cross-products."""
    results = []

    # --- Sprite + action combos (sprite file x action x easing) ---
    sprites = ["hero.png", "enemy.png", "coin.png", "bullet.png", "gem.png",
               "star.png", "box.png", "ball.png", "bird.png", "ship.png",
               "arrow.png", "shield.png", "potion.png", "bomb.png", "key.png"]
    positions = [
        ("50, 50", "bottom-left"), ("240, 160", "center"), ("400, 300", "top-right"),
        ("120, 400", "upper-left"), ("360, 80", "lower-right"), ("240, 50", "bottom-center"),
        ("240, 400", "top-center"), ("50, 160", "left-center"), ("430, 160", "right-center"),
    ]
    action_types = [
        ("move to ({tx}, {ty})",
         "cc.moveTo({dur}, cc.p({tx}, {ty}))"),
        ("move by ({dx}, {dy})",
         "cc.moveBy({dur}, cc.p({dx}, {dy}))"),
        ("scale to {sv}x",
         "cc.scaleTo({dur}, {sv})"),
        ("rotate by {angle} degrees",
         "cc.rotateBy({dur}, {angle})"),
        ("fade to opacity {opa}",
         "cc.fadeTo({dur}, {opa})"),
    ]
    easing_pool = [
        ("", ""), (".easing(cc.easeBounceOut())", " with bounce"),
        (".easing(cc.easeBackOut())", " with back ease-out"),
        (".easing(cc.easeSineInOut())", " with sine ease"),
        (".easing(cc.easeElasticOut())", " with elastic ease"),
    ]

    random.seed(42)
    combos_done = set()
    for _ in range(250):
        sp = pick(sprites)
        px, pname = pick(positions)
        at_desc, at_code = pick(action_types)
        ease_code, ease_name = pick(easing_pool)
        dur = pick(["0.3", "0.5", "0.8", "1.0", "1.5", "2.0"])
        tx, ty = str(random.randint(50, 430)), str(random.randint(50, 300))
        dx, dy = str(random.randint(-200, 200)), str(random.randint(-200, 200))
        sv = pick(["0.5", "1.2", "1.5", "2.0", "0.8"])
        angle = pick(["45", "90", "180", "360"])
        opa = pick(["0", "64", "128", "200", "255"])

        desc = at_desc.format(tx=tx, ty=ty, dx=dx, dy=dy, sv=sv, angle=angle, opa=opa)
        code = at_code.format(dur=dur, tx=tx, ty=ty, dx=dx, dy=dy, sv=sv, angle=angle, opa=opa)

        key = f"{sp}_{desc}_{ease_name}"
        if key in combos_done:
            continue
        combos_done.add(key)

        results.append(jl(
            f"Write a complete example of creating a '{sp}' sprite at {pname} and running {desc}{ease_name} over {dur}s.",
            f"""```js
// Create '{sp}' at {pname} and {desc}{ease_name}
var sprite = new cc.Sprite('res/{sp}');
sprite.setPosition({px});
this.addChild(sprite);
sprite.runAction({code}{ease_code});
```"""))

    # --- Sequence combos (action1 then action2) ---
    seq_actions = [
        ("move to center", "cc.moveTo(1.0, cc.p(240, 160))"),
        ("fade in", "cc.fadeIn(0.5)"),
        ("fade out", "cc.fadeOut(0.5)"),
        ("scale up to 1.5x", "cc.scaleTo(0.3, 1.5)"),
        ("scale down to 0.5x", "cc.scaleTo(0.3, 0.5)"),
        ("rotate 360 degrees", "cc.rotateBy(1.0, 360)"),
        ("blink 3 times", "cc.blink(0.5, 3)"),
        ("wait 1 second", "cc.delayTime(1.0)"),
        ("remove itself", "cc.removeSelf()"),
        ("show", "cc.show()"),
        ("hide", "cc.hide()"),
        ("jump in place", "cc.jumpBy(0.5, cc.p(0, 0), 50, 1)"),
    ]
    combos_done = set()
    for _ in range(200):
        a1_desc, a1_code = pick(seq_actions)
        a2_desc, a2_code = pick(seq_actions)
        if a1_desc == a2_desc:
            continue
        key = f"{a1_desc}_{a2_desc}"
        if key in combos_done:
            continue
        combos_done.add(key)
        sp = pick(sprites)

        results.append(jl(
            f"Write a complete example of a sprite that first does '{a1_desc}' then '{a2_desc}' in sequence.",
            f"""```js
// Sequence: {a1_desc} then {a2_desc}
var sprite = new cc.Sprite('res/{sp}');
sprite.setPosition(240, 160);
this.addChild(sprite);
sprite.runAction(cc.sequence(
    {a1_code},
    {a2_code}
));
```"""))

    # --- Spawn combos (action1 + action2 simultaneously) ---
    spawn_actions = [
        ("move to (300, 200)", "cc.moveTo(1.0, cc.p(300, 200))"),
        ("scale to 2x", "cc.scaleTo(1.0, 2.0)"),
        ("rotate by 180", "cc.rotateBy(1.0, 180)"),
        ("fade to 128", "cc.fadeTo(1.0, 128)"),
        ("tint to red", "cc.tintTo(1.0, 255, 0, 0)"),
        ("move by (100, 50)", "cc.moveBy(1.0, cc.p(100, 50))"),
    ]
    combos_done = set()
    for _ in range(80):
        a1_desc, a1_code = pick(spawn_actions)
        a2_desc, a2_code = pick(spawn_actions)
        if a1_desc == a2_desc:
            continue
        key = f"{a1_desc}+{a2_desc}"
        if key in combos_done:
            continue
        combos_done.add(key)
        sp = pick(sprites)

        results.append(jl(
            f"Write a complete example of a sprite that runs '{a1_desc}' and '{a2_desc}' simultaneously.",
            f"""```js
// Simultaneous: {a1_desc} + {a2_desc}
var sprite = new cc.Sprite('res/{sp}');
sprite.setPosition(150, 150);
this.addChild(sprite);
sprite.runAction(cc.spawn(
    {a1_code},
    {a2_code}
));
```"""))

    # --- Label variations (font x size x text x effects) ---
    fonts = ["Arial", "Impact", "Helvetica", "Verdana", "Georgia",
             "Courier New", "Times New Roman"]
    sizes = ["14", "18", "20", "24", "28", "32", "36", "48"]
    texts = ["Score: 0", "GAME OVER", "READY?", "Level 1", "VICTORY!",
             "PAUSED", "3", "2", "1", "GO!", "TAP TO START",
             "Loading...", "COMBO x5", "NEW RECORD!", "FAILED",
             "CONTINUE?", "BOSS FIGHT", "MISSION COMPLETE"]
    effects = [
        ("no effects", ""),
        ("black outline",
         "\nlabel.enableOutline(cc.color(0, 0, 0, 255), 2);"),
        ("drop shadow",
         "\nlabel.enableShadow(cc.color(0, 0, 0, 128), cc.size(2, -2), 0);"),
        ("outline and shadow",
         "\nlabel.enableOutline(cc.color(0, 0, 0, 255), 2);\nlabel.enableShadow(cc.color(0, 0, 0, 128), cc.size(2, -2), 0);"),
    ]
    combos_done = set()
    for _ in range(100):
        font = pick(fonts)
        sz = pick(sizes)
        text = pick(texts)
        eff_desc, eff_code = pick(effects)
        cr = random.randint(100, 255)
        cg = random.randint(100, 255)
        cb = random.randint(0, 200)
        key = f"{text}_{font}_{sz}_{eff_desc}"
        if key in combos_done:
            continue
        combos_done.add(key)

        results.append(jl(
            f"Write a complete example of a '{text}' label using {font} font at size {sz} with {eff_desc}.",
            f"""```js
// Label: '{text}' in {font} size {sz} with {eff_desc}
var label = cc.Label.createWithSystemFont('{text}', '{font}', {sz});
label.setPosition(cc.director.getWinSize().width / 2, 240);
label.setTextColor(cc.color({cr}, {cg}, {cb}));{eff_code}
this.addChild(label);
```"""))

    # --- DrawNode shape variations ---
    shapes = [
        ("a dot at ({x}, {y}) with radius {r}",
         "draw.drawDot(cc.p({x}, {y}), {r}, cc.color({cr}, {cg}, {cb}, 255));"),
        ("a line from ({x1}, {y1}) to ({x2}, {y2})",
         "draw.drawSegment(cc.p({x1}, {y1}), cc.p({x2}, {y2}), 2, cc.color({cr}, {cg}, {cb}, 255));"),
        ("a rectangle from ({x1}, {y1}) to ({x2}, {y2})",
         "draw.drawRect(cc.p({x1}, {y1}), cc.p({x2}, {y2}), cc.color({cr}, {cg}, {cb}, 128), 2, cc.color({cr}, {cg}, {cb}, 255));"),
        ("a circle at ({x}, {y}) with radius {r}",
         "draw.drawCircle(cc.p({x}, {y}), {r}, 0, 36, false, 2, cc.color({cr}, {cg}, {cb}, 255));"),
    ]
    color_names = [("red", 255, 0, 0), ("green", 0, 255, 0), ("blue", 0, 0, 255),
                   ("yellow", 255, 255, 0), ("white", 255, 255, 255), ("cyan", 0, 255, 255),
                   ("orange", 255, 165, 0), ("purple", 128, 0, 255)]
    combos_done = set()
    for _ in range(60):
        shape_desc, shape_code = pick(shapes)
        col_name, cr, cg, cb = pick(color_names)
        x, y = random.randint(50, 400), random.randint(50, 280)
        x1, y1 = random.randint(20, 200), random.randint(20, 150)
        x2, y2 = random.randint(250, 450), random.randint(160, 300)
        r = random.randint(5, 100)
        desc = shape_desc.format(x=x, y=y, x1=x1, y1=y1, x2=x2, y2=y2, r=r)
        code = shape_code.format(x=x, y=y, x1=x1, y1=y1, x2=x2, y2=y2, r=r, cr=cr, cg=cg, cb=cb)
        key = desc + col_name
        if key in combos_done:
            continue
        combos_done.add(key)

        results.append(jl(
            f"Write a complete example of drawing {desc} in {col_name} using DrawNode.",
            f"""```js
// Draw {desc} in {col_name}
var draw = new cc.DrawNode();
this.addChild(draw);
{code}
```"""))

    # --- Touch event + response combos ---
    touch_responses = [
        ("log the touch position", "cc.log('Touch at:', loc.x, loc.y);"),
        ("spawn a particle at the touch", "var p = new cc.ParticleExplosion();\n            p.setPosition(loc);\n            p.setAutoRemoveOnFinish(true);\n            this.addChild(p);"),
        ("move the hero to the touch position", "hero.runAction(cc.moveTo(0.5, loc));"),
        ("create a sprite at the touch position", "var s = new cc.Sprite('res/mark.png');\n            s.setPosition(loc);\n            this.addChild(s);"),
        ("play a sound effect", "cc.audioEngine.playEffect('res/audio/sfx_tap.mp3');"),
    ]
    for resp_desc, resp_code in touch_responses:
        results.append(jl(
            f"Write a complete example of a touch listener that will {resp_desc} on touch.",
            f"""```js
// Touch listener that will {resp_desc}
cc.eventManager.addListener({{
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    swallowTouches: true,
    onTouchBegan: function(touch, event) {{
        var loc = touch.getLocation();
        {resp_code}
        return true;
    }}
}}, this);
```"""))

    # --- Keyboard + game action combos ---
    key_game_combos = [
        ("cc.KEY.space", "space bar", "make the hero shoot a bullet",
         "var bullet = new cc.Sprite('res/bullet.png');\n        bullet.setPosition(hero.x + 20, hero.y);\n        this.addChild(bullet);\n        bullet.runAction(cc.sequence(cc.moveBy(1.0, cc.p(500, 0)), cc.removeSelf()));"),
        ("cc.KEY.up", "up arrow", "make the hero jump",
         "if (!this._jumping) {\n            this._jumping = true;\n            hero.runAction(cc.sequence(\n                cc.moveBy(0.3, cc.p(0, 80)).easing(cc.easeOut(2)),\n                cc.moveBy(0.3, cc.p(0, -80)).easing(cc.easeIn(2)),\n                cc.callFunc(function() { this._jumping = false; }.bind(this))\n            ));\n        }"),
        ("cc.KEY.p", "P key", "toggle pause",
         "if (cc.director.isPaused()) {\n            cc.director.resume();\n        } else {\n            cc.director.pause();\n        }"),
        ("cc.KEY.r", "R key", "restart the scene",
         "cc.director.runScene(new GameScene());"),
        ("cc.KEY.m", "M key", "toggle music",
         "if (cc.audioEngine.isMusicPlaying()) {\n            cc.audioEngine.pauseMusic();\n        } else {\n            cc.audioEngine.resumeMusic();\n        }"),
        ("cc.KEY.f", "F key", "toggle fullscreen stats",
         "var showing = cc.director.isDisplayStats();\n        cc.director.setDisplayStats(!showing);"),
    ]
    for key_code, key_name, action_desc, action_code in key_game_combos:
        results.append(jl(
            f"Write a complete example of pressing {key_name} to {action_desc}.",
            f"""```js
// Press {key_name} to {action_desc}
cc.eventManager.addListener({{
    event: cc.EventListener.KEYBOARD,
    onKeyPressed: function(keyCode, event) {{
        if (keyCode === {key_code}) {{
            {action_code}
        }}
    }}
}}, this);
```"""))

    # --- ccui widget property combos ---
    btn_configs = [
        {"label": "START", "size": "24", "color": "cc.color(255, 255, 255)", "action": "start the game"},
        {"label": "RETRY", "size": "20", "color": "cc.color(255, 200, 0)", "action": "restart the level"},
        {"label": "EXIT", "size": "18", "color": "cc.color(200, 200, 200)", "action": "quit to menu"},
        {"label": "NEXT", "size": "22", "color": "cc.color(100, 255, 100)", "action": "go to next level"},
        {"label": "BUY", "size": "20", "color": "cc.color(255, 215, 0)", "action": "purchase the item"},
        {"label": "EQUIP", "size": "18", "color": "cc.color(150, 200, 255)", "action": "equip the item"},
        {"label": "UPGRADE", "size": "20", "color": "cc.color(0, 255, 200)", "action": "upgrade the skill"},
        {"label": "COLLECT", "size": "22", "color": "cc.color(255, 180, 0)", "action": "collect the reward"},
    ]
    for cfg in btn_configs:
        results.append(jl(
            f"Write a complete example of a '{cfg['label']}' button that will {cfg['action']}.",
            f"""```js
// '{cfg['label']}' button to {cfg['action']}
var btn = new ccui.Button('res/btn_normal.png', 'res/btn_pressed.png');
btn.setTitleText('{cfg["label"]}');
btn.setTitleFontSize({cfg["size"]});
btn.setTitleColor({cfg["color"]});
btn.setPosition(cc.director.getWinSize().width / 2, 200);
btn.addClickEventListener(function() {{
    cc.log('{cfg["label"]} clicked - {cfg["action"]}');
}});
this.addChild(btn);
```"""))

    # --- Platform check variations ---
    platform_checks = [
        ("cc.sys.isNative", "running on native platform", "adjust native-specific settings"),
        ("!cc.sys.isNative", "running in browser", "use HTML5-specific features"),
        ("cc.sys.isMobile", "on a mobile device", "enable touch joystick"),
        ("!cc.sys.isMobile", "on desktop", "enable keyboard controls"),
        ("cc.sys.platform === cc.sys.ANDROID", "on Android", "handle Android back button"),
        ("cc.sys.os === cc.sys.OS_IOS", "on iOS", "adjust for notch safe area"),
        ("cc.sys.capabilities.touches", "device supports touch", "enable touch input"),
        ("cc.sys.capabilities.keyboard", "device has keyboard", "enable keyboard shortcuts"),
    ]
    for check, desc, action in platform_checks:
        results.append(jl(
            f"Write a complete example of checking if {desc} and {action}.",
            f"""```js
// Check if {desc} and {action}
if ({check}) {{
    cc.log('{desc} detected');
    // {action}
}}
```"""))

    # --- Spine animation pair combos ---
    spine_pairs = [
        ("idle", "walk"), ("walk", "run"), ("run", "idle"),
        ("idle", "attack"), ("attack", "idle"), ("walk", "jump"),
        ("jump", "idle"), ("idle", "die"), ("run", "attack"),
        ("attack", "walk"), ("idle", "cast"), ("cast", "idle"),
    ]
    for anim1, anim2 in spine_pairs:
        mix_dur = pick(["0.1", "0.2", "0.3", "0.4"])
        results.append(jl(
            f"Write a complete example of setting up a {mix_dur}s blend from '{anim1}' to '{anim2}' in Spine.",
            f"""```js
// Spine blend: '{anim1}' to '{anim2}' with {mix_dur}s transition
var skel = new sp.SkeletonAnimation('res/char/char.json', 'res/char/char.atlas');
skel.setPosition(240, 80);
this.addChild(skel);
skel.setMix('{anim1}', '{anim2}', {mix_dur});
skel.setAnimation(0, '{anim1}', true);
// Later: skel.setAnimation(0, '{anim2}', true);
```"""))

    # --- CCS armature speed variations ---
    speeds = ["0.25", "0.5", "0.75", "1.0", "1.5", "2.0", "3.0"]
    ccs_anims = ["idle", "walk", "run", "attack", "jump"]
    for speed in speeds:
        anim = pick(ccs_anims)
        speed_desc = "quarter" if speed == "0.25" else "half" if speed == "0.5" else "normal" if speed == "1.0" else f"{speed}x"
        results.append(jl(
            f"Write a complete example of playing a CocosStudio armature '{anim}' animation at {speed_desc} speed.",
            f"""```js
// Play armature '{anim}' at {speed_desc} speed
ccs.armatureDataManager.addArmatureFileInfo('res/char/char.ExportJson');
var armature = ccs.Armature.create('char');
armature.setPosition(240, 160);
this.addChild(armature);
armature.animation.play('{anim}', -1, -1);
armature.animation.setSpeedScale({speed});
```"""))

    # --- LayerColor/Gradient variations ---
    layer_colors = [
        ("black", "0, 0, 0"), ("white", "255, 255, 255"),
        ("red", "255, 0, 0"), ("blue", "0, 0, 200"),
        ("dark gray", "40, 40, 40"), ("navy", "0, 20, 60"),
    ]
    opacities = ["64", "128", "180", "200", "230", "255"]
    for col_name, col_rgb in layer_colors:
        opa = pick(opacities)
        results.append(jl(
            f"Write a complete example of a {col_name} LayerColor overlay at opacity {opa}.",
            f"""```js
// {col_name.capitalize()} overlay at opacity {opa}
var overlay = new cc.LayerColor(cc.color({col_rgb}, {opa}));
overlay.setContentSize(cc.director.getWinSize());
this.addChild(overlay, 100);
```"""))

    grad_combos = [
        ("sky blue to dark", "100, 180, 255", "10, 20, 60"),
        ("sunset orange to purple", "255, 130, 50", "80, 20, 100"),
        ("green to black", "50, 200, 50", "5, 10, 5"),
        ("white to gray", "255, 255, 255", "100, 100, 100"),
        ("pink to purple", "255, 150, 200", "80, 0, 120"),
        ("yellow to red", "255, 255, 50", "200, 30, 0"),
    ]
    for desc, c1, c2 in grad_combos:
        results.append(jl(
            f"Write a complete example of a gradient background going from {desc}.",
            f"""```js
// Gradient: {desc}
var grad = new cc.LayerGradient(
    cc.color({c1}, 255),
    cc.color({c2}, 255),
    cc.p(0, -1)
);
this.addChild(grad, -1);
```"""))

    # --- cc.path usage variations ---
    path_examples = [
        ("res/sprites/hero.png", "join segments 'res', 'sprites', 'hero.png'",
         "var path = cc.path.join('res', 'sprites', 'hero.png');"),
        ("res/audio/bgm.mp3", "get the extension",
         "var ext = cc.path.extname('res/audio/bgm.mp3');\ncc.log(ext); // '.mp3'"),
        ("res/levels/level_01.json", "get the filename without extension",
         "var name = cc.path.basename('res/levels/level_01.json', '.json');\ncc.log(name); // 'level_01'"),
        ("res/ui/buttons/play.png", "get the directory path",
         "var dir = cc.path.dirname('res/ui/buttons/play.png');\ncc.log(dir); // 'res/ui/buttons'"),
    ]
    for filepath, desc, code in path_examples:
        results.append(jl(
            f"Write a complete example of using cc.path to {desc} for '{filepath}'.",
            f"""```js
// cc.path: {desc}
{code}
```"""))

    # --- cc math utility combos ---
    math_examples = [
        ("calculate distance between hero and enemy",
         "var dist = cc.pDistance(hero.getPosition(), enemy.getPosition());\ncc.log('Distance:', dist);"),
        ("find the direction from hero to target",
         "var dir = cc.pNormalize(cc.pSub(target.getPosition(), hero.getPosition()));\ncc.log('Direction:', dir.x, dir.y);"),
        ("find the midpoint between two nodes",
         "var mid = cc.pMidpoint(nodeA.getPosition(), nodeB.getPosition());\ncc.log('Midpoint:', mid.x, mid.y);"),
        ("calculate the angle between two vectors",
         "var angle = cc.pAngle(cc.p(1, 0), cc.p(0, 1));\ncc.log('Angle (radians):', angle);"),
        ("add two position vectors",
         "var sum = cc.pAdd(cc.p(100, 200), cc.p(50, -30));\ncc.log('Sum:', sum.x, sum.y);"),
        ("scale a direction vector by speed",
         "var dir = cc.pNormalize(cc.p(1, 1));\nvar velocity = cc.pMult(dir, 200);\ncc.log('Velocity:', velocity.x, velocity.y);"),
        ("lerp between two positions at 50%",
         "var result = cc.pLerp(cc.p(0, 0), cc.p(100, 200), 0.5);\ncc.log('Lerp 50%:', result.x, result.y);"),
        ("clamp a value between min and max",
         "var clamped = cc.clampf(150, 0, 100);\ncc.log('Clamped:', clamped); // 100"),
        ("convert degrees to radians",
         "var rad = cc.degreesToRadians(90);\ncc.log('90 degrees =', rad, 'radians');"),
        ("convert radians to degrees",
         "var deg = cc.radiansToDegrees(Math.PI);\ncc.log('PI radians =', deg, 'degrees');"),
    ]
    for desc, code in math_examples:
        results.append(jl(
            f"Write a complete example of using cc point/math utilities to {desc}.",
            f"""```js
// {desc}
{code}
```"""))

    return results


def gen_bulk_completion():
    """Generate more code completion via templates."""
    results = []

    # Template: given a sprite, complete with specific action
    actions_to_complete = [
        ("spin forever", "sprite.runAction(cc.repeatForever(cc.rotateBy(2.0, 360)));"),
        ("blink 5 times then hide", "sprite.runAction(cc.sequence(\n    cc.blink(1.0, 5),\n    cc.hide()\n));"),
        ("grow to 3x size", "sprite.runAction(cc.scaleTo(1.0, 3.0));"),
        ("move to top-right corner", "var ws = cc.director.getWinSize();\nsprite.runAction(cc.moveTo(1.0, cc.p(ws.width - 30, ws.height - 30)));"),
        ("bounce up and down 3 times", "sprite.runAction(cc.repeat(cc.sequence(\n    cc.moveBy(0.3, cc.p(0, 60)).easing(cc.easeOut(2)),\n    cc.moveBy(0.3, cc.p(0, -60)).easing(cc.easeBounceOut())\n), 3));"),
        ("fade to 50% opacity", "sprite.runAction(cc.fadeTo(0.5, 128));"),
        ("skew by 15 degrees on X axis", "sprite.runAction(cc.skewTo(0.5, 15, 0));"),
        ("tint to blue", "sprite.runAction(cc.tintTo(0.5, 0, 100, 255));"),
        ("move along a bezier curve to (400, 300)", "sprite.runAction(cc.bezierTo(2.0, [\n    cc.p(100, 300), cc.p(300, 350), cc.p(400, 300)\n]));"),
        ("flip horizontally then move right", "sprite.runAction(cc.sequence(\n    cc.flipX(true),\n    cc.moveBy(1.0, cc.p(200, 0))\n));"),
    ]

    sprites = ["hero.png", "coin.png", "enemy.png", "gem.png", "star.png"]
    for act_desc, act_code in actions_to_complete:
        sp = pick(sprites)
        results.append(jl(
            f"""Complete this code to make the sprite {act_desc}:
```
var sprite = new cc.Sprite('res/{sp}');
sprite.setPosition(240, 160);
this.addChild(sprite);
// TODO: {act_desc}
```""",
            f"""```js
var sprite = new cc.Sprite('res/{sp}');
sprite.setPosition(240, 160);
this.addChild(sprite);
// {act_desc.capitalize()}
{act_code}
```"""))

    # Template: given a label, complete with effects
    label_completions = [
        ("add a red glow effect", "label.enableGlow(cc.color(255, 0, 0, 255));"),
        ("set text alignment to center with 200px width", "label.setDimensions(200, 0);\nlabel.setHorizontalAlignment(cc.TEXT_ALIGNMENT_CENTER);"),
        ("change the font size to 48", "label.setSystemFontSize(48);"),
        ("add both outline and shadow", "label.enableOutline(cc.color(0, 0, 0, 255), 2);\nlabel.enableShadow(cc.color(0, 0, 0, 128), cc.size(2, -2), 0);"),
        ("set the line height to 30", "label.setLineHeight(30);"),
    ]
    for desc, code in label_completions:
        results.append(jl(
            f"""Complete this code to {desc}:
```
var label = cc.Label.createWithSystemFont('Hello World', 'Arial', 24);
label.setPosition(240, 200);
this.addChild(label);
// TODO: {desc}
```""",
            f"""```js
var label = cc.Label.createWithSystemFont('Hello World', 'Arial', 24);
label.setPosition(240, 200);
this.addChild(label);
// {desc.capitalize()}
{code}
```"""))

    # Template: create various node configurations
    node_completions = [
        ("set anchor to bottom-center", "sprite.setAnchorPoint(cc.p(0.5, 0));"),
        ("set anchor to top-left", "sprite.setAnchorPoint(cc.p(0, 1));"),
        ("enable cascade opacity for children", "sprite.setCascadeOpacityEnabled(true);"),
        ("set content size to 100x100", "sprite.setContentSize(cc.size(100, 100));"),
        ("set normalized position to center of parent", "sprite.setNormalizedPosition(cc.p(0.5, 0.5));"),
        ("add with z-order 10 and tag 'ui'", "this.addChild(sprite, 10, 'ui');"),
    ]
    for desc, code in node_completions:
        results.append(jl(
            f"""Complete this code to {desc}:
```
var sprite = new cc.Sprite('res/icon.png');
// TODO: {desc}
this.addChild(sprite);
```""",
            f"""```js
var sprite = new cc.Sprite('res/icon.png');
// {desc.capitalize()}
{code}
this.addChild(sprite);
```"""))

    # Template: various scheduling completions
    schedule_completions = [
        ("unschedule all callbacks on this node", "this.unscheduleAllCallbacks();"),
        ("schedule update with priority 5", "this.scheduleUpdateWithPriority(5);"),
        ("run a callback once after 10 seconds", "this.scheduleOnce(function() {\n    cc.log('10 seconds elapsed');\n}, 10.0);"),
        ("schedule a repeating timer every 0.5 seconds", "this.schedule(function(dt) {\n    cc.log('tick');\n}, 0.5);"),
        ("set time scale to 2x for fast forward", "cc.director.getScheduler().setTimeScale(2.0);"),
    ]
    for desc, code in schedule_completions:
        results.append(jl(
            f"""Complete this code to {desc}:
```
// TODO: {desc}
```""",
            f"""```js
// {desc.capitalize()}
{code}
```"""))

    # Template: DrawNode completions
    draw_completions = [
        ("draw 5 random dots", "for (var i = 0; i < 5; i++) {\n    draw.drawDot(cc.p(Math.random() * 480, Math.random() * 320), 5, cc.color(255, 0, 0, 255));\n}"),
        ("draw a pentagon", "var pts = [];\nfor (var i = 0; i < 5; i++) {\n    var a = i * Math.PI * 2 / 5 - Math.PI / 2;\n    pts.push(cc.p(240 + 80 * Math.cos(a), 160 + 80 * Math.sin(a)));\n}\ndraw.drawPoly(pts, cc.color(0, 200, 100, 150), 2, cc.color(0, 255, 100, 255));"),
        ("draw a cross/plus at (240, 160)", "var s = 30;\ndraw.drawSegment(cc.p(240 - s, 160), cc.p(240 + s, 160), 2, cc.color(255, 255, 255, 255));\ndraw.drawSegment(cc.p(240, 160 - s), cc.p(240, 160 + s), 2, cc.color(255, 255, 255, 255));"),
    ]
    for desc, code in draw_completions:
        results.append(jl(
            f"""Complete this code to {desc}:
```
var draw = new cc.DrawNode();
this.addChild(draw);
// TODO: {desc}
```""",
            f"""```js
var draw = new cc.DrawNode();
this.addChild(draw);
// {desc.capitalize()}
{code}
```"""))

    # Template: localStorage completions
    storage_completions = [
        ("save player name 'Hero' to local storage", "cc.sys.localStorage.setItem('playerName', 'Hero');"),
        ("load and parse a JSON settings object", "var raw = cc.sys.localStorage.getItem('settings');\nvar settings = raw ? JSON.parse(raw) : { volume: 1.0, lang: 'en' };"),
        ("clear all saved data", "cc.sys.localStorage.clear();"),
        ("remove a specific saved key", "cc.sys.localStorage.removeItem('tempData');"),
    ]
    for desc, code in storage_completions:
        results.append(jl(
            f"""Complete this code to {desc}:
```
// TODO: {desc}
```""",
            f"""```js
// {desc.capitalize()}
{code}
```"""))

    # Template: event dispatch completions
    event_completions = [
        ("dispatch a custom 'level:complete' event with level number",
         "cc.eventManager.dispatchCustomEvent('level:complete', { level: 5 });"),
        ("listen for 'player:hit' custom event",
         "cc.eventManager.addCustomListener('player:hit', function(event) {\n    var data = event.getUserData();\n    cc.log('Player hit! Damage:', data.damage);\n});"),
        ("remove all custom listeners for 'game:over'",
         "cc.eventManager.removeCustomListeners('game:over');"),
        ("remove all listeners from a node",
         "cc.eventManager.removeListeners(targetNode);"),
    ]
    for desc, code in event_completions:
        results.append(jl(
            f"""Complete this code to {desc}:
```
// TODO: {desc}
```""",
            f"""```js
// {desc.capitalize()}
{code}
```"""))

    # --- More action completions via cross-product ---
    move_targets = [("100, 100", "(100,100)"), ("300, 200", "(300,200)"),
                    ("50, 400", "(50,400)"), ("400, 50", "(400,50)"),
                    ("240, 320", "(240,320)"), ("160, 80", "(160,80)")]
    easing_completions = [
        ("cc.easeBounceOut()", "bounce"), ("cc.easeBackOut()", "back ease-out"),
        ("cc.easeSineInOut()", "sine"), ("cc.easeElasticOut()", "elastic"),
        ("cc.easeExponentialOut()", "exponential"), ("cc.easeIn(2.0)", "ease-in rate 2"),
        ("cc.easeOut(3.0)", "ease-out rate 3"), ("cc.easeCubicActionOut()", "cubic"),
        ("cc.easeQuadraticActionOut()", "quadratic"), ("cc.easeCircleActionOut()", "circle"),
    ]
    for pos, pos_desc in move_targets:
        for ease_code, ease_name in easing_completions:
            results.append(jl(
                f"""Complete this code to move the sprite to {pos_desc} with {ease_name} easing:
```
var sprite = new cc.Sprite('res/box.png');
sprite.setPosition(240, 160);
this.addChild(sprite);
// TODO: move to {pos_desc} with {ease_name} easing
```""",
                f"""```js
var sprite = new cc.Sprite('res/box.png');
sprite.setPosition(240, 160);
this.addChild(sprite);
// Move to {pos_desc} with {ease_name} easing
sprite.runAction(cc.moveTo(1.0, cc.p({pos})).easing({ease_code}));
```"""))

    # --- Sprite frame switching completions ---
    frame_names = ["idle_01", "run_01", "jump_01", "attack_01", "hit_01", "die_01"]
    for frame in frame_names:
        results.append(jl(
            f"""Complete this code to switch the sprite's frame to '{frame}.png':
```
cc.spriteFrameCache.addSpriteFrames('res/hero.plist', 'res/hero.png');
var hero = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('idle_01.png'));
hero.setPosition(240, 160);
this.addChild(hero);
// TODO: switch to frame '{frame}.png'
```""",
            f"""```js
cc.spriteFrameCache.addSpriteFrames('res/hero.plist', 'res/hero.png');
var hero = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('idle_01.png'));
hero.setPosition(240, 160);
this.addChild(hero);
// Switch to frame '{frame}.png'
hero.setSpriteFrame('{frame}.png');
```"""))

    # --- Audio completion combos ---
    bgms = ["bgm_menu.mp3", "bgm_game.mp3", "bgm_boss.mp3"]
    vols = ["0.3", "0.5", "0.7", "0.9"]
    for bgm in bgms:
        for vol in vols:
            results.append(jl(
                f"""Complete this code to play '{bgm}' at volume {vol}:
```
// TODO: play background music '{bgm}' looping at volume {vol}
```""",
                f"""```js
// Play background music '{bgm}' looping at volume {vol}
cc.audioEngine.playMusic('res/audio/{bgm}', true);
cc.audioEngine.setMusicVolume({vol});
```"""))

    # --- ccui widget completions ---
    slider_percents = ["0", "25", "50", "75", "100"]
    for pct in slider_percents:
        results.append(jl(
            f"""Complete this code to set the slider to {pct}%:
```
var slider = new ccui.Slider();
slider.loadBarTexture('res/slider_bar.png');
slider.loadSlidBallTextures('res/slider_ball.png', 'res/slider_ball.png', '');
slider.loadProgressBarTexture('res/slider_progress.png');
slider.setPosition(240, 200);
// TODO: set to {pct}% and add change listener
this.addChild(slider);
```""",
            f"""```js
var slider = new ccui.Slider();
slider.loadBarTexture('res/slider_bar.png');
slider.loadSlidBallTextures('res/slider_ball.png', 'res/slider_ball.png', '');
slider.loadProgressBarTexture('res/slider_progress.png');
slider.setPosition(240, 200);
// Set to {pct}% and add change listener
slider.setPercent({pct});
slider.addEventListener(function(sender, type) {{
    cc.log('Slider:', sender.getPercent());
}}, this);
this.addChild(slider);
```"""))

    # --- Scene management completions ---
    scene_names = ["MenuScene", "GameScene", "ShopScene", "SettingsScene", "GameOverScene"]
    for sn in scene_names:
        results.append(jl(
            f"""Complete this code to create and run {sn}:
```
// TODO: create {sn} and run it
```""",
            f"""```js
// Create {sn} and run it
var scene = new cc.Scene();
scene.addChild(new {sn}Layer());
cc.director.runScene(scene);
```"""))

    # --- Mixed completions for remaining modules ---
    misc_completions = [
        ("create a CatmullRom spline path through 4 points",
         "sprite.runAction(cc.catmullRomTo(3.0, [\n    cc.p(50, 100), cc.p(150, 300), cc.p(300, 80), cc.p(420, 250)\n]));"),
        ("apply cc.waves3D grid effect",
         "sprite.runAction(cc.waves3D(3.0, cc.size(15, 10), 5, 30));"),
        ("use cc.actionTween to animate a custom property from 0 to 100",
         "node.updateTweenAction = function(value, key) { cc.log(key, value); };\nnode.runAction(cc.actionTween(2.0, 'health', 0, 100));"),
        ("apply cc.progressFromTo from 20% to 80%",
         "timer.runAction(cc.progressFromTo(2.0, 20, 80));"),
        ("set the node's global z-order to render on top",
         "node.setGlobalZOrder(100);"),
        ("use cc.rectUnion to merge two bounding boxes",
         "var combined = cc.rectUnion(nodeA.getBoundingBox(), nodeB.getBoundingBox());\ncc.log('Combined rect:', combined.x, combined.y, combined.width, combined.height);"),
    ]
    for desc, code in misc_completions:
        results.append(jl(
            f"""Complete this code to {desc}:
```
// TODO: {desc}
```""",
            f"""```js
// {desc.capitalize()}
{code}
```"""))

    return results


def gen_bulk_explanation():
    """Generate more code explanation variations."""
    results = []

    # Parametric: action with various parameters
    action_codes = [
        ("node.runAction(cc.scaleTo(0.5, 2.0, 1.0));",
         "This scales the node to 2.0x on the X axis and 1.0x on the Y axis over 0.5 seconds, creating a horizontal stretch effect. The two-parameter form of `cc.scaleTo` sets scaleX and scaleY independently, unlike the single-parameter form which sets both equally."),
        ("node.runAction(cc.skewTo(1.0, 30, 0));",
         "This skews the node's X axis by 30 degrees over 1 second, creating a slanting/italicizing effect. The Y skew remains at 0. Skew distorts the node by tilting it along one or both axes, useful for parallax effects or stylistic transformations."),
        ("node.runAction(cc.place(cc.p(200, 300)));",
         "This is an instant action that immediately teleports the node to position (200, 300) without any animation. Unlike `cc.moveTo` which interpolates over time, `cc.place` happens in a single frame. It's useful inside sequences, e.g., `cc.sequence(cc.fadeOut(0.5), cc.place(cc.p(100,100)), cc.fadeIn(0.5))`."),
        ("node.runAction(cc.sequence(cc.show(), cc.moveBy(1, cc.p(0, 100)), cc.hide()));",
         "This sequence: (1) instantly shows the node (if hidden), (2) moves it up 100 pixels over 1 second, (3) instantly hides it. `cc.show()` and `cc.hide()` are instant actions that toggle visibility within a sequence. The node becomes visible, floats up, then disappears."),
        ("var a = cc.moveTo(1, cc.p(300, 200)).clone();\nnode.runAction(a);",
         "This clones the move action and runs the clone on the node. `clone()` creates an independent copy of the action so the original can be reused. Without cloning, running the same action instance on multiple nodes or running it again after completion would fail because actions are single-use."),
        ("node.runAction(cc.cardinalSplineTo(3.0, [cc.p(0,0), cc.p(100,200), cc.p(200,50), cc.p(300,200)], 0.5));",
         "This moves the node along a cardinal spline curve through 4 control points over 3 seconds. The tension parameter (0.5) controls how tightly the curve follows the control points - 0 gives a Catmull-Rom spline, higher values make sharper turns. This creates smooth, natural-looking curved movement paths."),
        ("cc.director.getActionManager().removeAllActionsFromTarget(node, true);",
         "This removes all actions running on the specified node. The `true` parameter forces deletion even of actions that are currently running. This is the action manager's direct API, equivalent to `node.stopAllActions()` but accessible from anywhere without a reference to the node's method."),
    ]

    for code, explanation in action_codes:
        results.append(jl(
            f"""What does this code do?
```
{code}
```""",
            explanation))

    # Parametric: ccui widget code explanations
    widget_explanations = [
        ("var sv = new ccui.ScrollView();\nsv.setDirection(ccui.ScrollView.DIR_BOTH);",
         "This creates a scroll view that allows scrolling in both horizontal and vertical directions simultaneously. `DIR_BOTH` enables free 2D panning, unlike `DIR_VERTICAL` or `DIR_HORIZONTAL` which restrict to one axis. This is useful for large maps or spreadsheet-like content."),
        ("widget.ignoreContentAdaptWithSize(false);",
         "This tells the widget to NOT automatically resize to fit its content. By default, widgets auto-size to their content (texture/text). Setting this to `false` allows you to manually set the widget's size with `setSize()`, which is necessary for layouts, Scale9 sprites, or when you want a fixed-size widget."),
        ("btn.setPressedActionEnabled(true);\nbtn.setZoomScale(0.1);",
         "This enables the built-in press animation on a ccui.Button. When tapped, the button automatically zooms/scales by the zoom scale amount (0.1 = 10% larger), giving visual feedback without custom action code. This is simpler than manually adding touch event scale animations."),
        ("lv.setItemModel(model);\nlv.pushBackDefaultItem();",
         "This sets a template widget (`model`) for the ListView and creates a clone of it appended to the list. `setItemModel` defines the blueprint, and `pushBackDefaultItem` instantiates a copy. This is the data-driven approach for lists: define the template once, then clone it for each row."),
        ("param.setGravity(ccui.LinearLayoutParameter.CENTER_VERTICAL);\nwidget.setLayoutParameter(param);",
         "This sets a linear layout parameter on a widget to vertically center it within a horizontal linear layout. Layout parameters control how widgets are positioned when their parent uses `LINEAR_HORIZONTAL` or `LINEAR_VERTICAL` layout types. `CENTER_VERTICAL` centers the widget vertically within its row."),
    ]
    for code, explanation in widget_explanations:
        results.append(jl(
            f"""What does this code do?
```
{code}
```""",
            explanation))

    # Parametric: sys/platform code explanations
    sys_explanations = [
        ("cc.sys.isObjectValid(node);",
         "This checks whether a native object reference is still valid. In JSB (native) builds, C++ objects can be garbage collected while JavaScript still holds a reference. This function returns `false` if the underlying C++ object has been destroyed, preventing crashes from accessing deallocated memory. In HTML5, it always returns `true`."),
        ("cc.sys.windowPixelResolution;",
         "This property returns the actual pixel resolution of the browser window as a cc.Size (HTML5 only). It reflects the device's physical pixels, which may differ from the logical CSS pixels on high-DPI (Retina) displays. Useful for determining the actual rendering resolution for quality settings."),
        ("cc.formatStr('Player %s scored %d points', name, score);",
         "This formats a string using printf-style placeholders. `%s` is replaced with the string `name`, and `%d` is replaced with the number `score`. It returns the formatted string without logging it. Useful for constructing formatted messages for labels or debug output."),
    ]
    for code, explanation in sys_explanations:
        results.append(jl(
            f"""What does this code do?
```
{code}
```""",
            explanation))

    # Parametric: lifecycle/pattern explanations
    pattern_explanations = [
        ("var GameLayer = cc.Layer.extend({\n    ctor: function() {\n        this._super();\n    },\n    onEnter: function() {\n        this._super();\n    },\n    onExit: function() {\n        this._super();\n    }\n});",
         "This defines a custom Layer class using Cocos2d-x's class extension system. The `extend` method creates a new class inheriting from cc.Layer. `ctor` is the constructor (called once on creation), `onEnter` is called when added to the running scene (good for starting actions/listeners), and `onExit` is called when removed (good for cleanup). Each calls `this._super()` to invoke the parent class method, which is required for proper initialization."),
        ("cc.Class.extend",
         "This is Cocos2d-x's class inheritance system. `cc.Layer.extend({...})` creates a new class that inherits all methods and properties from cc.Layer. Inside the definition object, you define or override methods. Call `this._super()` in any overridden method to call the parent's version. This is the standard pattern for creating custom layers, scenes, and nodes."),
    ]
    for code, explanation in pattern_explanations:
        results.append(jl(
            f"""What does this code do?
```
{code}
```""",
            explanation))

    # Parametric: texture/sprite frame operations
    texture_explanations = [
        ("cc.spriteFrameCache.removeSpriteFramesFromFile('res/old_atlas.plist');",
         "This removes all sprite frames that were loaded from the specified plist file from the global cache. The textures they reference may also be released if no other sprite frames use them. This is used for memory management when transitioning between game sections that use different art assets."),
        ("cc.textureCache.removeTextureForKey('res/large_bg.png');",
         "This removes a specific texture from the texture cache by its file path key, freeing its GPU memory. If any sprites still reference this texture, they will display incorrectly. Call this only after ensuring no active sprites use the texture, typically during scene cleanup."),
        ("sprite.setTexture(cc.textureCache.getTextureForKey('res/atlas.png'));",
         "This sets the sprite's texture to an already-cached texture retrieved by its file path key. Using `getTextureForKey` instead of a file path avoids potentially reloading the texture. This is useful when you know the texture is already cached and want the most efficient reference."),
    ]
    for code, explanation in texture_explanations:
        results.append(jl(
            f"""What does this code do?
```
{code}
```""",
            explanation))

    # --- Parametric: action combo explanations ---
    combo_explanations = [
        ("node.runAction(cc.spawn(cc.moveTo(1, cc.p(300, 200)), cc.rotateBy(1, 180)));",
         "This runs two actions simultaneously using `cc.spawn`: the node moves to (300, 200) while rotating 180 degrees, both over 1 second. The result is a diagonal movement with a half-turn spin. `cc.spawn` ensures both actions start and progress together."),
        ("node.runAction(cc.repeat(cc.sequence(cc.moveBy(0.3, cc.p(0, 30)), cc.moveBy(0.3, cc.p(0, -30))), 5));",
         "This bounces the node up 30px then down 30px, repeating exactly 5 times. The inner `cc.sequence` defines one bounce cycle (0.6s), and `cc.repeat` runs it 5 times for a total of 3 seconds. After 5 bounces, the action completes and the node returns to its original position."),
        ("node.runAction(cc.sequence(cc.spawn(cc.moveTo(1, cc.p(400, 300)), cc.fadeTo(1, 0)), cc.removeSelf()));",
         "This runs a move and fade simultaneously (via `cc.spawn`), then removes the node from its parent. The node travels to (400, 300) while fading to invisible over 1 second. Once both complete, `cc.removeSelf` removes it from the scene graph, freeing its resources."),
        ("var a = cc.moveTo(1, cc.p(200, 200));\na.setTag(42);\nnode.runAction(a);\n// later: node.stopActionByTag(42);",
         "This tags a move action with the number 42, runs it, and shows how to stop it later by tag. Action tags let you identify and control specific actions without keeping a reference to the action object. `stopActionByTag(42)` finds and removes the action with that tag from the node."),
        ("node.runAction(cc.sequence(\n    cc.scaleTo(0.1, 0.8),\n    cc.scaleTo(0.15, 1.1).easing(cc.easeBackOut()),\n    cc.scaleTo(0.1, 1.0)\n));",
         "This creates a 'squish-and-pop' effect: the node quickly shrinks to 80%, then bounces up to 110% with a back ease-out overshoot, then settles to 100%. Total duration is 0.35 seconds. This is a common juice/feedback animation for button presses, collectibles, and UI interactions."),
        ("hero.runAction(cc.repeatForever(cc.sequence(\n    cc.moveBy(2.0, cc.p(200, 0)),\n    cc.flipX(true),\n    cc.moveBy(2.0, cc.p(-200, 0)),\n    cc.flipX(false)\n)));",
         "This creates a patrol pattern: the hero moves right 200px over 2 seconds, flips to face left, moves back 200px over 2 seconds, flips to face right, and repeats forever. The `cc.flipX` instant actions change the sprite's horizontal direction to match the movement."),
    ]
    for code, explanation in combo_explanations:
        results.append(jl(
            f"""What does this code do?
```
{code}
```""",
            explanation))

    # --- Parametric: ccui code explanations ---
    ccui_explanations = [
        ("var btn = new ccui.Button('btn.png', 'btn_sel.png', '', ccui.Widget.PLIST_TEXTURE);",
         "This creates a ccui.Button using sprite frames from the sprite frame cache (PLIST_TEXTURE type) rather than direct file paths. 'btn.png' is the normal state frame name, 'btn_sel.png' is the pressed state. The empty string means no disabled state texture. PLIST_TEXTURE mode looks up frames in `cc.spriteFrameCache`."),
        ("layout.setLayoutType(ccui.Layout.LINEAR_VERTICAL);\nlayout.forceDoLayout();",
         "This sets the layout to stack its children vertically from top to bottom, then forces an immediate layout recalculation. `forceDoLayout` ensures all children are repositioned according to the layout rules right away, rather than waiting for the next frame. Children need `ccui.LinearLayoutParameter` for margins and gravity."),
        ("sv.scrollToPercentVertical(80, 0.5, true);",
         "This animates the scroll view to scroll to 80% of its vertical content over 0.5 seconds with attenuation (deceleration). The percentage is 0-100 where 0 is the top and 100 is the bottom. The `true` parameter enables smooth deceleration rather than linear scrolling."),
        ("var found = ccui.helper.seekWidgetByName(root, 'btnPlay');",
         "This searches recursively through a UI widget tree starting from `root` to find a widget with the name 'btnPlay'. Returns the widget if found, or null. This is the standard way to find widgets in CocosStudio-loaded UI hierarchies, similar to DOM's `querySelector`."),
        ("lv.setItemsMargin(10);\nlv.setGravity(ccui.ListView.GRAVITY_CENTER_HORIZONTAL);",
         "This configures a ListView: `setItemsMargin(10)` adds 10 pixels of spacing between each list item, and `setGravity(CENTER_HORIZONTAL)` centers all items horizontally within the list width. Together they create a centered, evenly-spaced vertical list."),
    ]
    for code, explanation in ccui_explanations:
        results.append(jl(
            f"""What does this code do?
```
{code}
```""",
            explanation))

    # --- Parametric: scene/director explanations ---
    director_explanations = [
        ("cc.director.setAnimationInterval(1/30);",
         "This sets the target frame rate to 30 FPS (frames per second). The parameter is the time between frames in seconds (1/30 = ~0.033s). The default is 1/60 for 60 FPS. Lowering the frame rate reduces CPU/GPU usage and battery consumption, useful for menu screens or battery-saving modes."),
        ("cc.director.popToSceneStackLevel(1);",
         "This pops scenes from the stack until only 1 scene remains (the root scene plus the level-1 scene). If you pushed Menu -> Game -> Pause -> Settings, calling this with level=1 would pop back to Game, removing Settings and Pause. Level 0 would go back to the root Menu scene."),
        ("cc.director.getVisibleOrigin();",
         "This returns the bottom-left corner of the visible rectangle as a cc.Point. On most devices this is (0,0), but on devices with screen offsets (like some Android devices with soft navigation bars) it may be non-zero. Use this combined with `getVisibleSize()` for safe layout calculations."),
    ]
    for code, explanation in director_explanations:
        results.append(jl(
            f"""What does this code do?
```
{code}
```""",
            explanation))

    # --- Parametric: CCS/Spine explanations ---
    anim_explanations = [
        ("armature.animation.gotoAndPause(10);",
         "This jumps the CocosStudio armature animation to frame 10 and pauses. The armature displays the exact pose at frame 10 without playing. Useful for previewing specific animation frames or creating a 'frozen' pose effect."),
        ("hero.findBone('head');",
         "This searches the Spine skeleton for a bone named 'head' and returns it as a `spine.Bone` object (or null if not found). Bone objects provide world transform data (position, rotation, scale) useful for attaching effects, particles, or UI elements to specific skeleton parts."),
        ("hero.clearTrack(0);\nhero.clearTracks();",
         "The first line clears only track 0 (stops the animation on that track). The second line clears all tracks. After clearing, no animation plays on the cleared tracks. The skeleton displays the setup pose (or the last frame if `setToSetupPose` isn't called)."),
        ("armature.animation.getMovementCount();",
         "This returns the total number of available animations (movements) in the CocosStudio armature. Useful for iterating through all animations or validating that an animation index is in range before calling `playWithIndex`."),
    ]
    for code, explanation in anim_explanations:
        results.append(jl(
            f"""What does this code do?
```
{code}
```""",
            explanation))

    # --- Parametric: Node property explanations ---
    node_explanations = [
        ("node.setLocalZOrder(5);",
         "This sets the node's local Z-order to 5 within its parent's children. Children are drawn in ascending Z-order: lower values are drawn first (behind), higher values are drawn later (in front). Siblings with the same Z-order are drawn in the order they were added. This only affects ordering among siblings, not global rendering order."),
        ("node.getBoundingBoxToWorld();",
         "This returns the node's bounding rectangle in world (screen) coordinates as a cc.Rect, accounting for all parent transforms (position, rotation, scale). Unlike `getBoundingBox()` which returns the rect relative to the parent, this gives the absolute screen-space rectangle. Useful for collision detection between nodes in different parent hierarchies."),
        ("node.sortAllChildren();",
         "This manually triggers a sort of the node's children by their local Z-order. Normally Cocos2d-x sorts automatically when needed, but calling this explicitly ensures the sort happens immediately. This is rarely needed unless you modify Z-orders in a tight loop and need guaranteed ordering before the next render."),
        ("node.setVertexZ(10);",
         "This sets the node's Z-position in 3D space, affecting depth testing when 3D rendering is enabled. Unlike local Z-order (which controls 2D draw order), vertexZ affects actual depth buffer positioning. With depth testing enabled, nodes with higher vertexZ appear in front of nodes with lower values regardless of draw order."),
    ]
    for code, explanation in node_explanations:
        results.append(jl(
            f"""What does this code do?
```
{code}
```""",
            explanation))

    # --- Parametric: Type utility explanations ---
    type_explanations = [
        ("cc.rectContainsRect(outer, inner);",
         "This checks whether the `inner` rectangle is completely contained within the `outer` rectangle. Returns `true` only if all four corners of `inner` are inside `outer`. Useful for checking if a game object is fully within a boundary zone or screen area."),
        ("cc.affineTransformTranslate(t, 50, 100);",
         "This returns a new affine transform that is the original transform `t` with a translation of (50, 100) applied. Affine transforms combine position, rotation, scale, and skew into a single 2D transformation matrix. This is the matrix math equivalent of moving an already-transformed coordinate system."),
        ("cc.hexToColor('#FF8800');",
         "This converts a hexadecimal color string '#FF8800' to a cc.Color object with r=255, g=136, b=0, a=255. Useful for defining colors from CSS/web color codes. The '#' prefix is optional. The returned color can be used with any Cocos2d-x color API."),
        ("cc.pDistanceSQ(p1, p2);",
         "This returns the squared distance between two points (without the square root). It's faster than `cc.pDistance` because it avoids the expensive sqrt operation. Use squared distance when you only need to compare distances (e.g., 'is enemy within range?') since if distSQ < range*range, the distance is within range."),
    ]
    for code, explanation in type_explanations:
        results.append(jl(
            f"""What does this code do?
```
{code}
```""",
            explanation))

    return results


def gen_bulk_refactoring():
    """Generate more refactoring variations."""
    results = []

    # Parametric: various anti-patterns
    anti_patterns = [
        {
            "code": "node.setPosition(100, 200);\nnode.setPositionX(100);\nnode.setPositionY(200);",
            "problem": "Position is set twice",
            "fix": "node.setPosition(100, 200);",
            "explanation": "The first `setPosition` already sets x=100, y=200. The subsequent `setPositionX` and `setPositionY` calls are redundant. Remove the duplicate calls."
        },
        {
            "code": "if (node.isVisible() == true) {\n    // do something\n}",
            "problem": "Comparing boolean to true is redundant",
            "fix": "if (node.isVisible()) {\n    // do something\n}",
            "explanation": "`isVisible()` already returns a boolean. Comparing it to `true` with `==` is redundant and slightly less efficient. Just use the boolean directly in the condition."
        },
        {
            "code": "var children = node.getChildren();\nfor (var i = 0; i < children.length; i++) {\n    node.removeChild(children[i]);\n}",
            "problem": "Removing children while iterating modifies the array",
            "fix": "node.removeAllChildren(true);",
            "explanation": "Removing children during forward iteration causes skipped elements because the array shrinks. Use `removeAllChildren()` which handles this correctly in a single call. If you need conditional removal, iterate backwards: `for (var i = children.length - 1; i >= 0; i--)`."
        },
        {
            "code": "sprite.runAction(cc.moveTo(1, cc.p(200, 200)));\nsprite.runAction(cc.moveTo(1, cc.p(300, 300)));",
            "problem": "Two moveTo actions compete and produce unexpected results",
            "fix": "sprite.runAction(cc.sequence(\n    cc.moveTo(1, cc.p(200, 200)),\n    cc.moveTo(1, cc.p(300, 300))\n));",
            "explanation": "Running two moveTo actions simultaneously makes them fight over the position, causing jittering or only one working. If sequential: use `cc.sequence`. If you meant to change the destination, stop the first action before starting the second."
        },
        {
            "code": "this.schedule(function() {\n    if (gameOver) return;\n    spawnEnemy();\n}, 2.0);",
            "problem": "Checking a flag every call instead of unscheduling",
            "fix": "this.schedule(this.spawnEnemy, 2.0);\n// When game is over:\nthis.unschedule(this.spawnEnemy);",
            "explanation": "Instead of checking a `gameOver` flag every 2 seconds, unschedule the callback when the game ends. This saves the scheduler from calling a no-op function repeatedly and makes the code's intent clearer."
        },
        {
            "code": "var pos = node.getPosition();\nvar x = pos.x;\nvar y = pos.y;\ncc.log(x, y);",
            "problem": "Creating intermediate variables for a one-time read",
            "fix": "cc.log(node.x, node.y);",
            "explanation": "Use direct property access `node.x` and `node.y` instead of calling `getPosition()` which creates a temporary cc.Point object. Direct properties are faster and more concise for simple reads."
        },
        {
            "code": "new cc.Sprite('res/hero.png');\nvar hero = new cc.Sprite('res/hero.png');",
            "problem": "Creating a sprite that's immediately discarded",
            "fix": "var hero = new cc.Sprite('res/hero.png');",
            "explanation": "The first line creates a sprite that isn't assigned to any variable, so it's immediately eligible for garbage collection - a wasted allocation. Only create objects when you need the reference."
        },
        {
            "code": "node.setColor(cc.color(255, 255, 255, 255));\nnode.setOpacity(255);",
            "problem": "Setting color and opacity to defaults",
            "fix": "// These are default values, no need to set them",
            "explanation": "New nodes already have white color (255,255,255) and full opacity (255). Setting these explicitly is unnecessary unless you're resetting from a previously changed state."
        },
        {
            "code": "cc.audioEngine.playEffect('res/sfx.mp3');\ncc.audioEngine.playEffect('res/sfx.mp3');\ncc.audioEngine.playEffect('res/sfx.mp3');",
            "problem": "Playing the same sound three times simultaneously",
            "fix": "cc.audioEngine.playEffect('res/sfx.mp3');",
            "explanation": "Playing the same effect 3 times simultaneously creates overlapping audio that sounds garbled and louder than intended. Play it once. If you need it louder, adjust the volume parameter. If you want multiple distinct impacts, add slight random pitch variation."
        },
        {
            "code": "for (var i = 0; i < 100; i++) {\n    var s = new cc.Sprite('res/tile.png');\n    s.setPosition(i * 32, 0);\n    this.addChild(s);\n    s.runAction(cc.moveTo(0, cc.p(i * 32, 0)));\n}",
            "problem": "Running a zero-duration moveTo to the sprite's own position",
            "fix": "for (var i = 0; i < 100; i++) {\n    var s = new cc.Sprite('res/tile.png');\n    s.setPosition(i * 32, 0);\n    this.addChild(s);\n}",
            "explanation": "The `cc.moveTo(0, ...)` action moves the sprite to its current position over 0 seconds - completely pointless. It creates 100 unnecessary action objects that immediately complete. Remove the action entirely."
        },
        {
            "code": "var scene = new cc.Scene();\nvar layer = new cc.Layer();\nvar bg = new cc.LayerColor(cc.color(0,0,0));\nlayer.addChild(bg);\nscene.addChild(layer);\ncc.director.runScene(scene);",
            "problem": "Extra empty layer between scene and LayerColor",
            "fix": "var scene = new cc.Scene();\nvar bg = new cc.LayerColor(cc.color(0,0,0));\nscene.addChild(bg);\ncc.director.runScene(scene);",
            "explanation": "The empty `cc.Layer` serves no purpose - LayerColor can be added directly to the scene. Extra nodes in the hierarchy add unnecessary traversal overhead during rendering and event handling."
        },
    ]

    for item in anti_patterns:
        results.append(jl(
            f"""This code has an issue:
```
{item['code']}
```
{item['problem']}. How should this be fixed?""",
            f"""{item['explanation']}

```js
{item['fix']}
```"""))

    # Parametric: API preference improvements
    api_preferences = [
        {
            "bad": "node.getPosition().x + 10",
            "good": "node.x + 10",
            "why": "Direct property access `node.x` is faster than `getPosition().x` which creates a temporary cc.Point object."
        },
        {
            "bad": "node.setPosition(node.getPositionX() + dx, node.getPositionY() + dy)",
            "good": "node.x += dx;\nnode.y += dy;",
            "why": "Direct property assignment is shorter and avoids the overhead of getter/setter method calls."
        },
        {
            "bad": "node.setScale(1.5);\nnode.setScale(1.5, 1.5);",
            "good": "node.setScale(1.5);",
            "why": "Single-parameter `setScale` already sets both X and Y uniformly. The second call is redundant."
        },
        {
            "bad": "var s = cc.Sprite.create('res/hero.png');",
            "good": "var s = new cc.Sprite('res/hero.png');",
            "why": "The constructor form (`new cc.Sprite(...)`) is preferred over the static factory (`cc.Sprite.create(...)`) in modern Cocos2d-x JS. Both work, but `new` is the standard JavaScript pattern."
        },
        {
            "bad": "cc.log('x=' + node.x.toString() + ' y=' + node.y.toString());",
            "good": "cc.log('x=', node.x, 'y=', node.y);",
            "why": "`cc.log` accepts multiple arguments like console.log. No need for string concatenation or explicit toString() calls."
        },
    ]
    for item in api_preferences:
        results.append(jl(
            f"""This code works but uses a less preferred API pattern:
```
{item['bad']}
```
How can this be improved?""",
            f"""{item['why']}

```js
{item['good']}
```"""))

    return results


# ---------------------------------------------------------------------------
# Assemble all categories and write output
# ---------------------------------------------------------------------------

def main():
    random.seed(42)

    all_pairs = []

    # Hand-crafted pairs
    all_pairs.extend(COMPLETE_SNIPPETS)
    all_pairs.extend(CODE_COMPLETION)
    all_pairs.extend(CODE_EXPLANATION)
    all_pairs.extend(REFACTORING)

    # Programmatic variations
    all_pairs.extend(gen_complete_snippets_parametric())
    all_pairs.extend(gen_completion_parametric())
    all_pairs.extend(gen_explanation_parametric())
    all_pairs.extend(gen_refactoring_parametric())

    # Bulk generators for higher volume
    all_pairs.extend(gen_bulk_complete())
    all_pairs.extend(gen_bulk_completion())
    all_pairs.extend(gen_bulk_explanation())
    all_pairs.extend(gen_bulk_refactoring())

    # Shuffle for variety in training
    random.shuffle(all_pairs)

    # Deduplicate by instruction (first 120 chars)
    seen = set()
    unique = []
    for pair in all_pairs:
        key = pair["instruction"][:120]
        if key not in seen:
            seen.add(key)
            unique.append(pair)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for pair in unique:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    # Category counting
    cat_counts = {"complete": 0, "completion": 0, "explanation": 0, "refactoring": 0}
    for p in unique:
        inst = p["instruction"].lower()
        if inst.startswith("write a complete") or inst.startswith("write complete"):
            cat_counts["complete"] += 1
        elif inst.startswith("complete this") or inst.startswith("complete the"):
            cat_counts["completion"] += 1
        elif inst.startswith("what does this") or inst.startswith("what does the"):
            cat_counts["explanation"] += 1
        elif "can be improved" in inst or "can this be" in inst or "should be improved" in inst or "what's wrong" in inst or "what's the" in inst or "is there anything wrong" in inst:
            cat_counts["refactoring"] += 1
        elif "how can" in inst or "improve" in inst or "wrong" in inst or "issue" in inst or "refactor" in inst:
            cat_counts["refactoring"] += 1
        elif "```" in inst and ("complete" in inst or "todo" in inst):
            cat_counts["completion"] += 1
        elif "```" in inst:
            cat_counts["explanation"] += 1
        else:
            cat_counts["complete"] += 1

    print(f"Total unique QA pairs: {len(unique)}")
    print(f"  Complete snippets:   ~{cat_counts['complete']}")
    print(f"  Code completion:     ~{cat_counts['completion']}")
    print(f"  Code explanation:    ~{cat_counts['explanation']}")
    print(f"  Refactoring:         ~{cat_counts['refactoring']}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
