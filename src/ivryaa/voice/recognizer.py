"""Speech recognition module using Whisper"""

from openai import OpenAI

from ivryaa.utils.config import settings
from ivryaa.utils.logger import logger


class SpeechRecognizer:
    """Speech recognition class using OpenAI Whisper"""

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.whisper_model

    def transcribe(self, audio_data: bytes) -> str:
        """Convert audio data to text"""
        logger.info("Running speech recognition...")

        response = self.client.audio.transcriptions.create(
            model=self.model,
            file=("audio.wav", audio_data, "audio/wav"),
            language="ja",
        )

        text = response.text
        logger.info(f"Recognition result: {text}")

        return text
