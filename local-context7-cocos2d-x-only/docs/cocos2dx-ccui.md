# ccui — UI Widgets

UI widget system. All widgets extend `cc.ProtectedNode` → `cc.Node`. The base class is `ccui.Widget`.

## ccui.Widget — Base

All UI widgets share these members.

**Properties:**
```typescript
widget.enabled: boolean           // enables/disables interaction
widget.touchEnabled: boolean
widget.bright: boolean
widget.focused: boolean
widget.name: string
widget.sizeType: ccui.Widget.SizeType
widget.actionTag: number
widget.xPercent: number           // position x in % of parent width
widget.yPercent: number
widget.flippedX: boolean
widget.flippedY: boolean
widget.widgetParent: ccui.Widget  // readonly, null if parent is not a widget
```

**Touch events:**
```typescript
widget.addTouchEventListener(selector: (sender: ccui.Widget, eventType: number) => void, target?: object): void
widget.addClickEventListener(callback: Function): void

// Touch event types:
ccui.Widget.TOUCH_BEGAN    // finger/mouse down
ccui.Widget.TOUCH_MOVED
ccui.Widget.TOUCH_ENDED    // successful tap
ccui.Widget.TOUCH_CANCELED
```

**Example:**
```typescript
btn.addTouchEventListener((sender, type) => {
    if (type === ccui.Widget.TOUCH_ENDED) {
        cc.log('button tapped')
        this.onBtnClick()
    }
}, this)

// Or simpler click-only:
btn.addClickEventListener(() => this.onBtnClick())
```

**Size & Position:**
```typescript
widget.getSize(): cc.Size
widget.setSize(size: cc.Size): void
widget.getSizePercent(): cc.Point
widget.setSizePercent(percent: cc.Point): void  // width/height 0–1 of parent
widget.getSizeType(): ccui.Widget.SizeType
widget.setSizeType(type: ccui.Widget.SizeType): void
// SIZE_ABSOLUTE = absolute pixels, SIZE_PERCENT = fraction of parent

widget.getPositionPercent(): cc.Point
widget.setPositionPercent(percent: cc.Point): void
widget.getPositionType(): number
widget.setPositionType(type: number): void
// POSITION_ABSOLUTE, POSITION_PERCENT

widget.getWorldPosition(): cc.Point
widget.getLeftBoundary(): number
widget.getRightBoundary(): number
widget.getTopBoundary(): number
widget.getBottomBoundary(): number
```

**State:**
```typescript
widget.isEnabled(): boolean
widget.setEnabled(enabled: boolean): void
widget.isTouchEnabled(): boolean
widget.setTouchEnabled(enable: boolean): void
widget.isBright(): boolean
widget.setBright(bright: boolean): void
widget.isHighlighted(): boolean
widget.setHighlighted(highlight: boolean): void
widget.isFocused(): boolean
widget.setFocused(focus: boolean): void
widget.requestFocus(): void
widget.click(): void  // programmatic click (for QC/testing)
widget.clone(): ccui.Widget
widget.ignoreContentAdaptWithSize(ignore: boolean): void
widget.updateSizeAndPosition(parentSize: cc.Size): void
```

## ccui.Button

Button with normal/pressed/disabled states and optional title text. Extends `ccui.Widget`.

```typescript
new ccui.Button(normalImage?: string, selectedImage?: string, disableImage?: string, texType?: number)
ccui.Button.create(normalImage?, selectedImage?, disableImage?, texType?): ccui.Button

// texType: ccui.Widget.LOCAL_TEXTURE (file) or ccui.Widget.PLIST_TEXTURE (sprite frame)
```

**Texture loading:**
```typescript
btn.loadTextures(normal: string, selected: string, disabled: string, texType?: number): void
btn.loadTextureNormal(normal: string, texType?: number): void
btn.loadTexturePressed(selected: string, texType?: number): void
btn.loadTextureDisabled(disabled: string, texType?: number): void
```

**Title text:**
```typescript
btn.getTitleText(): string
btn.setTitleText(text: string): void
btn.getTitleColor(): cc.Color
btn.setTitleColor(color: cc.Color): void
btn.getTitleFontSize(): number
btn.setTitleFontSize(size: number): void
btn.getTitleFontName(): string
btn.setTitleFontName(fontName: string): void
btn.getTitleRenderer(): cc.LabelTTF
// Properties: btn.titleText, btn.titleFontSize, btn.titleFontName
```

