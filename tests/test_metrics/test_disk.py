"""Tests for disk metrics collector"""

from unittest.mock import MagicMock, patch

import pytest

from ivryaa.metrics.disk import DiskCollector


class TestDiskCollector:
    """Test cases for DiskCollector"""

    def test_collect_returns_float(self, mock_psutil_disk):
        """Test that collect() returns a float value"""
        collector = DiskCollector()
        result = collector.collect()

        assert isinstance(result, float)
        assert result == 72.3

    def test_collect_with_default_path(self, mock_psutil_disk):
        """Test that collect() uses default path '/'"""
        collector = DiskCollector()
        collector.collect()

        mock_psutil_disk.assert_called_with("/")

    def test_collect_with_custom_path(self, mock_psutil_disk):
        """Test that collect() works with custom path"""
        collector = DiskCollector(path="/tmp")
        collector.collect()

        mock_psutil_disk.assert_called_with("/tmp")

    def test_describe_returns_string(self):
        """Test that describe() returns a descriptive string"""
        collector = DiskCollector()
        result = collector.describe()

        assert isinstance(result, str)
        assert "Disk Usage" in result
        assert "/" in result

    def test_describe_includes_path(self):
        """Test that describe() includes the path"""
        collector = DiskCollector(path="/home")
        result = collector.describe()

        assert "/home" in result

    def test_get_detailed_returns_dict(self, mock_psutil_disk):
        """Test that get_detailed() returns a dictionary with expected keys"""
        collector = DiskCollector()
        result = collector.get_detailed()

        assert isinstance(result, dict)
        assert "percent" in result
        assert "total_gb" in result
        assert "used_gb" in result
        assert "free_gb" in result

    def test_get_detailed_gb_conversion(self, mock_psutil_disk):
        """Test that get_detailed() correctly converts bytes to GB"""
        collector = DiskCollector()
        result = collector.get_detailed()

        # 500107862016 bytes ≈ 465.76 GB
        assert result["total_gb"] == pytest.approx(465.76, rel=0.01)
        assert result["percent"] == 72.3
