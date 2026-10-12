"""
OZARK — RiskScore SQLAlchemy Model

ML-computed risk scores per company, versioned by model run.
All scores are 0–100 (higher = riskier).
"""

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgres import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.company import Company


class RiskLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @classmethod
    def from_score(cls, score: float) -> "RiskLevel":
        if score < 25:
            return cls.LOW
        if score < 50:
            return cls.MEDIUM
        if score < 75:
            return cls.HIGH
        return cls.CRITICAL


class RiskScore(UUIDMixin, Base):
    __tablename__ = "risk_scores"

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Composite score ────────────────────────────────────────────────────────
    overall_score: Mapped[float] = mapped_column(
        Numeric(5, 2), nullable=False, comment="0-100"
    )
    risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(RiskLevel, name="risk_level_enum"), nullable=False, index=True
    )

    # ── Sub-scores ────────────────────────────────────────────────────────────
    credit_risk: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    market_risk: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    operational_risk: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    liquidity_risk: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    esg_score: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), nullable=True, comment="ESG score (higher = better ESG)"
    )

    # ── Metadata ──────────────────────────────────────────────────────────────
    model_version: Mapped[str] = mapped_column(
        String(50), nullable=False, default="v1.0.0"
    )
    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationship
    company: Mapped["Company"] = relationship("Company", back_populates="risk_scores")

    def __repr__(self) -> str:
        return (
            f"<RiskScore company={self.company_id} "
            f"score={self.overall_score} level={self.risk_level}>"
        )