**Scale9 / capInsets:**
```typescript
btn.isScale9Enabled(): boolean
btn.setScale9Enabled(able: boolean): void
btn.setCapInsets(capInsets: cc.Rect): void
btn.setCapInsetsNormalRenderer(capInsets: cc.Rect): void
btn.setCapInsetsPressedRenderer(capInsets: cc.Rect): void
btn.setCapInsetsDisabledRenderer(capInsets: cc.Rect): void
btn.getNormalTextureSize(): cc.Size
btn.setPressedActionEnabled(enabled: boolean): void
btn.setZoomScale(scale: number): void
btn.getZoomScale(): number
```

**Example:**
```typescript
const btn = new ccui.Button('btn_normal.png', 'btn_pressed.png', '', ccui.Widget.PLIST_TEXTURE)
btn.setSize(cc.size(200, 60))
btn.setTitleText('PLAY')
btn.setTitleFontSize(24)
btn.setTitleColor(cc.color.WHITE)
btn.setPosition(centerX, 200)
btn.addClickEventListener(() => this.startGame())
this.addChild(btn)
```

## ccui.Layout

Container with layout management (absolute, linear, relative). Extends `ccui.Widget`.

```typescript
new ccui.Layout()

// Layout types:
ccui.Layout.ABSOLUTE          // free positioning (default)
ccui.Layout.LINEAR_HORIZONTAL // horizontal flow
ccui.Layout.LINEAR_VERTICAL   // vertical flow
ccui.Layout.RELATIVE          // relative positioning

// Background color types:
ccui.Layout.BG_COLOR_NONE
ccui.Layout.BG_COLOR_SOLID
ccui.Layout.BG_COLOR_GRADIENT

// Clipping types:
ccui.Layout.CLIPPING_STENCIL
ccui.Layout.CLIPPING_SCISSOR
```

**Layout type:**
```typescript
layout.layoutType: number
layout.getLayoutType(): number
layout.setLayoutType(type: number): void
layout.forceDoLayout(): void
layout.requestDoLayout(): void
```

**Clipping:**
```typescript
layout.clippingEnabled: boolean
layout.isClippingEnabled(): boolean
layout.setClippingEnabled(able: boolean): void
layout.getClippingType(): number
layout.setClippingType(type: number): void
```

**Background:**
```typescript
layout.setBackGroundImage(fileName: string, texType?: number): void
layout.removeBackGroundImage(): void
layout.setBackGroundImageScale9Enabled(able: boolean): void
layout.setBackGroundImageCapInsets(capInsets: cc.Rect): void
layout.setBackGroundColorType(type: number): void
layout.setBackGroundColor(color: cc.Color, endColor?: cc.Color): void
layout.setBackGroundColorOpacity(opacity: number): void
layout.setBackGroundColorVector(vector: cc.Point): void
layout.getBackGroundColor(): cc.Color
layout.getBackGroundEndColor(): cc.Color
layout.getBackGroundStartColor(): cc.Color
layout.getBackGroundColorOpacity(): number
layout.getBackGroundImageTextureSize(): cc.Size
```

**Example:**
```typescript
const panel = new ccui.Layout()
panel.setSize(cc.size(300, 400))
panel.setClippingEnabled(true)
panel.setBackGroundColorType(ccui.Layout.BG_COLOR_SOLID)
panel.setBackGroundColor(cc.color(0, 0, 0, 180))
panel.setPosition(100, 100)
this.addChild(panel)
```

## ccui.ScrollView

Scrollable container. Extends `ccui.Layout`.

```typescript
new ccui.ScrollView()

// Direction constants:
ccui.ScrollView.DIR_NONE
ccui.ScrollView.DIR_VERTICAL
ccui.ScrollView.DIR_HORIZONTAL
ccui.ScrollView.DIR_BOTH

// Events:
ccui.ScrollView.EVENT_SCROLL_TO_TOP
ccui.ScrollView.EVENT_SCROLL_TO_BOTTOM
ccui.ScrollView.EVENT_SCROLL_TO_LEFT
ccui.ScrollView.EVENT_SCROLL_TO_RIGHT
ccui.ScrollView.EVENT_SCROLLING
ccui.ScrollView.EVENT_BOUNCE_TOP / BOTTOM / LEFT / RIGHT
```

