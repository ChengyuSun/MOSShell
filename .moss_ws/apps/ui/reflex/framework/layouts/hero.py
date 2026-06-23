import reflex as rx

from framework.helpers.mixin import NameMixin


class HeroLayout(rx.ComponentState, NameMixin):
    """全屏演示布局：黑色背景，居中大字标题。用于演示的开幕与收束。"""

    title: str = ""

    @classmethod
    def name(cls) -> str:
        return "hero"

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        return rx.center(
            rx.skeleton(
                rx.heading(
                    cls.title,
                    size="9",
                    weight="bold",
                    color="white",
                    text_align="center",
                ),
                width="600px",
                height="80px",
                loading=cls.title == "",
            ),
            width="100%",
            height="100vh",
            background="#000000",
            **props,
        )
