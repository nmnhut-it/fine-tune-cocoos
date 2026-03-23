import json, os

def w(path, items):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"{path}: {len(items)} examples")

def e(instruction, output):
    return {"instruction": instruction, "input": "", "output": output}

# ============ CCUI ============
ccui = []

# ccui.Widget properties
ccui.append(e("What properties does ccui.Widget have?", "ccui.Widget properties: enabled, touchEnabled, bright, focused, name, sizeType, actionTag, xPercent, yPercent, flippedX, flippedY, widgetParent (readonly)."))
ccui.append(e("What is the type of widget.widgetParent?", "widget.widgetParent: ccui.Widget (readonly) — null if parent is not a widget."))
ccui.append(e("What is widget.actionTag?", "widget.actionTag: number — a tag used to identify the widget's action."))
ccui.append(e("What is widget.sizeType?", "widget.sizeType: ccui.Widget.SizeType — SIZE_ABSOLUTE or SIZE_PERCENT."))
ccui.append(e("How to listen for touch events on a ccui.Widget?", "widget.addTouchEventListener(callback, target) — callback receives (sender: ccui.Widget, eventType: number)."))
ccui.append(e("What are the ccui.Widget touch event type constants?", "ccui.Widget.TOUCH_BEGAN, ccui.Widget.TOUCH_MOVED, ccui.Widget.TOUCH_ENDED, ccui.Widget.TOUCH_CANCELED."))
ccui.append(e("How to add a simple click listener to a ccui.Widget?", "widget.addClickEventListener(callback: Function): void"))
ccui.append(e("What is the signature of addTouchEventListener?", "widget.addTouchEventListener(selector: (sender: ccui.Widget, eventType: number) => void, target?: object): void"))
ccui.append(e("What does widget.getSize() return?", "widget.getSize() returns cc.Size."))
ccui.append(e("What is the signature of widget.setSize?", "widget.setSize(size: cc.Size): void"))
ccui.append(e("What does widget.getSizePercent() return?", "widget.getSizePercent() returns cc.Point — width/height as 0–1 fraction of parent."))
ccui.append(e("What is the signature of widget.setSizePercent?", "widget.setSizePercent(percent: cc.Point): void — sets size as fraction of parent."))
ccui.append(e("What does widget.getSizeType() return?", "widget.getSizeType() returns ccui.Widget.SizeType — SIZE_ABSOLUTE or SIZE_PERCENT."))
ccui.append(e("What is the signature of widget.setSizeType?", "widget.setSizeType(type: ccui.Widget.SizeType): void"))
ccui.append(e("What does widget.getPositionPercent() return?", "widget.getPositionPercent() returns cc.Point."))
ccui.append(e("What is the signature of widget.setPositionPercent?", "widget.setPositionPercent(percent: cc.Point): void"))
ccui.append(e("What does widget.getPositionType() return?", "widget.getPositionType() returns number — POSITION_ABSOLUTE or POSITION_PERCENT."))
ccui.append(e("What does widget.getWorldPosition() return?", "widget.getWorldPosition() returns cc.Point — the widget's position in world coordinates."))
ccui.append(e("What does widget.getLeftBoundary() return?", "widget.getLeftBoundary() returns number — the left edge x-coordinate."))
ccui.append(e("What does widget.getRightBoundary() return?", "widget.getRightBoundary() returns number — the right edge x-coordinate."))
ccui.append(e("What does widget.getTopBoundary() return?", "widget.getTopBoundary() returns number — the top edge y-coordinate."))
ccui.append(e("What does widget.getBottomBoundary() return?", "widget.getBottomBoundary() returns number — the bottom edge y-coordinate."))
ccui.append(e("How to check if a widget is enabled?", "widget.isEnabled() returns boolean. Also accessible as widget.enabled property."))
ccui.append(e("What is the signature of widget.setEnabled?", "widget.setEnabled(enabled: boolean): void"))
ccui.append(e("How to check if touch is enabled on a widget?", "widget.isTouchEnabled() returns boolean."))
ccui.append(e("What is the signature of widget.setTouchEnabled?", "widget.setTouchEnabled(enable: boolean): void"))
ccui.append(e("What does widget.isBright() return?", "widget.isBright() returns boolean."))
ccui.append(e("What is the signature of widget.setBright?", "widget.setBright(bright: boolean): void"))
ccui.append(e("What does widget.isHighlighted() return?", "widget.isHighlighted() returns boolean."))
ccui.append(e("What is the signature of widget.setHighlighted?", "widget.setHighlighted(highlight: boolean): void"))
ccui.append(e("What does widget.isFocused() return?", "widget.isFocused() returns boolean."))
ccui.append(e("What is the signature of widget.setFocused?", "widget.setFocused(focus: boolean): void"))
ccui.append(e("What does widget.requestFocus() do?", "widget.requestFocus(): void — requests input focus for this widget."))
ccui.append(e("What does widget.click() do?", "widget.click(): void — triggers a programmatic click (for QC/testing)."))
ccui.append(e("What does widget.clone() return?", "widget.clone() returns ccui.Widget — a copy of the widget."))
ccui.append(e("What is the signature of widget.ignoreContentAdaptWithSize?", "widget.ignoreContentAdaptWithSize(ignore: boolean): void"))
ccui.append(e("What is the signature of widget.updateSizeAndPosition?", "widget.updateSizeAndPosition(parentSize: cc.Size): void"))
ccui.append(e("What are the ccui.Widget texture type constants?", "ccui.Widget.LOCAL_TEXTURE (file) and ccui.Widget.PLIST_TEXTURE (sprite frame)."))
ccui.append(e("Is ccui.Widget.PLIST_TEXTURE a valid constant?", "Yes. ccui.Widget.PLIST_TEXTURE indicates the texture comes from a sprite frame in a plist."))

# ccui.Button
ccui.append(e("How to create a ccui.Button?", "new ccui.Button(normalImage?, selectedImage?, disableImage?, texType?) or ccui.Button.create(normalImage?, selectedImage?, disableImage?, texType?)"))
ccui.append(e("What class does ccui.Button extend?", "ccui.Button extends ccui.Widget."))
ccui.append(e("What is the signature of ccui.Button constructor?", "new ccui.Button(normalImage?: string, selectedImage?: string, disableImage?: string, texType?: number)"))
ccui.append(e("What is the signature of btn.loadTextures?", "btn.loadTextures(normal: string, selected: string, disabled: string, texType?: number): void"))
ccui.append(e("What is the signature of btn.loadTextureNormal?", "btn.loadTextureNormal(normal: string, texType?: number): void"))
ccui.append(e("What is the signature of btn.loadTexturePressed?", "btn.loadTexturePressed(selected: string, texType?: number): void"))
ccui.append(e("What is the signature of btn.loadTextureDisabled?", "btn.loadTextureDisabled(disabled: string, texType?: number): void"))
ccui.append(e("What does btn.getTitleText() return?", "btn.getTitleText() returns string — the button's title text."))
ccui.append(e("What is the signature of btn.setTitleText?", "btn.setTitleText(text: string): void"))
ccui.append(e("What does btn.getTitleColor() return?", "btn.getTitleColor() returns cc.Color."))
ccui.append(e("What is the signature of btn.setTitleColor?", "btn.setTitleColor(color: cc.Color): void"))
ccui.append(e("What does btn.getTitleFontSize() return?", "btn.getTitleFontSize() returns number."))
ccui.append(e("What is the signature of btn.setTitleFontSize?", "btn.setTitleFontSize(size: number): void"))
ccui.append(e("What does btn.getTitleFontName() return?", "btn.getTitleFontName() returns string."))
ccui.append(e("What is the signature of btn.setTitleFontName?", "btn.setTitleFontName(fontName: string): void"))
ccui.append(e("What does btn.getTitleRenderer() return?", "btn.getTitleRenderer() returns cc.LabelTTF — the internal label renderer."))
ccui.append(e("What properties does ccui.Button expose for title?", "btn.titleText, btn.titleFontSize, btn.titleFontName — direct property access."))
ccui.append(e("How to check if Scale9 is enabled on a button?", "btn.isScale9Enabled() returns boolean."))
ccui.append(e("What is the signature of btn.setScale9Enabled?", "btn.setScale9Enabled(able: boolean): void"))
ccui.append(e("What is the signature of btn.setCapInsets?", "btn.setCapInsets(capInsets: cc.Rect): void"))
ccui.append(e("What is the signature of btn.setCapInsetsNormalRenderer?", "btn.setCapInsetsNormalRenderer(capInsets: cc.Rect): void"))
ccui.append(e("What is the signature of btn.setCapInsetsPressedRenderer?", "btn.setCapInsetsPressedRenderer(capInsets: cc.Rect): void"))
ccui.append(e("What is the signature of btn.setCapInsetsDisabledRenderer?", "btn.setCapInsetsDisabledRenderer(capInsets: cc.Rect): void"))
ccui.append(e("What does btn.getNormalTextureSize() return?", "btn.getNormalTextureSize() returns cc.Size."))
ccui.append(e("What is the signature of btn.setPressedActionEnabled?", "btn.setPressedActionEnabled(enabled: boolean): void"))
ccui.append(e("What is the signature of btn.setZoomScale?", "btn.setZoomScale(scale: number): void"))
ccui.append(e("What does btn.getZoomScale() return?", "btn.getZoomScale() returns number."))

