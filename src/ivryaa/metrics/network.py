"""ネットワーク統計収集モジュール"""

from typing import Any

import psutil

from ivryaa.metrics.collector import MetricsCollector


class NetworkCollector(MetricsCollector):
    """ネットワーク統計を収集するクラス"""

    def collect(self) -> dict[str, float]:
        """ネットワーク統計を返す"""
        net = psutil.net_io_counters()
        return {
            "bytes_sent_mb": net.bytes_sent / (1024**2),
            "bytes_recv_mb": net.bytes_recv / (1024**2),
        }

    def describe(self) -> str:
        return "ネットワーク統計"

    def get_detailed(self) -> dict[str, Any]:
        """詳細なネットワーク情報を返す"""
        net = psutil.net_io_counters()
        return {
            "bytes_sent_mb": net.bytes_sent / (1024**2),
            "bytes_recv_mb": net.bytes_recv / (1024**2),
            "packets_sent": net.packets_sent,
            "packets_recv": net.packets_recv,
            "errin": net.errin,
            "errout": net.errout,
        }
