# cc.Layer, cc.LayerColor, cc.LayerGradient

Layer classes for grouping nodes, drawing backgrounds, and managing input. All extend `cc.Node`.

## cc.Layer

Base layer. Use as a container for organizing the scene hierarchy.

```typescript
class cc.Layer extends cc.Node {
    constructor()
    bake(): void      // HTML5 only: cache children to a bake sprite
    unbake(): void
    isBaked(): boolean
}
```

**Example:**
```typescript
class GameLayer extends cc.Layer {
    constructor() {
        super()
        this.init()
    }
    init(): boolean {
        const sprite = new cc.Sprite('res/hero.png')
        sprite.setPosition(240, 160)
        this.addChild(sprite)
        this.scheduleUpdate()
        return true
    }
    update(dt: number) {
        // game logic
    }
}
const scene = new cc.Scene()
scene.addChild(new GameLayer())
cc.director.runScene(scene)
```

## cc.LayerColor

Solid color background layer. Extends `cc.Layer`.

```typescript
new cc.LayerColor(color?: cc.Color)
new cc.LayerColor(color: cc.Color, width: number, height: number)

cc.LayerColor.create(color?: cc.Color): cc.LayerColor
cc.LayerColor.create(color: cc.Color, width: number, height: number): cc.LayerColor

layer.changeWidth(w: number): void
layer.changeHeight(h: number): void
layer.changeWidthAndHeight(w: number, h: number): void
layer.getBlendFunc(): cc.BlendFunc
layer.setBlendFunc(src: cc.BlenderConst, dst: cc.BlenderConst): void
layer.setBlendFunc(blendFunc: cc.BlendFunc): void
```

**Example:**
```typescript
// Black background layer
const bg = new cc.LayerColor(cc.color(0, 0, 0, 255))
scene.addChild(bg, -1)

// Semi-transparent overlay
const overlay = new cc.LayerColor(cc.color(0, 0, 0, 128))
overlay.setContentSize(cc.director.getWinSize())
this.addChild(overlay, 10)
```

## cc.LayerGradient

Gradient color background. Extends `cc.LayerColor`.

```typescript
new cc.LayerGradient()
new cc.LayerGradient(start: cc.Color, end: cc.Color, v?: cc.Point)

cc.LayerGradient.create(): cc.LayerGradient
cc.LayerGradient.create(start: cc.Color, end: cc.Color, v?: cc.Point): cc.LayerGradient

layer.getStartColor(): cc.Color
layer.setStartColor(color: cc.Color): void
layer.getEndColor(): cc.Color
layer.setEndColor(color: cc.Color): void
layer.getStartOpacity(): number
layer.setStartOpacity(o: number): void  // 0–255
layer.getEndOpacity(): number
layer.setEndOpacity(o: number): void
layer.getVector(): cc.Point             // gradient direction
layer.setVector(v: cc.Point): void
layer.isCompressedInterpolation(): boolean
layer.setCompressedInterpolation(compress: boolean): void

// Properties:
layer.startColor: cc.Color
layer.endColor: cc.Color
layer.startOpacity: number
layer.endOpacity: number
layer.vector: number
```

**Example:**
```typescript
// Blue to black gradient (vertical, top to bottom)
const grad = new cc.LayerGradient(
    cc.color(30, 100, 200, 255),
    cc.color(5, 15, 40, 255),
    cc.p(0, -1)   // direction: downward
)
scene.addChild(grad, -1)
```

## cc.LayerMultiplex

Manages multiple layers, showing only one at a time.

```typescript
new cc.LayerMultiplex(...layers: cc.Layer[])
cc.LayerMultiplex.create(...layers: cc.Layer[]): cc.LayerMultiplex

multiplex.addLayer(layer: cc.Layer): void
multiplex.switchTo(n: number): void                   // show layer n, remove current
multiplex.switchToAndReleaseMe(n: number): void       // same + release current
```

**Example:**
```typescript
const multiplex = new cc.LayerMultiplex(mainLayer, settingsLayer)
scene.addChild(multiplex)
// Switch to settings:
multiplex.switchTo(1)
// Back to main:
multiplex.switchTo(0)
```