# ccui.Layout
ccui.append(e("How to create a ccui.Layout?", "new ccui.Layout() — creates a container with layout management."))
ccui.append(e("What class does ccui.Layout extend?", "ccui.Layout extends ccui.Widget."))
ccui.append(e("What are the ccui.Layout type constants?", "ccui.Layout.ABSOLUTE, ccui.Layout.LINEAR_HORIZONTAL, ccui.Layout.LINEAR_VERTICAL, ccui.Layout.RELATIVE."))
ccui.append(e("What are the ccui.Layout background color type constants?", "ccui.Layout.BG_COLOR_NONE, ccui.Layout.BG_COLOR_SOLID, ccui.Layout.BG_COLOR_GRADIENT."))
ccui.append(e("What are the ccui.Layout clipping type constants?", "ccui.Layout.CLIPPING_STENCIL, ccui.Layout.CLIPPING_SCISSOR."))
ccui.append(e("What does layout.getLayoutType() return?", "layout.getLayoutType() returns number — one of ABSOLUTE, LINEAR_HORIZONTAL, LINEAR_VERTICAL, RELATIVE."))
ccui.append(e("What is the signature of layout.setLayoutType?", "layout.setLayoutType(type: number): void"))
ccui.append(e("What does layout.forceDoLayout() do?", "layout.forceDoLayout(): void — forces an immediate layout recalculation."))
ccui.append(e("What does layout.requestDoLayout() do?", "layout.requestDoLayout(): void — marks the layout as needing recalculation."))
ccui.append(e("How to check if clipping is enabled on a layout?", "layout.isClippingEnabled() returns boolean. Also accessible as layout.clippingEnabled."))
ccui.append(e("What is the signature of layout.setClippingEnabled?", "layout.setClippingEnabled(able: boolean): void"))
ccui.append(e("What does layout.getClippingType() return?", "layout.getClippingType() returns number — CLIPPING_STENCIL or CLIPPING_SCISSOR."))
ccui.append(e("What is the signature of layout.setClippingType?", "layout.setClippingType(type: number): void"))
ccui.append(e("What is the signature of layout.setBackGroundImage?", "layout.setBackGroundImage(fileName: string, texType?: number): void"))
ccui.append(e("What does layout.removeBackGroundImage() do?", "layout.removeBackGroundImage(): void — removes the background image."))
ccui.append(e("What is the signature of layout.setBackGroundImageScale9Enabled?", "layout.setBackGroundImageScale9Enabled(able: boolean): void"))
ccui.append(e("What is the signature of layout.setBackGroundImageCapInsets?", "layout.setBackGroundImageCapInsets(capInsets: cc.Rect): void"))
ccui.append(e("What is the signature of layout.setBackGroundColorType?", "layout.setBackGroundColorType(type: number): void — BG_COLOR_NONE, BG_COLOR_SOLID, or BG_COLOR_GRADIENT."))
ccui.append(e("What is the signature of layout.setBackGroundColor?", "layout.setBackGroundColor(color: cc.Color, endColor?: cc.Color): void — pass two colors for gradient."))
ccui.append(e("What is the signature of layout.setBackGroundColorOpacity?", "layout.setBackGroundColorOpacity(opacity: number): void"))
ccui.append(e("What is the signature of layout.setBackGroundColorVector?", "layout.setBackGroundColorVector(vector: cc.Point): void — sets the gradient direction."))
ccui.append(e("What does layout.getBackGroundColor() return?", "layout.getBackGroundColor() returns cc.Color."))
ccui.append(e("What does layout.getBackGroundEndColor() return?", "layout.getBackGroundEndColor() returns cc.Color — the end color of a gradient background."))
ccui.append(e("What does layout.getBackGroundStartColor() return?", "layout.getBackGroundStartColor() returns cc.Color — the start color of a gradient background."))
ccui.append(e("What does layout.getBackGroundColorOpacity() return?", "layout.getBackGroundColorOpacity() returns number (0–255)."))
ccui.append(e("What does layout.getBackGroundImageTextureSize() return?", "layout.getBackGroundImageTextureSize() returns cc.Size."))

# ccui.ScrollView
ccui.append(e("How to create a ccui.ScrollView?", "new ccui.ScrollView() — creates a scrollable container."))
ccui.append(e("What class does ccui.ScrollView extend?", "ccui.ScrollView extends ccui.Layout."))
ccui.append(e("What are the ccui.ScrollView direction constants?", "ccui.ScrollView.DIR_NONE, ccui.ScrollView.DIR_VERTICAL, ccui.ScrollView.DIR_HORIZONTAL, ccui.ScrollView.DIR_BOTH."))
ccui.append(e("What are the ccui.ScrollView event constants?", "EVENT_SCROLL_TO_TOP, EVENT_SCROLL_TO_BOTTOM, EVENT_SCROLL_TO_LEFT, EVENT_SCROLL_TO_RIGHT, EVENT_SCROLLING, EVENT_BOUNCE_TOP/BOTTOM/LEFT/RIGHT."))
ccui.append(e("What does sv.getDirection() return?", "sv.getDirection() returns ccui.ScrollViewDirection."))
ccui.append(e("What is the signature of sv.setDirection?", "sv.setDirection(dir: ccui.ScrollViewDirection): void"))
ccui.append(e("What does sv.getInnerContainerSize() return?", "sv.getInnerContainerSize() returns cc.Size — the size of the inner scrollable area."))
ccui.append(e("What is the signature of sv.setInnerContainerSize?", "sv.setInnerContainerSize(size: cc.Size): void — must be >= scrollview size."))
ccui.append(e("What does sv.getInnerContainer() return?", "sv.getInnerContainer() returns ccui.Layout — the inner container to which children are added."))
ccui.append(e("What is the signature of sv.setInnerContainerPosition?", "sv.setInnerContainerPosition(pos: cc.Point): void"))
ccui.append(e("How to check if bounce is enabled on a ScrollView?", "sv.isBounceEnabled() returns boolean."))
ccui.append(e("What is the signature of sv.setBounceEnabled?", "sv.setBounceEnabled(enabled: boolean): void"))
ccui.append(e("How to check if inertia scroll is enabled?", "sv.isInertiaScrollEnabled() returns boolean."))
ccui.append(e("What is the signature of sv.setInertiaScrollEnabled?", "sv.setInertiaScrollEnabled(enabled: boolean): void"))
ccui.append(e("What is the signature of sv.setScrollBarEnabled?", "sv.setScrollBarEnabled(enabled: boolean): void"))
ccui.append(e("What is the signature of sv.setScrollBarColor?", "sv.setScrollBarColor(color: cc.Color): void"))
ccui.append(e("What is the signature of sv.setScrollBarOpacity?", "sv.setScrollBarOpacity(opacity: number): void"))
ccui.append(e("What is the signature of sv.setScrollBarWidth?", "sv.setScrollBarWidth(width: number): void"))
ccui.append(e("What is the signature of sv.setScrollBarAutoHideEnabled?", "sv.setScrollBarAutoHideEnabled(enabled: boolean): void"))
ccui.append(e("What is the signature of sv.setScrollBarAutoHideTime?", "sv.setScrollBarAutoHideTime(time: number): void"))
ccui.append(e("What does sv.jumpToTop() do?", "sv.jumpToTop(): void — instantly scrolls to the top."))
ccui.append(e("What does sv.jumpToBottom() do?", "sv.jumpToBottom(): void — instantly scrolls to the bottom."))
ccui.append(e("What does sv.jumpToLeft() do?", "sv.jumpToLeft(): void — instantly scrolls to the left."))
ccui.append(e("What does sv.jumpToRight() do?", "sv.jumpToRight(): void — instantly scrolls to the right."))
ccui.append(e("What does sv.jumpToTopLeft() do?", "sv.jumpToTopLeft(): void — instantly scrolls to the top-left corner."))
ccui.append(e("What does sv.jumpToTopRight() do?", "sv.jumpToTopRight(): void — instantly scrolls to the top-right corner."))
ccui.append(e("What does sv.jumpToBottomLeft() do?", "sv.jumpToBottomLeft(): void — instantly scrolls to the bottom-left corner."))
ccui.append(e("What does sv.jumpToBottomRight() do?", "sv.jumpToBottomRight(): void — instantly scrolls to the bottom-right corner."))
ccui.append(e("What is the signature of sv.jumpToPercentVertical?", "sv.jumpToPercentVertical(percent: number): void — percent is 0–100."))
ccui.append(e("What is the signature of sv.jumpToPercentHorizontal?", "sv.jumpToPercentHorizontal(percent: number): void — percent is 0–100."))
ccui.append(e("What is the signature of sv.jumpToPercentBothDirection?", "sv.jumpToPercentBothDirection(percent: cc.Point): void"))
ccui.append(e("What is the signature of sv.scrollToTop?", "sv.scrollToTop(time: number, attenuated: boolean): void"))
ccui.append(e("What is the signature of sv.scrollToBottom?", "sv.scrollToBottom(time: number, attenuated: boolean): void"))
ccui.append(e("What is the signature of sv.scrollToLeft?", "sv.scrollToLeft(time: number, attenuated: boolean): void"))
ccui.append(e("What is the signature of sv.scrollToRight?", "sv.scrollToRight(time: number, attenuated: boolean): void"))
ccui.append(e("What is the signature of sv.scrollToPercentVertical?", "sv.scrollToPercentVertical(percent: number, time: number, attenuated: boolean): void"))
ccui.append(e("What is the signature of sv.scrollToPercentHorizontal?", "sv.scrollToPercentHorizontal(percent: number, time: number, attenuated: boolean): void"))
ccui.append(e("How to listen for scroll events on a ScrollView?", "sv.addEventListener(selector: Function, target?: object): void"))
ccui.append(e("Is ccui.ScrollView.EVENT_SCROLLING a valid constant?", "Yes. ccui.ScrollView.EVENT_SCROLLING fires continuously while the user scrolls."))

# ccui.ImageView
ccui.append(e("How to create a ccui.ImageView?", "new ccui.ImageView(imageFileName?: string, texType?: number) or ccui.ImageView.create(imageFileName?, texType?)"))
ccui.append(e("What class does ccui.ImageView extend?", "ccui.ImageView extends ccui.Widget."))
ccui.append(e("What is the signature of view.loadTexture?", "view.loadTexture(fileName: string, texType?: number): void"))
ccui.append(e("What is the signature of view.setTextureRect?", "view.setTextureRect(rect: cc.Rect): void"))
ccui.append(e("How to enable Scale9 on an ImageView?", "view.setScale9Enabled(able: boolean): void"))
ccui.append(e("What is the signature of ImageView.setCapInsets?", "view.setCapInsets(capInsets: cc.Rect): void"))

