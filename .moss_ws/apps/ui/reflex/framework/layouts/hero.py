import reflex as rx
from PIL import Image

from framework.helpers.mixin import NameMixin


class HeroLayout(rx.ComponentState, NameMixin):
    """全屏开场布局：大字标题 + 副标题 + 全屏背景图。

    用于演示的开幕与收束。极简字段，强视觉冲击。
    Ghost 使用示例：
        <apps.ui_reflex:stream_title>MOSS</apps.ui_reflex:stream_title>
        <apps.ui_reflex:stream_subtitle>AI 操作系统</apps.ui_reflex:stream_subtitle>
        <apps.ui_reflex:append_background locator="pil-image://demo/logo" />
    """

    title: str = ""
    subtitle: str = ""
    background: list[Image.Image] = []

    @classmethod
    def name(cls) -> str:
        return "hero"

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        return rx.box(
            # ── 背景图层 ──
            rx.cond(
                cls.background.length() > 0,
                rx.box(
                    rx.foreach(
                        cls.background,
                        lambda img: rx.image(
                            img,
                            position="absolute",
                            top="0",
                            left="0",
                            width="100%",
                            height="100%",
                            object_fit="cover",
                            object_position="center",
                        ),
                    ),
                    position="absolute",
                    top="0",
                    left="0",
                    width="100%",
                    height="100%",
                    z_index="0",
                ),
            ),
            # ── 暗色叠层 ──
            rx.box(
                position="absolute",
                top="0",
                left="0",
                width="100%",
                height="100%",
                background="linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.6) 100%)",
                z_index="1",
            ),
            # ── 文字层：居中 ──
            rx.vstack(
                rx.skeleton(
                    rx.heading(
                        cls.title,
                        size="9",
                        weight="bold",
                        color="white",
                        text_align="center",
                        letter_spacing="-0.02em",
                        style={
                            "textShadow": "0 2px 40px rgba(0,0,0,0.5)",
                        },
                    ),
                    width="600px",
                    height="80px",
                    loading=cls.title == "",
                ),
                rx.skeleton(
                    rx.text(
                        cls.subtitle,
                        color_scheme="gray",
                        size="5",
                        text_align="center",
                        style={
                            "color": "rgba(255,255,255,0.75)",
                            "textShadow": "0 1px 20px rgba(0,0,0,0.5)",
                        },
                    ),
                    width="400px",
                    height="30px",
                    loading=cls.subtitle == "",
                ),
                position="absolute",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="2",
                spacing="6",
                align="center",
                width="100%",
                padding="0 32px",
            ),
            # ── 容器：全屏 ──
            width="100vw",
            height="100vh",
            position="relative",
            overflow="hidden",
            background="linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%)",
            **props,
        )