**Configuration:**
```typescript
sv.getDirection(): ccui.ScrollViewDirection
sv.setDirection(dir: ccui.ScrollViewDirection): void
sv.getInnerContainerSize(): cc.Size
sv.setInnerContainerSize(size: cc.Size): void  // must be >= scrollview size
sv.getInnerContainer(): ccui.Layout
sv.getInnerContainerPosition(): void
sv.setInnerContainerPosition(pos: cc.Point): void
sv.innerWidth: number
sv.innerHeight: number
sv.isBounceEnabled(): boolean
sv.setBounceEnabled(enabled: boolean): void
sv.isInertiaScrollEnabled(): boolean
sv.setInertiaScrollEnabled(enabled: boolean): void
sv.setScrollBarEnabled(enabled: boolean): void
sv.isScrollBarEnabled(): boolean
sv.setScrollBarColor(color: cc.Color): void
sv.setScrollBarOpacity(opacity: number): void
sv.setScrollBarWidth(width: number): void
sv.setScrollBarAutoHideEnabled(enabled: boolean): void
sv.setScrollBarAutoHideTime(time: number): void
```

**Scroll to position (instant):**
```typescript
sv.jumpToTop(): void
sv.jumpToBottom(): void
sv.jumpToLeft(): void
sv.jumpToRight(): void
sv.jumpToTopLeft(): void
sv.jumpToTopRight(): void
sv.jumpToBottomLeft(): void
sv.jumpToBottomRight(): void
sv.jumpToPercentVertical(percent: number): void    // 0–100
sv.jumpToPercentHorizontal(percent: number): void
sv.jumpToPercentBothDirection(percent: cc.Point): void
```

**Scroll animated:**
```typescript
sv.scrollToTop(time: number, attenuated: boolean): void
sv.scrollToBottom(time: number, attenuated: boolean): void
sv.scrollToLeft(time: number, attenuated: boolean): void
sv.scrollToRight(time: number, attenuated: boolean): void
sv.scrollToPercentVertical(percent: number, time: number, attenuated: boolean): void
sv.scrollToPercentHorizontal(percent: number, time: number, attenuated: boolean): void
```

**Event listener:**
```typescript
sv.addEventListener(selector: Function, target?: object): void
```

**Example:**
```typescript
const sv = new ccui.ScrollView()
sv.setSize(cc.size(300, 400))
sv.setInnerContainerSize(cc.size(300, 1200))  // tall inner content
sv.setDirection(ccui.ScrollView.DIR_VERTICAL)
sv.setBounceEnabled(true)
sv.setScrollBarEnabled(true)

// Add items to inner container
for (let i = 0; i < 20; i++) {
    const item = new ccui.Button('item_bg.png')
    item.setPosition(150, 1180 - i * 60)
    sv.getInnerContainer().addChild(item)
}

sv.addEventListener((sender, type) => {
    if (type === ccui.ScrollView.EVENT_SCROLL_TO_BOTTOM) {
        this.loadMoreItems()
    }
}, this)

this.addChild(sv)
sv.jumpToTop()
```

## ccui.ImageView

Displays an image, no interaction. Extends `ccui.Widget`.

```typescript
new ccui.ImageView(imageFileName?: string, texType?: number)
ccui.ImageView.create(imageFileName?, texType?): ccui.ImageView
view.loadTexture(fileName: string, texType?: number): void
view.setTextureRect(rect: cc.Rect): void
view.isScale9Enabled(): boolean
view.setScale9Enabled(able: boolean): void
view.setCapInsets(capInsets: cc.Rect): void
```

## ccui.Text

Text label widget. Extends `ccui.Widget`.

```typescript
new ccui.Text(textContent?: string, fontName?: string, fontSize?: number)
ccui.Text.create(text?, font?, fontSize?): ccui.Text
text.getString(): string
text.setString(text: string): void
text.getFontSize(): number
text.setFontSize(size: number): void
text.getFontName(): string
text.setFontName(name: string): void
text.getTextHorizontalAlignment(): number
text.setTextHorizontalAlignment(alignment: number): void
text.getTextVerticalAlignment(): number
text.setTextVerticalAlignment(alignment: number): void
text.setTextAreaSize(size: cc.Size): void
text.setTextColor(color: cc.Color): void
```

## ccui.TextField

Editable text input. Extends `ccui.Widget`.

```typescript
new ccui.TextField(placeholder?: string, fontName?: string, fontSize?: number)
tf.getString(): string
tf.setString(text: string): void
tf.getPlaceHolder(): string
tf.setPlaceHolder(value: string): void
tf.setPasswordEnabled(enable: boolean): void
tf.isPasswordEnabled(): boolean
tf.setMaxLength(length: number): void
tf.getMaxLength(): number
tf.setMaxLengthEnabled(enable: boolean): void
tf.setTouchAreaEnabled(enable: boolean): void
tf.addEventListener(callback: Function, target?: object): void
```