# ccui.Text
ccui.append(e("How to create a ccui.Text?", "new ccui.Text(textContent?: string, fontName?: string, fontSize?: number) or ccui.Text.create(text?, font?, fontSize?)"))
ccui.append(e("What class does ccui.Text extend?", "ccui.Text extends ccui.Widget."))
ccui.append(e("What does text.getString() return?", "text.getString() returns string."))
ccui.append(e("What is the signature of text.setString?", "text.setString(text: string): void"))
ccui.append(e("What does text.getFontSize() return?", "text.getFontSize() returns number."))
ccui.append(e("What is the signature of text.setFontSize?", "text.setFontSize(size: number): void"))
ccui.append(e("What does text.getFontName() return?", "text.getFontName() returns string."))
ccui.append(e("What is the signature of text.setFontName?", "text.setFontName(name: string): void"))
ccui.append(e("What does text.getTextHorizontalAlignment() return?", "text.getTextHorizontalAlignment() returns number — cc.TEXT_ALIGNMENT_LEFT/CENTER/RIGHT."))
ccui.append(e("What is the signature of text.setTextHorizontalAlignment?", "text.setTextHorizontalAlignment(alignment: number): void"))
ccui.append(e("What does text.getTextVerticalAlignment() return?", "text.getTextVerticalAlignment() returns number — cc.VERTICAL_TEXT_ALIGNMENT_TOP/CENTER/BOTTOM."))
ccui.append(e("What is the signature of text.setTextVerticalAlignment?", "text.setTextVerticalAlignment(alignment: number): void"))
ccui.append(e("What is the signature of text.setTextAreaSize?", "text.setTextAreaSize(size: cc.Size): void"))
ccui.append(e("What is the signature of text.setTextColor?", "text.setTextColor(color: cc.Color): void"))

# ccui.TextField
ccui.append(e("How to create a ccui.TextField?", "new ccui.TextField(placeholder?: string, fontName?: string, fontSize?: number)"))
ccui.append(e("What class does ccui.TextField extend?", "ccui.TextField extends ccui.Widget."))
ccui.append(e("What does tf.getString() return?", "tf.getString() returns string — the current input text."))
ccui.append(e("What is the signature of tf.setString?", "tf.setString(text: string): void"))
ccui.append(e("What does tf.getPlaceHolder() return?", "tf.getPlaceHolder() returns string."))
ccui.append(e("What is the signature of tf.setPlaceHolder?", "tf.setPlaceHolder(value: string): void"))
ccui.append(e("What is the signature of tf.setPasswordEnabled?", "tf.setPasswordEnabled(enable: boolean): void"))
ccui.append(e("What does tf.isPasswordEnabled() return?", "tf.isPasswordEnabled() returns boolean."))
ccui.append(e("What is the signature of tf.setMaxLength?", "tf.setMaxLength(length: number): void"))
ccui.append(e("What does tf.getMaxLength() return?", "tf.getMaxLength() returns number."))
ccui.append(e("What is the signature of tf.setMaxLengthEnabled?", "tf.setMaxLengthEnabled(enable: boolean): void"))
ccui.append(e("What is the signature of tf.setTouchAreaEnabled?", "tf.setTouchAreaEnabled(enable: boolean): void"))

# ccui.Slider
ccui.append(e("How to create a ccui.Slider?", "new ccui.Slider()"))
ccui.append(e("What class does ccui.Slider extend?", "ccui.Slider extends ccui.Widget."))
ccui.append(e("What is the signature of slider.loadBarTexture?", "slider.loadBarTexture(fileName: string, texType?: number): void"))
ccui.append(e("What is the signature of slider.loadSlidBallTextures?", "slider.loadSlidBallTextures(normal: string, pressed: string, disabled: string, texType?: number): void"))
ccui.append(e("What is the signature of slider.loadProgressBarTexture?", "slider.loadProgressBarTexture(fileName: string, texType?: number): void"))
ccui.append(e("What does slider.getPercent() return?", "slider.getPercent() returns number — current slider percentage."))
ccui.append(e("What is the signature of slider.setPercent?", "slider.setPercent(percent: number): void"))
ccui.append(e("What is the signature of slider.setMaxPercent?", "slider.setMaxPercent(percent: number): void"))

# ccui.CheckBox
ccui.append(e("How to create a ccui.CheckBox?", "new ccui.CheckBox(backGround?, backGroundSelected?, cross?, backGroundDisabled?, frontCrossDisabled?, texType?)"))
ccui.append(e("What class does ccui.CheckBox extend?", "ccui.CheckBox extends ccui.Widget."))
ccui.append(e("What does cb.isSelected() return?", "cb.isSelected() returns boolean — true if checkbox is checked."))
ccui.append(e("What is the signature of cb.setSelected?", "cb.setSelected(selected: boolean): void"))

# ccui.LoadingBar
ccui.append(e("How to create a ccui.LoadingBar?", "new ccui.LoadingBar(textureName?: string, percentage?: number)"))
ccui.append(e("What class does ccui.LoadingBar extend?", "ccui.LoadingBar extends ccui.Widget."))
ccui.append(e("What does bar.getPercent() return?", "bar.getPercent() returns number — current progress percentage."))
ccui.append(e("What is the signature of bar.setPercent?", "bar.setPercent(percent: number): void"))
ccui.append(e("What is the signature of bar.setDirection for LoadingBar?", "bar.setDirection(dir: number): void — LoadingBar.TYPE_LEFT or LoadingBar.TYPE_RIGHT."))
ccui.append(e("What is the signature of bar.loadTexture for LoadingBar?", "bar.loadTexture(fileName: string, texType?: number): void"))

# ccui.PageView
ccui.append(e("What class does ccui.PageView extend?", "ccui.PageView extends ccui.Layout."))
ccui.append(e("What is the signature of pv.addPage?", "pv.addPage(page: ccui.Layout): void"))
ccui.append(e("What is the signature of pv.removePage?", "pv.removePage(page: ccui.Layout): void"))
ccui.append(e("What is the signature of pv.scrollToPage?", "pv.scrollToPage(idx: number): void"))
ccui.append(e("What does pv.getCurrentPageIndex() return?", "pv.getCurrentPageIndex() returns number — the index of the currently visible page."))
ccui.append(e("What is the signature of pv.setCustomScrollThreshold?", "pv.setCustomScrollThreshold(threshold: number): void"))
ccui.append(e("What is the signature of pv.setUsingCustomScrollThreshold?", "pv.setUsingCustomScrollThreshold(flag: boolean): void"))

# ccui.ListView
ccui.append(e("What class does ccui.ListView extend?", "ccui.ListView extends ccui.ScrollView."))
ccui.append(e("What is the signature of lv.setItemModel?", "lv.setItemModel(model: ccui.Widget): void — sets the template widget for default items."))
ccui.append(e("What does lv.pushBackDefaultItem() do?", "lv.pushBackDefaultItem(): void — appends a clone of the item model to the list."))
ccui.append(e("What is the signature of lv.insertDefaultItem?", "lv.insertDefaultItem(index: number): void"))
ccui.append(e("What is the signature of lv.pushBackCustomItem?", "lv.pushBackCustomItem(item: ccui.Widget): void"))
ccui.append(e("What is the signature of lv.insertCustomItem?", "lv.insertCustomItem(item: ccui.Widget, index: number): void"))
ccui.append(e("What is the signature of lv.removeItem?", "lv.removeItem(index: number): void"))
ccui.append(e("What does lv.removeAllItems() do?", "lv.removeAllItems(): void — removes all items from the list."))
ccui.append(e("What does lv.getItem() return?", "lv.getItem(index: number) returns ccui.Widget."))
ccui.append(e("What does lv.getItems() return?", "lv.getItems() returns ccui.Widget[] — array of all items."))
ccui.append(e("What does lv.getIndex() return?", "lv.getIndex(item: ccui.Widget) returns number — the index of the given item."))
ccui.append(e("What does lv.getItemsCount() return?", "lv.getItemsCount() returns number."))
ccui.append(e("What is the signature of lv.setGravity?", "lv.setGravity(gravity: number): void"))
ccui.append(e("What is the signature of lv.setItemsMargin?", "lv.setItemsMargin(margin: number): void"))
ccui.append(e("What does lv.refreshView() do?", "lv.refreshView(): void — refreshes the list layout."))
ccui.append(e("What does lv.doLayout() do?", "lv.doLayout(): void — forces layout recalculation."))
ccui.append(e("What is the signature of lv.jumpToItem?", "lv.jumpToItem(idx: number, scroll: cc.Point, align: cc.Point): void"))
ccui.append(e("What is the signature of lv.scrollToItem?", "lv.scrollToItem(idx: number, scroll: cc.Point, align: cc.Point, time: number): void"))

# ccui.LinearLayoutParameter
ccui.append(e("How to create a ccui.LinearLayoutParameter?", "new ccui.LinearLayoutParameter()"))
ccui.append(e("What is the signature of param.setGravity for LinearLayoutParameter?", "param.setGravity(ccui.LinearLayoutParameter.CENTER_VERTICAL): void"))
ccui.append(e("What is the signature of param.setMargin?", "param.setMargin(new ccui.Margin(left, top, right, bottom)): void"))
ccui.append(e("How to assign a layout parameter to a widget?", "widget.setLayoutParameter(param: ccui.LayoutParameter): void"))

