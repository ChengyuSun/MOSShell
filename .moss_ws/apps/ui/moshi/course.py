"""课程数据结构与加载逻辑。

启动时用 scan_courses() 获取轻量列表（不加载章节内容）；
Ghost 选定后用 load_course() 加载完整数据。
"""

import yaml
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Chapter:
    """单个章节数据。"""
    id: str
    order: int
    title: str
    theme: str
    suggested_layout: str
    duration: str
    content: str  # chapter md body


@dataclass
class CourseMeta:
    """启动时扫描的轻量元信息，不加载章节内容。"""
    title: str
    chapter_count: int
    duration: str


@dataclass
class Course:
    """完整课程数据。"""
    title: str
    performance: str       # 格式化后的表演纪律
    knowledge: str         # _meta.md body（AIOS 知识背景）
    chapters: dict[str, Chapter]
    ordered_ids: list[str]


def _split_frontmatter(text: str) -> tuple[dict, str]:
    """分离 YAML frontmatter 和 markdown body。"""
    text = text.strip()
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    return yaml.safe_load(parts[1]) or {}, parts[2].strip()


def scan_courses(assets_dir: Path) -> dict[str, CourseMeta]:
    """扫描可用课程目录，返回 {name: CourseMeta}。不加载章节内容。"""
    if not assets_dir.exists():
        return {}
    result: dict[str, CourseMeta] = {}
    for d in sorted(assets_dir.iterdir()):
        if not d.is_dir():
            continue
        meta_file = d / "_meta.md"
        if not meta_file.exists():
            continue
        fm, _ = _split_frontmatter(meta_file.read_text())
        chapters = fm.get("chapters", [])
        result[d.name] = CourseMeta(
            title=fm.get("description", d.name),
            chapter_count=len(chapters),
            duration=fm.get("total_duration", "?"),
        )
    return result


def load_course(course_dir: Path) -> Course:
    """加载完整课程数据：_meta.md + 所有章节文件。"""
    meta_text = (course_dir / "_meta.md").read_text()
    fm, knowledge = _split_frontmatter(meta_text)

    perf = fm.get("performance", {})
    performance = (
        f"节奏：{perf.get('rhythm', '')}；"
        f"连续性：{perf.get('continuity', '')}；"
        f"容错：{perf.get('fallback', '')}"
    )

    chapters: dict[str, Chapter] = {}
    for ch_data in fm.get("chapters", []):
        ch_file = course_dir / ch_data["file"]
        content = ch_file.read_text()
        chapters[ch_data["id"]] = Chapter(
            id=ch_data["id"],
            order=ch_data["order"],
            title=ch_data["title"],
            theme=ch_data["theme"],
            suggested_layout=ch_data["suggested_layout"],
            duration=ch_data.get("duration", ""),
            content=content.strip(),
        )

    ordered = sorted(chapters.values(), key=lambda c: c.order)

    return Course(
        title=fm.get("description", course_dir.name),
        performance=performance,
        knowledge=knowledge,
        chapters=chapters,
        ordered_ids=[c.id for c in ordered],
    )
