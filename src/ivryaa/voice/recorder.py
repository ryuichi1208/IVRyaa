"""マイク入力の録音モジュール"""

import io
import wave
from typing import Optional

import pyaudio

from ivryaa.utils.config import settings
from ivryaa.utils.logger import logger


class AudioRecorder:
    """マイクからの音声を録音するクラス"""

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
        """指定した秒数だけ録音してWAV形式のバイトデータを返す"""
        audio = self._get_audio()

        logger.info(f"{duration}秒間の録音を開始します...")

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

        logger.info("録音完了")

        return self._frames_to_wav(frames)

    def _frames_to_wav(self, frames: list[bytes]) -> bytes:
        """フレームデータをWAV形式に変換"""
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self._get_audio().get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b"".join(frames))
        return buffer.getvalue()

    def close(self) -> None:
        """リソースを解放"""
        if self._audio is not None:
            self._audio.terminate()
            self._audio = None
