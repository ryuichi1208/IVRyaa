"""メトリクス収集モジュール"""

from ivryaa.metrics.collector import MetricsCollector
from ivryaa.metrics.cpu import CPUCollector
from ivryaa.metrics.disk import DiskCollector
from ivryaa.metrics.memory import MemoryCollector
from ivryaa.metrics.network import NetworkCollector

__all__ = [
    "MetricsCollector",
    "CPUCollector",
    "MemoryCollector",
    "DiskCollector",
    "NetworkCollector",
    "get_all_metrics",
]


def get_all_metrics() -> dict[str, float]:
    """全てのメトリクスを取得する"""
    return {
        "cpu": CPUCollector().collect(),
        "memory": MemoryCollector().collect(),
        "disk": DiskCollector().collect(),
    }
