"""PeachBlossomStage — 桃花源记 四层连续动画舞台。

暗空间光绘风格：粒子叙景 + 氛围统调。
单一布局承载全部 6 章，章节切换靠粒子态/情绪/图片素材变化。

Reflex ↔ Canvas 桥接：state 变更 → #peach-store data-* →
MutationObserver → window.__PEACH_* → Canvas rAF 每帧读取。

四层：z-0 暗底 / z-1 光晕 / z-2 统调 / z-3 暗角+背景图 / z-4 粒子
      z-6 过渡遮罩+光缝 / z-7 浮层 / z-8 body / z-10 HUD
"""

from PIL import Image

import reflex as rx
from framework.events import VideoLocator
from framework.helpers.mixin import NameMixin
from framework.components.peach_assets import (
    DEFAULT_MOOD,
    MOOD,
    PEACH_CSS,
    SYNC_SCRIPT,
    PARTICLE_SCRIPT,
)

_PROGRESS_LABELS = ["溪流", "桃林", "山洞", "豁然", "村落", "归来"]

# 章节先后关系：label → 排在其后的所有章节（用于推导 "done" 态）
_AFTER: dict[str, list[str]] = {
    "溪流": ["桃林", "山洞", "豁然", "村落", "归来"],
    "桃林": ["山洞", "豁然", "村落", "归来"],
    "山洞": ["豁然", "村落", "归来"],
    "豁然": ["村落", "归来"],
    "村落": ["归来"],
}


def _is_chapter_done(chapter_id: rx.Var, label: str) -> rx.Var:
    """label 在 chapter_id 之前？即 chapter_id 是否在 label 的后续章节中。"""
    after = _AFTER.get(label, [])
    if not after:
        return chapter_id == ""  # 最后一章永远不"done"，返回恒假
    result = chapter_id == after[0]
    for a in after[1:]:
        result = result | (chapter_id == a)
    return result


def _safe_mood(mood: rx.Var) -> rx.Var:
    """确保 mood 值在已知范围内，否则返回默认值。构建嵌套 rx.cond。"""
    result = DEFAULT_MOOD
    for v in reversed(list(MOOD.keys())):
        result = rx.cond(mood == v, v, result)
    return result


class PeachBlossomState(rx.ComponentState, NameMixin):
    """桃花源记 — 五层连续动画舞台。13 字段全自动生成命令。"""

    # 氛围
    atmosphere: str = DEFAULT_MOOD

    # 光灵 — 已移除。舞台仅保留粒子环境、内容面板、HUD。

    # 背景（z-10，光灵后）
    background_image: Image.Image | None = None
    background_video: VideoLocator = ""

    # 浮层（z-40，光灵前）
    overlay_images: list[Image.Image] = []
    overlay_videos: list[VideoLocator] = []

    # 正文（z-45）
    body: str = ""

    # 过渡
    transition: str = ""

    # 字幕
    subtitles: list[str] = []

    # HUD
    chapter_title: str = ""
    chapter_id: str = ""

    @classmethod
    def name(cls) -> str:
        return "peach_blossom_stage"

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        mood = _safe_mood(cls.atmosphere)

        # ── helper: single progress dot ──
        def dot(label: str, i: int) -> rx.Component:
            return rx.box(
                class_name=rx.cond(
                    cls.chapter_id == label,
                    "peach-progress-dot active",
                    rx.cond(
                        _is_chapter_done(cls.chapter_id, label),
                        "peach-progress-dot done",
                        "peach-progress-dot",
                    ),
                ),
                title=label,
            )

        dots = []
        for i, label in enumerate(_PROGRESS_LABELS):
            dots.append(dot(label, i))
            if i < 5:
                dots.append(rx.box(class_name="peach-progress-line"))

        return rx.box(
            # ── Bridge: Reflex state → JS globals ──
            rx.el.div(id="peach-store",
                      data_atmosphere=mood,
                      data_transition=cls.transition,
                      hidden=True),

            # z-0: scene + background image (conditionally rendered, like overlay_images)
            rx.box(class_name="peach-scene"),
            rx.cond(
                cls.background_image != None,
                rx.image(
                    src=cls.background_image,
                    class_name="peach-bg-img",
                ),
            ),
            rx.video(
                src=cls.background_video,
                playing=True,
                controls=False,
                muted=True,
                loop=True,
                style=rx.cond(
                    cls.background_video != "",
                    {"opacity": "1", "transition": "opacity 0.8s ease"},
                    {"opacity": "0", "transition": "opacity 0.8s ease"},
                ),
                class_name="peach-bg-video",
            ),

            # z-10: radial glow
            rx.box(class_name=f"peach-glow {mood}"),

            # z-15: atmosphere color grade
            rx.box(class_name=f"peach-grade {mood}"),

            # z-16: vignette
            rx.box(class_name=f"peach-vignette {mood}"),

            # z-17: light slit (cave scene — "仿佛若有光")
            rx.box(class_name=f"peach-slit {mood}"),

            # z-6: transition overlay — 时空隧道黑色遮罩 + clip-path 洞口
            rx.box(class_name="peach-transition-overlay"),

            # z-5: transition glow — 洞口后方径向金光 + 旋转光纹
            rx.box(class_name="peach-transition-glow"),

            # z-4: particle canvas
            rx.el.canvas(id="peach-particles"),

            # z-40: overlay images + videos (光灵前方，浮层区)
            rx.box(
                rx.foreach(
                    cls.overlay_images,
                    lambda img: rx.image(src=img, class_name="peach-overlay-item"),
                ),
                rx.foreach(
                    cls.overlay_videos,
                    lambda v: rx.video(
                        src=v,
                        playing=True,
                        controls=False,
                        muted=True,
                        loop=True,
                        class_name="peach-overlay-item",
                    ),
                ),
                class_name="peach-overlay-area",
            ),

            # z-45: body text (fixed size)
            rx.cond(
                cls.body != "",
                rx.box(
                    rx.text(cls.body, class_name="peach-body-text"),
                    class_name="peach-body-area",
                ),
            ),

            # z-50: HUD (chapter title + progress dots)
            rx.box(
                rx.cond(
                    cls.chapter_title != "",
                    rx.text(cls.chapter_title, class_name="peach-chapter-title"),
                ),
                rx.box(*dots, class_name="peach-progress"),
                class_name="peach-hud",
            ),

            # Scripts + CSS
            rx.script(SYNC_SCRIPT),
            rx.script(PARTICLE_SCRIPT),
            rx.html(f"<style>{PEACH_CSS}</style>"),
            class_name=rx.cond(
                cls.transition == "constrict",
                "peach-transition-constrict",
                "",
            ),
            **props,
        )
