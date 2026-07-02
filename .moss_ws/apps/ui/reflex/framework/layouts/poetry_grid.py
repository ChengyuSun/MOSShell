"""PoetryGrid — 诗文四宫格卡片布局。

章节开场：全屏视频 → 图+标题居中亮相 → 缩到左上角 badge。
逐句填卡：配图先在屏幕中央浮层亮相，再填入下一个空格子。
章节转场：卡片四向飞出 + 黑幕。纯 CSS 动效，无 Canvas/JS。

Ghost 操作节奏：
```
set_chapter_image <locator>           # splash 图+标题居中淡入
set_show_badge "true"                 # 缩到左上角 badge
# --- 每句 ---
set_active_overlay_image <locator>    # 浮层亮相
[Ghost 等待 ~1.5s]
clear active_overlay_image            # 浮层消失
append_card_images <locator>          # 图落入格子
stream_lines "床前明月光，"           # 诗句墨迹浮现
# --- 章末 ---
set_transition "next"                 # 飞出+黑幕
```
"""

from PIL import Image

import reflex as rx
from framework.events import VideoLocator
from framework.helpers.mixin import NameMixin

# ═══════════════════════════════════════════════════════════════════════════════
# Style definitions
# ═══════════════════════════════════════════════════════════════════════════════

_STYLES: dict[str, dict[str, str]] = {
    "ink": {
        "bg": "#e8e0d0",
        "card_bg": "#f5f0e8",
        "text": "#2c1810",
        "sub": "#6b5a4e",
        "border": "rgba(44,24,16,0.08)",
        "shadow": "rgba(44,24,16,0.12)",
        "accent": "#8b5e3c",
        "label": "古典诗词",
    },
    "warm": {
        "bg": "#ede4d2",
        "card_bg": "#faf6f0",
        "text": "#3d2b1f",
        "sub": "#7a6a5c",
        "border": "rgba(61,43,31,0.06)",
        "shadow": "rgba(61,43,31,0.10)",
        "accent": "#a0784c",
        "label": "田园思乡",
    },
    "dark": {
        "bg": "#0d0d0d",
        "card_bg": "#1a1a1a",
        "text": "#e0d8c8",
        "sub": "#8a8070",
        "border": "rgba(224,216,200,0.06)",
        "shadow": "rgba(0,0,0,0.40)",
        "accent": "#c0a878",
        "label": "边塞羁旅",
    },
    "fresh": {
        "bg": "#dce8dc",
        "card_bg": "#f0f4f0",
        "text": "#1a2f1a",
        "sub": "#5a6e5a",
        "border": "rgba(26,47,26,0.06)",
        "shadow": "rgba(26,47,26,0.10)",
        "accent": "#4a7a4a",
        "label": "山水写景",
    },
}

_DEFAULT_STYLE = "ink"


def _style_css() -> str:
    """Generate per-style CSS custom properties."""
    parts = []
    for name, s in _STYLES.items():
        parts.append(f"""
.poetry-root.{name} {{
    --p-bg: {s['bg']};
    --p-card-bg: {s['card_bg']};
    --p-text: {s['text']};
    --p-sub: {s['sub']};
    --p-border: {s['border']};
    --p-shadow: {s['shadow']};
    --p-accent: {s['accent']};
}}
""")
    return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════════════════════
# CSS — pure CSS animations, no Canvas/JS
# ═══════════════════════════════════════════════════════════════════════════════

