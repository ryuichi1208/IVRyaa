"""CPU使用率収集モジュール"""

from typing import Any

import psutil

from ivryaa.metrics.collector import MetricsCollector


class CPUCollector(MetricsCollector):
    """CPU使用率を収集するクラス"""

    def collect(self) -> float:
        """CPU使用率をパーセントで返す"""
        return psutil.cpu_percent(interval=0.1)

    def describe(self) -> str:
        return "CPU使用率"

    def get_detailed(self) -> dict[str, Any]:
        """詳細なCPU情報を返す"""
        return {
            "percent": self.collect(),
            "count": psutil.cpu_count(),
            "count_logical": psutil.cpu_count(logical=True),
            "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        }
