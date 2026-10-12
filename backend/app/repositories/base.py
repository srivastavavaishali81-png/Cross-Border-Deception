"""
OZARK — Generic Async Repository Base

Provides type-safe CRUD operations over any SQLAlchemy model.
Concrete repositories inherit from this and add domain-specific queries.
"""

from typing import Any, Generic, Sequence, Type, TypeVar
import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """
    Generic async repository.

    Usage:
        class CompanyRepository(BaseRepository[Company]):
            model = Company
    """

    model: Type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ── Read ──────────────────────────────────────────────────────────────────

    async def get(self, id: uuid.UUID) -> ModelT | None:
        """Fetch a single record by primary key."""
        result = await self._session.execute(
            select(self.model).where(self.model.id == id)  # type: ignore[attr-defined]
        )
        return result.scalar_one_or_none()

    async def get_or_raise(self, id: uuid.UUID) -> ModelT:
        """Fetch by PK or raise ValueError."""
        obj = await self.get(id)
        if obj is None:
            raise ValueError(f"{self.model.__name__} {id} not found.")
        return obj

    async def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelT]:
        """Return paginated records."""
        result = await self._session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def count(self) -> int:
        """Return total number of records."""
        result = await self._session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar_one()

    async def exists(self, id: uuid.UUID) -> bool:
        result = await self._session.execute(
            select(func.count()).select_from(self.model).where(
                self.model.id == id  # type: ignore[attr-defined]
            )
        )
        return result.scalar_one() > 0

    # ── Write ─────────────────────────────────────────────────────────────────

    async def create(self, obj: ModelT) -> ModelT:
        """Persist a new model instance and return it with DB-generated values."""
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def update(self, obj: ModelT, data: dict[str, Any]) -> ModelT:
        """Apply a dict of field updates to an existing model instance."""
        for field, value in data.items():
            setattr(obj, field, value)
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def delete(self, obj: ModelT) -> None:
        """Delete a model instance."""
        await self._session.delete(obj)
        await self._session.flush()

    async def bulk_create(self, objs: list[ModelT]) -> list[ModelT]:
        """Persist multiple instances in a single flush."""
        self._session.add_all(objs)
        await self._session.flush()
        for obj in objs:
            await self._session.refresh(obj)
        return objs
