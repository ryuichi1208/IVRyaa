"""Tests for intent parsing"""

import pytest

from ivryaa.dialog.intent import Intent, IntentParser, IntentType


class TestIntentType:
    """Test cases for IntentType enum"""

    def test_all_intent_types_exist(self):
        """Test that all expected intent types are defined"""
        assert IntentType.GET_CPU
        assert IntentType.GET_MEMORY
        assert IntentType.GET_DISK
        assert IntentType.GET_NETWORK
        assert IntentType.GET_ALL
        assert IntentType.HELP
        assert IntentType.EXIT
        assert IntentType.UNKNOWN


class TestIntent:
    """Test cases for Intent dataclass"""

    def test_intent_creation(self):
        """Test Intent dataclass creation"""
        intent = Intent(
            type=IntentType.GET_CPU,
            confidence=0.8,
            raw_text="CPUの状態を教えて"
        )

        assert intent.type == IntentType.GET_CPU
        assert intent.confidence == 0.8
        assert intent.raw_text == "CPUの状態を教えて"


class TestIntentParser:
    """Test cases for IntentParser"""

    @pytest.fixture
    def parser(self):
        """Create IntentParser instance"""
        return IntentParser()

    # CPU intent tests
    @pytest.mark.parametrize("text", [
        "cpu",
        "CPU",
        "シーピーユー",
        "プロセッサ",
        "処理",
        "CPUの状態を教えて",
    ])
    def test_parse_cpu_intent(self, parser, text):
        """Test parsing CPU-related intents"""
        result = parser.parse(text)
        assert result.type == IntentType.GET_CPU
        assert result.confidence == 0.8

    # Memory intent tests
    @pytest.mark.parametrize("text", [
        "メモリ",
        "memory",
        "MEMORY",
        "ram",
        "ラム",
        "メモリの使用量は？",
    ])
    def test_parse_memory_intent(self, parser, text):
        """Test parsing memory-related intents"""
        result = parser.parse(text)
        assert result.type == IntentType.GET_MEMORY
        assert result.confidence == 0.8

    # Disk intent tests
    @pytest.mark.parametrize("text", [
        "ディスク",
        "disk",
        "ストレージ",
        "容量",
        "ディスクの空き容量",
    ])
    def test_parse_disk_intent(self, parser, text):
        """Test parsing disk-related intents"""
        result = parser.parse(text)
        assert result.type == IntentType.GET_DISK
        assert result.confidence == 0.8

    # Network intent tests
    @pytest.mark.parametrize("text", [
        "ネットワーク",
        "network",
        "通信",
        "ネット",
        "ネットワークの状態",
    ])
    def test_parse_network_intent(self, parser, text):
        """Test parsing network-related intents"""
        result = parser.parse(text)
        assert result.type == IntentType.GET_NETWORK
        assert result.confidence == 0.8

    # Get all intent tests
    @pytest.mark.parametrize("text", [
        "全部",
        "すべて",
        "all",
        "全体",
        "まとめて",
        "全部教えて",
    ])
    def test_parse_all_intent(self, parser, text):
        """Test parsing get-all intents"""
        result = parser.parse(text)
        assert result.type == IntentType.GET_ALL
        assert result.confidence == 0.8

    # Help intent tests
    @pytest.mark.parametrize("text", [
        "ヘルプ",
        "help",
        "使い方",
        "何ができる",
    ])
    def test_parse_help_intent(self, parser, text):
        """Test parsing help intents"""
        result = parser.parse(text)
        assert result.type == IntentType.HELP
        assert result.confidence == 0.8

    # Exit intent tests
    @pytest.mark.parametrize("text", [
        "終了",
        "exit",
        "quit",
        "終わり",
        "さようなら",
        "バイバイ",
    ])
    def test_parse_exit_intent(self, parser, text):
        """Test parsing exit intents"""
        result = parser.parse(text)
        assert result.type == IntentType.EXIT
        assert result.confidence == 0.8

    # Unknown intent tests
    @pytest.mark.parametrize("text", [
        "こんにちは",
        "今日の天気は？",
        "xyz123",
        "",
    ])
    def test_parse_unknown_intent(self, parser, text):
        """Test parsing unknown intents"""
        result = parser.parse(text)
        assert result.type == IntentType.UNKNOWN
        assert result.confidence == 0.0

    def test_parse_preserves_raw_text(self, parser):
        """Test that raw_text is preserved in result"""
        text = "CPUの状態を教えてください"
        result = parser.parse(text)
        assert result.raw_text == text

    def test_parse_case_insensitive(self, parser):
        """Test that parsing is case insensitive"""
        result1 = parser.parse("CPU")
        result2 = parser.parse("cpu")
        result3 = parser.parse("Cpu")

        assert result1.type == IntentType.GET_CPU
        assert result2.type == IntentType.GET_CPU
        assert result3.type == IntentType.GET_CPU
