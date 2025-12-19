"""Tests for memory metrics collector"""

from unittest.mock import MagicMock, patch

import pytest

from ivryaa.metrics.memory import MemoryCollector


class TestMemoryCollector:
    """Test cases for MemoryCollector"""

    def test_collect_returns_float(self, mock_psutil_memory):
        """Test that collect() returns a float value"""
        collector = MemoryCollector()
        result = collector.collect()

        assert isinstance(result, float)
        assert result == 65.2

    def test_collect_calls_psutil(self, mock_psutil_memory):
        """Test that collect() calls psutil.virtual_memory"""
        collector = MemoryCollector()
        collector.collect()

        mock_psutil_memory.assert_called()

    def test_describe_returns_string(self):
        """Test that describe() returns a descriptive string"""
        collector = MemoryCollector()
        result = collector.describe()

        assert isinstance(result, str)
        assert result == "Memory Usage"

    def test_get_detailed_returns_dict(self, mock_psutil_memory):
        """Test that get_detailed() returns a dictionary with expected keys"""
        collector = MemoryCollector()
        result = collector.get_detailed()

        assert isinstance(result, dict)
        assert "percent" in result
        assert "total_gb" in result
        assert "available_gb" in result
        assert "used_gb" in result

    def test_get_detailed_gb_conversion(self, mock_psutil_memory):
        """Test that get_detailed() correctly converts bytes to GB"""
        collector = MemoryCollector()
        result = collector.get_detailed()

        # 17179869184 bytes = 16.0 GB
        assert result["total_gb"] == pytest.approx(16.0, rel=0.01)
        assert result["percent"] == 65.2