# ccui.RelativeLayoutParameter
ccui.append(e("How to create a ccui.RelativeLayoutParameter?", "new ccui.RelativeLayoutParameter()"))
ccui.append(e("What is the signature of rel.setAlign?", "rel.setAlign(ccui.RelativeLayoutParameter.PARENT_TOP_LEFT): void"))
ccui.append(e("What is the signature of rel.setRelativeName?", "rel.setRelativeName(name: string): void"))

# ccui.Margin
ccui.append(e("How to create a ccui.Margin?", "new ccui.Margin(left: number, top: number, right: number, bottom: number)"))

# ccui.Scale9Sprite
ccui.append(e("How to create a ccui.Scale9Sprite?", "new ccui.Scale9Sprite(spriteFrame: string | cc.SpriteFrame, capInsets?: cc.Rect)"))
ccui.append(e("What is the signature of s9.setCapInsets?", "s9.setCapInsets(capInsets: cc.Rect): void"))
ccui.append(e("What is the signature of s9.setInsetLeft?", "s9.setInsetLeft(inset: number): void"))
ccui.append(e("What is the signature of s9.setInsetRight?", "s9.setInsetRight(inset: number): void"))
ccui.append(e("What is the signature of s9.setInsetTop?", "s9.setInsetTop(inset: number): void"))
ccui.append(e("What is the signature of s9.setInsetBottom?", "s9.setInsetBottom(inset: number): void"))
ccui.append(e("What is the signature of s9.setScale9Enabled?", "s9.setScale9Enabled(enabled: boolean): void"))

# ccui.helper
ccui.append(e("What is the signature of ccui.helper.seekWidgetByName?", "ccui.helper.seekWidgetByName(root: ccui.Widget, name: string): ccui.Widget"))
ccui.append(e("What is the signature of ccui.helper.seekWidgetByTag?", "ccui.helper.seekWidgetByTag(root: ccui.Widget, tag: number): ccui.Widget"))
ccui.append(e("What does ccui.helper.changeLayoutSystemActiveState do?", "ccui.helper.changeLayoutSystemActiveState(active: boolean): void — enables/disables the layout system."))

# Correct vs wrong
ccui.append(e("Is ccui.Widget.addChildren() a valid method?", "No. The correct method is ccui.Widget's parent cc.Node.addChild(child, localZOrder, tag)."))
ccui.append(e("Is ccui.Button.setText() a valid method?", "No. Use btn.setTitleText(text: string) instead."))
ccui.append(e("Is ccui.ScrollView.scrollTo() a valid method?", "No. Use specific methods like sv.scrollToTop(time, attenuated), sv.scrollToBottom(time, attenuated), etc."))
ccui.append(e("Is ccui.ListView.addItem() a valid method?", "No. Use lv.pushBackCustomItem(item: ccui.Widget) or lv.pushBackDefaultItem()."))
ccui.append(e("Is ccui.Layout.setBackground() a valid method?", "No. Use layout.setBackGroundImage(fileName, texType) or layout.setBackGroundColor(color)."))
ccui.append(e("Is ccui.TextField.getText() a valid method?", "No. Use tf.getString() to get the text content."))
ccui.append(e("Is ccui.CheckBox.isChecked() a valid method?", "No. Use cb.isSelected() to check if the checkbox is checked."))
ccui.append(e("Is ccui.Slider.getValue() a valid method?", "No. Use slider.getPercent() to get the current value."))

# Class membership
ccui.append(e("Which class has the addTouchEventListener method?", "ccui.Widget — addTouchEventListener(selector, target)."))
ccui.append(e("Which class has the setTitleText method?", "ccui.Button — setTitleText(text: string)."))
ccui.append(e("Which class has the setInnerContainerSize method?", "ccui.ScrollView — setInnerContainerSize(size: cc.Size)."))
ccui.append(e("Which class has the setItemModel method?", "ccui.ListView — setItemModel(model: ccui.Widget)."))
ccui.append(e("Which class has the addPage method?", "ccui.PageView — addPage(page: ccui.Layout)."))
ccui.append(e("Which class has the setPlaceHolder method?", "ccui.TextField — setPlaceHolder(value: string)."))
ccui.append(e("Which class has the loadBarTexture method?", "ccui.Slider — loadBarTexture(fileName, texType)."))
ccui.append(e("Which class has the setBackGroundColorType method?", "ccui.Layout — setBackGroundColorType(type: number)."))
ccui.append(e("Which class has the seekWidgetByName function?", "ccui.helper — ccui.helper.seekWidgetByName(root, name)."))

# Comparison
ccui.append(e("Difference between ccui.Widget.addTouchEventListener and addClickEventListener?", "addTouchEventListener fires for BEGAN/MOVED/ENDED/CANCELED events. addClickEventListener fires only on successful tap (click)."))
ccui.append(e("Difference between ccui.Layout.ABSOLUTE and LINEAR_VERTICAL?", "ABSOLUTE uses free positioning (x,y). LINEAR_VERTICAL stacks children top-to-bottom with layout parameters."))
ccui.append(e("Difference between sv.jumpToTop() and sv.scrollToTop()?", "jumpToTop() moves instantly. scrollToTop(time, attenuated) animates over `time` seconds."))
ccui.append(e("Difference between ccui.Text and ccui.TextField?", "ccui.Text is a read-only label widget. ccui.TextField is an editable text input with placeholder support."))
ccui.append(e("Difference between ccui.ImageView and cc.Sprite?", "ccui.ImageView extends ccui.Widget with UI features (touch, layout). cc.Sprite is a lighter scene graph node."))
ccui.append(e("Difference between lv.pushBackDefaultItem() and lv.pushBackCustomItem()?", "pushBackDefaultItem() clones the item model set by setItemModel(). pushBackCustomItem(item) adds a specific widget."))
ccui.append(e("Difference between widget.getSize() and widget.getContentSize()?", "widget.getSize() returns the widget's UI size. getContentSize() is inherited from cc.Node and may differ if ignoreContentAdaptWithSize is used."))

# Property access
ccui.append(e("How to get or set button title text?", "btn.setTitleText('text') / btn.getTitleText(), or directly btn.titleText = 'text'."))
ccui.append(e("How to get or set widget enabled state?", "widget.setEnabled(true) / widget.isEnabled(), or widget.enabled = true."))
ccui.append(e("How to get or set widget touch enabled?", "widget.setTouchEnabled(true) / widget.isTouchEnabled(), or widget.touchEnabled = true."))
ccui.append(e("How to access the inner container of a ScrollView?", "sv.getInnerContainer() returns ccui.Layout — add children to this container."))
ccui.append(e("How to get or set layout clipping?", "layout.setClippingEnabled(true) / layout.isClippingEnabled(), or layout.clippingEnabled = true."))

w('D:/fine-tune-cocoos/data/raw-api/ccui.jsonl', ccui)

# ============ NODE ============
node = []

# Properties
node.append(e("What properties does cc.Node have?", "x, y, width, height, rotation, rotationX, rotationY, scale, scaleX, scaleY, skewX, skewY, opacity, color, visible, tag, zIndex, parent, children, childrenCount, running, anchorX, anchorY, and more."))
node.append(e("What is node.running?", "node.running: boolean (readonly) — true if the node is currently on the stage (added to the scene graph)."))
node.append(e("What is node.cascadeOpacity?", "node.cascadeOpacity: boolean — when true, opacity changes propagate to child nodes."))
node.append(e("What is node.cascadeColor?", "node.cascadeColor: boolean — when true, color changes propagate to child nodes."))
node.append(e("What is node.ignoreAnchor?", "node.ignoreAnchor: boolean — if true, anchor point is ignored for positioning (treated as 0,0)."))
node.append(e("What is node.userData?", "node.userData: object — custom user data attached to the node."))
node.append(e("What is node.scheduler?", "node.scheduler: cc.Scheduler — the scheduler associated with this node."))
node.append(e("What is node.actionManager?", "node.actionManager: cc.ActionManager — the action manager for this node."))
node.append(e("What is node.shaderProgram?", "node.shaderProgram: cc.GLProgram — the shader program used by this node."))
node.append(e("What is node.vertexZ?", "node.vertexZ: number — the real OpenGL Z vertex."))

# Position methods
node.append(e("What does node.getPosition() return?", "node.getPosition() returns cc.Point."))
node.append(e("What is the signature of node.setPosition?", "node.setPosition(x: number, y: number): void — or node.setPosition(pos: cc.Point): void."))
node.append(e("What does node.getPositionX() return?", "node.getPositionX() returns number."))
node.append(e("What is the signature of node.setPositionX?", "node.setPositionX(x: number): void"))
node.append(e("What does node.getPositionY() return?", "node.getPositionY() returns number."))
node.append(e("What is the signature of node.setPositionY?", "node.setPositionY(y: number): void"))
node.append(e("What does node.getNormalizedPosition() return?", "node.getNormalizedPosition() returns cc.Point — position as 0-1 fraction of parent size."))
node.append(e("What is the signature of node.setNormalizedPosition?", "node.setNormalizedPosition(pos: cc.Point): void — or node.setNormalizedPosition(x, y)."))

# Size & Anchor
node.append(e("What does node.getContentSize() return?", "node.getContentSize() returns cc.Size."))
node.append(e("What is the signature of node.setContentSize?", "node.setContentSize(size: cc.Size): void — or node.setContentSize(width, height)."))
node.append(e("What does node.getAnchorPoint() return?", "node.getAnchorPoint() returns cc.Point — normalized (0-1) anchor."))
node.append(e("What is the signature of node.setAnchorPoint?", "node.setAnchorPoint(point: cc.Point): void — or node.setAnchorPoint(x, y)."))
node.append(e("What does node.getAnchorPointInPoints() return?", "node.getAnchorPointInPoints() returns cc.Point — anchor position in pixels."))
node.append(e("What is the signature of node.ignoreAnchorPointForPosition?", "node.ignoreAnchorPointForPosition(newValue: boolean): void"))
node.append(e("What does node.isIgnoreAnchorPointForPosition() return?", "node.isIgnoreAnchorPointForPosition() returns boolean."))

