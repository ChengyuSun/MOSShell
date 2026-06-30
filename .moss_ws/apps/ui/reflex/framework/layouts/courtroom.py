"""CourtroomLayout — 极限审判。

AI 法官是暗空间中央的失重光团流体（8 个径向渐变 orb，screen 叠加混合），
涟漪光波 + 三层声呐脉冲 + 四圈光环呼吸。三情绪驱动色调联动：
- calm（平静）：银灰线条，涟漪慢扩，4s 呼吸 — 宣读罪名、陈述事实
- mercy（怜悯）：蓝紫线条，涟漪中速，柔和波动 — 听取申辩、考虑减刑
- anger（愤怒）：猩红线条 + 核心抖动，涟漪快扩，脉冲加剧 — 证据确凿、被告撒谎

情绪由根节点 .courtroom-root 驱动，--anim-speed CSS 变量控制全局动画速度
（calm=1, mercy=0.7, anger=0.4）。所有子元素通过后代选择器响应。

动效层：涟漪光波（多层同心环扩散）+ 三层声呐脉冲（错相扩散）+
光环呼吸旋转 + 椭圆变形 + 光线核心三层密度多速旋转 + 浮动 + 脉冲呼吸。
暗角强制聚拢视觉重心。

CSS 外置到 framework.components.courtroom_styles，
计时器外置到 framework.components.countdown_timer。
"""

from PIL import Image

import reflex as rx
from pydantic import BaseModel, Field

from framework.components.courtroom_styles import COURTROOM_CSS
from framework.components.countdown_timer import TIMER_SCRIPT, timer_elements
from framework.events import VideoLocator
from framework.helpers.mixin import NameMixin


# ═══════════════════════════════════════════════════════════════════════════════
# Model
# ═══════════════════════════════════════════════════════════════════════════════

class ScoreBar(BaseModel):
    """分数维度环。与 brain CellBar 同模式。"""
    label: str = Field(default="", description="维度名")
    value: int = Field(default=0, description="0-100")
    color: str = Field(default="#6366f1", description="环颜色")


# ═══════════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════════

_DANMAKU_LANE_H = 44
_DANMAKU_LANES = 6


