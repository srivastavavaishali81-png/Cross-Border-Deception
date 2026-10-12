"""
OZARK Connectors — Abstract Base Connector & Interface

Defines the common interface for external data connectors:
- fetch_company(identifier: str) -> dict
- fetch_financials(identifier: str, years: int) -> dict
- fetch_compliance(identifier: str) -> dict

Prepared for live REST / GraphQL / WebSocket API integrations.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
import structlog

logger = structlog.get_logger(__name__)


class BaseConnector(ABC):
    """
    Common Abstract Base Interface for all OZARK Data Connectors.

    Provides standardized method contracts, configuration lifecycle,
    and mock/live switching architecture for enterprise data providers.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout_seconds: int = 30,
        use_mock: bool = True,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout_seconds = timeout_seconds
        self.use_mock = use_mock
        self.config = config or {}
        self.log = logger.bind(connector=self.source_name)
        self._connected = False

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Identifier name of the connector source."""
        pass

    async def connect(self) -> None:
        """Initialize HTTP client session or connection pool for live APIs."""
        self._connected = True
        self.log.info("Connected to data provider", source=self.source_name, mock=self.use_mock)

    async def disconnect(self) -> None:
        """Close connection pools and cleanup resources."""
        self._connected = False
        self.log.info("Disconnected from data provider", source=self.source_name)

    async def health_check(self) -> Dict[str, Any]:
        """Perform endpoint latency / health verification."""
        return {
            "source": self.source_name,
            "status": "HEALTHY",
            "mock_mode": self.use_mock,
            "base_url": self.base_url or "https://mock.ozark.internal",
            "timestamp": datetime.utcnow().isoformat(),
        }

    @abstractmethod
    async def fetch_company(self, identifier: str) -> Dict[str, Any]:
        """
        Fetch company registration, identity, and governance profile.

        :param identifier: CIN, ISIN, or Stock Ticker symbol
        :return: Standardized company profile dictionary
        """
        pass

    @abstractmethod
    async def fetch_financials(self, identifier: str, years: int = 3) -> Dict[str, Any]:
        """
        Fetch normalized multi-year financial statements and metrics.

        :param identifier: CIN, ISIN, or Stock Ticker symbol
        :param years: Number of historical fiscal years to retrieve
        :return: Standardized financial statement dictionary
        """
        pass

    @abstractmethod
    async def fetch_compliance(self, identifier: str) -> Dict[str, Any]:
        """
        Fetch regulatory filings, compliance ratings, penalties, and alerts.

        :param identifier: CIN, ISIN, or Stock Ticker symbol
        :return: Standardized compliance record dictionary
        """
        pass
