"""
OZARK — User Repository

Provides async SQLAlchemy database operations for User model.
"""

from typing import Optional, Sequence
import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Async repository for User records."""

    model = User

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Fetch user by email (case-insensitive)."""
        stmt = select(User).where(func.lower(User.email) == email.lower().strip())
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_with_alerts(self, user_id: uuid.UUID) -> Optional[User]:
        """Fetch user with associated alerts eager loaded."""
        stmt = (
            select(User)
            .options(selectinload(User.alerts))
            .where(User.id == user_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        """Check if an email already exists."""
        stmt = select(func.count()).select_from(User).where(
            func.lower(User.email) == email.lower().strip()
        )
        result = await self._session.execute(stmt)
        return (result.scalar_one() or 0) > 0
