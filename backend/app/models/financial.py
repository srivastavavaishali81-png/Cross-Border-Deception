"""
OZARK — Financial SQLAlchemy Model

Stores quarterly / annual financials per company.
All monetary values are in millions USD.
"""

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgres import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.company import Company


class Financial(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "financials"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "fiscal_year", "fiscal_quarter",
            name="uq_financials_company_period"
        ),
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    # NULL = annual report; 1-4 = quarterly
    fiscal_quarter: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # ── Income statement ──────────────────────────────────────────────────────
    revenue: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    gross_profit: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    ebitda: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    net_income: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    eps: Mapped[Optional[float]] = mapped_column(Numeric(10, 4), nullable=True)

    # ── Balance sheet ─────────────────────────────────────────────────────────
    total_assets: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    total_debt: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    cash_and_equivalents: Mapped[Optional[float]] = mapped_column(
        Numeric(20, 2), nullable=True
    )

    # ── Cash flow ─────────────────────────────────────────────────────────────
    operating_cash_flow: Mapped[Optional[float]] = mapped_column(
        Numeric(20, 2), nullable=True
    )
    capex: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)

    # ── Ratios ────────────────────────────────────────────────────────────────
    pe_ratio: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    debt_to_equity: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 4), nullable=True
    )
    current_ratio: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 4), nullable=True
    )

    reported_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relationship
    company: Mapped["Company"] = relationship("Company", back_populates="financials")

    def __repr__(self) -> str:
        period = (
            f"Q{self.fiscal_quarter}" if self.fiscal_quarter else "Annual"
        )
        return f"<Financial company={self.company_id} {self.fiscal_year}-{period}>"
