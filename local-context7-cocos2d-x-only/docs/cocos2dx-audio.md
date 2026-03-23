# cc.audioEngine

Singleton audio engine for playing music and sound effects. Access via `cc.audioEngine`.

## cc.audioEngine — Music (Background)

```typescript
cc.audioEngine.playMusic(url: string, loop: boolean): void
cc.audioEngine.stopMusic(releaseData?: boolean): void
cc.audioEngine.pauseMusic(): void
cc.audioEngine.resumeMusic(): void
cc.audioEngine.rewindMusic(): void
cc.audioEngine.isMusicPlaying(): boolean
cc.audioEngine.willPlayMusic(): boolean
cc.audioEngine.getMusicVolume(): number
cc.audioEngine.setMusicVolume(volume: number): void  // 0.0 – 1.0
cc.audioEngine.preloadMusic(path: string): void
```

**Example:**
```typescript
// Start background music looping
cc.audioEngine.playMusic('res/audio/bgm_main.mp3', true)
cc.audioEngine.setMusicVolume(0.7)

// Pause/resume on game pause
cc.audioEngine.pauseMusic()
cc.audioEngine.resumeMusic()

// Stop and release
cc.audioEngine.stopMusic(true)
```

## cc.audioEngine — Sound Effects

```typescript
cc.audioEngine.playEffect(url: string, loop?: boolean, pitch?: number, pan?: number, gain?: number): number | null
// Returns audio ID (number) to control the specific effect

cc.audioEngine.stopEffect(audioId: number): void
cc.audioEngine.pauseEffect(audioId: number): void
cc.audioEngine.resumeEffect(audioId: number): void
cc.audioEngine.stopAllEffects(): void
cc.audioEngine.pauseAllEffects(): void
cc.audioEngine.resumeAllEffects(): void
cc.audioEngine.unloadEffect(url: string): void
cc.audioEngine.getEffectsVolume(): number
cc.audioEngine.setEffectsVolume(volume: number): void  // 0.0 – 1.0
cc.audioEngine.preloadEffect(path: string): void
```

**Example:**
```typescript
// Play once
cc.audioEngine.playEffect('res/audio/sfx_coin.mp3')

// Play and track ID to stop later
const id = cc.audioEngine.playEffect('res/audio/sfx_loop.mp3', true)
// Later:
cc.audioEngine.stopEffect(id)

// Preload at startup
cc.audioEngine.preloadEffect('res/audio/sfx_hit.mp3')
cc.audioEngine.preloadEffect('res/audio/sfx_coin.mp3')

// Set volume
cc.audioEngine.setEffectsVolume(0.5)
```

## cc.audioEngine — Cleanup

```typescript
cc.audioEngine.end(): void  // stop music and all effects, release all
```

**Example:**
```typescript
// On game exit or scene cleanup
cc.audioEngine.stopAllEffects()
cc.audioEngine.stopMusic()
```
