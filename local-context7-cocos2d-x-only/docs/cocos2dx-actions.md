# cc Actions

Actions animate node properties over time. Run with `node.runAction(action)`. All actions are composable via `cc.sequence`, `cc.spawn`, `cc.repeat`, etc.

## Action Base Classes

```typescript
abstract class cc.Action            // base
abstract class cc.FiniteTimeAction  // has duration
abstract class cc.ActionInstant     // zero-duration instant
abstract class cc.ActionInterval    // time-based interpolated
```

**ActionInterval shared methods:**
```typescript
action.getDuration(): number
action.setDuration(duration: number): void
action.reverse(): this
action.repeat(times: number): this
action.repeatForever(): this
action.easing(easeObj: cc.ActionEase): this
action.getSpeed(): number
action.setSpeed(speed: number): void
action.clone(): this
```

## Move Actions

```typescript
cc.moveTo(duration: number, x: number, y: number): MoveTo
cc.moveTo(duration: number, pos: cc.Point): MoveTo
cc.moveBy(duration: number, dx: number, dy: number): MoveBy
cc.moveBy(duration: number, dPos: cc.Point): MoveBy
```

**Example:**
```typescript
// Move to absolute position in 1 second
node.runAction(cc.moveTo(1.0, cc.p(300, 400)))
// Move relatively
node.runAction(cc.moveBy(0.5, cc.p(100, 0)))
// Chain: move right then move left
node.runAction(cc.sequence(
    cc.moveBy(0.5, cc.p(200, 0)),
    cc.moveBy(0.5, cc.p(-200, 0))
))
```

## Scale Actions

```typescript
cc.scaleTo(duration: number, scale: number): ScaleTo
cc.scaleTo(duration: number, scaleX: number, scaleY: number): ScaleTo
cc.scaleBy(duration: number, scale: number): ScaleBy
cc.scaleBy(duration: number, scaleX: number, scaleY: number): ScaleBy
```

**Example:**
```typescript
node.runAction(cc.scaleTo(0.3, 1.2))           // pop effect
node.runAction(cc.sequence(
    cc.scaleTo(0.15, 1.2),
    cc.scaleTo(0.15, 1.0)
))
```

## Rotate Actions

```typescript
cc.rotateTo(duration: number, angle: number): RotateTo
cc.rotateTo(duration: number, deltaAngleX: number, deltaAngleY: number): RotateTo
cc.rotateTo(duration: number, vector: cc.math.Vec3): RotateTo
cc.rotateBy(duration: number, angle: number): RotateBy
cc.rotateBy(duration: number, deltaAngleX: number, deltaAngleY: number): RotateBy
```

**Example:**
```typescript
// Spin forever
node.runAction(cc.repeatForever(cc.rotateBy(2.0, 360)))
// Rotate to specific angle
node.runAction(cc.rotateTo(0.5, 90))
```

## Fade Actions

```typescript
cc.fadeIn(duration: number): FadeIn     // opacity 0 → 255
cc.fadeOut(duration: number): FadeOut   // opacity 255 → 0
cc.fadeTo(duration: number, opacity: number): FadeTo
```

**Example:**
```typescript
node.setOpacity(0)
node.runAction(cc.fadeIn(0.5))
// Fade out then remove
node.runAction(cc.sequence(
    cc.fadeOut(0.5),
    cc.callFunc(() => node.removeFromParent())
))
```

## Jump & Bezier Actions

```typescript
cc.jumpTo(duration: number, position: cc.Point, height: number, jumps: number): JumpTo
cc.jumpTo(duration: number, x: number, y: number, height: number, jumps: number): JumpTo
cc.jumpBy(duration: number, position: cc.Point, height: number, jumps: number): JumpBy
cc.bezierTo(duration: number, points: cc.Point[]): BezierTo   // 3 control points
cc.bezierBy(duration: number, points: cc.Point[]): BezierBy
cc.catmullRomTo(duration: number, points: cc.Point[]): CatmullRomTo
cc.catmullRomBy(duration: number, points: cc.Point[]): CatmullRomBy
cc.cardinalSplineTo(duration: number, points: cc.Point[], tension: number): CardinalSplineTo
cc.cardinalSplineBy(duration: number, points: cc.Point[], tension: number): CardinalSplineBy
```

**Example:**
```typescript
node.runAction(cc.jumpTo(1.0, cc.p(300, 100), 80, 3))
// Bezier path (3 control points required)
node.runAction(cc.bezierTo(2.0, [
    cc.p(0, 200), cc.p(200, 200), cc.p(300, 0)
]))
```

## Tint Actions

```typescript
cc.tintTo(duration: number, red: number, green: number, blue: number): TintTo
cc.tintBy(duration: number, deltaRed: number, deltaGreen: number, deltaBlue: number): TintBy
```

## Blink & Skew

```typescript
cc.blink(duration: number, blinks: number): Blink
cc.skewTo(duration: number, skewX: number, skewY: number): SkewTo
cc.skewBy(duration: number, skewX: number, skewY: number): SkewBy
cc.delayTime(duration: number): DelayTime
```

## Instant Actions

```typescript
cc.show(): Show
cc.hide(): Hide
cc.toggleVisibility(): ToggleVisibility
cc.place(x: number, y: number): Place
cc.place(pos: cc.Point): Place
cc.removeSelf(): RemoveSelf
cc.flipX(flip: boolean): FlipX
cc.flipY(flip: boolean): FlipY
cc.callFunc(callback: Function): CallFunc
cc.callFunc<T>(callback: (this: T, target: cc.Node, data: P) => void, selectorTarget?: T, data?: P): CallFunc
```

