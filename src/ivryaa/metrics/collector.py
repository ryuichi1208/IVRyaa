"""Base class for metrics collection"""

from abc import ABC, abstractmethod
from typing import Any


class MetricsCollector(ABC):
    """Base class for metrics collectors"""

    @abstractmethod
    def collect(self) -> Any:
        """Collect and return metrics"""
        pass

    @abstractmethod
    def describe(self) -> str:
        """Return description of this collector"""
        pass
