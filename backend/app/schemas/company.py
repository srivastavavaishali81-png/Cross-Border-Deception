"""
OZARK — Company Schemas (Pydantic v2)
"""

import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.company import ExchangeEnum
from app.models.risk_score import RiskLevel
from app.models.alert import AlertType, AlertSeverity


# ── Nested Sub-Schemas ────────────────────────────────────────────────────────

class RiskScoreSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    overall_score: float
    risk_level: RiskLevel
    recommendation: Optional[str] = None
    credit_risk: Optional[float] = None
    market_risk: Optional[float] = None
    operational_risk: Optional[float] = None
    liquidity_risk: Optional[float] = None
    esg_score: Optional[float] = None
    calculated_at: Optional[datetime] = None


class FinancialOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[uuid.UUID] = None
    fiscal_year: int
    fiscal_quarter: Optional[int] = None
    revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    ebitda: Optional[float] = None
    net_income: Optional[float] = None
    eps: Optional[float] = None
    total_assets: Optional[float] = None
    total_debt: Optional[float] = None
    cash_and_equivalents: Optional[float] = None
    operating_cash_flow: Optional[float] = None
    capex: Optional[float] = None
    pe_ratio: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    reported_at: Optional[date] = None


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[uuid.UUID] = None
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: Optional[str] = None
    description: Optional[str] = None
    is_read: bool = False
    is_resolved: bool = False
    created_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

    def model_post_init(self, __context: Any) -> None:
        if self.message is None and self.description is not None:
            self.message = self.description
        elif self.description is None and self.message is not None:
            self.description = self.message


# ── Company Schemas ───────────────────────────────────────────────────────────

class CompanyBase(BaseModel):
    name: str
    ticker: str
    sector: str
    industry: str
    country: str = "United States"
    state: Optional[str] = None
    city: Optional[str] = None
    exchange: ExchangeEnum = ExchangeEnum.NASDAQ
    market_cap: Optional[float] = None
    employees: Optional[int] = None
    founded_year: Optional[int] = None
    website: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    ticker: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    exchange: Optional[ExchangeEnum] = None
    market_cap: Optional[float] = None
    employees: Optional[int] = None
    founded_year: Optional[int] = None
    website: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CompanySummary(CompanyBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: Optional[datetime] = None
    latest_risk_score: Optional[RiskScoreSummary] = None


class CompanyDetail(CompanySummary):
    financials: List[FinancialOut] = Field(default_factory=list)
    risk_scores: List[RiskScoreSummary] = Field(default_factory=list)
    alerts: List[AlertOut] = Field(default_factory=list)
    key_stats: Optional[Dict[str, Any]] = None


# ── Paginated & Search Response Schemas ───────────────────────────────────────

class FilterOptions(BaseModel):
    industries: List[str] = Field(default_factory=list)
    states: List[str] = Field(default_factory=list)
    sectors: List[str] = Field(default_factory=list)
    exchanges: List[str] = Field(default_factory=list)
    risk_levels: List[str] = Field(default_factory=list)


class CompanyListResponse(BaseModel):
    items: List[CompanySummary]
    total: int
    page: int
    page_size: int
    total_pages: int
    facets: Optional[FilterOptions] = None


class CompanySearchResponse(CompanyListResponse):
    query: Optional[str] = None


class CompanyRiskResponse(BaseModel):
    company_id: str
    ticker: Optional[str] = None
    name: Optional[str] = None
    risk_score: float
    risk_level: RiskLevel
    recommendation: str
    formula_weights: Optional[Dict[str, float]] = None
    breakdown: Optional[Dict[str, Any]] = None
