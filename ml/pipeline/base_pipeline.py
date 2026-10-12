"""
OZARK ML Pipeline — Abstract Base Pipeline
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
import structlog

logger = structlog.get_logger(__name__)


class BasePipeline(ABC):
    """
    Abstract base for OZARK ML pipelines.

    Lifecycle:
      load_data → preprocess → train → evaluate → save
    """

    name: str = "base"

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.log = logger.bind(pipeline=self.name)
        self.model: Any = None

    @abstractmethod
    def load_data(self) -> Any:
        """Load raw data for the pipeline."""
        ...

    @abstractmethod
    def preprocess(self, data: Any) -> Any:
        """Clean and transform raw data."""
        ...

    @abstractmethod
    def train(self, data: Any) -> None:
        """Train the model."""
        ...

    @abstractmethod
    def evaluate(self, data: Any) -> dict[str, float]:
        """Return evaluation metrics."""
        ...

    def save(self, path: str | Path) -> None:
        """Persist the trained model to disk."""
        raise NotImplementedError("Implement save() for your pipeline.")

    def run(self) -> dict[str, float]:
        """Execute the full ML pipeline."""
        self.log.info("Pipeline starting")
        raw = self.load_data()
        data = self.preprocess(raw)
        self.train(data)
        metrics = self.evaluate(data)
        self.log.info("Pipeline complete", metrics=metrics)
        return metrics