_POETRY_GRID_CSS = (
    _style_css()
    + """
/* ── Root ── */
.poetry-root {
    position: relative;
    width: 100%; height: 100vh;
    overflow: hidden;
    background: var(--p-bg, #e8e0d0);
    transition: background 0.8s ease;
    font-family: "Noto Serif SC", "Source Han Serif SC", "Songti SC", Georgia, serif;
}

/* ── Background media ── */
.poetry-bg-img {
    position: fixed; inset: 0;
    width: 100%; height: 100%;
    object-fit: cover;
    z-index: 0;
    opacity: 0.45;
    pointer-events: none;
}
.poetry-bg-video {
    position: fixed; inset: 0;
    width: 100%; height: 100%;
    object-fit: cover;
    z-index: 0;
    opacity: 0.45;
    pointer-events: none;
    transition: opacity 0.8s ease;
}

/* ═══════════════════════════════════════════ */
/* PHASE 1: Splash — chapter image + title centered */
/* ═══════════════════════════════════════════ */
.poetry-splash {
    position: fixed; inset: 0; z-index: 60;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    pointer-events: none;
}
.poetry-splash-img {
    width: 50vw; height: 50vh;
    object-fit: cover; border-radius: 16px;
    box-shadow: 0 12px 60px rgba(0,0,0,0.4);
    animation: splashEnter 0.8s cubic-bezier(0.22, 0.61, 0.36, 1) both;
}
.poetry-splash-title {
    margin-top: 20px;
    font-size: 32px; font-weight: 700; color: var(--p-text);
    letter-spacing: 0.08em;
    animation: splashEnter 0.8s 0.15s cubic-bezier(0.22, 0.61, 0.36, 1) both;
}
@keyframes splashEnter {
    from { opacity: 0; transform: scale(0.85); }
    to   { opacity: 1; transform: scale(1); }
}

/* ── Shrink to badge (triggered by .has-badge on root) ── */
.poetry-root.has-badge .poetry-splash-img {
    animation: splashToBadge 0.7s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
.poetry-root.has-badge .poetry-splash-title {
    animation: splashTitleOut 0.7s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
.poetry-root.has-badge .poetry-splash {
    animation: splashFadeOut 0.01s 0.7s forwards;
}
@keyframes splashToBadge {
    to {
        width: 80px; height: 80px; border-radius: 10px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.25);
        position: fixed; top: 24px; left: 32px;
        transform: none;
    }
}
@keyframes splashTitleOut {
    to { opacity: 0; transform: translateY(-20px); }
}
@keyframes splashFadeOut {
    to { opacity: 0; pointer-events: none; }
}

/* ── Badge (top-left, appears after shrink) ── */
.poetry-badge {
    position: fixed; top: 24px; left: 32px; z-index: 9;
    display: flex; align-items: center; gap: 12px;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s 0.5s ease;
}
.poetry-root.has-badge .poetry-badge {
    opacity: 1;
}
.poetry-badge-img {
    width: 64px; height: 64px;
    border-radius: 10px; object-fit: cover;
    box-shadow: 0 2px 12px rgba(0,0,0,0.25);
}
.poetry-badge-text {
    font-size: 22px; font-weight: 700; color: var(--p-text);
    letter-spacing: 0.06em;
}

/* ═══════════════════════════════════════════ */
/* PHASE 2: Grid (2×2) */
/* ═══════════════════════════════════════════ */
.poetry-grid {
    position: absolute; inset: 0; z-index: 5;
    display: grid;
    grid-template-columns: minmax(0, 420px) minmax(0, 420px);
    grid-template-rows: minmax(0, 1fr) minmax(0, 1fr);
    gap: 36px;
    padding: 120px 60px 60px;
    align-content: center; justify-content: center;
    pointer-events: none;
}

/* ── Card ── */
.poetry-card {
    position: relative; border-radius: 12px; overflow: hidden;
    background: var(--p-card-bg);
    box-shadow: 0 4px 24px var(--p-shadow);
    border: 1px solid var(--p-border);
    display: flex; flex-direction: column;
    animation: cardEnter 0.5s 0.1s cubic-bezier(0.22, 0.61, 0.36, 1) both;
}
@keyframes cardEnter {
    from { opacity: 0; transform: translateY(30px) scale(0.7); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

.poetry-card-media-wrap {
    flex: 0 0 65%;
    position: relative; overflow: hidden;
    background: var(--p-card-bg);
}
.poetry-card-media-wrap::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0;
    height: 40%;
    background: linear-gradient(transparent, var(--p-card-bg));
    pointer-events: none; z-index: 1;
}
.poetry-card-media {
    width: 100%; height: 100%;
    object-fit: cover; display: block;
}

.poetry-card-text-wrap {
    flex: 0 0 35%;
    display: flex; align-items: center; justify-content: center;
    padding: 8px 16px 16px;
}
.poetry-card-text {
    font-size: 22px; font-weight: 600; color: var(--p-text);
    letter-spacing: 0.06em; line-height: 1.4; text-align: center;
    animation: inkReveal 0.8s cubic-bezier(0.22, 0.61, 0.36, 1) both;
}
@keyframes inkReveal {
    0%   { opacity: 0; filter: blur(3px); transform: translateY(14px); }
    60%  { opacity: 0.8; filter: blur(0.5px); }
    100% { opacity: 1; filter: blur(0); transform: translateY(0); }
}

/* ── Empty placeholder ── */
.poetry-card-placeholder {
    border: 1px dashed var(--p-border);
    background: transparent;
    box-shadow: none;
    animation: none;
    opacity: 0.25;
}

/* ═══════════════════════════════════════════ */
/* PHASE 2b: Active overlay (center-screen) */
/* ═══════════════════════════════════════════ */
.poetry-overlay-area {
    position: fixed; inset: 0; z-index: 50;
    pointer-events: none;
    overflow: hidden;  /* clip off-screen overlay items during slide */
}
.poetry-overlay-item {
    position: absolute;
    top: 50%; left: 50%;
    max-width: 78vw; max-height: 72vh;
    border-radius: 14px; object-fit: contain;
    box-shadow: 0 8px 48px rgba(0,0,0,0.35);
    /* Inactive: parked off-left, invisible. No transition — wake from this state
       via .active (entrance animation) or .exiting (exit animation). */
    opacity: 0;
    transform: translate(-180%, -50%);
    pointer-events: none;
}
/* Enter: right → center with delay.  Keyframe animation — video loads unseen
   during the 0.5s hold, then slides in. */
.poetry-overlay-item.active {
    pointer-events: auto;
    animation: overlaySlideIn 0.45s 0.5s cubic-bezier(0.16, 0.84, 0.44, 1) both;
}
/* Exit: center → left, immediate.  Triggered by overlay_exiting state flag
   (set by __setattr__ intercept of clear).  After animation ends,
   element naturally stays at the parked position (opacity:0, -180%). */
.poetry-overlay-item.exiting {
    animation: overlaySlideOut 0.35s cubic-bezier(0.4, 0, 0.2, 1) both;
}
@keyframes overlaySlideIn {
    from { opacity: 0; transform: translate(100%, -50%); }
    to   { opacity: 1; transform: translate(-50%, -50%); }
}
@keyframes overlaySlideOut {
    from { opacity: 1; transform: translate(-50%, -50%); }
    to   { opacity: 0; transform: translate(-180%, -50%); }
}

/* ═══════════════════════════════════════════ */
/* Caption — body text at bottom center */
/* ═══════════════════════════════════════════ */
.poetry-caption {
    position: fixed; bottom: 6%; left: 50%;
    transform: translateX(-50%);
    z-index: 70; pointer-events: none;
    text-align: center;
}
.poetry-caption-text {
    font-size: 40px; font-weight: 500; color: var(--p-text);
    letter-spacing: 0.08em; line-height: 1.6;
    text-shadow: 0 0 20px var(--p-bg), 0 0 40px var(--p-bg);
    animation: inkReveal 0.8s cubic-bezier(0.22, 0.61, 0.36, 1) both;
}

/* ═══════════════════════════════════════════ */
/* PHASE 3: Transition */
/* ═══════════════════════════════════════════ */
.poetry-root.transitioning .poetry-card {
    animation: none;
}
.poetry-root.transitioning .poetry-card:nth-child(1) {
    animation: cardExitTL 0.5s ease-in both;
}
.poetry-root.transitioning .poetry-card:nth-child(2) {
    animation: cardExitTR 0.5s ease-in both;
}
.poetry-root.transitioning .poetry-card:nth-child(3) {
    animation: cardExitBL 0.5s ease-in both;
}
.poetry-root.transitioning .poetry-card:nth-child(4) {
    animation: cardExitBR 0.5s ease-in both;
}
@keyframes cardExitTL { to { opacity: 0; transform: translate(-120vw, -80vh) rotate(-5deg); } }
@keyframes cardExitTR { to { opacity: 0; transform: translate(120vw, -80vh) rotate(5deg); } }
@keyframes cardExitBL { to { opacity: 0; transform: translate(-120vw, 80vh) rotate(5deg); } }
@keyframes cardExitBR { to { opacity: 0; transform: translate(120vw, 80vh) rotate(-5deg); } }

.poetry-curtain {
    position: fixed; inset: 0; z-index: 200;
    background: #000; pointer-events: none;
    animation: curtainFade 0.8s ease-in-out both;
}
@keyframes curtainFade {
    0%   { opacity: 0; }
    30%  { opacity: 1; }
    70%  { opacity: 1; }
    100% { opacity: 0; }
}
"""
)


