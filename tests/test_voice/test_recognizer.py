"""Tests for speech recognizer"""

from unittest.mock import MagicMock, patch

import pytest


class TestSpeechRecognizer:
    """Test cases for SpeechRecognizer"""

    @pytest.fixture
    def mock_settings(self):
        """Mock settings"""
        with patch("ivryaa.voice.recognizer.settings") as mock:
            mock.openai_api_key = "test-api-key"
            mock.whisper_model = "whisper-1"
            yield mock

    @pytest.fixture
    def mock_openai(self):
        """Mock OpenAI client"""
        with patch("ivryaa.voice.recognizer.OpenAI") as mock:
            client = MagicMock()
            response = MagicMock()
            response.text = "テスト認識結果"
            client.audio.transcriptions.create.return_value = response
            mock.return_value = client
            yield {"class": mock, "client": client, "response": response}

    @pytest.fixture
    def recognizer(self, mock_settings, mock_openai):
        """Create SpeechRecognizer instance"""
        from ivryaa.voice.recognizer import SpeechRecognizer
        return SpeechRecognizer()

    def test_init_creates_client(self, mock_settings, mock_openai):
        """Test that __init__ creates OpenAI client"""
        from ivryaa.voice.recognizer import SpeechRecognizer
        recognizer = SpeechRecognizer()

        mock_openai["class"].assert_called_with(api_key="test-api-key")

    def test_init_sets_model(self, recognizer, mock_settings):
        """Test that __init__ sets model from settings"""
        assert recognizer.model == "whisper-1"

    def test_transcribe_returns_string(self, recognizer):
        """Test that transcribe() returns a string"""
        audio_data = b"\x00" * 1024
        result = recognizer.transcribe(audio_data)

        assert isinstance(result, str)
        assert result == "テスト認識結果"

    def test_transcribe_calls_api(self, recognizer, mock_openai):
        """Test that transcribe() calls the API with correct parameters"""
        audio_data = b"\x00" * 1024
        recognizer.transcribe(audio_data)

        mock_openai["client"].audio.transcriptions.create.assert_called_once()
        call_kwargs = mock_openai["client"].audio.transcriptions.create.call_args.kwargs
        assert call_kwargs["model"] == "whisper-1"
        assert call_kwargs["language"] == "ja"

    def test_transcribe_passes_audio_data(self, recognizer, mock_openai):
        """Test that transcribe() passes audio data to API"""
        audio_data = b"\x00" * 1024
        recognizer.transcribe(audio_data)

        call_kwargs = mock_openai["client"].audio.transcriptions.create.call_args.kwargs
        # file is a tuple: (filename, data, mime_type)
        assert call_kwargs["file"][0] == "audio.wav"
        assert call_kwargs["file"][1] == audio_data
        assert call_kwargs["file"][2] == "audio/wav"