## ccui.Slider

Slider input. Extends `ccui.Widget`.

```typescript
new ccui.Slider()
slider.loadBarTexture(fileName: string, texType?: number): void
slider.loadSlidBallTextures(normal: string, pressed: string, disabled: string, texType?: number): void
slider.loadProgressBarTexture(fileName: string, texType?: number): void
slider.getPercent(): number
slider.setPercent(percent: number): void
slider.setMaxPercent(percent: number): void
slider.addEventListener(callback: Function, target?: object): void
```

## ccui.CheckBox

Checkbox toggle. Extends `ccui.Widget`.

```typescript
new ccui.CheckBox(
    backGround?: string, backGroundSelected?: string,
    cross?: string, backGroundDisabled?: string, frontCrossDisabled?: string,
    texType?: number
)
cb.isSelected(): boolean
cb.setSelected(selected: boolean): void
cb.addEventListener(callback: Function, target?: object): void
```

## ccui.LoadingBar

Progress bar. Extends `ccui.Widget`.

```typescript
new ccui.LoadingBar(textureName?: string, percentage?: number)
bar.loadTexture(fileName: string, texType?: number): void
bar.getPercent(): number
bar.setPercent(percent: number): void
bar.setDirection(dir: number): void   // LoadingBar.TYPE_LEFT or TYPE_RIGHT
```

## ccui.PageView

Swipeable paged view. Extends `ccui.Layout`.

```typescript
pv.addPage(page: ccui.Layout): void
pv.removePage(page: ccui.Layout): void
pv.scrollToPage(idx: number): void
pv.getCurrentPageIndex(): number
pv.addEventListener(callback: Function, target?: object): void
pv.setCustomScrollThreshold(threshold: number): void
pv.setUsingCustomScrollThreshold(flag: boolean): void
```

## ccui.ListView

Virtualized scrollable list. Extends `ccui.ScrollView`.

```typescript
lv.setItemModel(model: ccui.Widget): void
lv.addChild(child: ccui.Widget): void
lv.pushBackDefaultItem(): void
lv.insertDefaultItem(index: number): void
lv.pushBackCustomItem(item: ccui.Widget): void
lv.insertCustomItem(item: ccui.Widget, index: number): void
lv.removeItem(index: number): void
lv.removeAllItems(): void
lv.getItem(index: number): ccui.Widget
lv.getItems(): ccui.Widget[]
lv.getIndex(item: ccui.Widget): number
lv.getItemsCount(): number
lv.setGravity(gravity: number): void
lv.setItemsMargin(margin: number): void
lv.addEventListener(callback: Function, target?: object): void
lv.refreshView(): void
lv.doLayout(): void
lv.jumpToItem(idx: number, scroll: cc.Point, align: cc.Point): void
lv.scrollToItem(idx: number, scroll: cc.Point, align: cc.Point, time: number): void
```

## ccui Layout Parameters

Use `LayoutParameter` with LINEAR/RELATIVE layout types.

```typescript
// Linear layout parameter
const param = new ccui.LinearLayoutParameter()
param.setGravity(ccui.LinearLayoutParameter.CENTER_VERTICAL)
param.setMargin(new ccui.Margin(5, 5, 5, 5))
widget.setLayoutParameter(param)

// Relative layout parameter
const rel = new ccui.RelativeLayoutParameter()
rel.setAlign(ccui.RelativeLayoutParameter.PARENT_TOP_LEFT)
rel.setRelativeName('myWidget')
widget.setLayoutParameter(rel)

// Margin
const margin = new ccui.Margin(left, top, right, bottom)
```

## ccui Scale9Sprite

9-slice sprite for scalable UI elements.

```typescript
new ccui.Scale9Sprite(spriteFrame: string | cc.SpriteFrame, capInsets?: cc.Rect)
s9.setCapInsets(capInsets: cc.Rect): void
s9.setInsetLeft(inset: number): void
s9.setInsetRight(inset: number): void
s9.setInsetTop(inset: number): void
s9.setInsetBottom(inset: number): void
s9.setScale9Enabled(enabled: boolean): void
```

## ccui.helper

```typescript
ccui.helper.seekWidgetByName(root: ccui.Widget, name: string): ccui.Widget
ccui.helper.seekWidgetByTag(root: ccui.Widget, tag: number): ccui.Widget
ccui.helper.changeLayoutSystemActiveState(active: boolean): void
```
