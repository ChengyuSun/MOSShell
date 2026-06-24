# 资源存储声明 — 声明可寻址的资源数据集。
# 在此文件中定义 ResourceStorageMeta 实例，Matrix 启动时自动发现。
#
# 显式继承全局 resources，然后追加 mode 专属的：
import subprocess
from pathlib import Path
from datetime import datetime, timezone

from pydantic import Field
from ghoshell_container import IoCContainer, INSTANCE

from ghoshell_moss.core.resources.local_video import (
    LocalVideoInfo,
    LocalVideoItem,
    LocalVideoStorage,
    LocalVideoResourceMeta,
)

from MOSS.manifests.resources import *  # noqa: F403

from ghoshell_moss.apps.ui.moshi.src.course_storage import CourseResourceStorageMeta

moshi_course_storage_meta = CourseResourceStorageMeta()

class LocalWebmInfo(LocalVideoInfo):
    """WebM 视频资源元信息."""

    content_type: str = Field(default="video/webm")

    @classmethod
    def scheme(cls) -> str:
        return "local-webm"

    @classmethod
    def scheme_description(cls) -> str:
        return "WebM 视频资源 — VP8/VP9 编码，开源 Chromium (Qt WebEngine) 兼容"


class LocalWebmItem(LocalVideoItem):
    """WebM 视频资源项."""

    def __init__(self, meta: LocalWebmInfo, file_path: Path) -> None:
        super().__init__(meta, file_path)

    @classmethod
    def meta_type(cls) -> type[LocalWebmInfo]:
        return LocalWebmInfo


class LocalWebmStorage(LocalVideoStorage):
    """WebM 视频存储.

    继承 LocalVideoStorage，put() 时用 ffmpeg 将源视频转为 WebM (VP9 + Opus)。
    """

    INDEX_FILE = "local-webm.jsonl"
    FILES_DIR = "local-webm"

    def scheme(self) -> str:
        return LocalWebmInfo.scheme()

    def scheme_description(self) -> str:
        return LocalWebmInfo.scheme_description()

    # -- CRUD overrides --------------------------------------------------

    async def list_infos(self, query: str | None = None, limit: int = -1):
        metas: list[LocalWebmInfo] = []
        for line in self._read_lines():
            meta = LocalWebmInfo.model_validate_json(line)
            if query and query.lower() not in meta.file_name.lower():
                continue
            metas.append(meta)
            if limit >= 0 and len(metas) >= limit:
                break
        return metas

    async def get(self, path: str) -> LocalWebmItem | None:
        meta = self._find_meta(path)
        if meta is None:
            return None
        file_path = self._files_dir / meta.file_name
        if not file_path.exists() or not file_path.is_file():
            return None
        return LocalWebmItem(meta, file_path)

    async def put(self, item) -> str:
        source = await item.get()
        source_path = Path(source)

        path = item.info.path or source_path.stem

        stem = source_path.stem
        webm_filename = f"{stem}.webm"
        dest = self._files_dir / webm_filename

        # ffmpeg → WebM
        self._encode_to_webm(source_path, dest)

        meta = LocalWebmInfo(
            host=self._host,
            path=path,
            description=item.info.description or "",
            file_name=webm_filename,
            file_size=dest.stat().st_size,
            content_type="video/webm",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._upsert_meta(meta)
        return meta.locator

    # -- internal overrides -----------------------------------------------

    def _find_meta(self, path: str) -> LocalWebmInfo | None:
        for line in self._read_lines():
            meta = LocalWebmInfo.model_validate_json(line)
            if meta.path == path:
                return meta
        return None

    def _to_info(self, file_path: Path) -> LocalWebmInfo:
        stat = file_path.stat()
        return LocalWebmInfo(
            host=self._host,
            path=file_path.stem,
            description=file_path.stem.replace("_", " ").replace("-", " "),
            file_name=file_path.name,
            file_size=stat.st_size,
            content_type="video/webm",
        )

    def _encode_to_webm(self, src: Path, dest: Path) -> None:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(src),
            "-c:v", "libvpx-vp9",
            "-b:v", "0",
            "-c:a", "libopus",
            str(dest),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg conversion failed: {result.stderr}")


class LocalWebmResourceMeta(LocalVideoResourceMeta):
    """WebM 资源存储元信息."""

    def __init__(self, host: str = "workspace-assets", assets_sub_path: str = "videos"):
        self._host = host
        self._assets_sub_path = assets_sub_path

    @classmethod
    def scheme(cls) -> str:
        return LocalWebmInfo.scheme()

    def description(self) -> str:
        return "Local WebM video resource storage — ffmpeg VP9 transcoding, Qt WebEngine compatible"

    def factory(self, con: IoCContainer) -> INSTANCE:
        from ghoshell_moss.contracts.workspace import Workspace
        workspace = con.force_fetch(Workspace)
        data_dir = workspace.assets().abspath() / self._assets_sub_path
        data_dir.mkdir(parents=True, exist_ok=True)
        return LocalWebmStorage(data_dir, host=self._host)


# local_webm_storage_meta = LocalWebmResourceMeta()
