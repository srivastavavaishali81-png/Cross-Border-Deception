"""
OZARK — Risk Score Schemas (Pydantic v2)
"""

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.risk_score import RiskLevel


class RiskScoreBase(BaseModel):
    company_id: uuid.UUID
    overall_score: float = Field(..., ge=0, le=100)
    risk_level: RiskLevel
    credit_risk: Optional[float] = Field(default=None, ge=0, le=100)
    market_risk: Optional[float] = Field(default=None, ge=0, le=100)
    operational_risk: Optional[float] = Field(default=None, ge=0, le=100)
    liquidity_risk: Optional[float] = Field(default=None, ge=0, le=100)
    esg_score: Optional[float] = Field(default=None, ge=0, le=100)
    model_version: str = "v1.0.0"


class RiskScoreCreate(RiskScoreBase):
    pass


class RiskScoreResponse(RiskScoreBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    calculated_at: datetime
    created_at: datetime
