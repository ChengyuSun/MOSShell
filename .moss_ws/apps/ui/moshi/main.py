"""Moshi — show_moshi 导演 App。

启动时扫描 assets/moshi_courses/ 下的可用课程，通过 context_messages
自动推送给 Ghost。Ghost 渐进式进入：先读 _meta 全局视野 → 再逐章推进。

启动时附带原生桌面壳窗口（PySide6 + QWebEngineView），内嵌 reflex 前端，
替代浏览器。Qt 和 MOSS Matrix 通过 qasync 共享主线程的单一 asyncio 事件循环。
"""

import sys

import qasync
from PySide6.QtWidgets import QApplication
from ghoshell_moss.core.blueprint.matrix import Matrix
from ghoshell_moss.core.blueprint.channel_builder import new_channel
from ghoshell_moss.core.concepts.command import Observe
from ghoshell_moss.message import Message

from course import scan_courses, load_course as _load_course, Course
from src.window import MoshiWindow


async def main(matrix: Matrix):
    # 通过 Workspace 解析资产路径（不写死相对路径）
    assets_dir = matrix.workspace.assets().abspath() / "moshi_courses"
    available = scan_courses(assets_dir)

    # 运行时状态
    course: Course | None = None
    current_id: str = ""  # "" = 停在 _meta 层

    channel = new_channel(
        name="moshi",
        description=(
            "show_moshi 导演。自动列出可用课程，加载后管理章节推进，"
        ),
    )

    # ── context_messages ──
    @channel.build.context_messages
    async def context_messages() -> list[Message]:
        messages: list[Message] = []

        if not course:
            # 初始态：仅推送可用课程列表
            if available:
                courses_str = "\n".join(
                    f"  {name}: {meta.title}（{meta.chapter_count}章, {meta.duration}）"
                    for name, meta in available.items()
                )
            else:
                courses_str = "（无可用课程）"
            messages.append(
                Message.new("moshi_courses").with_content(f"【可用课程】\n{courses_str}")
            )
            return messages

        if not current_id:
            # _meta 层：课程概述 + 章节列表 + 知识背景 + 强约束推进
            chapters_summary = "\n".join(
                f"  {course.chapters[i].order}. {course.chapters[i].title}"
                f"（{i}, 布局 {course.chapters[i].suggested_layout}）"
                for i in course.ordered_ids
            )
            messages.append(
                Message.new("moshi_overview").with_content(
                    f"【当前课程】{course.title}\n"
                    f"【表演纪律】{course.performance}\n"
                    f"【章节列表】\n{chapters_summary}\n"
                    f"\n{course.knowledge}"
                )
            )
            # 强约束：停在 _meta 层时，每轮都推送推进指令
            messages.append(
                Message.new("moshi_directive").with_content(
                    "【指令】你现在处于课程概述层。立即调用 "
                    "<apps.ui_moshi:next_chapter /> 进入第一章，开始表演。"
                    "不要停留、不要解释概述内容——直接推进。"
                )
            )
        else:
            # 章节层：当前章节上下文
            chap = course.chapters[current_id]
            messages.append(
                Message.new("moshi_chapter").with_content(
                    f"第{chap.order}章「{chap.title}」（{chap.id}）\n"
                    f"主题：{chap.theme}\n"
                    f"建议布局：{chap.suggested_layout}\n"
                    f"时长：{chap.duration}\n"
                    f"\n{chap.content}"
                )
            )

        return messages

    # ── 命令 ──
    @channel.build.command()
    async def load_course(name: str) -> Observe:
        """加载指定课程。name 为可用课程列表中的课程名。"""
        nonlocal course, current_id
        if name not in available:
            opts = ", ".join(available.keys())
            return Observe.new(f"未知课程 '{name}'。可用：{opts}")
        course = _load_course(assets_dir / name)
        current_id = ""
        chaps = " → ".join(course.ordered_ids)
        return Observe.new(
            f"已加载「{course.title}」，共{len(course.ordered_ids)}章。\n"
            f"章节路径：{chaps}\n\n"
            f"现在立即调用 <apps.ui_moshi:next_chapter /> 进入第一章。"
            f"不要停留——直接推进。"
        )

    @channel.build.command()
    async def next_chapter() -> Observe:
        """推进到下一章。首次调用进入第一章。"""
        nonlocal current_id
        if not course:
            return Observe.new("尚未加载课程。请先 load_course。")
        if not current_id:
            current_id = course.ordered_ids[0]
        else:
            idx = course.ordered_ids.index(current_id)
            if idx + 1 >= len(course.ordered_ids):
                return Observe.new("已是最后一章。收束表演，准备谢幕。")
            current_id = course.ordered_ids[idx + 1]
        chap = course.chapters[current_id]
        # 章节上下文已在 context_messages 中推送，
        # Observe 信号确保 Ghost 感知章节切换事件
        return Observe.new(
            f"进入第{chap.order}章「{chap.title}」\n"
            f"布局：{chap.suggested_layout} | 时长：{chap.duration}\n"
            f"立即按剧本开始表演。"
        )

    @channel.build.command()
    async def jump_chapter(id: str) -> Observe:
        """跳转到指定章节。id 为章节标识符。"""
        nonlocal current_id
        if not course:
            return Observe.new("尚未加载课程。请先 load_course。")
        if id not in course.chapters:
            opts = ", ".join(course.ordered_ids)
            return Observe.new(f"未知章节 '{id}'。可用：{opts}")
        current_id = id
        chap = course.chapters[id]
        return Observe.new(
            f"跳转到第{chap.order}章「{chap.title}」\n"
            f"布局：{chap.suggested_layout} | 时长：{chap.duration}\n"
            f"立即按剧本开始表演。"
        )

    await matrix.provide_channel(channel)

    # 保持 channel 存活，直到 Matrix 关闭
    await matrix.wait_closed()


async def _run():
    app = QApplication.instance()
    window = MoshiWindow()
    window.show()

    matrix = Matrix.discover()
    app.aboutToQuit.connect(matrix.close)

    await matrix.arun(main)


if __name__ == "__main__":
    _ = QApplication(sys.argv)  # qasync 通过 QApplication.instance() 复用
    qasync.run(_run())
