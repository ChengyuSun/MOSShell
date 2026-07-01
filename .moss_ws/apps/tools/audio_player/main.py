"""Audio Player — play audio files via macOS afplay command.

Usage:
  MOSS:    moss apps start tools/audio_player
           Then via CTML:
             <apps.tools_audio_player:play locator="local-audio://workspace-assets/my_song" />
             <apps.tools_audio_player:play_file file_path="/path/to/file.mp3" />
             <apps.tools_audio_player:stop />

Note: afplay supports mp3, wav, aac, m4a, aiff. Does NOT support flac, ogg, opus.
"""

from __future__ import annotations

import asyncio
import logging
import signal
import subprocess
import shutil
from pathlib import Path
from typing import Any, Optional

from ghoshell_moss.core.blueprint.channel_builder import new_channel
from ghoshell_moss.core.blueprint.matrix import Matrix


class _PlayerState:
    """Tracks the currently playing afplay process."""

    def __init__(self) -> None:
        self._process: Optional[subprocess.Popen] = None

    @property
    def is_playing(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def play(self, file_path: str) -> str:
        """Start playing a file. Stops any current playback first."""
        if self.is_playing:
            self.stop()

        if not shutil.which("afplay"):
            raise RuntimeError("afplay not found — macOS only")

        self._process = subprocess.Popen(
            ["afplay", file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return f"Playing: {Path(file_path).name}"

    def stop(self) -> str:
        """Stop current playback."""
        if self._process is not None:
            proc = self._process
            self._process = None
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                return "Playback stopped."
        return "No audio is currently playing."


async def main(matrix: Matrix) -> None:
    player = _PlayerState()

    # Register signal handlers so SIGTERM/SIGINT stop playback on exit.
    loop = asyncio.get_running_loop()
    main_task = asyncio.current_task()

    def _on_signal(signum: int, _frame: Any) -> None:
        loop.call_soon_threadsafe(main_task.cancel)

    signal.signal(signal.SIGTERM, _on_signal)
    signal.signal(signal.SIGINT, _on_signal)

    try:
        channel = new_channel(
            name="audio_player",
            description="Play audio files via macOS afplay. Supports mp3, wav, aac, m4a, aiff.",
        )

        @channel.build.command()
        async def play(locator: str) -> str:
            """Play an audio file from resource storage by its locator.

            locator format: local-audio://host/path
            Example: local-audio://workspace-assets/notification.mp3

            Note: afplay supports mp3, wav, aac, m4a, aiff.
                  Does NOT support flac, ogg, opus.
            """
            if "://" not in locator:
                return f"Error: invalid locator format. Expected scheme://host/path, got: {locator}"

            item = await matrix.resources().get(locator)
            if item is None:
                return f"Error: resource not found for locator '{locator}'"

            file_path = await item.get()
            file_path_str = str(file_path)

            if not Path(file_path_str).exists():
                return f"Error: file not found on disk: {file_path_str}"

            return player.play(file_path_str)

        @channel.build.command()
        async def stop() -> str:
            """Stop any currently playing audio."""
            return player.stop()

        await matrix.provide_channel(channel)

        # Keep alive until signalled or cancelled.
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            pass

    finally:
        player.stop()


if __name__ == "__main__":
    Matrix.discover().run(main)
