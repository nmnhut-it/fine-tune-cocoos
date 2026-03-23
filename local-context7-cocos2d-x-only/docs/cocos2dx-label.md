# cc.Label

Unified label class supporting TTF fonts, bitmap fonts (BMFont), system fonts, and char maps. Extends `cc.Node`.

## cc.Label Static Factory Methods

```typescript
// System font (platform font, simplest)
cc.Label.createWithSystemFont(
    text: string,
    font: string,        // font family name or file path
    fontSize: number,
    dimensions?: cc.Size,
    hAlignment?: number, // cc.TEXT_ALIGNMENT_LEFT/CENTER/RIGHT
    vAlignment?: number  // cc.VERTICAL_TEXT_ALIGNMENT_TOP/CENTER/BOTTOM
): cc.Label

// TTF font (FreeType2, cross-platform)
cc.Label.createWithTTF(ttfConfig: any, text: string, hAlignment?: number, maxLineWidth?: number): cc.Label

// Bitmap font (.fnt file)
cc.Label.createWithBMFont(
    bmfontFilePath: string,
    text: string,
    hAlignment?: number,
    maxLineWidth?: number,
    imageOffset?: cc.Point
): cc.Label

// Char map
cc.Label.createWithCharMap(charMapFile: string, itemWidth: number, itemHeight: number, startCharCode: number): cc.Label
cc.Label.createWithCharMap(texture: cc.Texture2D, itemWidth: number, itemHeight: number, startCharCode: number): cc.Label
cc.Label.createWithCharMap(plistFile: string): cc.Label

cc.Label.create(): cc.Label  // empty label
```

**Example:**
```typescript
// System font
const lbl = cc.Label.createWithSystemFont('Hello World', 'Arial', 24)
this.addChild(lbl)
lbl.setPosition(cc.director.getWinSize().width / 2, 300)

// BMFont
const bm = cc.Label.createWithBMFont('res/fonts/score.fnt', '0000')
bm.setHorizontalAlignment(cc.TEXT_ALIGNMENT_RIGHT)

// TTF
const ttfConfig = { fontFilePath: 'res/fonts/myfont.ttf', fontSize: 32 }
const ttfLbl = cc.Label.createWithTTF(ttfConfig, 'Score: 0')
```

## cc.Label Text

```typescript
label.getString(): string
label.setString(text: string): void
label.getStringLength(): number
label.getStringNumLines(): number
label.updateContent(): void  // force immediate update
```

**Example:**
```typescript
label.setString(`Score: ${score}`)
label.setString('Hello\nWorld')  // multi-line
```

## cc.Label Alignment & Dimensions

```typescript
label.getHorizontalAlignment(): number
label.setHorizontalAlignment(alignment: number): void   // cc.TEXT_ALIGNMENT_LEFT/CENTER/RIGHT
label.getVerticalAlignment(): number
label.setVerticalAlignment(alignment: number): void     // cc.VERTICAL_TEXT_ALIGNMENT_TOP/CENTER/BOTTOM
label.setAlignment(hAlignment: number, vAlignment?: number): void
label.getTextAlignment(): number

label.getDimensions(): cc.Size
label.setDimensions(width: number, height: number): void  // clipping box
label.getWidth(): number
label.setWidth(width: number): void
label.getHeight(): number
label.setHeight(height: number): void
label.getMaxLineWidth(): number
label.setMaxLineWidth(maxLineWidth: number): void
label.setLineBreakWithoutSpace(enabled: boolean): void
label.setClipMarginEnabled(enabled: boolean): void
label.isClipMarginEnabled(): boolean
```

**Example:**
```typescript
// Center-aligned, fixed-width label
const lbl = cc.Label.createWithSystemFont('Hello', 'Arial', 20)
lbl.setDimensions(200, 0)  // width=200, height=0 means auto
lbl.setHorizontalAlignment(cc.TEXT_ALIGNMENT_CENTER)
lbl.setVerticalAlignment(cc.VERTICAL_TEXT_ALIGNMENT_CENTER)
```

## cc.Label Color & Effects

```typescript
label.getTextColor(): cc.Color
label.setTextColor(color: cc.Color): void   // different from node color

// Outline (TTF / system font only)
label.enableOutline(color: cc.Color, outlineSize: number): void

// Shadow
label.enableShadow(color?: cc.Color, offset?: cc.Size, blurRadius?: number): void

// Glow (TTF only)
label.enableGlow(color: cc.Color): void

// Gradient
label.enableGradient(first: cc.Color, second: cc.Color, direction: cc.Color): void
label.enableGradient(first: cc.Color, second: cc.Color, third: cc.Color, direction: cc.Color): void

// Disable effects
label.disableEffect(): void
label.disableEffect(effect: number): void

label.getBlendFunc(): cc.BlendFunc
label.setBlendFunc(src: cc.BlendFunc): void
label.setBlendFunc(src: cc.BlenderConst, dst: cc.BlenderConst): void
```

**Example:**
```typescript
const lbl = cc.Label.createWithSystemFont('SCORE', 'Impact', 36)
lbl.setTextColor(cc.color(255, 220, 0))
lbl.enableOutline(cc.color(0, 0, 0, 255), 2)
lbl.enableShadow(cc.color(0, 0, 0, 128), cc.size(2, -2), 0)
```

## cc.Label Font Configuration

```typescript
// System font
label.getSystemFontName(): string
label.setSystemFontName(fontName: string): void
label.getSystemFontSize(): number
label.setSystemFontSize(fontSize: number): void

// BMFont
label.getBMFontFilePath(): string
label.setBMFontFilePath(path: string, imageOffset: cc.Point): void

// TTF
label.getTTFConfig(): any

// Kerning / Line height (not system font)
label.getLineHeight(): number
label.setLineHeight(lineHeight: number): void
label.getAdditionalKerning(): number
label.setAdditionalKerning(kerning: number): void
```

## cc.Label Letter Sprite

Access individual character as sprite (not supported for system fonts).

```typescript
label.getLetter(letterIndex: number): cc.Sprite
```

**Example:**
```typescript
// Animate first letter
const letter = label.getLetter(0)
letter.runAction(cc.sequence(
    cc.scaleTo(0.1, 1.5),
    cc.scaleTo(0.1, 1.0)
))
```

## cc.Label Bezier Text

```typescript
label.enableCubicBezierCurves(
    origin: cc.Point, control1: cc.Point, control2: cc.Point, destination: cc.Point,
    align?: number, segments?: number
): void
label.enableQuadBezierCurves(
    origin: cc.Point, control: cc.Point, destination: cc.Point,
    align?: number, segments?: number
): void
label.setBezierAlignment(align: number): void  // 0=LEFT,1=CENTER,2=RIGHT,3=STRETCH
```

## Alignment Constants

```typescript
cc.TEXT_ALIGNMENT_LEFT    // 0
cc.TEXT_ALIGNMENT_CENTER  // 1
cc.TEXT_ALIGNMENT_RIGHT   // 2
cc.VERTICAL_TEXT_ALIGNMENT_TOP    // 0
cc.VERTICAL_TEXT_ALIGNMENT_CENTER // 1
cc.VERTICAL_TEXT_ALIGNMENT_BOTTOM // 2
```
