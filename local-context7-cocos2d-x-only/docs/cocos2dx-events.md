# cc Events & Input

Event system, touch/mouse/keyboard listeners, and custom events.

## cc.EventListener.create

The primary way to register input listeners. Attach to a node via `cc.eventManager.addListener`.

```typescript
cc.EventListener.create(option: EventListenerCreateParam): cc.EventListener
```

**Touch (one by one — recommended for UI):**
```typescript
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    swallowTouches: true,
    onTouchBegan: (touch: cc.Touch, event: cc.Event) => boolean,
    onTouchMoved: (touch: cc.Touch, event: cc.EventTouch) => void,
    onTouchEnded: (touch: cc.Touch, event: cc.Event) => void,
    onTouchCancelled: (touch: cc.Touch, event: cc.Event) => void,
}, node)
```

**Touch (all at once — for multi-touch):**
```typescript
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ALL_AT_ONCE,
    onTouchesBegan: (touches: cc.Touch[], event: cc.Event) => void,
    onTouchesMoved: (touches: cc.Touch[], event: cc.Event) => void,
    onTouchesEnded: (touches: cc.Touch[], event: cc.Event) => void,
    onTouchesCancelled: (touches: cc.Touch[], event: cc.Event) => void,
}, node)
```

**Keyboard:**
```typescript
cc.eventManager.addListener({
    event: cc.EventListener.KEYBOARD,
    onKeyPressed: (keyCode: cc.KEY, event: cc.Event) => void,
    onKeyReleased: (keyCode: cc.KEY, event: cc.Event) => void,
}, node)
```

**Mouse:**
```typescript
cc.eventManager.addListener({
    event: cc.EventListener.MOUSE,
    onMouseDown: (event: cc.EventMouse) => void,
    onMouseUp: (event: cc.EventMouse) => void,
    onMouseMove: (event: cc.EventMouse) => void,
    onMouseScroll: (event: cc.EventMouse) => void,
}, node)
```

**Custom:**
```typescript
cc.eventManager.addListener({
    event: cc.EventListener.CUSTOM,
    callback: (event: cc.Event) => void,
}, priority_number)

// Shorthand for custom:
cc.eventManager.addCustomListener(eventName: string | number, callback: (event: cc.Event) => void): cc.EventListener
```

## cc.eventManager Methods

```typescript
cc.eventManager.addListener<T extends cc.EventListener>(listener: T, nodeOrPriority: cc.Node | number): T
cc.eventManager.removeListener(listener: cc.EventListener): void
cc.eventManager.removeListeners(listenerType: cc.Node | number, recursive?: boolean): void
cc.eventManager.removeCustomListeners(customEventName: string | number): void
cc.eventManager.removeAllListeners(): void
cc.eventManager.setPriority(listener: cc.EventListener, fixedPriority: number): void
cc.eventManager.dispatchEvent(event: cc.Event): void
cc.eventManager.dispatchCustomEvent(eventName: string | number, optionalUserData?: any): void
```

**Example:**
```typescript
class MyLayer extends cc.Layer {
    private _listener: cc.EventListener

    onEnter() {
        super.onEnter()
        this._listener = cc.eventManager.addListener({
            event: cc.EventListener.TOUCH_ONE_BY_ONE,
            swallowTouches: true,
            onTouchBegan: (touch, event) => {
                const loc = touch.getLocation()
                const nodeLocal = this.convertToNodeSpace(loc)
                cc.log('touch at', nodeLocal.x, nodeLocal.y)
                return true  // must return true to receive move/end
            },
            onTouchEnded: (touch, event) => {
                // handle tap
            }
        }, this)
    }

    onExit() {
        cc.eventManager.removeListener(this._listener)
        super.onExit()
    }
}
```

## cc.Touch

```typescript
touch.getID(): number | undefined            // native: touch index; H5: undefined
touch.getLocation(): cc.Point               // world position
touch.getLocationX(): number
touch.getLocationY(): number
touch.getPreviousLocation(): cc.Point
touch.getStartLocation(): cc.Point
touch.getDelta(): cc.Point                   // movement delta since last event
touch.getLocationInView(): cc.Point         // screen coordinates
touch.getPreviousLocationInView(): cc.Point
touch.getStartLocationInView(): cc.Point
```

**Example:**
```typescript
onTouchMoved: (touch, event) => {
    const delta = touch.getDelta()
    node.x += delta.x
    node.y += delta.y
}
```

## cc.EventMouse

```typescript
event.getButton(): number          // BUTTON_LEFT=0, BUTTON_RIGHT=1, BUTTON_MIDDLE=2
event.getLocation(): cc.Point
event.getLocationX(): number
event.getLocationY(): number
event.getDelta(): cc.Point
event.getDeltaX(): number
event.getDeltaY(): number
event.getScrollX(): number         // scroll delta x
event.getScrollY(): number         // scroll delta y

// Button constants:
cc.EventMouse.BUTTON_LEFT
cc.EventMouse.BUTTON_RIGHT
cc.EventMouse.BUTTON_MIDDLE
cc.EventMouse.DOWN
cc.EventMouse.UP
cc.EventMouse.MOVE
cc.EventMouse.SCROLL
```

## cc.Event

```typescript
event.getType(): number   // cc.Event.TOUCH, KEYBOARD, MOUSE, CUSTOM, etc.
event.getUserData<T>(): T
event.setUserData(data: any): void

// Type constants:
cc.Event.TOUCH
cc.Event.KEYBOARD
cc.Event.ACCELERATION
cc.Event.MOUSE
cc.Event.CUSTOM
```

## cc.EventTouch

```typescript
event.getTouches(): cc.Touch[]

// EventCode constants:
cc.EventTouch.EventCode.BEGAN
cc.EventTouch.EventCode.MOVED
cc.EventTouch.EventCode.ENDED
cc.EventTouch.EventCode.CANCELLED
cc.EventTouch.MAX_TOUCHES
```

## Custom Events (Pub/Sub)

```typescript
// Dispatch
cc.eventManager.dispatchCustomEvent('game:score_update', { score: 100 })

// Listen
const listener = cc.eventManager.addCustomListener('game:score_update', (event) => {
    const data = event.getUserData<{ score: number }>()
    updateScoreLabel(data.score)
})

// Remove
cc.eventManager.removeListener(listener)
// Or remove all:
cc.eventManager.removeCustomListeners('game:score_update')
```

## cc.KEY Enum

```typescript
cc.KEY.none = 0
cc.KEY.back = 6       // Android back
cc.KEY.menu = 18      // Android menu
cc.KEY.backspace = 8
cc.KEY.tab = 9
cc.KEY.enter = 13
cc.KEY.shift = 16
cc.KEY.ctrl = 17
cc.KEY.alt = 18
cc.KEY.escape = 27
cc.KEY.space = 32
cc.KEY.left = 37, cc.KEY.up = 38, cc.KEY.right = 39, cc.KEY.down = 40
cc.KEY.Delete = 46
cc.KEY.a–z (65–90)
cc.KEY['0'–'9'] (48–57)
cc.KEY.f1–f12 (112–123)
cc.KEY.dpadLeft = 1000, dpadRight = 1001, dpadUp = 1003, dpadDown = 1004
```

**Example:**
```typescript
cc.eventManager.addListener({
    event: cc.EventListener.KEYBOARD,
    onKeyPressed: (keyCode, event) => {
        if (keyCode === cc.KEY.back) {
            // Android back button
            cc.director.popScene()
        }
    }
}, this)
```
