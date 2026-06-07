"""
Audio capture contracts — shared abstractions for system audio input.

Capture source → raw PCM → transport → consumers (ASR, waveform, AI perception).
Transport isolates audio core from Matrix/Zenoh, keeping contracts layer dependency-free.
"""
import logging
from abc import ABC, abstractmethod
from typing import Callable

import numpy as np
from pydantic import BaseModel, Field

from ghoshell_moss.contracts.configs import ConfigType
from ghoshell_moss.core.blueprint.session import StreamSubscriber
from ghoshell_moss.core.concepts.topic import TOPIC_MODEL, TopicModel, TopicWindow

__all__ = [
    "AudioFrameMeta",
    "AudioChunk",
    "AudioCaptureConfig",
    "AudioRuntimeInfo",
    "AudioCaptureSource",
    "AudioPullLatest",
    "AudioSequentialConsumer",
    "AudioTransport",
]


class AudioFrameMeta(BaseModel):
    """Per-frame metadata computed once at capture, shared by all consumers."""

    rms_db: float = 0.0
    bands: dict[str, float] = Field(default_factory=lambda: {"bass": -96, "mid": -96, "high": -96})
    is_silent: bool = True


class AudioChunk(BaseModel):
    """One frame of captured audio — raw PCM plus precomputed metadata."""

    model_config = {"arbitrary_types_allowed": True}

    seq: int = 0
    timestamp: float = 0.0
    samples: np.ndarray = Field(default_factory=lambda: np.array([], dtype=np.int16))
    meta: AudioFrameMeta = Field(default_factory=AudioFrameMeta)


class AudioCaptureConfig(ConfigType):
    """Format consensus — consumers read this to know stream parameters."""

    sample_rate: int = 44100
    channels: int = 1
    format: str = "pcm_s16le"
    frame_duration_ms: int = 50
    device_pattern: str = "blackhole"

    @classmethod
    def conf_name(cls) -> str:
        return "audio_capture"


class AudioRuntimeInfo(BaseModel):
    """Runtime discovery — where the stream lives and whether it's alive."""

    running: bool = False
    stream_key: str = ""
    device_name: str = ""
    device_explain: str = ""
    started_at: float = 0.0
    last_heartbeat: float = 0.0


class AudioCaptureSource(ABC):
    """Singleton capture source. Owns the microphone, publishes PCM to Zenoh."""

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    def device_explain(self) -> str: ...

    @abstractmethod
    def new_consumer(self, ring_buffer_frames: int = 64) -> "AudioPullLatest": ...

    @abstractmethod
    def new_sequential_consumer(self, max_queue_frames: int = 128) -> "AudioSequentialConsumer": ...

    @abstractmethod
    async def close(self) -> None: ...


class AudioPullLatest(ABC):
    """Non-blocking latest-frame consumer. For waveform display, AI perception."""

    @abstractmethod
    def pull_latest(self) -> AudioChunk | None: ...

    @abstractmethod
    def close(self) -> None: ...


class AudioSequentialConsumer(ABC):
    """Ordered, lossless consumer with backpressure. For ASR, audio recording."""

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    def __aiter__(self) -> "AudioSequentialConsumer": ...

    @abstractmethod
    async def __anext__(self) -> AudioChunk: ...


class AudioTransport(ABC):
    """Transport abstraction isolating audio core from Matrix/Session/Zenoh.

    Audio capture only needs: publish PCM, subscribe to PCM, process lock,
    topic broadcast, and a logger. How those are implemented (Zenoh, FileLocker,
    TopicService) is the adapter's concern — not audio core's.

    Single coupling point: MatrixAudioTransport in host/speech/capture/.
    """

    # -- PCM stream --
    @abstractmethod
    def pub_pcm(self, chunk: bytes) -> None:
        """Publish a raw PCM chunk to the audio stream."""
        ...

    @abstractmethod
    def sub_pcm_callback(self, on_chunk: Callable[[bytes], None]) -> Callable[[], None]:
        """Subscribe to PCM stream via callback. Returns a release handle."""
        ...

    @abstractmethod
    def sub_pcm_stream(self, maxsize: int) -> StreamSubscriber:
        """Subscribe to PCM stream as an async iterable."""
        ...

    # -- process lock --
    @abstractmethod
    def acquire_lock(self) -> bool:
        """Acquire cross-process lock for exclusive device access."""
        ...

    @abstractmethod
    def release_lock(self) -> None:
        """Release the process lock."""
        ...

    # -- topic broadcast --
    @abstractmethod
    def pub_topic(self, topic: TopicModel) -> None:
        """Publish a topic via the transport's topic service."""
        ...

    @abstractmethod
    def topic_window(self, model: type[TOPIC_MODEL], max_size: int) -> TopicWindow[TOPIC_MODEL]:
        """Create a bounded sliding window over a topic stream."""
        ...

    # -- logger --
    @property
    @abstractmethod
    def logger(self) -> logging.Logger:
        """Logger for audio capture diagnostics."""
        ...
