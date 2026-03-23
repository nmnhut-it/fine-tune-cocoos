# ccs — Armature / Skeletal Animation (CocosStudio)

Armature system for CocosStudio skeletal animations. Use `ccs.Armature` + `ccs.ArmatureAnimation`.

## ccs.armatureDataManager — Loading Data

Must call `addArmatureFileInfo` before creating armatures.

```typescript
ccs.armatureDataManager.addArmatureFileInfo(configFilePath: string): void
ccs.armatureDataManager.addArmatureFileInfo(
    imagePath: string,
    plistPath: string,
    configFilePath: string
): void
```

**Example:**
```typescript
// Load armature data first (usually at scene init)
ccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson')
// Then create armatures as needed
const armature = ccs.Armature.create('hero')
```

## ccs.Armature

Skeletal animation node. Extends `cc.Node`.

```typescript
new ccs.Armature(name?: string, parentBone?: ccs.Bone)
ccs.Armature.create(name?: string, parentBone?: ccs.Bone): ccs.Armature

// Properties:
armature.animation: ccs.ArmatureAnimation  // the animation controller
armature.name: string
armature.armatureData: ccs.ArmatureData
armature.batchNode: cc.SpriteBatchNode
armature.parentBone: ccs.Bone
armature.version: number
```

**Bone access:**
```typescript
armature.getBone(name: string): ccs.Bone
armature.getBoneAtPoint(x: number, y: number): ccs.Bone
armature.getBoneDic(): object
armature.addBone(bone: ccs.Bone, parentName: string): void
armature.removeBone(bone: ccs.Bone, recursion: boolean): void
armature.createBone(boneName: string): ccs.Bone
armature.changeBoneParent(bone: ccs.Bone, parentName: string): void
armature.getAnimation(): ccs.ArmatureAnimation
armature.getArmatureData(): ccs.ArmatureData
armature.getBoundingBox(): cc.Rect   // recalculates from all bones each call
armature.getBlendFunc(): cc.BlendFunc
armature.setBlendFunc(blendFunc: cc.BlendFunc): void
armature.setBlendFunc(src: cc.BlenderConst, dst: cc.BlenderConst): void
armature.setColliderFilter(filter: ccs.ColliderFilter): void
armature.drawContour(): void
```

**Example:**
```typescript
ccs.armatureDataManager.addArmatureFileInfo('res/hero/hero.ExportJson')

const armature = ccs.Armature.create('hero')
armature.setPosition(240, 160)
this.addChild(armature)

// Play animation
armature.animation.play('run', -1, 1)  // -1=no durationTo, 1=loop
armature.animation.setSpeedScale(1.5)  // 1.5x speed

// Listen to animation events
armature.animation.setMovementEventCallFunc((arm, movType, movId) => {
    if (movType === ccs.MovementEventType.COMPLETE) {
        cc.log('animation complete:', movId)
    }
})
```

## ccs.ArmatureAnimation

Controls playback of armature animations. Accessed via `armature.animation`.

```typescript
armature.animation.play(animationName: string, durationTo?: number, loop?: number): void
// durationTo: frames to blend between animations (-1 = no blending)
// loop: -1=forever, 0=no loop, 1+=count

armature.animation.playWithIndex(index: number, durationTo?: number, loop?: number): void
armature.animation.playWithNames(names: string[], durationTo?: number, loop?: boolean): void
armature.animation.playWithIndexes(indexes: number[], durationTo?: number, loop?: boolean): void

armature.animation.gotoAndPlay(frameIndex: number): void   // go to frame and play
armature.animation.gotoAndPause(frameIndex: number): void  // go to frame and pause

armature.animation.pause(): void
armature.animation.resume(): void
armature.animation.stop(): void

armature.animation.getSpeedScale(): number
armature.animation.setSpeedScale(scale: number): void   // 1.0 = normal speed

armature.animation.getMovementCount(): number
armature.animation.getCurrentMovementID(): string
armature.animation.getAnimationData(): ccs.AnimationData
armature.animation.setAnimationData(data: ccs.AnimationData): void
```

**Event callbacks:**
```typescript
// Movement (animation state) events
armature.animation.setMovementEventCallFunc(
    (armature: ccs.Armature, movementType: number, movementID: string) => void
): void
// movementType values: ccs.MovementEventType.START, COMPLETE, LOOP_COMPLETE

// Frame events (triggered by frame events set in CocosStudio)
armature.animation.setFrameEventCallFunc(
    (bone: ccs.Bone, frameEventName: string, originFrameIndex: number, currentFrameIndex: number) => void
): void
```

**Example:**
```typescript
const anim = armature.animation

// Play idle, then walk on complete
anim.setMovementEventCallFunc((arm, type, id) => {
    if (type === ccs.MovementEventType.COMPLETE && id === 'attack') {
        anim.play('idle', 5, -1)
    }
})

// Blend transition in 8 frames
anim.play('walk', 8, -1)

// Speed up when running
anim.play('run', -1, -1)
anim.setSpeedScale(1.5)

// Frame event (triggered by CocosStudio keyframe)
anim.setFrameEventCallFunc((bone, eventName, orig, cur) => {
    if (eventName === 'footstep') {
        cc.audioEngine.playEffect('res/sfx_step.mp3')
    }
})
```

## ccs.Bone

Individual bone in an armature.

```typescript
bone.getName(): string
bone.getArmature(): ccs.Armature
bone.getDisplayManager(): ccs.DisplayManager
bone.getColliderDetector(): ccs.ColliderDetector
bone.getTween(): ccs.Tween
bone.setVisible(visible: boolean): void
bone.getWorldPosition(): cc.Point
bone.getNodeToWorldTransform(): cc.AffineTransform
```

## ccs.ActionTimeline (Alternative Animation via Timeline)

CocosStudio timeline-based action system.

```typescript
ccs.actionManager.loadAnimationActionWithFile(file: string): ccs.ActionTimeline
ccs.actionManager.getAnimationActionWithName(file: string): ccs.ActionTimeline
ccs.actionManager.playAnimationInfo(target: cc.Node, animationInfo: object): ccs.ActionTimeline

const timeline = ccs.actionManager.loadAnimationActionWithFile('res/ui/mainmenu.csb')
node.runAction(timeline)
timeline.gotoFrameAndPlay(0, true)  // frame 0, loop=true
timeline.gotoFrameAndPause(0)
timeline.setCurrentFrame(frame: number): void
timeline.getCurrentFrame(): number
timeline.getStartFrame(): number
timeline.getEndFrame(): number
timeline.setTimeSpeed(speed: number): void
timeline.getTimeSpeed(): number
```

**Example:**
```typescript
// Load a CocosStudio .csb UI file with animation
const timeline = ccs.actionManager.loadAnimationActionWithFile('res/ui/dialog.csb')
dialogNode.runAction(timeline)
timeline.gotoFrameAndPlay(0, false)   // play once (no loop)
```
