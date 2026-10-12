"""
OZARK — Company Repository

Provides async SQLAlchemy database operations for companies with filtering,
search, and relational eager loading.
"""

from typing import List, Optional, Sequence
import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.company import Company
from app.repositories.base import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    """Async repository for Company model."""

    model = Company

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_with_relations(self, company_id: uuid.UUID) -> Optional[Company]:
        """Fetch company along with financials, risk scores, and alerts."""
        stmt = (
            select(Company)
            .options(
                selectinload(Company.financials),
                selectinload(Company.risk_scores),
                selectinload(Company.alerts),
            )
            .where(Company.id == company_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_ticker(self, ticker: str) -> Optional[Company]:
        """Fetch company by ticker symbol (case-insensitive)."""
        stmt = (
            select(Company)
            .options(
                selectinload(Company.financials),
                selectinload(Company.risk_scores),
                selectinload(Company.alerts),
            )
            .where(func.upper(Company.ticker) == ticker.upper().strip())
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def search_and_filter(
        self,
        *,
        query: Optional[str] = None,
        industry: Optional[str] = None,
        state: Optional[str] = None,
        name: Optional[str] = None,
        sector: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Company]:
        """Query companies with multi-field search and filters."""
        stmt = (
            select(Company)
            .options(
                selectinload(Company.risk_scores),
            )
            .where(Company.is_active.is_(True))
        )

        if query:
            q_pattern = f"%{query.strip()}%"
            stmt = stmt.where(
                or_(
                    Company.name.ilike(q_pattern),
                    Company.ticker.ilike(q_pattern),
                    Company.industry.ilike(q_pattern),
                    Company.sector.ilike(q_pattern),
                    Company.state.ilike(q_pattern),
                    Company.city.ilike(q_pattern),
                )
            )

        if industry:
            stmt = stmt.where(func.lower(Company.industry) == industry.lower().strip())

        if state:
            stmt = stmt.where(func.lower(Company.state) == state.lower().strip())

        if name:
            name_pattern = f"%{name.strip()}%"
            stmt = stmt.where(
                or_(
                    Company.name.ilike(name_pattern),
                    Company.ticker.ilike(name_pattern),
                )
            )

        if sector:
            stmt = stmt.where(func.lower(Company.sector) == sector.lower().strip())

        stmt = stmt.order_by(Company.market_cap.desc().nullslast()).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()
