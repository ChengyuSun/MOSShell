"""Moshi — show_moshi 导演 App。

启动时扫描 assets/moshi_courses/ 下的可用课程，通过 context_messages
自动推送给 Ghost。Ghost 渐进式进入：先读 _meta 全局视野 → 再逐章推进。
"""

from ghoshell_moss.core.blueprint.matrix import Matrix
from ghoshell_moss.core.blueprint.channel_builder import new_channel
from ghoshell_moss.message import Message

from course import scan_courses, load_course, Course


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
            "通过 context_messages 为 Ghost 提供当前章节上下文。"
        ),
    )

    # ── context_messages ──
    @channel.build.context_messages
    async def context_messages() -> list[Message]:
        messages: list[Message] = []

        # 始终推送可用课程列表
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

        if not course:
            return messages

        if not current_id:
            # _meta 层：课程概述
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
    async def load_course(name: str) -> str:
        """加载指定课程。name 为可用课程列表中的课程名。"""
        nonlocal course, current_id
        if name not in available:
            opts = ", ".join(available.keys())
            return f"未知课程 '{name}'。可用：{opts}"
        course = load_course(assets_dir / name)
        current_id = ""
        chaps = " → ".join(course.ordered_ids)
        return (
            f"已加载「{course.title}」，共{len(course.ordered_ids)}章。\n"
            f"章节路径：{chaps}\n"
            f"现在你已看到课程概述。调用 next_chapter 开始第一章。"
        )

    @channel.build.command()
    async def next_chapter() -> str:
        """推进到下一章。首次调用进入第一章。"""
        nonlocal current_id
        if not course:
            return "尚未加载课程。请先 load_course。"
        if not current_id:
            current_id = course.ordered_ids[0]
        else:
            idx = course.ordered_ids.index(current_id)
            if idx + 1 >= len(course.ordered_ids):
                return "已是最后一章。"
            current_id = course.ordered_ids[idx + 1]
        chap = course.chapters[current_id]
        return f"第{chap.order}章「{chap.title}」（布局 {chap.suggested_layout}）"

    @channel.build.command()
    async def jump_chapter(id: str) -> str:
        """跳转到指定章节。id 为章节标识符。"""
        nonlocal current_id
        if not course:
            return "尚未加载课程。请先 load_course。"
        if id not in course.chapters:
            opts = ", ".join(course.ordered_ids)
            return f"未知章节 '{id}'。可用：{opts}"
        current_id = id
        chap = course.chapters[id]
        return f"第{chap.order}章「{chap.title}」（布局 {chap.suggested_layout}）"

    await matrix.provide_channel(channel)


if __name__ == "__main__":
    Matrix.discover().run(main)
