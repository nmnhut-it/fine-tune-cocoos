# cc.sys, cc.path, cc Utilities

Platform detection, local storage, path utilities, and global helper functions.

## cc.sys — Platform Detection

```typescript
cc.sys.platform: number      // current platform code
cc.sys.isNative: boolean     // true in JSB (iOS/Android/Windows), false in browser
cc.sys.isMobile: boolean
cc.sys.os: string            // OS name string
cc.sys.language: number      // system language code

// Platform constants:
cc.sys.WIN32        // 0
cc.sys.LINUX        // 1
cc.sys.MACOS        // 2
cc.sys.ANDROID      // 3
cc.sys.IPHONE       // 4
cc.sys.IPAD         // 5
cc.sys.MOBILE_BROWSER   // 100
cc.sys.DESKTOP_BROWSER  // 101

// OS string constants:
cc.sys.OS_IOS        // 'iOS'
cc.sys.OS_ANDROID    // 'Android'
cc.sys.OS_WINDOWS    // 'Windows'
cc.sys.OS_OSX        // 'OS X'
cc.sys.OS_LINUX      // 'Linux'

// Language codes:
cc.sys.LANGUAGE_ENGLISH   // 'en'
cc.sys.LANGUAGE_CHINESE   // 'zh'
cc.sys.LANGUAGE_FRENCH    // 'fr'
cc.sys.LANGUAGE_GERMAN    // 'de'
cc.sys.LANGUAGE_JAPANESE  // 'ja'
cc.sys.LANGUAGE_KOREAN    // 'ko'
cc.sys.LANGUAGE_SPANISH   // 'es'
cc.sys.LANGUAGE_RUSSIAN   // 'ru'
cc.sys.LANGUAGE_PORTUGUESE // 'pt'

// Capabilities:
cc.sys.capabilities: {
    opengl: boolean
    accelerometer: boolean
    touches: boolean
    keyboard: boolean
    mouse: boolean
}

// Browser info (H5 only):
cc.sys.browserType: string | null   // 'chrome', 'safari', 'firefox', etc.
cc.sys.browserVersion: string | null
cc.sys.windowPixelResolution: cc.Size
```

**Example:**
```typescript
if (cc.sys.isNative) {
    // JSB-specific code (iOS/Android)
    const fileUtils = jsb.fileUtils
} else {
    // Web
}

if (cc.sys.platform === cc.sys.ANDROID) {
    // Android specific
}

if (cc.sys.os === cc.sys.OS_IOS) {
    // iOS specific UI adjustments
}

if (cc.sys.language === cc.sys.LANGUAGE_CHINESE) {
    loadChineseAssets()
}
```

## cc.sys — Local Storage

Persistent key-value storage.

```typescript
cc.sys.localStorage.setItem(key: string, value: string | number): void
cc.sys.localStorage.getItem(key: string): string | null | undefined
cc.sys.localStorage.removeItem(key: string): void
cc.sys.localStorage.clear(): void
```

**Example:**
```typescript
// Save/load player data
cc.sys.localStorage.setItem('highscore', score.toString())
cc.sys.localStorage.setItem('volume', '0.8')

const saved = cc.sys.localStorage.getItem('highscore')
const highscore = saved ? parseInt(saved) : 0

// Save JSON
cc.sys.localStorage.setItem('playerData', JSON.stringify({ name: 'Alice', level: 5 }))
const raw = cc.sys.localStorage.getItem('playerData')
const player = raw ? JSON.parse(raw) : {}
```

## cc.sys — System Utilities

```typescript
cc.sys.openURL(url: string): void      // open URL in system browser
cc.sys.garbageCollect(): void          // JSB only
cc.sys.dumpRoot(): void                // JSB only
cc.sys.restartVM(): void               // JSB only
cc.sys.isObjectValid(obj: object): boolean
cc.sys.dump(): void                    // dump system info
```

## cc.path — Path Utilities

