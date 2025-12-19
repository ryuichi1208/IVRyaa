"""Tests for response generation"""

from unittest.mock import MagicMock, patch

import pytest

from ivryaa.dialog.intent import Intent, IntentType
from ivryaa.dialog.response import ResponseGenerator


class TestResponseGenerator:
    """Test cases for ResponseGenerator"""

    @pytest.fixture
    def generator(self):
        """Create ResponseGenerator instance"""
        return ResponseGenerator()

    def test_generate_cpu_response(self, generator, mock_psutil_cpu):
        """Test CPU response generation"""
        intent = Intent(type=IntentType.GET_CPU, confidence=0.8, raw_text="cpu")
        result = generator.generate(intent)

        assert isinstance(result, str)
        assert "45.5" in result
        assert "パーセント" in result

    def test_generate_memory_response(self, generator, mock_psutil_memory):
        """Test memory response generation"""
        intent = Intent(type=IntentType.GET_MEMORY, confidence=0.8, raw_text="メモリ")
        result = generator.generate(intent)

        assert isinstance(result, str)
        assert "65.2" in result
        assert "パーセント" in result

    def test_generate_disk_response(self, generator, mock_psutil_disk):
        """Test disk response generation"""
        intent = Intent(type=IntentType.GET_DISK, confidence=0.8, raw_text="ディスク")
        result = generator.generate(intent)

        assert isinstance(result, str)
        assert "72.3" in result
        assert "パーセント" in result

    def test_generate_network_response(self, generator, mock_psutil_network):
        """Test network response generation"""
        intent = Intent(type=IntentType.GET_NETWORK, confidence=0.8, raw_text="ネットワーク")
        result = generator.generate(intent)

        assert isinstance(result, str)
        assert "メガバイト" in result

    def test_generate_all_response(self, generator, mock_psutil_cpu, mock_psutil_memory, mock_psutil_disk):
        """Test all metrics response generation"""
        intent = Intent(type=IntentType.GET_ALL, confidence=0.8, raw_text="全部")
        result = generator.generate(intent)

        assert isinstance(result, str)
        assert "CPU" in result or "cpu" in result.lower()
        assert "メモリ" in result
        assert "ディスク" in result

    def test_generate_help_response(self, generator):
        """Test help response generation"""
        intent = Intent(type=IntentType.HELP, confidence=0.8, raw_text="ヘルプ")
        result = generator.generate(intent)

        assert isinstance(result, str)
        assert "CPU" in result or "cpu" in result.lower()
        assert "メモリ" in result
        assert "ディスク" in result
        assert "終了" in result

    def test_generate_exit_response(self, generator):
        """Test exit response generation"""
        intent = Intent(type=IntentType.EXIT, confidence=0.8, raw_text="終了")
        result = generator.generate(intent)

        assert isinstance(result, str)
        assert "終了" in result

    def test_generate_unknown_response(self, generator):
        """Test unknown intent response generation"""
        intent = Intent(type=IntentType.UNKNOWN, confidence=0.0, raw_text="xyz")
        result = generator.generate(intent)

        assert isinstance(result, str)
        assert "聞き取れません" in result or "もう一度" in result
