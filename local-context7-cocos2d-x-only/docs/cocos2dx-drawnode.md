# cc.DrawNode

Node for drawing immediate-mode vector graphics: dots, lines, polygons, circles, curves. Extends `cc.Node`.

## cc.DrawNode Creation

```typescript
new cc.DrawNode()
cc.DrawNode.create(): cc.DrawNode
```

**Example:**
```typescript
const draw = new cc.DrawNode()
this.addChild(draw)
```

## cc.DrawNode — Basic Shapes

```typescript
// Dot
draw.drawDot(pos: cc.Point, radius: number, color: cc.Color): void
draw.drawDots(points: cc.Point[], radius: number, color: cc.Color): void

// Line segment
draw.drawSegment(from: cc.Point, to: cc.Point, lineWidth: number, color?: cc.Color): void

// Rectangle
draw.drawRect(
    origin: cc.Point,
    destination: cc.Point,
    fillColor?: cc.Color | null,
    lineWidth?: number | null,
    lineColor?: cc.Color
): void

// Polygon
draw.drawPoly(
    verts: cc.Point[],
    fillColor?: cc.Color,
    lineWidth?: number,
    lineColor?: cc.Color
): void

// Circle
draw.drawCircle(
    center: cc.Point,
    radius: number,
    angle: number,
    segments: number,
    drawLineToCenter: boolean,
    lineWidth: number,
    color?: cc.Color
): void
```

**Example:**
```typescript
const draw = cc.DrawNode.create()
this.addChild(draw)

// Filled red dot
draw.drawDot(cc.p(100, 100), 5, cc.color(255, 0, 0, 255))

// Blue line
draw.drawSegment(cc.p(0, 0), cc.p(200, 100), 2, cc.color(0, 0, 255, 255))

// Filled green triangle
draw.drawPoly(
    [cc.p(100, 0), cc.p(200, 150), cc.p(0, 150)],
    cc.color(0, 255, 0, 100),  // fill
    1,
    cc.color(0, 200, 0, 255)   // border
)

// Hollow circle
draw.drawCircle(cc.p(160, 240), 80, 0, 32, false, 2, cc.color(255, 255, 0, 255))

// Filled rect
draw.drawRect(
    cc.p(50, 50), cc.p(150, 100),
    cc.color(0, 100, 200, 128),  // fill
    2,
    cc.color(0, 50, 255, 255)    // border
)
```

## cc.DrawNode — Curves

```typescript
// Quadratic Bezier
draw.drawQuadBezier(
    origin: cc.Point,
    control: cc.Point,
    destination: cc.Point,
    segments: number,
    lineWidth: number,
    color?: cc.Color
): void

// Cubic Bezier
draw.drawCubicBezier(
    origin: cc.Point,
    control1: cc.Point,
    control2: cc.Point,
    destination: cc.Point,
    segments: number,
    lineWidth: number,
    color?: cc.Color
): void

// Cardinal Spline
draw.drawCardinalSpline(
    config: cc.Point[],
    tension: number,
    segments: number,
    lineWidth: number,
    color?: cc.Color
): void

// CatmullRom
draw.drawCatmullRom(
    points: cc.Point[],
    segments: number,
    lineWidth: number,
    color?: cc.Color
): void
```

**Example:**
```typescript
// Draw a smooth curve
draw.drawCubicBezier(
    cc.p(0, 100),
    cc.p(80, 300),
    cc.p(160, 0),
    cc.p(240, 200),
    30,    // segments (higher = smoother)
    2,
    cc.color(255, 100, 0, 255)
)

// CatmullRom through waypoints
draw.drawCatmullRom(
    [cc.p(0,100), cc.p(80,200), cc.p(160,50), cc.p(240,180)],
    30,
    2,
    cc.color(0, 255, 100, 255)
)
```

## cc.DrawNode — State & Blending

```typescript
draw.clear(): void   // erase all drawn geometry

draw.getDrawColor(): cc.Color
draw.setDrawColor(color: cc.Color): void

draw.getLineWidth(): number
draw.setLineWidth(width: number): void

draw.getBlendFunc(): cc.BlendFunc
draw.setBlendFunc(blendFunc: cc.BlendFunc): void
draw.setBlendFunc(src: cc.BlenderConst, dst: cc.BlenderConst): void
```

**Example:**
```typescript
// Draw a debug bounding box that updates each frame
class DebugLayer extends cc.Layer {
    private _draw: cc.DrawNode
    private _target: cc.Node

    onEnter() {
        super.onEnter()
        this._draw = cc.DrawNode.create()
        this.addChild(this._draw)
        this.scheduleUpdate()
    }

    update(dt: number) {
        this._draw.clear()
        const box = this._target.getBoundingBoxToWorld()
        this._draw.drawRect(
            cc.p(box.x, box.y),
            cc.p(box.x + box.width, box.y + box.height),
            null,   // no fill
            1,
            cc.color(255, 0, 0, 255)
        )
    }
}
```