# ═══════════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════════

def _safe_style(style: rx.Var) -> rx.Var:
    """Ensure style value is in known range, fallback to ink."""
    result = _DEFAULT_STYLE
    for v in reversed(list(_STYLES.keys())):
        result = rx.cond(style == v, v, result)
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# Layout State
# ═══════════════════════════════════════════════════════════════════════════════

class PoetryGridState(rx.ComponentState, NameMixin):
    """诗文四宫格（2×2）卡片布局 — 章节开场→逐句填卡→转场。

    分三阶段：
    1. Splash：chapter_image + title 居中亮相 → 缩到左上角 badge
    2. Fill：每句配图先浮层居中亮相，再落入下一个格子
    3. Transition：卡片四向飞出 + 黑幕转场

    Ghost 操作字段（13 个，全部由 event_generator 自动生成命令）：

    章节级：
    - title: str                              → set / stream / clear
    - chapter_image: Image.Image | None       → set / clear
    - show_badge: str = ""                    → set / clear  ("true" 触发缩略动画)
    - style: str = "ink"                      → set / clear

    背景：
    - background_image: Image.Image | None    → set / clear
    - background_video: VideoLocator          → set / clear

    浮层（单张，中央亮相）：
    - active_overlay_image: Image.Image | None → set / clear
    - active_overlay_video: VideoLocator       → set / clear

    格子（列表，按索引对应）：
    - card_images: list[Image.Image]          → append / pop / clear
    - card_videos: list[VideoLocator]         → append / pop / clear
    - lines: list[str]                        → stream / pop / clear

    字幕/转场：
    - body: str                               → set / stream / clear
    - transition: str = ""                    → set / clear  ("next" 触发转场)
    """

    # Chapter
    title: str = ""
    chapter_image: Image.Image | None = None
    show_badge: str = ""
    style: str = _DEFAULT_STYLE

    # Background
    background_image: Image.Image | None = None
    background_video: VideoLocator = ""

    # Overlay (single active item, center-screen)
    active_overlay_image: Image.Image | None = None
    active_overlay_video: VideoLocator = ""

    # Cards (settled in grid, index-aligned with lines)
    card_images: list[Image.Image] = []
    card_videos: list[VideoLocator] = []
    lines: list[str] = []

    # Caption / Transition
    body: str = ""
    transition: str = ""

    # Overlay exit animation state (cleared via on_animation_end after CSS exit plays)
    overlay_exiting: str = ""
    _ov_cache: str = ""            # cached active_overlay_video src during exit
    _oi_cache: Image.Image | None = None  # cached active_overlay_image during exit

    def __setattr__(self, name: str, value: object) -> None:
        """Intercept clear_active_overlay_* to trigger CSS exit animation before wipe."""
        if name == "active_overlay_video":
            if value == "":
                old = self.active_overlay_video
                if old != "" and self.overlay_exiting != "1":
                    super().__setattr__("_ov_cache", old)
                    super().__setattr__("overlay_exiting", "1")
            elif value != "":
                # New overlay set → cancel any stale exit
                super().__setattr__("overlay_exiting", "")
                super().__setattr__("_ov_cache", "")
        elif name == "active_overlay_image":
            if value is None:
                old = self.active_overlay_image
                if old is not None and self.overlay_exiting != "1":
                    super().__setattr__("_oi_cache", old)
                    super().__setattr__("overlay_exiting", "1")
            elif value is not None:
                super().__setattr__("overlay_exiting", "")
                super().__setattr__("_oi_cache", None)
        super().__setattr__(name, value)

    async def _on_overlay_exit_end(self):
        """Called by on_animation_end — clear cache + exiting flag after CSS exit."""
        if self.overlay_exiting:
            self.overlay_exiting = ""
            self._ov_cache = ""
            self._oi_cache = None

    @classmethod
    def name(cls) -> str:
        return "poetry_grid"

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        style = _safe_style(cls.style)

        # ── Card builder: one card per line ──
        def _card(text: rx.Var, idx: rx.Var) -> rx.Component:
            """Build a grid card. text=lines[idx], media=card_images[idx] or card_videos[idx].

            Length-guarded: card_images / card_videos may be shorter than lines
            during state transitions. Access without guard → render error block.
            """
            return rx.box(
                # Image (if list has this index and value is not None)
                rx.cond(
                    cls.card_images.length() > idx,
                    rx.cond(
                        cls.card_images[idx] != None,
                        rx.box(
                            rx.image(
                                src=cls.card_images[idx],
                                class_name="poetry-card-media",
                            ),
                            class_name="poetry-card-media-wrap",
                        ),
                    ),
                ),
                # Video (if list has this index, value is non-empty, and no image at same idx)
                rx.cond(
                    cls.card_videos.length() > idx,
                    rx.cond(
                        cls.card_videos[idx] != "",
                        rx.box(
                            rx.video(
                                src=cls.card_videos[idx],
                                playing=True,
                                controls=False,
                                muted=True,
                                loop=True,
                                class_name="poetry-card-media",
                            ),
                            class_name="poetry-card-media-wrap",
                        ),
                    ),
                ),
                # Text
                rx.box(
                    rx.text(text, class_name="poetry-card-text"),
                    class_name="poetry-card-text-wrap",
                ),
                class_name="poetry-card",
            )

        # ── Component tree ──
        return rx.box(
            rx.html(f"<style>{_POETRY_GRID_CSS}</style>"),

            # z-0: background image (conditional)
            rx.cond(
                cls.background_image != None,
                rx.image(
                    src=cls.background_image,
                    class_name="poetry-bg-img",
                ),
            ),
            # z-0: background video (always rendered, opacity toggle)
            rx.video(
                src=cls.background_video,
                playing=True,
                controls=False,
                muted=True,
                loop=True,
                style=rx.cond(
                    cls.background_video != "",
                    {"opacity": "0.45", "transition": "opacity 0.8s ease"},
                    {"opacity": "0", "transition": "opacity 0.8s ease"},
                ),
                class_name="poetry-bg-video",
            ),

            # ═══ PHASE 1: Splash (chapter image + title centered) ═══
            rx.cond(
                (cls.chapter_image != None) & (cls.show_badge != "true"),
                rx.box(
                    rx.image(
                        src=cls.chapter_image,
                        class_name="poetry-splash-img",
                    ),
                    rx.cond(
                        cls.title != "",
                        rx.text(cls.title, class_name="poetry-splash-title"),
                    ),
                    class_name="poetry-splash",
                ),
            ),

            # ═══ Badge (top-left, appears after shrink) ═══
            rx.cond(
                (cls.chapter_image != None) & (cls.show_badge == "true"),
                rx.box(
                    rx.image(
                        src=cls.chapter_image,
                        class_name="poetry-badge-img",
                    ),
                    rx.cond(
                        cls.title != "",
                        rx.text(cls.title, class_name="poetry-badge-text"),
                    ),
                    class_name="poetry-badge",
                ),
            ),

            # ═══ PHASE 2: Grid ═══
            rx.box(
                rx.foreach(cls.lines, _card),
                class_name="poetry-grid",
            ),

            # ═══ PHASE 2b: Active overlay (center-screen, always-mounted) ═══
            # .poetry-overlay-item lives directly on img/video.
            # On clear, __setattr__ intercept caches the last src → .exiting class
            # → CSS exit animation (center→left).  Animation ends parked off-left.
            rx.box(
                rx.image(
                    src=rx.cond(
                        cls.active_overlay_image != None,
                        cls.active_overlay_image,
                        rx.cond(
                            cls.overlay_exiting != "",
                            rx.cond(cls._oi_cache != None, cls._oi_cache, ""),
                            "",
                        ),
                    ),
                    class_name=rx.cond(
                        (cls.active_overlay_image != None) & (cls.overlay_exiting == ""),
                        "poetry-overlay-item active",
                        rx.cond(
                            cls.overlay_exiting != "",
                            "poetry-overlay-item exiting",
                            "poetry-overlay-item",
                        ),
                    ),
                ),
                rx.video(
                    src=rx.cond(
                        cls.active_overlay_video != "",
                        cls.active_overlay_video,
                        rx.cond(
                            cls.overlay_exiting != "",
                            cls._ov_cache,
                            "",
                        ),
                    ),
                    playing=rx.cond(
                        (cls.active_overlay_video != "") | (cls.overlay_exiting != ""),
                        True,
                        False,
                    ),
                    controls=False,
                    muted=True,
                    loop=True,
                    class_name=rx.cond(
                        (cls.active_overlay_video != "") & (cls.overlay_exiting == ""),
                        "poetry-overlay-item active",
                        rx.cond(
                            cls.overlay_exiting != "",
                            "poetry-overlay-item exiting",
                            "poetry-overlay-item",
                        ),
                    ),
                ),
                class_name="poetry-overlay-area",
            ),

            # ═══ Caption (body text at bottom center) ═══
            rx.cond(
                cls.body != "",
                rx.box(
                    rx.text(cls.body, class_name="poetry-caption-text"),
                    class_name="poetry-caption",
                ),
            ),

            # ═══ PHASE 3: Transition curtain ═══
            rx.cond(
                cls.transition == "next",
                rx.box(class_name="poetry-curtain"),
            ),

            # Root class (priority: transitioning > has-badge > default)
            class_name=rx.cond(
                cls.transition == "next",
                f"poetry-root transitioning {style}",
                rx.cond(
                    cls.show_badge == "true",
                    f"poetry-root has-badge {style}",
                    f"poetry-root {style}",
                ),
            ),
            **props,
        )


# Module-level alias for config registration
PoetryGrid = PoetryGridState
