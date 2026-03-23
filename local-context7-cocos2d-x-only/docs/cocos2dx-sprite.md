# cc.Sprite

2D image node. Extends `cc.Node`. Default anchor is (0.5, 0.5). Can render a full texture, a sub-rect, or a sprite frame from an atlas.

## cc.Sprite Constructor & Static Create

```typescript
// Constructors
new cc.Sprite()
new cc.Sprite(filename: string)
new cc.Sprite(texture: cc.Texture2D)
new cc.Sprite(texture: cc.Texture2D, rect: cc.Rect)
new cc.Sprite(spriteFrame: cc.SpriteFrame)

// Static factory (preferred in some patterns)
cc.Sprite.create(): cc.Sprite
cc.Sprite.create(filename: string): cc.Sprite
cc.Sprite.create(filename: string, rect: cc.Rect): cc.Sprite
```

**Example:**
```typescript
const s1 = new cc.Sprite('res/hero.png')
const s2 = new cc.Sprite('res/atlas.png', cc.rect(0, 0, 64, 64))
const s3 = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('hero_01.png'))
```

## cc.Sprite Texture Methods

```typescript
sprite.getTexture(): cc.Texture2D
sprite.setTexture(filename: string): void
sprite.setTexture(texture: cc.Texture2D): void
sprite.getTextureRect(): cc.Rect
sprite.setTextureRect(rect: cc.Rect): void
sprite.setTextureRect(rect: cc.Rect, rotated: boolean, untrimmedSize: cc.Size): void
sprite.isTextureRectRotated(): boolean
sprite.textureLoaded(): boolean
```

**Example:**
```typescript
sprite.setTexture('res/new_texture.png')
sprite.setTextureRect(cc.rect(64, 0, 64, 64))  // sub-rect of atlas
```

## cc.Sprite Frame Methods

```typescript
sprite.getSpriteFrame(): cc.SpriteFrame
sprite.setSpriteFrame(frameName: string): void
sprite.setSpriteFrame(frame: cc.SpriteFrame): void
sprite.isFrameDisplayed(frame: cc.SpriteFrame): boolean
sprite.setDisplayFrameWithAnimationName(animationName: string, frameIndex: number): void
```

**Example:**
```typescript
// Change frame by name (must be in spriteFrameCache)
sprite.setSpriteFrame('hero_run_01.png')
// Change frame by object
const frame = cc.spriteFrameCache.getSpriteFrame('hero_idle.png')
sprite.setSpriteFrame(frame)
```

## cc.Sprite Flip

```typescript
sprite.isFlippedX(): boolean
sprite.setFlippedX(flippedX: boolean): void
sprite.isFlippedY(): boolean
sprite.setFlippedY(flippedY: boolean): void
```

**Example:**
```typescript
// Flip sprite to face left
sprite.setFlippedX(true)
// Alternatively, use negative scale (also flips children):
sprite.setScaleX(sprite.getScaleX() * -1)
```

## cc.Sprite Blend & Batch

```typescript
sprite.getBlendFunc(): cc.BlendFunc
sprite.setBlendFunc(blendFunc: cc.BlendFunc): void
sprite.getBatchNode(): cc.SpriteBatchNode | null
sprite.setBatchNode(batchNode: cc.SpriteBatchNode): void
sprite.getAtlasIndex(): number
sprite.setAtlasIndex(index: number): void
sprite.getTextureAtlas(): cc.TextureAtlas
sprite.isDirty(): boolean
sprite.setDirty(dirty: boolean): void
```

## cc.Sprite Initialization (Advanced)

```typescript
sprite.initWithTexture(texture: cc.Texture2D): boolean
sprite.initWithTexture(texture: cc.Texture2D, rect: cc.Rect): boolean
sprite.initWithSpriteFrame(frame: cc.SpriteFrame): boolean
sprite.initWithSpriteFrameName(frameName: string): boolean
sprite.initWithFile(filename: string, rect?: cc.Rect): boolean
```

## cc.SpriteFrame

A frame referencing a region of a texture (used in atlases).

```typescript
new cc.SpriteFrame(filename: string | cc.Texture2D, rect: cc.Rect)
new cc.SpriteFrame(filename: string | cc.Texture2D, rect: cc.Rect, rotated: boolean, offset: cc.Point, originalSize: cc.Size)

frame.getTexture(): cc.Texture2D
frame.setTexture(texture: cc.Texture2D): void
frame.getOriginalSize(): cc.Size
frame.getRectInPixels(): cc.Rect
frame.isRotated(): boolean
```

## cc.spriteFrameCache

Global singleton for managing sprite frames loaded from plist files.

```typescript
cc.spriteFrameCache.addSpriteFrames(url: string, texture: string): void
cc.spriteFrameCache.getSpriteFrame(path: string): cc.SpriteFrame
cc.spriteFrameCache.removeUnusedSpriteFrames(): void
cc.spriteFrameCache.removeSpriteFramesFromFile(url: string): void
```

**Example:**
```typescript
// Load plist atlas
cc.spriteFrameCache.addSpriteFrames('res/ui.plist', 'res/ui.png')
// Use frame
const sprite = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('btn_play.png'))
// Or by name directly:
sprite.setSpriteFrame('btn_play.png')
```

## cc.SpriteBatchNode

Renders many sprites using one draw call (all must share the same texture).

```typescript
// Usage pattern:
const batch = new cc.SpriteBatchNode('res/atlas.png', 100)
layer.addChild(batch)
const s = new cc.Sprite(cc.spriteFrameCache.getSpriteFrame('enemy.png'))
batch.addChild(s)
```

## cc.textureCache

Global texture cache for managing loaded textures.

```typescript
cc.textureCache.addImage(path: string): void
cc.textureCache.getTextureForKey(key: string): cc.Texture2D
cc.textureCache.removeTextureForKey(key: string): void
cc.textureCache.removeUnusedTextures(): void
cc.textureCache.removeAllTextures(): void
```

## cc.Texture2D

Represents a GPU texture.

```typescript
texture.getContentSize(): cc.Size
texture.getContentSizeInPixels(): cc.Size
texture.getPixelsHigh(): number
texture.getPixelsWide(): number
texture.hasPremultipliedAlpha(): boolean
texture.setTexParameters(minFilter, magFilter, wrapS, wrapT): void
```
