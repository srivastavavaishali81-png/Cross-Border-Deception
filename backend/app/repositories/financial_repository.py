"""
OZARK — Financial Repository

Provides async SQLAlchemy database operations for Financial model.
"""

from typing import Optional, Sequence
import uuid

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.financial import Financial
from app.repositories.base import BaseRepository


class FinancialRepository(BaseRepository[Financial]):
    """Async repository for Financial records."""

    model = Financial

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_company(
        self,
        company_id: uuid.UUID,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[Financial]:
        """Fetch all financial records for a given company, sorted by year/quarter descending."""
        stmt = (
            select(Financial)
            .where(Financial.company_id == company_id)
            .order_by(
                desc(Financial.fiscal_year),
                desc(Financial.fiscal_quarter).nullslast(),
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_company_and_period(
        self,
        company_id: uuid.UUID,
        fiscal_year: int,
        fiscal_quarter: Optional[int] = None,
    ) -> Optional[Financial]:
        """Fetch a specific financial report for a company and year/quarter."""
        stmt = select(Financial).where(
            Financial.company_id == company_id,
            Financial.fiscal_year == fiscal_year,
            Financial.fiscal_quarter == fiscal_quarter,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_latest_by_company(
        self,
        company_id: uuid.UUID,
    ) -> Optional[Financial]:
        """Fetch the most recent financial statement for a company."""
        stmt = (
            select(Financial)
            .where(Financial.company_id == company_id)
            .order_by(
                desc(Financial.fiscal_year),
                desc(Financial.fiscal_quarter).nullslast(),
            )
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