# Rotation & Scale
node.append(e("What does node.getRotation() return?", "node.getRotation() returns number — rotation in degrees (clockwise positive)."))
node.append(e("What is the signature of node.setRotation?", "node.setRotation(degrees: number): void"))
node.append(e("What does node.getScale() return?", "node.getScale() returns number."))
node.append(e("What is the signature of node.setScale?", "node.setScale(scale: number): void — or node.setScale(scaleX, scaleY)."))
node.append(e("What does node.getScaleX() return?", "node.getScaleX() returns number."))
node.append(e("What is the signature of node.setScaleX?", "node.setScaleX(scaleX: number): void"))
node.append(e("What does node.getScaleY() return?", "node.getScaleY() returns number."))
node.append(e("What is the signature of node.setScaleY?", "node.setScaleY(scaleY: number): void"))
node.append(e("What does node.getSkewX() return?", "node.getSkewX() returns number."))
node.append(e("What is the signature of node.setSkewX?", "node.setSkewX(degrees: number): void"))
node.append(e("What does node.getSkewY() return?", "node.getSkewY() returns number."))
node.append(e("What is the signature of node.setSkewY?", "node.setSkewY(degrees: number): void"))
node.append(e("What does node.getRotation3D() return?", "node.getRotation3D() returns cc.math.Vec3 — JSB native only."))
node.append(e("What is the signature of node.setRotation3D?", "node.setRotation3D(rotation: cc.math.Vec3): void — JSB native only."))
node.append(e("What does node.getPosition3D() return?", "node.getPosition3D() returns cc.math.Vec3 — JSB native only."))
node.append(e("What is the signature of node.setPosition3D?", "node.setPosition3D(position: cc.math.Vec3): void — JSB native only."))

# Visibility & Color
node.append(e("What does node.isVisible() return?", "node.isVisible() returns boolean."))
node.append(e("What is the signature of node.setVisible?", "node.setVisible(visible: boolean): void"))
node.append(e("What does node.getOpacity() return?", "node.getOpacity() returns number (0–255)."))
node.append(e("What is the signature of node.setOpacity?", "node.setOpacity(opacity: number): void — 0–255."))
node.append(e("What does node.getDisplayedOpacity() return?", "node.getDisplayedOpacity() returns number — the inherited/cascaded opacity."))
node.append(e("What does node.getColor() return?", "node.getColor() returns cc.Color."))
node.append(e("What is the signature of node.setColor?", "node.setColor(color: cc.Color): void"))
node.append(e("What does node.getDisplayedColor() return?", "node.getDisplayedColor() returns cc.Color — the inherited/cascaded color."))
node.append(e("What does node.isCascadeOpacityEnabled() return?", "node.isCascadeOpacityEnabled() returns boolean."))
node.append(e("What is the signature of node.setCascadeOpacityEnabled?", "node.setCascadeOpacityEnabled(enabled: boolean): void"))
node.append(e("What does node.isCascadeColorEnabled() return?", "node.isCascadeColorEnabled() returns boolean."))
node.append(e("What is the signature of node.setCascadeColorEnabled?", "node.setCascadeColorEnabled(enabled: boolean): void"))

# Z-Order
node.append(e("What does node.getLocalZOrder() return?", "node.getLocalZOrder() returns number."))
node.append(e("What is the signature of node.setLocalZOrder?", "node.setLocalZOrder(z: number): void"))
node.append(e("Is node.setZOrder() a valid method?", "Yes. node.setZOrder(z) is an alias for node.setLocalZOrder(z)."))
node.append(e("What does node.getGlobalZOrder() return?", "node.getGlobalZOrder() returns number."))
node.append(e("What is the signature of node.setGlobalZOrder?", "node.setGlobalZOrder(z: number): void"))
node.append(e("What is the signature of node.reorderChild?", "node.reorderChild(child: cc.Node, zOrder: number): void"))
node.append(e("What does node.sortAllChildren() do?", "node.sortAllChildren(): void — sorts children by z-order."))

# Children Management
node.append(e("What is the signature of node.addChild?", "node.addChild(child: cc.Node, localZOrder?: number, tag?: number | string): void"))
node.append(e("What is the signature of node.removeChild?", "node.removeChild(child: cc.Node, cleanup?: boolean): void"))
node.append(e("What is the signature of node.removeChildByTag?", "node.removeChildByTag(tag: number, cleanup?: boolean): void"))
node.append(e("What is the signature of node.removeChildByName?", "node.removeChildByName(name: string, cleanup?: boolean): void"))
node.append(e("What does node.removeAllChildren() do?", "node.removeAllChildren(cleanup?: boolean): void — removes all child nodes."))
node.append(e("What does node.removeFromParent() do?", "node.removeFromParent(cleanup?: boolean): void — removes this node from its parent."))
node.append(e("What does node.getChildByTag() return?", "node.getChildByTag(tag: number) returns cc.Node or null."))
node.append(e("What does node.getChildByName() return?", "node.getChildByName(name: string) returns cc.Node or null."))
node.append(e("What does node.getChildren() return?", "node.getChildren() returns cc.Node[] — array of child nodes."))
node.append(e("What does node.getChildrenCount() return?", "node.getChildrenCount() returns number."))
node.append(e("What does node.getParent() return?", "node.getParent() returns cc.Node."))
node.append(e("What is the signature of node.setParent?", "node.setParent(parent: cc.Node): void"))
node.append(e("What is the signature of node.enumerateChildren?", "node.enumerateChildren(name: string, callback: (node: cc.Node) => boolean): void"))

# Tag & Name
node.append(e("What does node.getTag() return?", "node.getTag() returns number."))
node.append(e("What is the signature of node.setTag?", "node.setTag(tag: number): void"))
node.append(e("What does node.getName() return?", "node.getName() returns string."))
node.append(e("What is the signature of node.setName?", "node.setName(name: string): void"))

# Bounding Box
node.append(e("What does node.getBoundingBox() return?", "node.getBoundingBox() returns cc.Rect — in local/parent space."))
node.append(e("What does node.getBoundingBoxToWorld() return?", "node.getBoundingBoxToWorld() returns cc.Rect — in world space."))

# Coordinate Conversion
node.append(e("What is the signature of node.convertToNodeSpace?", "node.convertToNodeSpace(worldPoint: cc.Point): cc.Point"))
node.append(e("What is the signature of node.convertToWorldSpace?", "node.convertToWorldSpace(nodePoint: cc.Point): cc.Point"))
node.append(e("What is the signature of node.convertToNodeSpaceAR?", "node.convertToNodeSpaceAR(worldPoint: cc.Point): cc.Point — anchor-relative."))
node.append(e("What is the signature of node.convertToWorldSpaceAR?", "node.convertToWorldSpaceAR(nodePoint: cc.Point): cc.Point — anchor-relative."))
node.append(e("What is the signature of node.convertTouchToNodeSpace?", "node.convertTouchToNodeSpace(touch: cc.Touch): cc.Point"))
node.append(e("What is the signature of node.convertTouchToNodeSpaceAR?", "node.convertTouchToNodeSpaceAR(touch: cc.Touch): cc.Point"))
node.append(e("Difference between convertToNodeSpace and convertToNodeSpaceAR?", "convertToNodeSpace uses the node's bottom-left as origin. convertToNodeSpaceAR uses the anchor point as origin."))

# Transform
node.append(e("What does node.getNodeToParentTransform() return?", "node.getNodeToParentTransform(parent?: cc.Node) returns cc.AffineTransform."))
node.append(e("What does node.getNodeToWorldTransform() return?", "node.getNodeToWorldTransform() returns cc.AffineTransform."))
node.append(e("What does node.getParentToNodeTransform() return?", "node.getParentToNodeTransform() returns cc.AffineTransform."))
node.append(e("What does node.getWorldToNodeTransform() return?", "node.getWorldToNodeTransform() returns cc.AffineTransform."))
node.append(e("What is the signature of node.setAdditionalTransform?", "node.setAdditionalTransform(t: cc.AffineTransform): void"))

# Actions
node.append(e("What does node.runAction() return?", "node.runAction(action: cc.Action) returns cc.Action — the same action passed in."))
node.append(e("What does node.stopAllActions() do?", "node.stopAllActions(): void — stops and removes all running actions."))
node.append(e("What is the signature of node.stopAction?", "node.stopAction(action: cc.Action): void"))
node.append(e("What is the signature of node.stopActionByTag?", "node.stopActionByTag(tag: number): void"))
node.append(e("What does node.getActionByTag() return?", "node.getActionByTag(tag: number) returns cc.Action."))
node.append(e("What does node.getNumberOfRunningActions() return?", "node.getNumberOfRunningActions() returns number."))

# Scheduling
node.append(e("What does node.scheduleUpdate() do?", "node.scheduleUpdate(): void — registers update(dt) to be called every frame."))
node.append(e("What is the signature of node.scheduleUpdateWithPriority?", "node.scheduleUpdateWithPriority(priority: number): void"))
node.append(e("What does node.unscheduleUpdate() do?", "node.unscheduleUpdate(): void — stops the per-frame update callback."))
node.append(e("What is the signature of node.schedule?", "node.schedule(callback, interval?, repeat?, delay?, key?): void"))
node.append(e("What is the signature of node.scheduleOnce?", "node.scheduleOnce(callback: (dt: number) => void, delay: number, key?: string): void"))
node.append(e("What does node.unscheduleAllCallbacks() do?", "node.unscheduleAllCallbacks(): void — removes all scheduled callbacks."))

