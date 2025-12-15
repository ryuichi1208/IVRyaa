"""TTS音声合成モジュール"""

import subprocess
import tempfile
from pathlib import Path

from openai import OpenAI

from ivryaa.utils.config import settings
from ivryaa.utils.logger import logger


class SpeechSynthesizer:
    """OpenAI TTSを使用した音声合成クラス"""

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.tts_model
        self.voice = settings.tts_voice

    def speak(self, text: str) -> None:
        """テキストを音声に変換して再生する"""
        logger.info(f"音声合成: {text}")

        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text,
        )

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(response.content)
            temp_path = Path(f.name)

        try:
            self._play_audio(temp_path)
        finally:
            temp_path.unlink(missing_ok=True)

    def _play_audio(self, path: Path) -> None:
        """音声ファイルを再生する（macOS対応）"""
        try:
            subprocess.run(["afplay", str(path)], check=True)
        except FileNotFoundError:
            subprocess.run(["mpv", "--no-video", str(path)], check=True)
