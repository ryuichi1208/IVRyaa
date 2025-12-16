"""TTS speech synthesis module"""

import subprocess
import tempfile
from pathlib import Path

from openai import OpenAI

from ivryaa.utils.config import settings
from ivryaa.utils.logger import logger


class SpeechSynthesizer:
    """Speech synthesis class using OpenAI TTS"""

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.tts_model
        self.voice = settings.tts_voice

    def speak(self, text: str) -> None:
        """Convert text to speech and play it"""
        logger.info(f"Speech synthesis: {text}")

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
        """Play audio file (macOS compatible)"""
        try:
            subprocess.run(["afplay", str(path)], check=True)
        except FileNotFoundError:
            subprocess.run(["mpv", "--no-video", str(path)], check=True)
