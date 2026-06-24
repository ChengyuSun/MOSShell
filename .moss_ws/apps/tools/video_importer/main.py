"""Video Importer — batch import videos into the local-video resource storage.

Usage:
  GUI:     moss apps test tools/video_importer   (primary)
  MOSS:    moss apps start tools/video_importer
           Then via CTML: <apps.tools_video_importer:import_dir directory="/path" />
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from ghoshell_moss.core.blueprint.channel_builder import new_channel
from ghoshell_moss.core.blueprint.matrix import Matrix
from ghoshell_moss.core.resources.local_video import (
    _VIDEO_EXTENSIONS,
    LocalVideoInfo,
    LocalVideoItem,
    LocalVideoStorage,
)

_APP_DIR = Path(__file__).resolve().parent


def _find_workspace_root() -> Path:
    """Walk up to find the workspace root (the directory containing .moss_ws)."""
    d = _APP_DIR
    for _ in range(10):
        if (d / ".moss_ws").is_dir():
            return d
        parent = d.parent
        if parent == d:
            break
        d = parent
    return Path.cwd()


def _assets_dir() -> Path:
    return _find_workspace_root() / ".moss_ws" / "assets" / "videos"


def scan_videos(directory: Path) -> list[Path]:
    """Scan a directory for supported video files (case-insensitive)."""
    files: list[Path] = []
    for p in directory.iterdir():
        if p.is_file() and p.suffix.lower() in _VIDEO_EXTENSIONS:
            files.append(p)
    return sorted(files)


async def import_videos(
    storage: LocalVideoStorage,
    video_paths: list[Path],
    on_progress=None,
) -> dict:
    """Import videos into the storage.  Returns {imported, skipped, errors}."""
    stats = {"imported": 0, "skipped": 0, "errors": 0}

    all_infos = await storage.list_infos(limit=-1)
    existing_names = {m.file_name for m in all_infos}

    for i, vid_path in enumerate(video_paths):
        name = vid_path.name
        stem = vid_path.stem

        if name in existing_names:
            stats["skipped"] += 1
            if on_progress:
                on_progress(i, len(video_paths), name, "skipped (already exists)")
            continue

        try:
            meta = LocalVideoInfo(
                path=name,
                description=stem.replace("_", " ").replace("-", " "),
            )
            item = LocalVideoItem(meta, vid_path)
            locator = await storage.put(item)
            existing_names.add(name)
            stats["imported"] += 1
            if on_progress:
                on_progress(i, len(video_paths), name, f"ok → {locator}")

        except Exception as exc:
            stats["errors"] += 1
            if on_progress:
                on_progress(i, len(video_paths), name, f"error: {exc}")

    return stats


# -- GUI ------------------------------------------------------------------

def main_gui() -> None:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    root = tk.Tk()
    root.title("Video Importer — MOSS local-video Storage")
    root.geometry("640x460")
    root.resizable(True, True)

    selected_dir = tk.StringVar()
    host_var = tk.StringVar(value="workspace-assets")
    status_var = tk.StringVar(value="Ready.")
    file_count_var = tk.StringVar(value="")

    def select_directory() -> None:
        path = filedialog.askdirectory(title="Select a directory containing videos")
        if not path:
            return
        selected_dir.set(path)
        vids = scan_videos(Path(path))
        file_count_var.set(f"{len(vids)} video(s) found")

    async def do_import() -> None:
        path = selected_dir.get()
        if not path:
            messagebox.showwarning("Warning", "Select a directory first")
            return

        video_paths = scan_videos(Path(path))
        if not video_paths:
            messagebox.showinfo("No videos", f"No supported videos in:\n{path}")
            return

        progress_bar["maximum"] = len(video_paths)
        import_btn["state"] = "disabled"

        storage = LocalVideoStorage(_assets_dir(), host=host_var.get())

        def update(i: int, total: int, name: str, status: str) -> None:
            progress_bar["value"] = i + 1
            status_var.set(f"[{i + 1}/{total}] {name}: {status}")
            root.update_idletasks()

        try:
            stats = await import_videos(storage, video_paths, on_progress=update)
            messagebox.showinfo(
                "Done",
                f"Imported: {stats['imported']}\nSkipped: {stats['skipped']}\nErrors: {stats['errors']}",
            )
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
        finally:
            progress_bar["value"] = 0
            status_var.set("Ready.")
            import_btn["state"] = "normal"

    def run_import() -> None:
        asyncio.run(do_import())

    # -- layout --
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Batch Import Videos to MOSS Resource Storage",
              font=("", 14, "bold")).pack(pady=(0, 20))

    # directory row
    dir_frame = ttk.Frame(frame)
    dir_frame.pack(fill=tk.X, pady=6)
    ttk.Label(dir_frame, text="Directory  ", width=11).pack(side=tk.LEFT)
    ttk.Entry(dir_frame, textvariable=selected_dir).pack(side=tk.LEFT, padx=6, fill=tk.X, expand=True)
    ttk.Button(dir_frame, text="Browse...", command=select_directory).pack(side=tk.LEFT)

    ttk.Label(frame, textvariable=file_count_var, foreground="gray").pack(anchor="w", padx=11, pady=(0, 6))

    # host row
    host_frame = ttk.Frame(frame)
    host_frame.pack(fill=tk.X, pady=6)
    ttk.Label(host_frame, text="Host       ", width=11).pack(side=tk.LEFT)
    ttk.Entry(host_frame, textvariable=host_var, width=24).pack(side=tk.LEFT, padx=6)

    # progress
    progress_bar = ttk.Progressbar(frame, mode="determinate")
    progress_bar.pack(fill=tk.X, pady=(16, 6))

    ttk.Label(frame, textvariable=status_var, wraplength=580).pack(pady=4)

    # import button
    import_btn = ttk.Button(frame, text="Import Videos", command=run_import)
    import_btn.pack(pady=12)

    ttk.Label(frame, text="Supported: MP4, WEBM, MOV, AVI, MKV, M4V, OGV",
              foreground="gray").pack(side=tk.BOTTOM, pady=(8, 0))

    root.mainloop()


# -- MOSS Channel ---------------------------------------------------------

async def _do_import_dir(directory: str, host: str) -> str:
    dir_path = Path(directory).resolve()
    if not dir_path.is_dir():
        return f"Error: '{directory}' is not a valid directory"

    video_paths = scan_videos(dir_path)
    if not video_paths:
        return f"No supported videos found in '{directory}'"

    storage = LocalVideoStorage(_assets_dir(), host=host)
    stats = await import_videos(storage, video_paths)
    return f"{stats['imported']} imported, {stats['skipped']} skipped, {stats['errors']} errors"


async def main(matrix: Matrix) -> None:
    channel = new_channel(
        name="video_importer",
        description="Batch import video files into the local-video resource storage.",
    )

    @channel.build.command()
    async def import_dir(directory: str, host: str = "workspace-assets") -> str:
        """Import all video files from a directory into local-video resource storage.

        directory: absolute path to a directory with video files
        host:      storage host name (default: workspace-assets)
        """
        return await _do_import_dir(directory, host)

    @channel.build.command()
    async def list_videos(query: str = "", limit: int = 50) -> str:
        """List videos currently in local-video storage.  query matches file_name."""
        infos = await matrix.resources().list_infos(
            "local-video", query=query or None, limit=limit
        )
        if not infos:
            return "No videos found."
        lines = [f"{len(infos)} video(s):"]
        for info in infos:
            size_mb = info.file_size / (1024 * 1024) if info.file_size else 0
            lines.append(f"  {info.path}  {size_mb:.1f}MB  {info.content_type}")
        return "\n".join(lines)

    await matrix.provide_channel(channel)


# -- entry ----------------------------------------------------------------

if __name__ == "__main__":
    main_gui()
