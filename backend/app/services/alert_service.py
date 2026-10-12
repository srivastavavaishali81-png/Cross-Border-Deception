"""
OZARK — Alert Service (Business Logic)

Handles CRUD and notification/resolution operations for alerts.
"""

from datetime import datetime, timezone
from typing import List, Optional
import uuid

import structlog
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import Alert, AlertSeverity, AlertType
from app.repositories.alert_repository import AlertRepository
from app.repositories.company_repository import CompanyRepository
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate

log = structlog.get_logger(__name__)


class AlertService:
    """Service layer for alert management."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = AlertRepository(db)
        self.company_repo = CompanyRepository(db)

    async def get_by_id(self, alert_id: uuid.UUID) -> AlertResponse:
        record = await self.repo.get_with_relations(alert_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alert {alert_id} not found.",
            )
        return AlertResponse.model_validate(record)

    async def get_by_company(
        self,
        company_id: uuid.UUID,
        skip: int = 0,
        limit: int = 50,
    ) -> List[AlertResponse]:
        if not await self.company_repo.exists(company_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company {company_id} not found.",
            )
        records = await self.repo.get_by_company(company_id, skip=skip, limit=limit)
        return [AlertResponse.model_validate(r) for r in records]

    async def get_by_user(
        self,
        user_id: uuid.UUID,
        unread_only: bool = False,
        skip: int = 0,
        limit: int = 50,
    ) -> List[AlertResponse]:
        records = await self.repo.get_by_user(user_id, unread_only=unread_only, skip=skip, limit=limit)
        return [AlertResponse.model_validate(r) for r in records]

    async def get_unresolved(
        self,
        severity: Optional[AlertSeverity] = None,
        alert_type: Optional[AlertType] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[AlertResponse]:
        records = await self.repo.get_unresolved(
            severity=severity, alert_type=alert_type, skip=skip, limit=limit
        )
        return [AlertResponse.model_validate(r) for r in records]

    async def create(self, payload: AlertCreate) -> AlertResponse:
        if not await self.company_repo.exists(payload.company_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company {payload.company_id} not found.",
            )

        data = payload.model_dump()
        metadata_val = data.pop("metadata", None)

        record = Alert(
            alert_metadata=metadata_val,
            **data,
        )
        created = await self.repo.create(record)
        log.info("Alert created", id=str(created.id), type=created.alert_type, severity=created.severity)
        return AlertResponse.model_validate(created)

    async def update(self, alert_id: uuid.UUID, payload: AlertUpdate) -> AlertResponse:
        record = await self.repo.get(alert_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alert {alert_id} not found.",
            )

        data = payload.model_dump(exclude_unset=True)
        if data.get("is_resolved") and not record.is_resolved:
            data["resolved_at"] = datetime.now(timezone.utc)

        updated = await self.repo.update(record, data)
        log.info("Alert updated", id=str(alert_id))
        return AlertResponse.model_validate(updated)

    async def mark_read(self, alert_id: uuid.UUID) -> None:
        success = await self.repo.mark_as_read(alert_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alert {alert_id} not found.",
            )

    async def mark_all_read_for_user(self, user_id: uuid.UUID) -> int:
        return await self.repo.mark_all_as_read_for_user(user_id)

    async def delete(self, alert_id: uuid.UUID) -> None:
        record = await self.repo.get(alert_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alert {alert_id} not found.",
            )
        await self.repo.delete(record)
        log.info("Alert deleted", id=str(alert_id))
