"""CPU usage collection module"""

from typing import Any

import psutil

from ivryaa.metrics.collector import MetricsCollector


class CPUCollector(MetricsCollector):
    """Class for collecting CPU usage"""

    def collect(self) -> float:
        """Return CPU usage as percentage"""
        return psutil.cpu_percent(interval=0.1)

    def describe(self) -> str:
        return "CPU Usage"

    def get_detailed(self) -> dict[str, Any]:
        """Return detailed CPU information"""
        return {
            "percent": self.collect(),
            "count": psutil.cpu_count(),
            "count_logical": psutil.cpu_count(logical=True),
            "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        }
