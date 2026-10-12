"""
OZARK — Alert Repository

Provides async SQLAlchemy database operations for Alert model.
"""

from typing import Optional, Sequence
import uuid

from sqlalchemy import desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.alert import Alert, AlertSeverity, AlertType
from app.repositories.base import BaseRepository


class AlertRepository(BaseRepository[Alert]):
    """Async repository for Alert records."""

    model = Alert

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_with_relations(self, alert_id: uuid.UUID) -> Optional[Alert]:
        """Fetch alert with company and user relations eager loaded."""
        stmt = (
            select(Alert)
            .options(
                selectinload(Alert.company),
                selectinload(Alert.user),
            )
            .where(Alert.id == alert_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_company(
        self,
        company_id: uuid.UUID,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[Alert]:
        """Fetch alerts for a specific company."""
        stmt = (
            select(Alert)
            .where(Alert.company_id == company_id)
            .order_by(desc(Alert.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_user(
        self,
        user_id: uuid.UUID,
        *,
        unread_only: bool = False,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[Alert]:
        """Fetch alerts assigned to or relevant to a specific user."""
        stmt = (
            select(Alert)
            .options(selectinload(Alert.company))
            .where(
                (Alert.user_id == user_id) | (Alert.user_id.is_(None))
            )
        )
        if unread_only:
            stmt = stmt.where(Alert.is_read.is_(False))

        stmt = stmt.order_by(desc(Alert.created_at)).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_unresolved(
        self,
        *,
        severity: Optional[AlertSeverity] = None,
        alert_type: Optional[AlertType] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[Alert]:
        """Fetch open/unresolved alerts with optional filtering."""
        stmt = (
            select(Alert)
            .options(selectinload(Alert.company))
            .where(Alert.is_resolved.is_(False))
        )
        if severity:
            stmt = stmt.where(Alert.severity == severity)
        if alert_type:
            stmt = stmt.where(Alert.alert_type == alert_type)

        stmt = stmt.order_by(desc(Alert.created_at)).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def mark_as_read(self, alert_id: uuid.UUID) -> bool:
        """Mark an alert as read."""
        stmt = (
            update(Alert)
            .where(Alert.id == alert_id)
            .values(is_read=True)
        )
        result = await self._session.execute(stmt)
        await self._session.flush()
        return result.rowcount > 0

    async def mark_all_as_read_for_user(self, user_id: uuid.UUID) -> int:
        """Mark all unread alerts for a user as read."""
        stmt = (
            update(Alert)
            .where(
                ((Alert.user_id == user_id) | (Alert.user_id.is_(None)))
                & (Alert.is_read.is_(False))
            )
            .values(is_read=True)
        )
        result = await self._session.execute(stmt)
        await self._session.flush()
        return result.rowcount
