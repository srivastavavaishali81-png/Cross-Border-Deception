"""
OZARK Backend — Base Connector Architecture

Defines the abstract base class and normalized response schemas for external
data source connectors (SEBI, Moneycontrol, Zerodha, MCA, SMC).

All connectors adhere to the common interface:
- fetch_company(identifier: str) -> ConnectorCompany
- fetch_financials(identifier: str, years: int) -> ConnectorFinancials
- fetch_compliance(identifier: str) -> ConnectorCompliance
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ── Normalized Response Models ───────────────────────────────────────────────

class ConnectorCompany(BaseModel):
    """Normalized company profile returned across all external sources."""
    source: str = Field(..., description="Connector source name (e.g., MCA, Zerodha, SEBI)")
    identifier: str = Field(..., description="Queried identifier (CIN, ISIN, or Ticker)")
    cin: Optional[str] = None
    isin: Optional[str] = None
    ticker: Optional[str] = None
    name: str
    legal_name: Optional[str] = None
    status: str = "ACTIVE"  # ACTIVE, DORMANT, UNDER_LIQUIDATION, STRUCK_OFF
    incorporation_date: Optional[str] = None
    registered_state: Optional[str] = None
    registered_address: Optional[str] = None
    authorized_capital_inr: Optional[float] = None
    paid_up_capital_inr: Optional[float] = None
    industry: Optional[str] = None
    sector: Optional[str] = None
    directors_count: Optional[int] = None
    raw_response: Optional[Dict[str, Any]] = None
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


class FinancialYearRecord(BaseModel):
    """Financial statement snapshot for a single fiscal period."""
    fiscal_year: str
    revenue_inr_cr: float
    operating_profit_inr_cr: float
    net_profit_inr_cr: float
    total_assets_inr_cr: float
    total_debt_inr_cr: float
    net_worth_inr_cr: float
    operating_margin_pct: float
    debt_to_equity: float
    current_ratio: Optional[float] = None
    interest_coverage_ratio: Optional[float] = None


class ConnectorFinancials(BaseModel):
    """Normalized multi-year financial statements and metrics."""
    source: str
    identifier: str
    currency: str = "INR"
    unit: str = "Crores (10M INR)"
    statements: List[FinancialYearRecord] = Field(default_factory=list)
    key_ratios: Dict[str, float] = Field(default_factory=dict)
    credit_rating: Optional[str] = None
    credit_outlook: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


class ComplianceFiling(BaseModel):
    """Regulatory filing / disclosure item."""
    filing_type: str  # e.g., AOC-4, MGT-7, REG_30, SAST_DISCLOSURE
    filing_date: str
    status: str  # APPROVED, PENDING, DELAYED, REJECTED
    form_id: Optional[str] = None
    description: Optional[str] = None


class RegulatoryPenalty(BaseModel):
    """Penal action or adjudication order."""
    authority: str  # SEBI, MCA, ROC, RBI
    order_date: str
    section_violated: str
    penalty_amount_inr: float
    adjudication_status: str  # SETTLED, APPEALED, OPEN
    summary: str


class ConnectorCompliance(BaseModel):
    """Normalized compliance and regulatory risk data."""
    source: str
    identifier: str
    compliance_score: float = Field(..., ge=0.0, le=100.0, description="0 (Failing) to 100 (Pristine)")
    status: str = "COMPLIANT"  # COMPLIANT, DEFICIENT, SEVERE_BREACH
    filings: List[ComplianceFiling] = Field(default_factory=list)
    penalties: List[RegulatoryPenalty] = Field(default_factory=list)
    director_disqualifications_found: bool = False
    shell_company_signals_flagged: bool = False
    annual_general_meeting_date: Optional[str] = None
    balance_sheet_filing_status: str = "FILED"
    raw_response: Optional[Dict[str, Any]] = None
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


# ── Common Connector Abstract Base Class ──────────────────────────────────────

class BaseConnector(ABC):
    """
    Common Abstract Interface for OZARK Data Connectors.

    Provides standardized method contracts, configuration lifecycle,
    and mock/live switching architecture for enterprise data providers.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout_seconds: int = 30,
        use_mock: bool = True,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout_seconds = timeout_seconds
        self.use_mock = use_mock
        self._connected = False

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Identifier name of the connector source."""
        pass

    async def connect(self) -> None:
        """Initialize HTTP client session or connection pool for live APIs."""
        self._connected = True

    async def disconnect(self) -> None:
        """Close connection pools and cleanup resources."""
        self._connected = False

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
    async def fetch_company(self, identifier: str) -> ConnectorCompany:
        """
        Fetch company registration, identity, and governance profile.

        :param identifier: CIN, ISIN, or Stock Ticker symbol
        :return: Normalized ConnectorCompany model
        """
        pass

    @abstractmethod
    async def fetch_financials(self, identifier: str, years: int = 3) -> ConnectorFinancials:
        """
        Fetch normalized multi-year financial statements and metrics.

        :param identifier: CIN, ISIN, or Stock Ticker symbol
        :param years: Number of historical fiscal years to retrieve
        :return: Normalized ConnectorFinancials model
        """
        pass

    @abstractmethod
    async def fetch_compliance(self, identifier: str) -> ConnectorCompliance:
        """
        Fetch regulatory filings, MCA/SEBI compliance status, and penalties.

        :param identifier: CIN, ISIN, or Stock Ticker symbol
        :return: Normalized ConnectorCompliance model
        """
        pass
