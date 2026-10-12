"""
OZARK — Company SQLAlchemy Model
"""

import enum
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Enum, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgres import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.financial import Financial
    from app.models.risk_score import RiskScore
    from app.models.alert import Alert


class ExchangeEnum(str, enum.Enum):
    NYSE = "NYSE"
    NASDAQ = "NASDAQ"
    LSE = "LSE"
    TSX = "TSX"
    ASX = "ASX"
    HKEX = "HKEX"
    OTHER = "OTHER"


class Company(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    ticker: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False, index=True
    )
    sector: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    industry: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    exchange: Mapped[ExchangeEnum] = mapped_column(
        Enum(ExchangeEnum, name="exchange_enum"), nullable=False
    )
    market_cap: Mapped[Optional[float]] = mapped_column(
        Numeric(20, 2), nullable=True, comment="Market cap in millions USD"
    )
    employees: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    founded_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    financials: Mapped[List["Financial"]] = relationship(
        "Financial", back_populates="company", cascade="all, delete-orphan"
    )
    risk_scores: Mapped[List["RiskScore"]] = relationship(
        "RiskScore", back_populates="company", cascade="all, delete-orphan"
    )
    alerts: Mapped[List["Alert"]] = relationship(
        "Alert", back_populates="company", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Company ticker={self.ticker} name={self.name}>"