```typescript
cc.path.join(...args: string[]): string    // join path segments
cc.path.extname(pathStr: string): string   // get extension (.png, .json)
cc.path.basename(pathStr: string, extname: string): string  // get filename
cc.path.dirname(pathStr: string): string   // get directory
```

**Example:**
```typescript
cc.path.join('res', 'hero', 'hero.png')  // 'res/hero/hero.png'
cc.path.extname('sprite.png')             // '.png'
cc.path.basename('res/hero.png', '.png') // 'hero'
cc.path.dirname('res/ui/button.png')     // 'res/ui'
```

## cc Global Logging

```typescript
cc.log(...args: any[]): void     // info log
cc.warn(...args: any[]): void    // warning log
cc.error(...args: any[]): void   // error log
cc.assert(...args: any[]): void  // assertion
cc.formatStr(...args: any[]): string  // format string
```

## cc Global Type Checks

```typescript
cc.isFunction(obj): obj is Function
cc.isNumber(obj): obj is number
cc.isString(obj): obj is string
cc.isArray(obj): obj is any[]
cc.isUndefined(obj): obj is undefined
cc.isObject(obj): obj is object
```

## cc.GLProgram & cc.GLProgramState — Custom Shaders

```typescript
const program = new cc.GLProgram()
program.initWithString(vertShaderStr: string, fragShaderStr: string): void
program.addAttribute(name: string, index: number): void
program.link(): void
program.use(): void
program.updateUniforms(): void
program.getUniformLocationForName(name: string): WebGLUniformLocation
program.setUniformLocationWith1f(loc, f1): void
program.setUniformLocationWith2f(loc, f1, f2): void
program.setUniformLocationWith4f(loc, f1, f2, f3, f4): void
program.setUniformLocationWithMatrix4fv(loc, mat: Float32Array): void
program.setUniformsForBuiltins(): void
program.getProgram(): WebGLProgram

// GLProgramState (simpler interface for uniforms)
const state = node.getGLProgramState()
state.setUniformInt(name: string, value: number): void
state.setUniformFloat(name: string, value: number): void
state.setUniformVec2(name: string, value: cc.Point): void
state.setUniformVec3(name: string, value: cc.math.Vec3): void
state.setUniformVec4(name: string, value: cc.math.Vec4): void
state.setUniformMat4(name: string, value: Float32Array): void
```

## cc.BlendFunc

```typescript
new cc.BlendFunc(src: cc.BlenderConst, dst: cc.BlenderConst)

// Common constants:
cc.ONE, cc.ZERO
cc.SRC_ALPHA, cc.ONE_MINUS_SRC_ALPHA
cc.DST_ALPHA, cc.ONE_MINUS_DST_ALPHA
cc.SRC_COLOR, cc.ONE_MINUS_SRC_COLOR
cc.BLEND_SRC, cc.BLEND_DST  // default blend func values

// Common blend presets:
// Normal alpha blend: src=SRC_ALPHA, dst=ONE_MINUS_SRC_ALPHA
// Additive: src=ONE, dst=ONE
// Premultiplied alpha: src=ONE, dst=ONE_MINUS_SRC_ALPHA
```

**Example:**
```typescript
// Additive blend for particles/glow
sprite.setBlendFunc(new cc.BlendFunc(cc.ONE, cc.ONE))
// Normal alpha blend:
sprite.setBlendFunc(new cc.BlendFunc(cc.SRC_ALPHA, cc.ONE_MINUS_SRC_ALPHA))
```

## gl Texture Constants

```typescript
gl.NEAREST            // pixelated sampling
gl.LINEAR             // smooth sampling
gl.NEAREST_MIPMAP_NEAREST
gl.LINEAR_MIPMAP_LINEAR  // trilinear filtering

gl.CLAMP_TO_EDGE      // clamp texture coordinates
gl.REPEAT             // tile
gl.MIRRORED_REPEAT    // mirror tile
```