def _emotion_class(judge_state: rx.Var) -> rx.Var:
    """Root emotion class: courtroom-root + calm|mercy|anger."""
    return rx.cond(
        judge_state == "mercy",
        "courtroom-root mercy",
        rx.cond(
            judge_state == "anger",
            "courtroom-root anger",
            "courtroom-root calm",
        ),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Layout
# ═══════════════════════════════════════════════════════════════════════════════

class CourtroomState(rx.ComponentState, NameMixin):
    """审判布局。

    光魂中心——三情绪驱动色调联动（calm/mercy/anger），根节点统一驱动所有
    子元素情绪样式。字段全部使用 event_generator 原生支持的类型。

    Ghost 可操作字段：
    - judge_state: str       → set (值: "calm" | "mercy" | "anger", 空=calm)
    - scores: list[ScoreBar] → append / update / pop / clear
    - evidence_images: list[Image.Image]  → append / pop / clear
    - evidence_videos: list[VideoLocator] → append / pop / clear
    - timer_state: str       → set (格式 "stopped:0" / "running:60")
    - title / sub_title: str → set

    仅飞书 Topic 写入（Ghost 不应操作）：
    - danmaku_text / danmaku_emphasis / danmaku_system: list[str]
    """

    judge_state: str = ""
    scores: list[ScoreBar] = []
    evidence_images: list[Image.Image] = []
    evidence_videos: list[VideoLocator] = []
    danmaku_text: list[str] = []
    danmaku_emphasis: list[str] = []
    danmaku_system: list[str] = []
    timer_state: str = ""
    title: str = ""
    sub_title: str = ""

    @classmethod
    def name(cls) -> str:
        return "courtroom"

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        return rx.box(
            # ── Scene background ──
            rx.box(class_name="courtroom-scene"),
            # ── Radial Glow ──
            rx.box(class_name="courtroom-glow"),
            # ── Sonar pulses (3 staggered layers) ──
            rx.box(
                rx.box(class_name="sonar-p3"),
                class_name="courtroom-sonar",
            ),
            # ── Ambient Rings ×4 ──
            rx.box(class_name="courtroom-ambient-ring",
                   style={"width": "400px", "height": "400px"}),
            rx.box(class_name="courtroom-ambient-ring r2",
                   style={"width": "520px", "height": "520px"}),
            rx.box(class_name="courtroom-ambient-ring r3",
                   style={"width": "640px", "height": "640px"}),
            rx.box(class_name="courtroom-ambient-ring r4",
                   style={"width": "760px", "height": "760px"}),
            # ── Orb cluster — 8 光团叠加，screen 混合制造流体感 ──
            rx.box(
                rx.box(rx.box(class_name="orb core"), class_name="orb-wrap n1"),
                rx.box(rx.box(class_name="orb core"), class_name="orb-wrap n2"),
                rx.box(rx.box(class_name="orb core"), class_name="orb-wrap n3"),
                rx.box(rx.box(class_name="orb core"), class_name="orb-wrap n4"),
                rx.box(rx.box(class_name="orb mid"),  class_name="orb-wrap n5"),
                rx.box(rx.box(class_name="orb mid"),  class_name="orb-wrap n6"),
                rx.box(rx.box(class_name="orb mid"),  class_name="orb-wrap n7"),
                rx.box(rx.box(class_name="orb haze"), class_name="orb-wrap n8"),
                class_name="courtroom-core",
            ),
            # ── Evidence layer ──
            rx.cond(
                (cls.evidence_images.length() > 0) | (cls.evidence_videos.length() > 0),
                rx.box(
                    rx.foreach(
                        cls.evidence_images,
                        lambda img: rx.box(
                            rx.image(src=img, width="100%", height="auto",
                                     object_fit="contain"),
                            class_name="courtroom-evidence-item",
                        ),
                    ),
                    rx.foreach(
                        cls.evidence_videos,
                        lambda v: rx.box(
                            rx.video(src=v, playing=True, controls=False,
                                     muted=True, loop=True,
                                     width="100%", height="auto"),
                            class_name="courtroom-evidence-item",
                        ),
                    ),
                    class_name="courtroom-evidence-layer",
                ),
            ),
            # ── Score rings ──
            rx.box(
                rx.foreach(
                    cls.scores,
                    lambda bar, i: rx.box(
                        rx.vstack(
                            rx.box(
                                rx.box(
                                    class_name=rx.cond(
                                        i == 3,
                                        "score-ring-progress total",
                                        "score-ring-progress",
                                    ),
                                    style={
                                        "background": f"conic-gradient({bar.color} calc({bar.value} * 3.6 * 1deg), transparent 0deg)",
                                    },
                                ),
                                rx.text(f"{bar.value}", class_name="score-ring-value"),
                                class_name=rx.cond(
                                    i == 3, "score-ring total", "score-ring",
                                ),
                            ),
                            rx.text(bar.label, class_name="score-ring-label"),
                            spacing="1", align="center",
                            class_name="score-ring-wrap",
                        ),
                    ),
                ),
                class_name="courtroom-scores",
            ),
            # ── Timer (from countdown_timer component) ──
            *timer_elements(cls.timer_state),
            # ── HUD ──
            rx.cond(
                cls.title != "",
                rx.text(cls.title, class_name="courtroom-title"),
            ),
            rx.cond(
                cls.sub_title != "",
                rx.text(cls.sub_title, class_name="courtroom-subtitle"),
            ),
            # ── Danmaku layer ──
            rx.box(
                rx.foreach(
                    cls.danmaku_text,
                    lambda text, i: rx.box(
                        text,
                        class_name="danmaku-item danmaku-normal",
                        style={"top": f"{(i % _DANMAKU_LANES) * _DANMAKU_LANE_H + 8}px"},
                    ),
                ),
                rx.foreach(
                    cls.danmaku_emphasis,
                    lambda text, i: rx.box(
                        text,
                        class_name="danmaku-item danmaku-emphasis",
                        style={"top": f"{(i % _DANMAKU_LANES) * _DANMAKU_LANE_H + 8}px"},
                    ),
                ),
                rx.foreach(
                    cls.danmaku_system,
                    lambda text, i: rx.box(
                        text,
                        class_name="danmaku-item danmaku-system",
                        style={"top": f"{(i % _DANMAKU_LANES) * _DANMAKU_LANE_H + 8}px"},
                    ),
                ),
                id="danmaku-layer",
            ),
            # ── Scripts & CSS ──
            rx.script(TIMER_SCRIPT),
            rx.html(f"<style>{COURTROOM_CSS}</style>"),
            # ── Debug ──
            rx.text("courtroom css", class_name="courtroom-debug"),
            # Root emotion class
            class_name=_emotion_class(cls.judge_state),
            **props,
        )
