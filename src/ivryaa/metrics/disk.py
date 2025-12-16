"""Disk usage collection module"""

from typing import Any

import psutil

from ivryaa.metrics.collector import MetricsCollector


class DiskCollector(MetricsCollector):
    """Class for collecting disk usage"""

    def __init__(self, path: str = "/") -> None:
        self.path = path

    def collect(self) -> float:
        """Return disk usage as percentage"""
        return psutil.disk_usage(self.path).percent

    def describe(self) -> str:
        return f"Disk Usage ({self.path})"

    def get_detailed(self) -> dict[str, Any]:
        """Return detailed disk information"""
        disk = psutil.disk_usage(self.path)
        return {
            "percent": disk.percent,
            "total_gb": disk.total / (1024**3),
            "used_gb": disk.used / (1024**3),
            "free_gb": disk.free / (1024**3),
        }
