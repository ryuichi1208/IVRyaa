"""Whisperによる音声認識モジュール"""

from openai import OpenAI

from ivryaa.utils.config import settings
from ivryaa.utils.logger import logger


class SpeechRecognizer:
    """OpenAI Whisperを使用した音声認識クラス"""

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.whisper_model

    def transcribe(self, audio_data: bytes) -> str:
        """音声データをテキストに変換する"""
        logger.info("音声認識を実行中...")

        response = self.client.audio.transcriptions.create(
            model=self.model,
            file=("audio.wav", audio_data, "audio/wav"),
            language="ja",
        )

        text = response.text
        logger.info(f"認識結果: {text}")

        return text