**Example:**
```typescript
const seq = cc.sequence(
    cc.moveTo(1.0, cc.p(200, 200)),
    cc.show(),
    cc.callFunc(() => console.log('done'))
)
node.runAction(seq)
```

## Composite Actions

```typescript
// Run actions one after another
cc.sequence(actions: cc.FiniteTimeAction[]): Sequence
cc.sequence(...actions: cc.FiniteTimeAction[]): Sequence

// Run actions simultaneously
cc.spawn(actions: cc.FiniteTimeAction[]): Spawn
cc.spawn(...actions: cc.FiniteTimeAction[]): Spawn

// Repeat
cc.repeat(action: cc.FiniteTimeAction, times: number): Repeat
cc.repeatForever(action: cc.FiniteTimeAction): RepeatForever

// Reverse time
cc.reverseTime(action: cc.FiniteTimeAction): ReverseTime

// Run action on specific target
cc.targetedAction(target: cc.Node, action: cc.FiniteTimeAction): TargetedAction

// Speed modifier
cc.speed(action: cc.FiniteTimeAction, speed: number): Speed

// Follow a node
cc.follow(followedNode: cc.Node, rect: cc.Rect): Follow
```

**Example:**
```typescript
// Move and fade simultaneously, then call back
const move = cc.moveTo(1.0, cc.p(400, 300))
const fade = cc.fadeTo(1.0, 100)
const done = cc.callFunc(() => { /* cleanup */ })
node.runAction(cc.sequence(cc.spawn(move, fade), done))

// Bounce loop
node.runAction(cc.repeatForever(cc.sequence(
    cc.moveBy(0.5, cc.p(0, 50)),
    cc.moveBy(0.5, cc.p(0, -50))
)))
```

## Ease Functions

Apply to any `ActionInterval` via `.easing(easeObj)` or wrapping.

```typescript
cc.easeIn(rate: number)
cc.easeOut(rate: number)
cc.easeInOut(rate: number)
cc.easeSineIn()
cc.easeSineOut()
cc.easeSineInOut()
cc.easeBackIn()
cc.easeBackOut()
cc.easeBackInOut()
cc.easeBounceIn()
cc.easeBounceOut()
cc.easeBounceInOut()
cc.easeElasticIn(period?)
cc.easeElasticOut(period?)
cc.easeElasticInOut(period?)
cc.easeExponentialIn()
cc.easeExponentialOut()
cc.easeExponentialInOut()
cc.easeQuadraticActionIn()
cc.easeQuadraticActionOut()
cc.easeQuadraticActionInOut()
cc.easeCubicActionIn()
cc.easeCubicActionOut()
cc.easeCubicActionInOut()
cc.easeQuarticActionIn() / Out() / InOut()
cc.easeQuinticActionIn() / Out() / InOut()
cc.easeCircleActionIn() / Out() / InOut()
cc.easeBezierAction(p0, p1, p2, p3)
```

**Example:**
```typescript
// Bounce ease on move
node.runAction(cc.moveTo(1.0, cc.p(300, 300)).easing(cc.easeBounceOut()))
// Or via spawn:
node.runAction(
    cc.sequence(
        cc.scaleTo(0.3, 1.3).easing(cc.easeBackOut()),
        cc.scaleTo(0.1, 1.0)
    )
)
```

## Animation Actions

```typescript
cc.animate(animation: cc.Animation): Animate
```

**cc.Animation:**
```typescript
new cc.Animation(frames: (cc.AnimationFrame | cc.SpriteFrame)[], delay: number, loops?: number)
animation.addSpriteFrame(frame: cc.SpriteFrame): void
animation.getDelayPerUnit(): number
animation.setDelayPerUnit(delay: number): void
animation.getLoops(): number
animation.setLoops(n: number): void
animation.setRestoreOriginalFrame(restore: boolean): void
```

**Example:**
```typescript
const frames = []
for (let i = 1; i <= 8; i++) {
    frames.push(cc.spriteFrameCache.getSpriteFrame(`run_${i.toString().padStart(2,'0')}.png`))
}
const anim = new cc.Animation(frames, 0.08, 0)  // 0 = loop forever
sprite.runAction(cc.repeatForever(cc.animate(anim)))
```

## Progress Actions

```typescript
cc.progressTo(duration: number, percent: number): ProgressTo
cc.progressFromTo(duration: number, from: number, to: number): ProgressFromTo
```

## ActionTween

Animates any numeric property by key string.

```typescript
cc.actionTween(duration: number, key: string, from: number, to: number): ActionTween
// target must implement updateTweenAction(value, key) or have the property
```

## Grid / 3D Actions

```typescript
cc.flipX3D(duration: number): FlipX3D
cc.flipY3D(duration: number): FlipY3D
cc.shaky3D(duration, gridSize, range, shakeZ): Shaky3D
cc.liquid(duration, gridSize, waves, amplitude): Liquid
cc.waves(duration, gridSize, waves, amplitude, horizontal, vertical): Waves
cc.waves3D(duration, gridSize, waves, amplitude): Waves3D
cc.ripple3D(duration, gridSize, position, radius, waves, amplitude): Ripple3d
cc.twirl(duration, gridSize, position, twirls, amplitude): Twirl
cc.lens3D(duration, gridSize, position, radius): Lens3D
cc.pageTurn3D(duration, gridSize): PageTurn3D
cc.reuseGrid(times: number): ReuseGrid
cc.stopGrid(): StopGrid
```
