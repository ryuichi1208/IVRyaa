"""メモリ使用率収集モジュール"""

from typing import Any

import psutil

from ivryaa.metrics.collector import MetricsCollector


class MemoryCollector(MetricsCollector):
    """メモリ使用率を収集するクラス"""

    def collect(self) -> float:
        """メモリ使用率をパーセントで返す"""
        return psutil.virtual_memory().percent

    def describe(self) -> str:
        return "メモリ使用率"

    def get_detailed(self) -> dict[str, Any]:
        """詳細なメモリ情報を返す"""
        mem = psutil.virtual_memory()
        return {
            "percent": mem.percent,
            "total_gb": mem.total / (1024**3),
            "available_gb": mem.available / (1024**3),
            "used_gb": mem.used / (1024**3),
        }
