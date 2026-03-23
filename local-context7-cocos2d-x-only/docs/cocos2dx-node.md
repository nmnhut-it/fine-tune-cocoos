# cc.Node

Base class for all scene graph objects in Cocos2d-x. Every visual object (Sprite, Layer, Label, etc.) extends `cc.Node`. Manages position, rotation, scale, children, actions, and scheduling.

## cc.Node Properties

Direct property access (faster than getter/setter in JS).

```typescript
node.x: number            // position x
node.y: number            // position y
node.width: number        // content width
node.height: number       // content height
node.rotation: number     // rotation in degrees (clockwise positive)
node.rotationX: number    // X-axis rotation skew
node.rotationY: number    // Y-axis rotation skew
node.scale: number        // uniform scale
node.scaleX: number
node.scaleY: number
node.skewX: number
node.skewY: number
node.opacity: number      // 0–255
node.color: cc.Color
node.visible: boolean
node.tag: number
node.zIndex: number       // local z-order
node.parent: cc.Node      // read/write
node.children: cc.Node[]  // readonly array
node.childrenCount: number // readonly
node.running: boolean     // readonly — true if on stage
node.cascadeOpacity: boolean
node.cascadeColor: boolean
node.ignoreAnchor: boolean
node.size: cc.Size        // contentSize
node.anchorX: number
node.anchorY: number
node.userData: object
node.scheduler: cc.Scheduler
node.actionManager: cc.ActionManager
node.shaderProgram: cc.GLProgram
node.vertexZ: number
```

**Example:**
```typescript
node.x = 300
node.y = 400
node.scale = 1.5
node.opacity = 128
node.visible = false
```

## cc.Node Position Methods

```typescript
node.getPosition(): cc.Point
node.setPosition(x: number, y: number): void
node.setPosition(pos: cc.Point): void
node.getPositionX(): number
node.setPositionX(x: number): void
node.getPositionY(): number
node.setPositionY(y: number): void
node.getNormalizedPosition(): cc.Point  // 0-1 relative to parent
node.setNormalizedPosition(pos: cc.Point): void
node.setNormalizedPosition(x: number, y: number): void
```

**Example:**
```typescript
node.setPosition(100, 200)
node.setPosition(cc.p(100, 200))
const pos = node.getPosition()   // cc.Point
// Move relative:
node.setPosition(pos.x + 10, pos.y)
```

## cc.Node Size & Anchor

```typescript
node.getContentSize(): cc.Size
node.setContentSize(size: cc.Size): void
node.setContentSize(width: number, height: number): void
node.getAnchorPoint(): cc.Point       // normalized (0-1)
node.setAnchorPoint(point: cc.Point): void
node.setAnchorPoint(x: number, y: number): void
node.getAnchorPointInPoints(): cc.Point  // in pixels
node.ignoreAnchorPointForPosition(newValue: boolean): void
node.isIgnoreAnchorPointForPosition(): boolean
```

**Example:**
```typescript
node.setAnchorPoint(cc.p(0.5, 0.5))  // center (default for Sprite)
node.setAnchorPoint(cc.p(0, 0))       // bottom-left
node.setContentSize(cc.size(200, 100))
const size = node.getContentSize()
```

## cc.Node Rotation & Scale

```typescript
node.getRotation(): number
node.setRotation(degrees: number): void   // clockwise positive
node.getScale(): number
node.setScale(scale: number): void
node.setScale(scaleX: number, scaleY: number): void
node.getScaleX(): number
node.setScaleX(scaleX: number): void
node.getScaleY(): number
node.setScaleY(scaleY: number): void
node.getSkewX(): number
node.setSkewX(degrees: number): void
node.getSkewY(): number
node.setSkewY(degrees: number): void
// 3D (JSB native only):
node.getRotation3D(): cc.math.Vec3
node.setRotation3D(rotation: cc.math.Vec3): void
node.getPosition3D(): cc.math.Vec3
node.setPosition3D(position: cc.math.Vec3): void
```

## cc.Node Visibility & Color

```typescript
node.isVisible(): boolean
node.setVisible(visible: boolean): void
node.getOpacity(): number
node.setOpacity(opacity: number): void     // 0–255
node.getDisplayedOpacity(): number         // inherited opacity
node.getColor(): cc.Color
node.setColor(color: cc.Color): void
node.getDisplayedColor(): cc.Color
node.isCascadeOpacityEnabled(): boolean
node.setCascadeOpacityEnabled(enabled: boolean): void
node.isCascadeColorEnabled(): boolean
node.setCascadeColorEnabled(enabled: boolean): void
```

## cc.Node Z-Order

```typescript
node.getLocalZOrder(): number
node.setLocalZOrder(z: number): void
node.setZOrder(z: number): void           // alias for setLocalZOrder
node.getGlobalZOrder(): number
node.setGlobalZOrder(z: number): void
node.reorderChild(child: cc.Node, zOrder: number): void
node.sortAllChildren(): void
```

## cc.Node Children Management

```typescript
node.addChild(child: cc.Node, localZOrder?: number, tag?: number | string): void
node.removeChild(child: cc.Node, cleanup?: boolean): void
node.removeChildByTag(tag: number, cleanup?: boolean): void
node.removeChildByName(name: string, cleanup?: boolean): void
node.removeAllChildren(cleanup?: boolean): void
node.removeFromParent(cleanup?: boolean): void
node.getChildByTag(tag: number): cc.Node
node.getChildByName(name: string): cc.Node
node.getChildren(): cc.Node[]
node.getChildrenCount(): number
node.getParent(): cc.Node
node.setParent(parent: cc.Node): void
node.enumerateChildren(name: string, callback: (node: cc.Node) => boolean): void
```