# Lifecycle
node.append(e("What are the cc.Node lifecycle callbacks?", "onEnter, onExit, onEnterTransitionDidFinish, onExitTransitionDidStart, cleanup, update."))
node.append(e("When is node.onEnter() called?", "node.onEnter() is called when the node is added to the stage (scene graph)."))
node.append(e("When is node.onExit() called?", "node.onExit() is called when the node is removed from the stage."))
node.append(e("What does node.cleanup() do?", "node.cleanup(): void — stops all actions and scheduled callbacks."))
node.append(e("What does node.pause() do?", "node.pause(): void — pauses all actions and schedulers."))
node.append(e("What does node.resume() do?", "node.resume(): void — resumes all paused actions and schedulers."))

# Shader & Physics
node.append(e("What does node.getShaderProgram() return?", "node.getShaderProgram() returns cc.GLProgram."))
node.append(e("What is the signature of node.setShaderProgram?", "node.setShaderProgram(program: cc.GLProgram): void"))
node.append(e("What does node.getGLProgramState() return?", "node.getGLProgramState() returns cc.GLProgramState."))
node.append(e("What is the signature of node.setPhysicsBody?", "node.setPhysicsBody(body: any): void"))
node.append(e("What does node.getPhysicsBody() return?", "node.getPhysicsBody() returns the physics body or null."))
node.append(e("What is the signature of node.setCameraMask?", "node.setCameraMask(mask: number, applyChildren?: boolean): void"))
node.append(e("What does node.getScene() return?", "node.getScene() returns cc.Scene or null."))

# attr
node.append(e("What is the signature of node.attr?", "node.attr(attrs: object): void — sets multiple properties at once."))

# Correct vs wrong
node.append(e("Is cc.Node.addChildren() a valid method?", "No. The correct method is cc.Node.addChild(child, localZOrder, tag)."))
node.append(e("Is cc.Node.setPos() a valid method?", "No. Use node.setPosition(x, y) or node.setPosition(cc.p(x, y))."))
node.append(e("Is cc.Node.getChildByIndex() a valid method?", "No. Use node.getChildren()[index] to access a child by index."))
node.append(e("Is cc.Node.removeAllChildrenAndCleanup() a valid method?", "No. Use node.removeAllChildren(cleanup?: boolean) — pass true to cleanup."))

# Class membership
node.append(e("Which class has the runAction method?", "cc.Node — node.runAction(action: cc.Action): cc.Action."))
node.append(e("Which class has the scheduleUpdate method?", "cc.Node — node.scheduleUpdate(): void."))
node.append(e("Which class has the convertToWorldSpace method?", "cc.Node — node.convertToWorldSpace(nodePoint: cc.Point): cc.Point."))
node.append(e("Which class has the getBoundingBox method?", "cc.Node — node.getBoundingBox(): cc.Rect."))

# Comparison
node.append(e("Difference between node.getLocalZOrder() and node.getGlobalZOrder()?", "getLocalZOrder() returns z-order relative to siblings. getGlobalZOrder() returns z-order in the global rendering order."))
node.append(e("Difference between node.removeChild() and node.removeFromParent()?", "removeChild(child) removes a specific child. removeFromParent() removes the node itself from its parent."))
node.append(e("Difference between node.x and node.getPositionX()?", "Both return the x position. node.x is direct property access (faster). getPositionX() is the getter method."))

w('D:/fine-tune-cocoos/data/raw-api/node.jsonl', node)

# ============ ACTIONS ============
actions = []

# Base classes
actions.append(e("What are the action base classes in Cocos2d-x?", "cc.Action (base), cc.FiniteTimeAction (has duration), cc.ActionInstant (zero-duration), cc.ActionInterval (time-based)."))
actions.append(e("What does action.getDuration() return?", "action.getDuration() returns number — the duration in seconds."))
actions.append(e("What is the signature of action.setDuration?", "action.setDuration(duration: number): void"))
actions.append(e("What does action.reverse() return?", "action.reverse() returns the reversed action (same type)."))
actions.append(e("What does action.repeat() do?", "action.repeat(times: number) returns the action repeated N times."))
actions.append(e("What does action.repeatForever() do?", "action.repeatForever() returns the action repeating indefinitely."))
actions.append(e("What is the signature of action.easing?", "action.easing(easeObj: cc.ActionEase): this — applies an easing function."))
actions.append(e("What does action.getSpeed() return?", "action.getSpeed() returns number."))
actions.append(e("What is the signature of action.setSpeed?", "action.setSpeed(speed: number): void"))
actions.append(e("What does action.clone() return?", "action.clone() returns a copy of the action."))

# Move
actions.append(e("What is the signature of cc.moveTo?", "cc.moveTo(duration: number, x: number, y: number): MoveTo — or cc.moveTo(duration, pos: cc.Point)."))
actions.append(e("What is the signature of cc.moveBy?", "cc.moveBy(duration: number, dx: number, dy: number): MoveBy — or cc.moveBy(duration, dPos: cc.Point)."))
actions.append(e("What does cc.moveTo() return?", "cc.moveTo() returns a MoveTo action instance."))
actions.append(e("What does cc.moveBy() return?", "cc.moveBy() returns a MoveBy action instance."))

# Scale
actions.append(e("What is the signature of cc.scaleTo?", "cc.scaleTo(duration: number, scale: number): ScaleTo — or cc.scaleTo(duration, scaleX, scaleY)."))
actions.append(e("What is the signature of cc.scaleBy?", "cc.scaleBy(duration: number, scale: number): ScaleBy — or cc.scaleBy(duration, scaleX, scaleY)."))
actions.append(e("What does cc.scaleTo() return?", "cc.scaleTo() returns a ScaleTo action instance."))
actions.append(e("What does cc.scaleBy() return?", "cc.scaleBy() returns a ScaleBy action instance."))

# Rotate
actions.append(e("What is the signature of cc.rotateTo?", "cc.rotateTo(duration: number, angle: number): RotateTo — also supports (duration, angleX, angleY) and (duration, vec3)."))
actions.append(e("What is the signature of cc.rotateBy?", "cc.rotateBy(duration: number, angle: number): RotateBy — also supports (duration, angleX, angleY)."))
actions.append(e("What does cc.rotateTo() return?", "cc.rotateTo() returns a RotateTo action instance."))
actions.append(e("What does cc.rotateBy() return?", "cc.rotateBy() returns a RotateBy action instance."))

# Fade
actions.append(e("What is the signature of cc.fadeIn?", "cc.fadeIn(duration: number): FadeIn — fades opacity from 0 to 255."))
actions.append(e("What is the signature of cc.fadeOut?", "cc.fadeOut(duration: number): FadeOut — fades opacity from 255 to 0."))
actions.append(e("What is the signature of cc.fadeTo?", "cc.fadeTo(duration: number, opacity: number): FadeTo"))
actions.append(e("What does cc.fadeIn() return?", "cc.fadeIn() returns a FadeIn action instance."))
actions.append(e("What does cc.fadeOut() return?", "cc.fadeOut() returns a FadeOut action instance."))

# Jump & Bezier
actions.append(e("What is the signature of cc.jumpTo?", "cc.jumpTo(duration, position: cc.Point, height: number, jumps: number): JumpTo — or cc.jumpTo(duration, x, y, height, jumps)."))
actions.append(e("What is the signature of cc.jumpBy?", "cc.jumpBy(duration, position: cc.Point, height: number, jumps: number): JumpBy"))
actions.append(e("What is the signature of cc.bezierTo?", "cc.bezierTo(duration: number, points: cc.Point[]): BezierTo — requires 3 control points."))
actions.append(e("What is the signature of cc.bezierBy?", "cc.bezierBy(duration: number, points: cc.Point[]): BezierBy — requires 3 control points."))
actions.append(e("What is the signature of cc.catmullRomTo?", "cc.catmullRomTo(duration: number, points: cc.Point[]): CatmullRomTo"))
actions.append(e("What is the signature of cc.catmullRomBy?", "cc.catmullRomBy(duration: number, points: cc.Point[]): CatmullRomBy"))
actions.append(e("What is the signature of cc.cardinalSplineTo?", "cc.cardinalSplineTo(duration: number, points: cc.Point[], tension: number): CardinalSplineTo"))
actions.append(e("What is the signature of cc.cardinalSplineBy?", "cc.cardinalSplineBy(duration: number, points: cc.Point[], tension: number): CardinalSplineBy"))

# Tint
actions.append(e("What is the signature of cc.tintTo?", "cc.tintTo(duration: number, red: number, green: number, blue: number): TintTo"))
actions.append(e("What is the signature of cc.tintBy?", "cc.tintBy(duration: number, deltaRed: number, deltaGreen: number, deltaBlue: number): TintBy"))

# Blink & Skew
actions.append(e("What is the signature of cc.blink?", "cc.blink(duration: number, blinks: number): Blink"))
actions.append(e("What is the signature of cc.skewTo?", "cc.skewTo(duration: number, skewX: number, skewY: number): SkewTo"))
actions.append(e("What is the signature of cc.skewBy?", "cc.skewBy(duration: number, skewX: number, skewY: number): SkewBy"))
actions.append(e("What is the signature of cc.delayTime?", "cc.delayTime(duration: number): DelayTime"))

# Instant Actions
actions.append(e("What does cc.show() return?", "cc.show() returns a Show action — makes the node visible."))
actions.append(e("What does cc.hide() return?", "cc.hide() returns a Hide action — makes the node invisible."))
actions.append(e("What does cc.toggleVisibility() return?", "cc.toggleVisibility() returns a ToggleVisibility action — toggles node.visible."))
actions.append(e("What is the signature of cc.place?", "cc.place(x: number, y: number): Place — or cc.place(pos: cc.Point)."))
actions.append(e("What does cc.removeSelf() return?", "cc.removeSelf() returns a RemoveSelf action — removes the node from its parent."))
actions.append(e("What is the signature of cc.flipX?", "cc.flipX(flip: boolean): FlipX"))
actions.append(e("What is the signature of cc.flipY?", "cc.flipY(flip: boolean): FlipY"))
actions.append(e("What is the signature of cc.callFunc?", "cc.callFunc(callback: Function): CallFunc — or cc.callFunc(callback, selectorTarget, data)."))

