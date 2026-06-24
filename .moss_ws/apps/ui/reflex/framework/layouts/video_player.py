import reflex as rx

from framework.events import VideoLocator
from framework.helpers.mixin import NameMixin


class VideoPlayerLayout(rx.ComponentState, NameMixin):
    """纯视频播放布局。居中、自动播放、静音、循环，无控制条。

    仅 list[VideoLocator] 字段——取最后一个 locator 对应的 HTTP URL 渲染。
    插入后用 skeleton 过渡，空态不占位。
    """

    videos: list[VideoLocator] = []

    @classmethod
    def name(cls) -> str:
        return "video_player"

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        return rx.center(
            rx.skeleton(
                rx.video(
                    src=cls.videos[-1],
                    playing=True,
                    controls=False,
                    muted=True,
                    loop=True,
                    width="100%",
                    height="100%",
                ),
                width="100vw",
                height="100vh",
                loading=cls.videos.length() == 0,
            ),
            width="100vw",
            height="100vh",
            overflow="hidden",
            background="#000000",
            **props,
        )