**Example:**
```typescript
const child = new cc.Sprite('img.png')
child.setTag(1)
parent.addChild(child, 1)         // zOrder = 1
parent.addChild(child, 1, 'hero') // string tag

const found = parent.getChildByName('hero')
parent.removeChild(child, true)   // cleanup=true removes actions
parent.removeAllChildren()
```

## cc.Node Tag & Name

```typescript
node.getTag(): number
node.setTag(tag: number): void
node.getName(): string
node.setName(name: string): void
node.getUserData(): any
node.setUserData(data: any): void
```

## cc.Node Bounding Box

```typescript
node.getBoundingBox(): cc.Rect        // local space (relative to parent)
node.getBoundingBoxToWorld(): cc.Rect // world space
```

## cc.Node Coordinate Conversion

```typescript
node.convertToNodeSpace(worldPoint: cc.Point): cc.Point
node.convertToWorldSpace(nodePoint: cc.Point): cc.Point
node.convertToNodeSpaceAR(worldPoint: cc.Point): cc.Point    // anchor-relative
node.convertToWorldSpaceAR(nodePoint: cc.Point): cc.Point    // anchor-relative
node.convertTouchToNodeSpace(touch: cc.Touch): cc.Point
node.convertTouchToNodeSpaceAR(touch: cc.Touch): cc.Point
```

**Example:**
```typescript
// Check if a touch hit a node
const localPt = node.convertTouchToNodeSpace(touch)
const nodeRect = cc.rect(0, 0, node.width, node.height)
if (cc.rectContainsPoint(nodeRect, localPt)) { /* hit */ }
```

## cc.Node Transform

```typescript
node.getNodeToParentTransform(parent?: cc.Node): cc.AffineTransform
node.getNodeToWorldTransform(): cc.AffineTransform
node.getParentToNodeTransform(): cc.AffineTransform
node.getWorldToNodeTransform(): cc.AffineTransform
node.setAdditionalTransform(t: cc.AffineTransform): void
```

## cc.Node Actions

```typescript
node.runAction(action: cc.Action): cc.Action
node.stopAllActions(): void
node.stopAction(action: cc.Action): void
node.stopActionByTag(tag: number): void
node.getActionByTag(tag: number): cc.Action
node.getNumberOfRunningActions(): number
```

**Example:**
```typescript
const move = cc.moveTo(1.0, cc.p(300, 300))
const fade = cc.fadeOut(0.5)
const seq = cc.sequence(move, fade, cc.callFunc(() => node.removeFromParent()))
node.runAction(seq)

// Tag an action for later retrieval
const action = cc.repeatForever(cc.rotateBy(1.0, 360))
action.setTag(10)
node.runAction(action)
node.stopActionByTag(10)
```

## cc.Node Scheduling

```typescript
node.scheduleUpdate(): void            // call update(dt) every frame
node.scheduleUpdateWithPriority(priority: number): void
node.unscheduleUpdate(): void
node.update(dt: number): void          // override this

node.schedule(callback: (dt: number) => void, interval?: number, repeat?: number, delay?: number, key?: string): void
node.scheduleOnce(callback: (dt: number) => void, delay: number, key?: string): void
node.unschedule(callback: Function): void
node.unscheduleAllCallbacks(): void
```

**Example:**
```typescript
class MyNode extends cc.Node {
    onEnter() {
        super.onEnter()
        this.scheduleUpdate()
        this.schedule(this.onTick, 2.0)  // every 2 seconds
        this.scheduleOnce(this.onDelay, 5.0) // once after 5s
    }
    update(dt: number) { /* called every frame */ }
    onTick(dt: number) { /* called every 2s */ }
    onDelay(dt: number) { /* called once after 5s */ }
}
```

## cc.Node Lifecycle Callbacks

Override these to hook into the scene graph lifecycle.

```typescript
node.onEnter(): void                        // called when added to stage
node.onExit(): void                         // called when removed from stage
node.onEnterTransitionDidFinish(): void     // after enter transition
node.onExitTransitionDidStart(): void       // before exit transition
node.cleanup(): void                        // stops all actions and timers
node.resume(): void
node.pause(): void
node.pauseSchedulerAndActions(): void
node.visit(): void                          // render traversal
node.update(dt: number): void               // per-frame (if scheduled)
```

## cc.Node Shader & Physics

```typescript
node.getShaderProgram(): cc.GLProgram
node.setShaderProgram(program: cc.GLProgram): void
node.getGLProgramState(): cc.GLProgramState
node.setGLProgramState(state: cc.GLProgramState): void
node.setPhysicsBody(body: any): void
node.getPhysicsBody(): any | null
node.setCameraMask(mask: number, applyChildren?: boolean): void
node.getScene(): cc.Scene | null
node.getEventDispatcher(): cc.EventDispatcher | null
```

## cc.Node attr (Batch Property Set)

```typescript
node.attr(attrs: object): void  // set multiple properties at once
```

**Example:**
```typescript
node.attr({
    x: 100,
    y: 200,
    scale: 1.5,
    opacity: 200,
    visible: true
})
```
