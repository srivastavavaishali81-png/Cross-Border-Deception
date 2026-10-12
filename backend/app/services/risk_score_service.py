"""
OZARK — Risk Score Service (Business Logic)

Handles CRUD and computation queries for ML risk scores.
"""

from typing import List, Optional
import uuid

import structlog
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.risk_score import RiskLevel, RiskScore
from app.repositories.company_repository import CompanyRepository
from app.repositories.risk_score_repository import RiskScoreRepository
from app.schemas.risk_score import RiskScoreCreate, RiskScoreResponse

log = structlog.get_logger(__name__)


class RiskScoreService:
    """Service layer for risk scores."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = RiskScoreRepository(db)
        self.company_repo = CompanyRepository(db)

    async def get_by_id(self, risk_score_id: uuid.UUID) -> RiskScoreResponse:
        record = await self.repo.get(risk_score_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Risk score {risk_score_id} not found.",
            )
        return RiskScoreResponse.model_validate(record)

    async def get_latest_by_company(self, company_id: uuid.UUID) -> RiskScoreResponse:
        if not await self.company_repo.exists(company_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company {company_id} not found.",
            )
        record = await self.repo.get_latest_by_company(company_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No risk scores calculated for company {company_id}.",
            )
        return RiskScoreResponse.model_validate(record)

    async def get_history_by_company(
        self,
        company_id: uuid.UUID,
        skip: int = 0,
        limit: int = 50,
    ) -> List[RiskScoreResponse]:
        if not await self.company_repo.exists(company_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company {company_id} not found.",
            )
        records = await self.repo.get_history_by_company(company_id, skip=skip, limit=limit)
        return [RiskScoreResponse.model_validate(r) for r in records]

    async def create(self, payload: RiskScoreCreate) -> RiskScoreResponse:
        if not await self.company_repo.exists(payload.company_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company {payload.company_id} not found.",
            )

        record = RiskScore(**payload.model_dump())
        created = await self.repo.create(record)
        log.info("Risk score created", id=str(created.id), company_id=str(created.company_id), score=created.overall_score)
        return RiskScoreResponse.model_validate(created)

    async def get_high_risk_companies(
        self,
        min_score: float = 75.0,
        skip: int = 0,
        limit: int = 50,
    ) -> List[RiskScoreResponse]:
        records = await self.repo.get_high_risk_scores(min_score=min_score, skip=skip, limit=limit)
        return [RiskScoreResponse.model_validate(r) for r in records]
