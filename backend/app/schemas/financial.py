"""
OZARK — Financial Schemas (Pydantic v2)
"""

import uuid
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class FinancialBase(BaseModel):
    company_id: uuid.UUID
    fiscal_year: int
    fiscal_quarter: Optional[int] = Field(default=None, ge=1, le=4)
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


class FinancialCreate(FinancialBase):
    pass


class FinancialUpdate(BaseModel):
    fiscal_year: Optional[int] = None
    fiscal_quarter: Optional[int] = Field(default=None, ge=1, le=4)
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


class FinancialResponse(FinancialBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
