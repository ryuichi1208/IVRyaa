"""Tests for CPU metrics collector"""

from unittest.mock import MagicMock, patch

import pytest

from ivryaa.metrics.cpu import CPUCollector


class TestCPUCollector:
    """Test cases for CPUCollector"""

    def test_collect_returns_float(self, mock_psutil_cpu):
        """Test that collect() returns a float value"""
        collector = CPUCollector()
        result = collector.collect()

        assert isinstance(result, float)
        assert result == 45.5

    def test_collect_calls_psutil(self, mock_psutil_cpu):
        """Test that collect() calls psutil.cpu_percent"""
        collector = CPUCollector()
        collector.collect()

        mock_psutil_cpu["percent"].assert_called_once_with(interval=0.1)

    def test_describe_returns_string(self):
        """Test that describe() returns a descriptive string"""
        collector = CPUCollector()
        result = collector.describe()

        assert isinstance(result, str)
        assert result == "CPU Usage"

    def test_get_detailed_returns_dict(self, mock_psutil_cpu):
        """Test that get_detailed() returns a dictionary with expected keys"""
        collector = CPUCollector()
        result = collector.get_detailed()

        assert isinstance(result, dict)
        assert "percent" in result
        assert "count" in result
        assert "count_logical" in result
        assert "freq" in result

    def test_get_detailed_values(self, mock_psutil_cpu):
        """Test that get_detailed() returns correct values"""
        collector = CPUCollector()
        result = collector.get_detailed()

        assert result["percent"] == 45.5
        assert result["count"] == 8
        assert result["count_logical"] == 8

    def test_get_detailed_freq_none(self):
        """Test get_detailed() when cpu_freq returns None"""
        with patch("psutil.cpu_percent", return_value=50.0), \
             patch("psutil.cpu_count", return_value=4), \
             patch("psutil.cpu_freq", return_value=None):
            collector = CPUCollector()
            result = collector.get_detailed()

            assert result["freq"] is None
