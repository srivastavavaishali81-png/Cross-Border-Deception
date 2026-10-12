"""
OZARK — Risk Score Repository

Provides async SQLAlchemy database operations for RiskScore model.
"""

from typing import List, Optional, Sequence
import uuid

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.risk_score import RiskLevel, RiskScore
from app.repositories.base import BaseRepository


class RiskScoreRepository(BaseRepository[RiskScore]):
    """Async repository for RiskScore records."""

    model = RiskScore

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_latest_by_company(
        self,
        company_id: uuid.UUID,
    ) -> Optional[RiskScore]:
        """Fetch the most recent risk score calculation for a company."""
        stmt = (
            select(RiskScore)
            .where(RiskScore.company_id == company_id)
            .order_by(desc(RiskScore.calculated_at))
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_history_by_company(
        self,
        company_id: uuid.UUID,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[RiskScore]:
        """Fetch historical risk scores for a company, newest first."""
        stmt = (
            select(RiskScore)
            .where(RiskScore.company_id == company_id)
            .order_by(desc(RiskScore.calculated_at))
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_risk_level(
        self,
        risk_level: RiskLevel,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[RiskScore]:
        """Fetch risk scores by severity level with company relations loaded."""
        stmt = (
            select(RiskScore)
            .options(selectinload(RiskScore.company))
            .where(RiskScore.risk_level == risk_level)
            .order_by(desc(RiskScore.overall_score))
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_high_risk_scores(
        self,
        min_score: float = 75.0,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[RiskScore]:
        """Fetch all risk scores above a specific threshold."""
        stmt = (
            select(RiskScore)
            .options(selectinload(RiskScore.company))
            .where(RiskScore.overall_score >= min_score)
            .order_by(desc(RiskScore.overall_score))
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
