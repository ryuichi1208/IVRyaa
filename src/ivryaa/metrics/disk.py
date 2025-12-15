"""ディスク使用率収集モジュール"""

from typing import Any

import psutil

from ivryaa.metrics.collector import MetricsCollector


class DiskCollector(MetricsCollector):
    """ディスク使用率を収集するクラス"""

    def __init__(self, path: str = "/") -> None:
        self.path = path

    def collect(self) -> float:
        """ディスク使用率をパーセントで返す"""
        return psutil.disk_usage(self.path).percent

    def describe(self) -> str:
        return f"ディスク使用率 ({self.path})"

    def get_detailed(self) -> dict[str, Any]:
        """詳細なディスク情報を返す"""
        disk = psutil.disk_usage(self.path)
        return {
            "percent": disk.percent,
            "total_gb": disk.total / (1024**3),
            "used_gb": disk.used / (1024**3),
            "free_gb": disk.free / (1024**3),
        }
