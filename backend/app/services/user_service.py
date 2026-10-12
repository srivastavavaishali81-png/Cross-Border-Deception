"""
OZARK — User Service (Business Logic)

Handles CRUD operations for user profiles.
"""

from typing import List, Optional
import uuid

import structlog
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, UserResponse

log = structlog.get_logger(__name__)


class UserService:
    """Service layer for user management."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = UserRepository(db)

    async def get_by_id(self, user_id: uuid.UUID) -> UserResponse:
        user = await self.repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found.",
            )
        return UserResponse.model_validate(user)

    async def get_by_email(self, email: str) -> Optional[UserResponse]:
        user = await self.repo.get_by_email(email)
        if not user:
            return None
        return UserResponse.model_validate(user)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = await self.repo.get_all(skip=skip, limit=limit)
        return [UserResponse.model_validate(u) for u in users]

    async def create_user(self, payload: RegisterRequest) -> UserResponse:
        if await self.repo.email_exists(payload.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        user = User(
            name=payload.name.strip(),
            email=payload.email.lower().strip(),
            password_hash=hash_password(payload.password),
        )
        created = await self.repo.create(user)
        log.info("User created via UserService", id=str(created.id), email=created.email)
        return UserResponse.model_validate(created)

    async def delete_user(self, user_id: uuid.UUID) -> None:
        user = await self.repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found.",
            )
        await self.repo.delete(user)
        log.info("User deleted", id=str(user_id))
