# sp.Skeleton & sp.SkeletonAnimation — Spine Runtime

Spine skeletal animation runtime. Use `sp.SkeletonAnimation` (extends `sp.Skeleton` extends `cc.Node`).

## sp.SkeletonAnimation — Creation

```typescript
// Most common: create from skeleton data file
const skel = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas', 1.0)
// or
const skel = sp.SkeletonAnimation.createWithJsonFile('res/hero/hero.json', 'res/hero/hero.atlas', 1.0)
const skel = sp.SkeletonAnimation.createWithBinaryFile('res/hero/hero.skel', 'res/hero/hero.atlas', 1.0)
```

## sp.SkeletonAnimation — Playback

```typescript
skel.setAnimation(trackIndex: number, name: string, loop: boolean): spine.TrackEntry | null
skel.addAnimation(trackIndex: number, name: string, loop: boolean, delay: number): spine.TrackEntry | null
skel.clearTrack(trackIndex: number): void
skel.clearTracks(): void
skel.getCurrent(trackIndex: number): spine.TrackEntry | null
```

**Parameters:**
- `trackIndex` — track slot (0 = base, 1 = overlay like face anim, etc.)
- `name` — animation name as exported from Spine editor
- `loop` — true to loop, false to play once
- `delay` — seconds delay before queued animation starts

**Example:**
```typescript
const hero = new sp.SkeletonAnimation('res/hero/hero.json', 'res/hero/hero.atlas')
hero.setPosition(240, 160)
this.addChild(hero)

// Play run animation looping on track 0
hero.setAnimation(0, 'run', true)

// Queue a jump, then return to run
hero.setAnimation(0, 'jump', false)
hero.addAnimation(0, 'run', true, 0)

// Overlay facial animation on track 1
hero.setAnimation(1, 'blink', true)

// Stop
hero.clearTrack(0)
hero.clearTracks()
```

## sp.SkeletonAnimation — Events & Listeners

```typescript
skel.setAnimationListener(target: object, callback: Function): void
// callback: (trackEntry: spine.TrackEntry, type: number, event: spine.Event) => void

skel.setStartListener(listener: Function): void   // animation started
skel.setEndListener(listener: Function): void     // animation ended / interrupted
```

**Example:**
```typescript
hero.setAnimationListener(this, (track, type, event) => {
    // type: sp.AnimationEventType.START, END, COMPLETE, EVENT
    if (type === sp.AnimationEventType.COMPLETE) {
        cc.log('animation complete:', track.animation.name)
    }
    if (type === sp.AnimationEventType.EVENT) {
        cc.log('frame event:', event.data.name)
        if (event.data.name === 'footstep') {
            cc.audioEngine.playEffect('res/sfx_step.mp3')
        }
    }
})
```

## sp.SkeletonAnimation — Blending

```typescript
skel.setMix(fromAnimation: string, toAnimation: string, duration: number): void
skel.setAnimationStateData(stateData: spine.AnimationStateData): void
```

**Example:**
```typescript
// Smooth 0.3s blend from walk to run
hero.setMix('walk', 'run', 0.3)
hero.setMix('run', 'idle', 0.2)
```

## sp.Skeleton — Base Methods

```typescript
skel.setSkin(skinName: string): void         // switch skin set
skel.setAttachment(slotName: string, attachmentName: string): void
skel.findSlot(slotName: string): spine.Slot | null
skel.findBone(boneName: string): spine.Bone | null
skel.getBoundingBox(): cc.Rect

skel.setTimeScale(scale: number): void       // animation speed (1.0 = normal)
skel.getTimeScale(): number

skel.setToSetupPose(): void                  // reset all bones to setup pose
skel.setBonesToSetupPose(): void
skel.setSlotsToSetupPose(): void

skel.setDebugBonesEnabled(enabled: boolean): void
skel.setDebugSlotsEnabled(enabled: boolean): void

skel.updateWorldTransform(): void
```

**Example:**
```typescript
// Switch character skin
hero.setSkin('warrior')

// Show specific attachment
hero.setAttachment('weapon_slot', 'sword')  // show sword attachment
hero.setAttachment('weapon_slot', null)      // hide attachment

// Slow motion
hero.setTimeScale(0.5)
```

## spine.TrackEntry

Returned by `setAnimation`/`addAnimation`. Controls a specific track.

```typescript
track.animation: spine.Animation       // animation playing
track.loop: boolean
track.delay: number
track.trackTime: number
track.trackEnd: number
track.timeScale: number                // per-track speed scale
track.alpha: number                    // blend weight 0–1
track.mixDuration: number
track.getAnimationTime(): number
```

**Example:**
```typescript
const track = hero.setAnimation(0, 'attack', false)
if (track) {
    track.timeScale = 2.0  // play attack at 2x speed
}
```