# Composite
actions.append(e("What is the signature of cc.sequence?", "cc.sequence(...actions: cc.FiniteTimeAction[]): Sequence — runs actions one after another."))
actions.append(e("What is the signature of cc.spawn?", "cc.spawn(...actions: cc.FiniteTimeAction[]): Spawn — runs actions simultaneously."))
actions.append(e("What is the signature of cc.repeat?", "cc.repeat(action: cc.FiniteTimeAction, times: number): Repeat"))
actions.append(e("What is the signature of cc.repeatForever?", "cc.repeatForever(action: cc.FiniteTimeAction): RepeatForever"))
actions.append(e("What is the signature of cc.reverseTime?", "cc.reverseTime(action: cc.FiniteTimeAction): ReverseTime"))
actions.append(e("What is the signature of cc.targetedAction?", "cc.targetedAction(target: cc.Node, action: cc.FiniteTimeAction): TargetedAction"))
actions.append(e("What is the signature of cc.speed?", "cc.speed(action: cc.FiniteTimeAction, speed: number): Speed"))
actions.append(e("What is the signature of cc.follow?", "cc.follow(followedNode: cc.Node, rect: cc.Rect): Follow"))

# Ease Functions
actions.append(e("How to apply easing to an action?", "action.easing(cc.easeBounceOut()) — chain .easing() on any ActionInterval."))
actions.append(e("What is the signature of cc.easeIn?", "cc.easeIn(rate: number) — accelerating ease."))
actions.append(e("What is the signature of cc.easeOut?", "cc.easeOut(rate: number) — decelerating ease."))
actions.append(e("What is the signature of cc.easeInOut?", "cc.easeInOut(rate: number) — accelerate then decelerate."))
actions.append(e("What does cc.easeSineIn() return?", "cc.easeSineIn() returns an ease object for sine-in easing."))
actions.append(e("What does cc.easeSineOut() return?", "cc.easeSineOut() returns an ease object for sine-out easing."))
actions.append(e("What does cc.easeSineInOut() return?", "cc.easeSineInOut() returns an ease object for sine-in-out easing."))
actions.append(e("What does cc.easeBackIn() return?", "cc.easeBackIn() returns an ease object — overshoots then returns."))
actions.append(e("What does cc.easeBackOut() return?", "cc.easeBackOut() returns an ease object — overshoots at the end."))
actions.append(e("What does cc.easeBackInOut() return?", "cc.easeBackInOut() returns an ease object — overshoots both ends."))
actions.append(e("What does cc.easeBounceIn() return?", "cc.easeBounceIn() returns an ease object — bounce at the start."))
actions.append(e("What does cc.easeBounceOut() return?", "cc.easeBounceOut() returns an ease object — bounce at the end."))
actions.append(e("What does cc.easeBounceInOut() return?", "cc.easeBounceInOut() returns an ease object — bounce at both ends."))
actions.append(e("What is the signature of cc.easeElasticIn?", "cc.easeElasticIn(period?: number) — elastic ease at the start."))
actions.append(e("What is the signature of cc.easeElasticOut?", "cc.easeElasticOut(period?: number) — elastic ease at the end."))
actions.append(e("What is the signature of cc.easeElasticInOut?", "cc.easeElasticInOut(period?: number) — elastic ease at both ends."))
actions.append(e("What does cc.easeExponentialIn() return?", "cc.easeExponentialIn() returns an exponential ease-in object."))
actions.append(e("What does cc.easeExponentialOut() return?", "cc.easeExponentialOut() returns an exponential ease-out object."))
actions.append(e("What does cc.easeExponentialInOut() return?", "cc.easeExponentialInOut() returns an exponential ease-in-out object."))
actions.append(e("What does cc.easeQuadraticActionIn() return?", "cc.easeQuadraticActionIn() returns a quadratic ease-in object."))
actions.append(e("What does cc.easeQuadraticActionOut() return?", "cc.easeQuadraticActionOut() returns a quadratic ease-out object."))
actions.append(e("What does cc.easeCubicActionIn() return?", "cc.easeCubicActionIn() returns a cubic ease-in object."))
actions.append(e("What does cc.easeCubicActionOut() return?", "cc.easeCubicActionOut() returns a cubic ease-out object."))
actions.append(e("What is the signature of cc.easeBezierAction?", "cc.easeBezierAction(p0: number, p1: number, p2: number, p3: number) — custom bezier easing."))

# Animation
actions.append(e("What is the signature of cc.animate?", "cc.animate(animation: cc.Animation): Animate"))
actions.append(e("How to create a cc.Animation?", "new cc.Animation(frames: cc.SpriteFrame[], delay: number, loops?: number)"))
actions.append(e("What is the signature of animation.addSpriteFrame?", "animation.addSpriteFrame(frame: cc.SpriteFrame): void"))
actions.append(e("What does animation.getDelayPerUnit() return?", "animation.getDelayPerUnit() returns number — seconds per frame."))
actions.append(e("What is the signature of animation.setDelayPerUnit?", "animation.setDelayPerUnit(delay: number): void"))
actions.append(e("What does animation.getLoops() return?", "animation.getLoops() returns number — 0 means loop forever."))
actions.append(e("What is the signature of animation.setLoops?", "animation.setLoops(n: number): void"))
actions.append(e("What is the signature of animation.setRestoreOriginalFrame?", "animation.setRestoreOriginalFrame(restore: boolean): void"))

# Progress
actions.append(e("What is the signature of cc.progressTo?", "cc.progressTo(duration: number, percent: number): ProgressTo"))
actions.append(e("What is the signature of cc.progressFromTo?", "cc.progressFromTo(duration: number, from: number, to: number): ProgressFromTo"))

# ActionTween
actions.append(e("What is the signature of cc.actionTween?", "cc.actionTween(duration: number, key: string, from: number, to: number): ActionTween"))

# Grid/3D Actions
actions.append(e("What is the signature of cc.flipX3D?", "cc.flipX3D(duration: number): FlipX3D"))
actions.append(e("What is the signature of cc.flipY3D?", "cc.flipY3D(duration: number): FlipY3D"))
actions.append(e("What is the signature of cc.shaky3D?", "cc.shaky3D(duration, gridSize, range, shakeZ): Shaky3D"))
actions.append(e("What is the signature of cc.liquid?", "cc.liquid(duration, gridSize, waves, amplitude): Liquid"))
actions.append(e("What is the signature of cc.waves?", "cc.waves(duration, gridSize, waves, amplitude, horizontal, vertical): Waves"))
actions.append(e("What is the signature of cc.waves3D?", "cc.waves3D(duration, gridSize, waves, amplitude): Waves3D"))
actions.append(e("What is the signature of cc.ripple3D?", "cc.ripple3D(duration, gridSize, position, radius, waves, amplitude): Ripple3d"))
actions.append(e("What is the signature of cc.twirl?", "cc.twirl(duration, gridSize, position, twirls, amplitude): Twirl"))
actions.append(e("What is the signature of cc.lens3D?", "cc.lens3D(duration, gridSize, position, radius): Lens3D"))
actions.append(e("What is the signature of cc.pageTurn3D?", "cc.pageTurn3D(duration, gridSize): PageTurn3D"))
actions.append(e("What does cc.reuseGrid() do?", "cc.reuseGrid(times: number): ReuseGrid — reuses the existing grid for N more actions."))
actions.append(e("What does cc.stopGrid() do?", "cc.stopGrid(): StopGrid — stops and removes the grid effect."))

# Correct vs wrong
actions.append(e("Is cc.MoveTo.create() a valid method?", "No. Use the factory function cc.moveTo(duration, x, y) instead."))
actions.append(e("Is cc.fadeIn(duration, opacity) a valid call?", "No. cc.fadeIn(duration) takes only duration. Use cc.fadeTo(duration, opacity) for a specific opacity."))
actions.append(e("Is cc.sequenceAction() a valid function?", "No. The correct function is cc.sequence(...actions)."))
actions.append(e("Is cc.spawnAction() a valid function?", "No. The correct function is cc.spawn(...actions)."))

# Comparison
actions.append(e("Difference between cc.moveTo and cc.moveBy?", "cc.moveTo moves to an absolute position. cc.moveBy moves by a relative offset."))
actions.append(e("Difference between cc.scaleTo and cc.scaleBy?", "cc.scaleTo scales to an absolute value. cc.scaleBy scales by a relative factor."))
actions.append(e("Difference between cc.rotateTo and cc.rotateBy?", "cc.rotateTo rotates to an absolute angle. cc.rotateBy rotates by a relative amount."))
actions.append(e("Difference between cc.fadeIn and cc.fadeTo?", "cc.fadeIn always fades from 0 to 255. cc.fadeTo fades to a specific opacity value."))
actions.append(e("Difference between cc.sequence and cc.spawn?", "cc.sequence runs actions one after another. cc.spawn runs all actions simultaneously."))
actions.append(e("Difference between cc.repeat and cc.repeatForever?", "cc.repeat(action, times) repeats N times. cc.repeatForever(action) repeats indefinitely."))

# Class membership
actions.append(e("Which function creates a delay action?", "cc.delayTime(duration: number): DelayTime"))
actions.append(e("Which function creates a callback action?", "cc.callFunc(callback: Function): CallFunc"))
actions.append(e("Which function applies speed to an action?", "cc.speed(action: cc.FiniteTimeAction, speed: number): Speed"))

w('D:/fine-tune-cocoos/data/raw-api/actions.jsonl', actions)

# ============ LABEL ============
label = []

