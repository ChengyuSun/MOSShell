"""Audio Importer — batch import audio files into the local-audio resource storage.

Usage:
  GUI:     moss apps test tools/audio_importer   (primary)
  MOSS:    moss apps start tools/audio_importer
           Then via CTML: <apps.tools_audio_importer:import_dir directory="/path" />
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from ghoshell_moss.core.blueprint.channel_builder import new_channel
from ghoshell_moss.core.blueprint.matrix import Matrix
from ghoshell_moss.core.resources.local_audio import (
    _AUDIO_EXTENSIONS,
    LocalAudioInfo,
    LocalAudioItem,
    LocalAudioStorage,
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
    return _find_workspace_root() / ".moss_ws" / "assets" / "audios"


def scan_audios(directory: Path) -> list[Path]:
    """Scan a directory for supported audio files (case-insensitive)."""
    files: list[Path] = []
    for p in directory.iterdir():
        if p.is_file() and p.suffix.lower() in _AUDIO_EXTENSIONS:
            files.append(p)
    return sorted(files)


async def import_audios(
    storage: LocalAudioStorage,
    audio_paths: list[Path],
    on_progress=None,
) -> dict:
    """Import audios into the storage.  Returns {imported, skipped, errors}."""
    stats = {"imported": 0, "skipped": 0, "errors": 0}

    all_infos = await storage.list_infos(limit=-1)
    existing_names = {m.file_name for m in all_infos}

    for i, audio_path in enumerate(audio_paths):
        name = audio_path.name
        stem = audio_path.stem

        if name in existing_names:
            stats["skipped"] += 1
            if on_progress:
                on_progress(i, len(audio_paths), name, "skipped (already exists)")
            continue

        try:
            meta = LocalAudioInfo(
                path=name,
                description=stem.replace("_", " ").replace("-", " "),
            )
            item = LocalAudioItem(meta, audio_path)
            locator = await storage.put(item)
            existing_names.add(name)
            stats["imported"] += 1
            if on_progress:
                on_progress(i, len(audio_paths), name, f"ok → {locator}")

        except Exception as exc:
            stats["errors"] += 1
            if on_progress:
                on_progress(i, len(audio_paths), name, f"error: {exc}")

    return stats


# -- GUI ------------------------------------------------------------------

def main_gui() -> None:
    import threading
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    root = tk.Tk()
    root.title("Audio Importer — MOSS local-audio Storage")
    root.geometry("640x400")
    root.resizable(True, True)

    selected_dir = tk.StringVar()
    host_var = tk.StringVar(value="workspace-assets")
    status_var = tk.StringVar(value="Ready.")
    file_count_var = tk.StringVar(value="")

    def select_directory() -> None:
        path = filedialog.askdirectory(title="Select a directory containing audio files")
        if not path:
            return
        selected_dir.set(path)
        audios = scan_audios(Path(path))
        file_count_var.set(f"{len(audios)} audio file(s) found")

    def _schedule_ui(cb) -> None:
        root.after_idle(cb)

    def _on_import_done() -> None:
        progress_bar["value"] = 0
        status_var.set("Ready.")
        import_btn["state"] = "normal"

    def _bg_import(audio_paths: list[Path]) -> None:
        """Run the async import in a background thread so tkinter stays responsive."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_do_import(audio_paths))
        except Exception as exc:
            _schedule_ui(lambda: messagebox.showerror("Error", str(exc)))
        finally:
            loop.close()
            _schedule_ui(_on_import_done)

    async def _do_import(audio_paths: list[Path]) -> None:
        storage = LocalAudioStorage(_assets_dir(), host=host_var.get())

        def update(i: int, total: int, name: str, status: str) -> None:
            def _apply() -> None:
                progress_bar["value"] = i + 1
                status_var.set(f"[{i + 1}/{total}] {name}: {status}")
            _schedule_ui(_apply)

        stats = await import_audios(storage, audio_paths, on_progress=update)

        def _show_done() -> None:
            messagebox.showinfo(
                "Done",
                f"Imported: {stats['imported']}\nSkipped: {stats['skipped']}\nErrors: {stats['errors']}",
            )
        _schedule_ui(_show_done)

    def run_import() -> None:
        path = selected_dir.get()
        if not path:
            messagebox.showwarning("Warning", "Select a directory first")
            return

        audio_paths = scan_audios(Path(path))
        if not audio_paths:
            messagebox.showinfo("No audio files", f"No supported audio files in:\n{path}")
            return

        progress_bar["maximum"] = len(audio_paths)
        import_btn["state"] = "disabled"
        threading.Thread(target=_bg_import, args=(audio_paths,), daemon=True).start()

    # -- layout --
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Batch Import Audio Files to MOSS Resource Storage",
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
    import_btn = ttk.Button(frame, text="Import Audios", command=run_import)
    import_btn.pack(pady=12)

    ttk.Label(frame, text="Supported: MP3, WAV, FLAC, OGG, M4A, AAC, WMA, OPUS, WEBA, AIFF, MKA",
              foreground="gray").pack(side=tk.BOTTOM, pady=(8, 0))

    root.mainloop()


# -- MOSS Channel ---------------------------------------------------------

async def _do_import_dir(directory: str, host: str) -> str:
    dir_path = Path(directory).resolve()
    if not dir_path.is_dir():
        return f"Error: '{directory}' is not a valid directory"

    audio_paths = scan_audios(dir_path)
    if not audio_paths:
        return f"No supported audio files found in '{directory}'"

    storage = LocalAudioStorage(_assets_dir(), host=host)
    stats = await import_audios(storage, audio_paths)
    return f"{stats['imported']} imported, {stats['skipped']} skipped, {stats['errors']} errors"


async def main(matrix: Matrix) -> None:
    channel = new_channel(
        name="audio_importer",
        description="Batch import audio files into the local-audio resource storage.",
    )

    @channel.build.command()
    async def import_dir(directory: str, host: str = "workspace-assets") -> str:
        """Import all audio files from a directory into resource storage.

        directory:  absolute path to a directory with audio files
        host:       storage host name (default: workspace-assets)
        """
        return await _do_import_dir(directory, host)

    await matrix.provide_channel(channel)


# -- entry ----------------------------------------------------------------

if __name__ == "__main__":
    main_gui()
