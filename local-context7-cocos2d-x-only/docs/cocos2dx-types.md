# Cocos2d-x Primitive Types

Core value types, math utilities, and global helpers used throughout the cc namespace.

## cc.Point / cc.p

A 2D point with `x` and `y` coordinates. Used everywhere for positions, sizes, anchors.

**Interface:**
```typescript
interface cc.Point { x: number; y: number }
```

**Factory functions:**
- `cc.p(x: number, y: number): cc.Point`
- `cc.p(point: cc.Point): cc.Point`

**Example:**
```typescript
const pos = cc.p(100, 200)
node.setPosition(pos)
node.setPosition(100, 200) // equivalent
```

## cc.Size / cc.size

Width and height dimensions.

**Interface:**
```typescript
interface cc.Size { width: number; height: number }
```

**Factory:**
- `cc.size(width: number, height: number): cc.Size`

**Example:**
```typescript
node.setContentSize(cc.size(200, 100))
const winSize = cc.director.getWinSize()  // cc.Size
```

## cc.Rect / cc.rect

Rectangle with position and dimensions. Origin is bottom-left.

**Interface:**
```typescript
interface cc.Rect { x: number; y: number; width: number; height: number }
```

**Factory:**
- `cc.rect(x, y, width, height): cc.Rect`
- `cc.rect(rect: cc.Rect): cc.Rect`

**Utility functions:**
- `cc.rectContainsPoint(rect, point): boolean`
- `cc.rectContainsRect(rect1, rect2): boolean`
- `cc.rectOverlapsRect(rectA, rectB): boolean`
- `cc.rectUnion(rectA, rectB): cc.Rect`
- `cc.rectIntersection(rectA, rectB): cc.Rect`

**Example:**
```typescript
const r = cc.rect(0, 0, 100, 50)
if (cc.rectContainsPoint(r, cc.p(50, 25))) { /* hit */ }
```

## cc.Color / cc.color

RGBA color with components 0–255.

**Class:**
```typescript
class cc.Color { r: number; g: number; b: number; a: number }
```

**Factory:**
- `cc.color(r, b, g, a?): cc.Color`

**Preset colors:**
- `cc.color.WHITE`, `cc.color.BLACK`, `cc.color.RED`, `cc.color.GREEN`
- `cc.color.BLUE`, `cc.color.YELLOW`, `cc.color.MAGENTA`, `cc.color.ORANGE`, `cc.color.GRAY`

**Utilities:**
- `cc.hexToColor(hex: string): cc.Color`
- `cc.colorToHex(color: cc.Color): string`

**Example:**
```typescript
node.setColor(cc.color(255, 0, 0))       // red
node.setColor(cc.color.WHITE)
label.setTextColor(cc.color(255, 200, 0, 200)) // semi-transparent gold
```

## cc.AffineTransform

2D affine transform matrix (a, b, c, d, tx, ty).

**Factory:** `cc.affineTransformMake(a, b, c, d, tx, ty): cc.AffineTransform`

**Utilities:**
- `cc.affineTransformTranslate(t, tx, ty): cc.AffineTransform`
- `cc.affineTransformScale(t, sx, sy): cc.AffineTransform`
- `cc.affineTransformRotate(t, angle): cc.AffineTransform`
- `cc.affineTransformConcat(t1, t2): cc.AffineTransform`
- `cc.affineTransformInvert(t): cc.AffineTransform`
- `cc.pointApplyAffineTransform(point, t): cc.Point`
- `cc.rectApplyAffineTransform(rect, t): cc.Rect`

## cc.math.Vec3 / cc.math.Vec4

3D and 4D vectors used for 3D transforms and rotations (JSB/native only).

**Vec3:**
```typescript
class cc.math.Vec3 { x: number; y: number; z: number }
cc.math.vec3(x, y, z): cc.math.Vec3
cc.math.vec3Cross(a, b): cc.math.Vec3
cc.math.vec3Dot(a, b): number
cc.math.vec3Normalize(a): cc.math.Vec3
```

**Vec4:**
```typescript
class cc.math.Vec4 { x: number; y: number; z: number; w: number }
cc.math.vec4(x, y, z, w): cc.math.Vec4
```

**Mat4:** `type cc.math.Mat4 = [16 numbers]`

**Example:**
```typescript
// 3D rotation (native only)
node.setRotation3D(cc.math.vec3(0, 45, 0))
node.setPosition3D(cc.math.vec3(100, 200, 0))
```

## cc Point Math Utilities

Vector math helpers for `cc.Point`.

```typescript
cc.pAdd(v1, v2): cc.Point       // v1 + v2
cc.pSub(v1, v2): cc.Point       // v1 - v2
cc.pMult(point, scalar): cc.Point
cc.pNeg(point): cc.Point
cc.pNormalize(v): cc.Point
cc.pLength(v): number
cc.pDistance(v1, v2): number
cc.pDistanceSQ(p1, p2): number
cc.pDot(v1, v2): number
cc.pLerp(a, b, alpha): cc.Point
cc.pMidpoint(v1, v2): cc.Point
cc.pAngle(a, b): number
cc.pRotateByAngle(v, pivot, angle): cc.Point
cc.clampf(value, min, max): number
```

**Example:**
```typescript
const dir = cc.pNormalize(cc.pSub(target, source))
const dist = cc.pDistance(nodeA.getPosition(), nodeB.getPosition())
```

## cc Constants

```typescript
cc.PI             // Math.PI
cc.RAD            // Math.PI / 180 (degrees to radians factor)
cc.DEG            // 180 / Math.PI (radians to degrees factor)
cc.FLT_EPSILON    // Float epsilon
cc.REPEAT_FOREVER // Repeat count constant for schedule
cc.winSize        // cc.Size - current window size (shortcut)

cc.degreesToRadians(angle): number
cc.radiansToDegrees(angle): number
cc.lerp(a, b, r): number
cc.clampf(value, min, max): number
```
