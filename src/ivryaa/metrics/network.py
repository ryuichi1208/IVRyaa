"""Network statistics collection module"""

from typing import Any

import psutil

from ivryaa.metrics.collector import MetricsCollector


class NetworkCollector(MetricsCollector):
    """Class for collecting network statistics"""

    def collect(self) -> dict[str, float]:
        """Return network statistics"""
        net = psutil.net_io_counters()
        return {
            "bytes_sent_mb": net.bytes_sent / (1024**2),
            "bytes_recv_mb": net.bytes_recv / (1024**2),
        }

    def describe(self) -> str:
        return "Network Statistics"

    def get_detailed(self) -> dict[str, Any]:
        """Return detailed network information"""
        net = psutil.net_io_counters()
        return {
            "bytes_sent_mb": net.bytes_sent / (1024**2),
            "bytes_recv_mb": net.bytes_recv / (1024**2),
            "packets_sent": net.packets_sent,
            "packets_recv": net.packets_recv,
            "errin": net.errin,
            "errout": net.errout,
        }
