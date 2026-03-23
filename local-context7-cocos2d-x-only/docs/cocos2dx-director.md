# cc.Director, cc.Scheduler, cc.ActionManager

Core engine singletons for scene management, scheduling, and action management.

## cc.director — Scene Management

`cc.director` is a singleton. Use `cc.director.methodName()`.

```typescript
cc.director.runScene(scene: cc.Scene): void      // replace current scene
cc.director.pushScene(scene: cc.Scene): void     // push onto stack
cc.director.popScene(): void                     // pop back to previous
cc.director.popToRootScene(): void               // pop all to root
cc.director.popToSceneStackLevel(level: number): void
cc.director.getRunningScene(): cc.Scene
cc.director.pause(): void
cc.director.resume(): void
cc.director.isPaused(): boolean
cc.director.end(): void                          // end director lifecycle
```

**Example:**
```typescript
const nextScene = new GameScene()
cc.director.runScene(nextScene)

// With transition:
const transition = new cc.TransitionFade(0.5, nextScene)
cc.director.runScene(transition)

// Push/pop pattern (modal):
cc.director.pushScene(pauseMenuScene)
// later:
cc.director.popScene()
```

## cc.director — Window & Display

```typescript
cc.director.getWinSize(): cc.Size          // window size in points
cc.director.getWinSizeInPixels(): cc.Size
cc.director.getVisibleSize(): cc.Size
cc.director.getVisibleOrigin(): cc.Point
cc.director.getContentScaleFactor(): number
cc.director.setContentScaleFactor(scale: number): void
cc.director.getDeltaTime(): number         // seconds since last frame
cc.director.getSecondsPerFrame(): number
cc.director.getTotalFrames(): number
cc.director.getAnimationInterval(): number // target FPS value (1/60)
cc.director.setAnimationInterval(value: number): void  // e.g. 1/60
cc.director.isDisplayStats(): boolean
cc.director.setDisplayStats(show: boolean): void
cc.director.getSafeAreaRect(): cc.Rect     // safe area on notched devices
cc.director.startAnimation(): void
cc.director.stopAnimation(): void
```

**Example:**
```typescript
const winSize = cc.director.getWinSize()
const centerX = winSize.width / 2
const centerY = winSize.height / 2
sprite.setPosition(centerX, centerY)

// Enable 30 FPS
cc.director.setAnimationInterval(1 / 30)
```

## cc.director — Subsystems

```typescript
cc.director.getScheduler(): cc.Scheduler
cc.director.setScheduler(scheduler: cc.Scheduler): void
cc.director.getActionManager(): cc.ActionManager
cc.director.setActionManager(manager: cc.ActionManager): void
cc.director.purgeCachedData(): void        // purge textureCache, spriteFrameCache, animationCache
cc.director.convertToGL(uiPoint: cc.Point): cc.Point  // UI coords → GL coords
cc.director.convertToUI(glPoint: cc.Point): cc.Point
```

## cc.Director Static Events

```typescript
cc.Director.EVENT_AFTER_DRAW: string    // fired after each draw
cc.Director.EVENT_AFTER_UPDATE: string  // fired after each update
cc.Director.EVENT_AFTER_VISIT: string
cc.Director.EVENT_PROJECTION_CHANGED: string
cc.Director.PROJECTION_2D: number
cc.Director.PROJECTION_3D: number       // default
```

## cc.Scene

Base class for scenes. Extends `cc.Node`.

```typescript
class cc.Scene extends cc.Node {}
class cc.TransitionScene extends cc.Scene {
    constructor(duration: number, scene: cc.Scene)
}
class cc.TransitionFade extends cc.TransitionScene {}
```

**Example:**
```typescript
class GameScene extends cc.Scene {
    onEnter() {
        super.onEnter()
        const layer = new GameLayer()
        this.addChild(layer)
    }
}
cc.director.runScene(new GameScene())
```

## cc.Scheduler

Manages scheduled callbacks and updates. Usually accessed via `cc.director.getScheduler()` or through node methods.

```typescript
// Via director:
const scheduler = cc.director.getScheduler()
scheduler.getTimeScale(): number
scheduler.setTimeScale(scale: number): void   // 0.5 = slow motion, 2.0 = fast
scheduler.update(dt: number): void

// Schedule for a target (prefer node.schedule() instead)
scheduler.scheduleCallbackForTarget<T extends cc.Class>(
    target: T,
    callback: (this: T, elapsed: number) => void,
    interval: number,
    repeat: number,
    delay: number,
    paused: boolean
): void
scheduler.unscheduleCallbackForTarget<T>(target: T, callback: Function): void
scheduler.scheduleUpdateForTarget(target: cc.Class, priority: number, paused: boolean): void
scheduler.unscheduleUpdateForTarget(target: cc.Class): void
scheduler.unscheduleAllCallbacksForTarget(target: cc.Class): void
scheduler.pauseTarget(target: cc.Class): void
scheduler.resumeTarget(target: cc.Class): void
scheduler.pauseAllTargets(): void
scheduler.pauseAllTargetsWithMinPriority(minPriority: number): void
scheduler.resumeTargets(targets: cc.Class[]): void
scheduler.isTargetPaused(target: cc.Class): boolean
```

**Example:**
```typescript
// Global time scale (slow motion effect)
cc.director.getScheduler().setTimeScale(0.5)
// Reset
cc.director.getScheduler().setTimeScale(1.0)
```

## cc.ActionManager

Manages all running actions. Usually accessed via `cc.director.getActionManager()` or `node.getActionManager()`.

```typescript
const mgr = cc.director.getActionManager()
mgr.addAction(action: cc.Action, target: cc.Node, paused: boolean): void
mgr.getActionByTag(tag: number, target: cc.Node): cc.Action
mgr.pauseAllRunningActions(): cc.Node[]   // returns paused targets
mgr.pauseTarget(target: cc.Node): void
mgr.resumeTarget(target: cc.Node): void
mgr.resumeTargets(targets: cc.Node[]): void
mgr.removeAction(action: cc.Action): void
mgr.removeActionByTag(tag: number, target: cc.Node): void
mgr.removeAllActions(): void
mgr.removeAllActionsFromTarget(target: cc.Node, forceDelete: boolean): void
```

**Example:**
```typescript
// Pause all actions (e.g. when game pauses)
const pausedTargets = cc.director.getActionManager().pauseAllRunningActions()
// Resume later:
cc.director.getActionManager().resumeTargets(pausedTargets)
```

## cc.loader

Utility for loading resources at runtime.

```typescript
cc.loader.load(resources: string[], cb: Function): void
cc.loader.load(resources: string[], option: { isCrossOrigin?: boolean }, cb: Function): void
cc.loader.loadJson(url: string, cb: (error: any, data: any) => void): void
cc.loader.loadBinary(url: string, cb: (err: any, data: Uint8Array | number[]) => void): void
cc.loader.loadTxt(url: string, cb: (err: any, data: string) => void): void
cc.loader.getRes(url: string): any
cc.loader.release(url: string): void
cc.loader.releaseAll(): void
cc.loader.getXMLHttpRequest(): XMLHttpRequest
```

**Example:**
```typescript
cc.loader.load(['res/level1.json', 'res/level1.png'], (err) => {
    if (err) return cc.error('Load failed', err)
    const data = cc.loader.getRes('res/level1.json')
    startGame(data)
})
```