# Factory methods
label.append(e("How to create a label with system font?", "cc.Label.createWithSystemFont(text, font, fontSize, dimensions?, hAlignment?, vAlignment?): cc.Label"))
label.append(e("What is the signature of cc.Label.createWithSystemFont?", "cc.Label.createWithSystemFont(text: string, font: string, fontSize: number, dimensions?: cc.Size, hAlignment?: number, vAlignment?: number): cc.Label"))
label.append(e("How to create a label with TTF font?", "cc.Label.createWithTTF(ttfConfig, text, hAlignment?, maxLineWidth?): cc.Label"))
label.append(e("What is the signature of cc.Label.createWithTTF?", "cc.Label.createWithTTF(ttfConfig: any, text: string, hAlignment?: number, maxLineWidth?: number): cc.Label"))
label.append(e("How to create a label with bitmap font?", "cc.Label.createWithBMFont(bmfontFilePath, text, hAlignment?, maxLineWidth?, imageOffset?): cc.Label"))
label.append(e("What is the signature of cc.Label.createWithBMFont?", "cc.Label.createWithBMFont(bmfontFilePath: string, text: string, hAlignment?: number, maxLineWidth?: number, imageOffset?: cc.Point): cc.Label"))
label.append(e("How to create a label with char map?", "cc.Label.createWithCharMap(charMapFile, itemWidth, itemHeight, startCharCode): cc.Label"))
label.append(e("What are the overloads of cc.Label.createWithCharMap?", "Three overloads: (charMapFile, itemWidth, itemHeight, startCharCode), (texture, itemWidth, itemHeight, startCharCode), (plistFile)."))
label.append(e("What does cc.Label.create() return?", "cc.Label.create() returns an empty cc.Label instance."))
label.append(e("What class does cc.Label extend?", "cc.Label extends cc.Node."))

# Text methods
label.append(e("What does label.getString() return?", "label.getString() returns string — the label's text content."))
label.append(e("What is the signature of label.setString?", "label.setString(text: string): void"))
label.append(e("What does label.getStringLength() return?", "label.getStringLength() returns number — character count of the text."))
label.append(e("What does label.getStringNumLines() return?", "label.getStringNumLines() returns number — number of text lines."))
label.append(e("What does label.updateContent() do?", "label.updateContent(): void — forces an immediate text update."))

# Alignment
label.append(e("What does label.getHorizontalAlignment() return?", "label.getHorizontalAlignment() returns number — cc.TEXT_ALIGNMENT_LEFT/CENTER/RIGHT."))
label.append(e("What is the signature of label.setHorizontalAlignment?", "label.setHorizontalAlignment(alignment: number): void"))
label.append(e("What does label.getVerticalAlignment() return?", "label.getVerticalAlignment() returns number — cc.VERTICAL_TEXT_ALIGNMENT_TOP/CENTER/BOTTOM."))
label.append(e("What is the signature of label.setVerticalAlignment?", "label.setVerticalAlignment(alignment: number): void"))
label.append(e("What is the signature of label.setAlignment?", "label.setAlignment(hAlignment: number, vAlignment?: number): void"))
label.append(e("What does label.getTextAlignment() return?", "label.getTextAlignment() returns number."))

# Dimensions
label.append(e("What does label.getDimensions() return?", "label.getDimensions() returns cc.Size — the clipping box dimensions."))
label.append(e("What is the signature of label.setDimensions?", "label.setDimensions(width: number, height: number): void — height=0 means auto."))
label.append(e("What does label.getMaxLineWidth() return?", "label.getMaxLineWidth() returns number."))
label.append(e("What is the signature of label.setMaxLineWidth?", "label.setMaxLineWidth(maxLineWidth: number): void"))
label.append(e("What is the signature of label.setLineBreakWithoutSpace?", "label.setLineBreakWithoutSpace(enabled: boolean): void"))
label.append(e("What does label.isClipMarginEnabled() return?", "label.isClipMarginEnabled() returns boolean."))
label.append(e("What is the signature of label.setClipMarginEnabled?", "label.setClipMarginEnabled(enabled: boolean): void"))
label.append(e("What does label.getWidth() return?", "label.getWidth() returns number."))
label.append(e("What is the signature of label.setWidth?", "label.setWidth(width: number): void"))
label.append(e("What does label.getHeight() return?", "label.getHeight() returns number."))
label.append(e("What is the signature of label.setHeight?", "label.setHeight(height: number): void"))

# Color & Effects
label.append(e("What does label.getTextColor() return?", "label.getTextColor() returns cc.Color."))
label.append(e("What is the signature of label.setTextColor?", "label.setTextColor(color: cc.Color): void — different from node.setColor()."))
label.append(e("What is the signature of label.enableOutline?", "label.enableOutline(color: cc.Color, outlineSize: number): void — TTF/system font only."))
label.append(e("What is the signature of label.enableShadow?", "label.enableShadow(color?: cc.Color, offset?: cc.Size, blurRadius?: number): void"))
label.append(e("What is the signature of label.enableGlow?", "label.enableGlow(color: cc.Color): void — TTF only."))
label.append(e("What is the signature of label.enableGradient?", "label.enableGradient(first: cc.Color, second: cc.Color, direction: cc.Color): void — also supports 3-color variant."))
label.append(e("What does label.disableEffect() do?", "label.disableEffect(): void — disables all effects. Or label.disableEffect(effect: number) to disable a specific one."))
label.append(e("What is the signature of label.setBlendFunc?", "label.setBlendFunc(src: cc.BlendFunc): void — or label.setBlendFunc(src, dst)."))

# Font Configuration
label.append(e("What does label.getSystemFontName() return?", "label.getSystemFontName() returns string — the system font family name."))
label.append(e("What is the signature of label.setSystemFontName?", "label.setSystemFontName(fontName: string): void"))
label.append(e("What does label.getSystemFontSize() return?", "label.getSystemFontSize() returns number."))
label.append(e("What is the signature of label.setSystemFontSize?", "label.setSystemFontSize(fontSize: number): void"))
label.append(e("What does label.getBMFontFilePath() return?", "label.getBMFontFilePath() returns string — the path to the .fnt file."))
label.append(e("What is the signature of label.setBMFontFilePath?", "label.setBMFontFilePath(path: string, imageOffset: cc.Point): void"))
label.append(e("What does label.getTTFConfig() return?", "label.getTTFConfig() returns the TTF configuration object."))
label.append(e("What does label.getLineHeight() return?", "label.getLineHeight() returns number — not supported for system fonts."))
label.append(e("What is the signature of label.setLineHeight?", "label.setLineHeight(lineHeight: number): void"))
label.append(e("What does label.getAdditionalKerning() return?", "label.getAdditionalKerning() returns number."))
label.append(e("What is the signature of label.setAdditionalKerning?", "label.setAdditionalKerning(kerning: number): void"))

# Letter Sprite
label.append(e("What does label.getLetter() return?", "label.getLetter(letterIndex: number) returns cc.Sprite — not supported for system fonts."))

# Bezier Text
label.append(e("What is the signature of label.enableCubicBezierCurves?", "label.enableCubicBezierCurves(origin, control1, control2, destination, align?, segments?): void"))
label.append(e("What is the signature of label.enableQuadBezierCurves?", "label.enableQuadBezierCurves(origin, control, destination, align?, segments?): void"))
label.append(e("What is the signature of label.setBezierAlignment?", "label.setBezierAlignment(align: number): void — 0=LEFT, 1=CENTER, 2=RIGHT, 3=STRETCH."))

# Alignment Constants
label.append(e("What are the horizontal text alignment constants?", "cc.TEXT_ALIGNMENT_LEFT (0), cc.TEXT_ALIGNMENT_CENTER (1), cc.TEXT_ALIGNMENT_RIGHT (2)."))
label.append(e("What are the vertical text alignment constants?", "cc.VERTICAL_TEXT_ALIGNMENT_TOP (0), cc.VERTICAL_TEXT_ALIGNMENT_CENTER (1), cc.VERTICAL_TEXT_ALIGNMENT_BOTTOM (2)."))

# Correct vs wrong
label.append(e("Is cc.Label.create(text, font, size) a valid call?", "No. cc.Label.create() takes no arguments. Use cc.Label.createWithSystemFont(text, font, size)."))
label.append(e("Is label.setText() a valid method?", "No. Use label.setString(text: string) to set the text content."))
label.append(e("Is label.setFontSize() a valid method?", "No. Use label.setSystemFontSize(fontSize) for system fonts, or set fontSize in the TTF config."))
label.append(e("Is cc.Label.createWithFont() a valid method?", "No. Use cc.Label.createWithSystemFont(), createWithTTF(), or createWithBMFont()."))
label.append(e("Is label.setOutline() a valid method?", "No. Use label.enableOutline(color: cc.Color, outlineSize: number)."))

# Class membership
label.append(e("Which class has the enableOutline method?", "cc.Label — label.enableOutline(color, outlineSize)."))
label.append(e("Which class has the enableGlow method?", "cc.Label — label.enableGlow(color). TTF only."))
label.append(e("Which class has the getLetter method?", "cc.Label — label.getLetter(letterIndex): cc.Sprite."))
label.append(e("Which class has the createWithBMFont method?", "cc.Label — static method cc.Label.createWithBMFont(path, text, ...)."))

# Comparison
label.append(e("Difference between label.setTextColor and label.setColor?", "setTextColor sets the text-specific color. setColor (from cc.Node) affects the entire node including effects."))
label.append(e("Difference between createWithSystemFont and createWithTTF?", "createWithSystemFont uses platform fonts. createWithTTF uses a .ttf file with FreeType2 for cross-platform consistency."))
label.append(e("Difference between enableOutline and enableGlow?", "enableOutline adds a colored outline border. enableGlow adds a soft glow effect (TTF only)."))

# Property access
label.append(e("How to change label text?", "label.setString('new text') — or label.getString() to read it."))
label.append(e("How to change label font size for system font?", "label.setSystemFontSize(24)"))

w('D:/fine-tune-cocoos/data/raw-api/label.jsonl', label)
