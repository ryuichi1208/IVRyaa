"""Microphone input recording module"""

import io
import wave
from typing import Optional

import pyaudio

from ivryaa.utils.config import settings
from ivryaa.utils.logger import logger


class AudioRecorder:
    """Class for recording audio from microphone"""

    def __init__(self) -> None:
        self.sample_rate = settings.audio_sample_rate
        self.channels = settings.audio_channels
        self.chunk_size = settings.audio_chunk_size
        self.format = pyaudio.paInt16
        self._audio: Optional[pyaudio.PyAudio] = None

    def _get_audio(self) -> pyaudio.PyAudio:
        if self._audio is None:
            self._audio = pyaudio.PyAudio()
        return self._audio

    def record(self, duration: float = 5.0) -> bytes:
        """Record for specified seconds and return WAV format byte data"""
        audio = self._get_audio()

        logger.info(f"Starting {duration} seconds recording...")

        stream = audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        frames: list[bytes] = []
        num_chunks = int(self.sample_rate / self.chunk_size * duration)

        for _ in range(num_chunks):
            data = stream.read(self.chunk_size)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        logger.info("Recording complete")

        return self._frames_to_wav(frames)

    def _frames_to_wav(self, frames: list[bytes]) -> bytes:
        """Convert frame data to WAV format"""
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self._get_audio().get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b"".join(frames))
        return buffer.getvalue()

    def close(self) -> None:
        """Release resources"""
        if self._audio is not None:
            self._audio.terminate()
            self._audio = None
