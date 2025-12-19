"""Tests for speech synthesizer"""

from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest


class TestSpeechSynthesizer:
    """Test cases for SpeechSynthesizer"""

    @pytest.fixture
    def mock_settings(self):
        """Mock settings"""
        with patch("ivryaa.voice.synthesizer.settings") as mock:
            mock.openai_api_key = "test-api-key"
            mock.tts_model = "tts-1"
            mock.tts_voice = "alloy"
            yield mock

    @pytest.fixture
    def mock_openai(self):
        """Mock OpenAI client"""
        with patch("ivryaa.voice.synthesizer.OpenAI") as mock:
            client = MagicMock()
            response = MagicMock()
            response.content = b"\x00" * 1024  # Fake MP3 data
            client.audio.speech.create.return_value = response
            mock.return_value = client
            yield {"class": mock, "client": client, "response": response}

    @pytest.fixture
    def mock_subprocess(self):
        """Mock subprocess.run"""
        with patch("ivryaa.voice.synthesizer.subprocess.run") as mock:
            yield mock

    @pytest.fixture
    def mock_tempfile(self):
        """Mock tempfile"""
        with patch("ivryaa.voice.synthesizer.tempfile.NamedTemporaryFile") as mock:
            temp = MagicMock()
            temp.__enter__ = MagicMock(return_value=temp)
            temp.__exit__ = MagicMock(return_value=False)
            temp.name = "/tmp/test_audio.mp3"
            mock.return_value = temp
            yield mock

    @pytest.fixture
    def mock_path_unlink(self):
        """Mock Path.unlink"""
        with patch.object(Path, "unlink") as mock:
            yield mock

    @pytest.fixture
    def synthesizer(self, mock_settings, mock_openai):
        """Create SpeechSynthesizer instance"""
        from ivryaa.voice.synthesizer import SpeechSynthesizer
        return SpeechSynthesizer()

    def test_init_creates_client(self, mock_settings, mock_openai):
        """Test that __init__ creates OpenAI client"""
        from ivryaa.voice.synthesizer import SpeechSynthesizer
        synthesizer = SpeechSynthesizer()

        mock_openai["class"].assert_called_with(api_key="test-api-key")

    def test_init_sets_model_and_voice(self, synthesizer, mock_settings):
        """Test that __init__ sets model and voice from settings"""
        assert synthesizer.model == "tts-1"
        assert synthesizer.voice == "alloy"

    def test_speak_calls_api(self, synthesizer, mock_openai, mock_subprocess, mock_path_unlink):
        """Test that speak() calls the API"""
        synthesizer.speak("テストメッセージ")

        mock_openai["client"].audio.speech.create.assert_called_once()

    def test_speak_api_parameters(self, synthesizer, mock_openai, mock_subprocess, mock_path_unlink):
        """Test that speak() passes correct parameters to API"""
        synthesizer.speak("テストメッセージ")

        call_kwargs = mock_openai["client"].audio.speech.create.call_args.kwargs
        assert call_kwargs["model"] == "tts-1"
        assert call_kwargs["voice"] == "alloy"
        assert call_kwargs["input"] == "テストメッセージ"

    def test_speak_plays_audio(self, synthesizer, mock_openai, mock_subprocess, mock_path_unlink):
        """Test that speak() plays the audio file"""
        synthesizer.speak("テストメッセージ")

        mock_subprocess.assert_called()

    def test_speak_cleans_up_temp_file(self, synthesizer, mock_openai, mock_subprocess, mock_path_unlink):
        """Test that speak() cleans up temporary file"""
        synthesizer.speak("テストメッセージ")

        mock_path_unlink.assert_called_with(missing_ok=True)

    def test_play_audio_tries_afplay_first(self, synthesizer, mock_subprocess):
        """Test that _play_audio tries afplay first (macOS)"""
        path = Path("/tmp/test.mp3")
        synthesizer._play_audio(path)

        mock_subprocess.assert_called_with(["afplay", "/tmp/test.mp3"], check=True)

    def test_play_audio_falls_back_to_mpv(self, synthesizer, mock_subprocess):
        """Test that _play_audio falls back to mpv if afplay not found"""
        mock_subprocess.side_effect = [FileNotFoundError, None]
        path = Path("/tmp/test.mp3")
        synthesizer._play_audio(path)

        assert mock_subprocess.call_count == 2
        mock_subprocess.assert_called_with(["mpv", "--no-video", "/tmp/test.mp3"], check=True)
