"""
OZARK — Financial Service (Business Logic)

Handles CRUD and metric computations for company financials.
"""

from typing import List, Optional, Sequence
import uuid

import structlog
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.financial import Financial
from app.repositories.company_repository import CompanyRepository
from app.repositories.financial_repository import FinancialRepository
from app.schemas.financial import FinancialCreate, FinancialResponse, FinancialUpdate

log = structlog.get_logger(__name__)


class FinancialService:
    """Service layer for financial records."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = FinancialRepository(db)
        self.company_repo = CompanyRepository(db)

    async def get_by_id(self, financial_id: uuid.UUID) -> FinancialResponse:
        record = await self.repo.get(financial_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Financial record {financial_id} not found.",
            )
        return FinancialResponse.model_validate(record)

    async def get_by_company(
        self,
        company_id: uuid.UUID,
        skip: int = 0,
        limit: int = 50,
    ) -> List[FinancialResponse]:
        # Validate company exists
        if not await self.company_repo.exists(company_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company {company_id} not found.",
            )
        records = await self.repo.get_by_company(company_id, skip=skip, limit=limit)
        return [FinancialResponse.model_validate(r) for r in records]

    async def create(self, payload: FinancialCreate) -> FinancialResponse:
        if not await self.company_repo.exists(payload.company_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company {payload.company_id} not found.",
            )

        existing = await self.repo.get_by_company_and_period(
            payload.company_id, payload.fiscal_year, payload.fiscal_quarter
        )
        if existing:
            period_str = f"Q{payload.fiscal_quarter}" if payload.fiscal_quarter else "Annual"
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Financial record already exists for {payload.fiscal_year} {period_str}.",
            )

        record = Financial(**payload.model_dump())
        created = await self.repo.create(record)
        log.info("Financial record created", id=str(created.id), company_id=str(created.company_id))
        return FinancialResponse.model_validate(created)

    async def update(
        self, financial_id: uuid.UUID, payload: FinancialUpdate
    ) -> FinancialResponse:
        record = await self.repo.get(financial_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Financial record {financial_id} not found.",
            )

        update_data = payload.model_dump(exclude_unset=True)
        updated = await self.repo.update(record, update_data)
        log.info("Financial record updated", id=str(financial_id))
        return FinancialResponse.model_validate(updated)

    async def delete(self, financial_id: uuid.UUID) -> None:
        record = await self.repo.get(financial_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Financial record {financial_id} not found.",
            )
        await self.repo.delete(record)
        log.info("Financial record deleted", id=str(financial_id))
