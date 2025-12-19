"""Tests for audio recorder"""

import wave
from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest


class TestAudioRecorder:
    """Test cases for AudioRecorder"""

    @pytest.fixture
    def mock_settings(self):
        """Mock settings"""
        with patch("ivryaa.voice.recorder.settings") as mock:
            mock.audio_sample_rate = 16000
            mock.audio_channels = 1
            mock.audio_chunk_size = 1024
            yield mock

    @pytest.fixture
    def recorder(self, mock_settings, mock_pyaudio):
        """Create AudioRecorder instance with mocked dependencies"""
        from ivryaa.voice.recorder import AudioRecorder
        return AudioRecorder()

    def test_init_sets_properties(self, mock_settings):
        """Test that __init__ sets properties from settings"""
        with patch("pyaudio.PyAudio"):
            from ivryaa.voice.recorder import AudioRecorder
            recorder = AudioRecorder()

            assert recorder.sample_rate == 16000
            assert recorder.channels == 1
            assert recorder.chunk_size == 1024

    def test_record_returns_bytes(self, recorder, mock_pyaudio):
        """Test that record() returns bytes"""
        result = recorder.record(duration=1.0)

        assert isinstance(result, bytes)

    def test_record_opens_stream(self, recorder, mock_pyaudio):
        """Test that record() opens an audio stream"""
        recorder.record(duration=1.0)

        mock_pyaudio["audio"].open.assert_called()

    def test_record_reads_frames(self, recorder, mock_pyaudio):
        """Test that record() reads audio frames"""
        recorder.record(duration=1.0)

        mock_pyaudio["stream"].read.assert_called()

    def test_record_closes_stream(self, recorder, mock_pyaudio):
        """Test that record() closes the stream after recording"""
        recorder.record(duration=1.0)

        mock_pyaudio["stream"].stop_stream.assert_called()
        mock_pyaudio["stream"].close.assert_called()

    def test_record_produces_valid_wav(self, recorder, mock_pyaudio):
        """Test that record() produces valid WAV format"""
        result = recorder.record(duration=0.1)

        # Check WAV header (RIFF)
        assert result[:4] == b"RIFF"
        # Check WAVE format
        assert result[8:12] == b"WAVE"

    def test_close_terminates_audio(self, recorder, mock_pyaudio):
        """Test that close() terminates PyAudio"""
        recorder._get_audio()  # Initialize audio
        recorder.close()

        mock_pyaudio["audio"].terminate.assert_called()

    def test_close_sets_audio_to_none(self, recorder, mock_pyaudio):
        """Test that close() sets _audio to None"""
        recorder._get_audio()  # Initialize audio
        recorder.close()

        assert recorder._audio is None

    def test_close_handles_none_audio(self, recorder):
        """Test that close() handles None _audio gracefully"""
        recorder._audio = None
        recorder.close()  # Should not raise

    def test_frames_to_wav_format(self, recorder, mock_pyaudio):
        """Test _frames_to_wav produces correct format"""
        frames = [b"\x00" * 1024, b"\x00" * 1024]
        result = recorder._frames_to_wav(frames)

        # Parse as WAV
        buffer = BytesIO(result)
        with wave.open(buffer, "rb") as wf:
            assert wf.getnchannels() == 1
            assert wf.getframerate() == 16000
