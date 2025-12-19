"""Tests for network metrics collector"""

from unittest.mock import MagicMock, patch

import pytest

from ivryaa.metrics.network import NetworkCollector


class TestNetworkCollector:
    """Test cases for NetworkCollector"""

    def test_collect_returns_dict(self, mock_psutil_network):
        """Test that collect() returns a dictionary"""
        collector = NetworkCollector()
        result = collector.collect()

        assert isinstance(result, dict)
        assert "bytes_sent_mb" in result
        assert "bytes_recv_mb" in result

    def test_collect_mb_conversion(self, mock_psutil_network):
        """Test that collect() correctly converts bytes to MB"""
        collector = NetworkCollector()
        result = collector.collect()

        # 1048576000 bytes = 1000 MB
        assert result["bytes_sent_mb"] == pytest.approx(1000.0, rel=0.01)
        # 2097152000 bytes = 2000 MB
        assert result["bytes_recv_mb"] == pytest.approx(2000.0, rel=0.01)

    def test_describe_returns_string(self):
        """Test that describe() returns a descriptive string"""
        collector = NetworkCollector()
        result = collector.describe()

        assert isinstance(result, str)
        assert result == "Network Statistics"

    def test_get_detailed_returns_dict(self, mock_psutil_network):
        """Test that get_detailed() returns a dictionary with all keys"""
        collector = NetworkCollector()
        result = collector.get_detailed()

        assert isinstance(result, dict)
        assert "bytes_sent_mb" in result
        assert "bytes_recv_mb" in result
        assert "packets_sent" in result
        assert "packets_recv" in result
        assert "errin" in result
        assert "errout" in result

    def test_get_detailed_values(self, mock_psutil_network):
        """Test that get_detailed() returns correct values"""
        collector = NetworkCollector()
        result = collector.get_detailed()

        assert result["packets_sent"] == 1000000
        assert result["packets_recv"] == 2000000
        assert result["errin"] == 10
        assert result["errout"] == 5
