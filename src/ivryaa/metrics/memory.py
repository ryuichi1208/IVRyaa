"""Memory usage collection module"""

from typing import Any

import psutil

from ivryaa.metrics.collector import MetricsCollector


class MemoryCollector(MetricsCollector):
    """Class for collecting memory usage"""

    def collect(self) -> float:
        """Return memory usage as percentage"""
        return psutil.virtual_memory().percent

    def describe(self) -> str:
        return "Memory Usage"

    def get_detailed(self) -> dict[str, Any]:
        """Return detailed memory information"""
        mem = psutil.virtual_memory()
        return {
            "percent": mem.percent,
            "total_gb": mem.total / (1024**3),
            "available_gb": mem.available / (1024**3),
            "used_gb": mem.used / (1024**3),
        }
