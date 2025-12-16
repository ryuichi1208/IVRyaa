"""Metrics collection module"""

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
    """Retrieve all metrics"""
    return {
        "cpu": CPUCollector().collect(),
        "memory": MemoryCollector().collect(),
        "disk": DiskCollector().collect(),
    }
