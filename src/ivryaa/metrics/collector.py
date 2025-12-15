"""メトリクス収集の基底クラス"""

from abc import ABC, abstractmethod
from typing import Any


class MetricsCollector(ABC):
    """メトリクスコレクターの基底クラス"""

    @abstractmethod
    def collect(self) -> Any:
        """メトリクスを収集して返す"""
        pass

    @abstractmethod
    def describe(self) -> str:
        """このコレクターの説明を返す"""
        pass
