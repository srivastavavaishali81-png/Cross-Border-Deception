"""
OZARK — FastAPI Auth Dependencies

Provides get_current_user dependency to protect any route.
"""

import uuid

import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.postgres import get_db
from app.models.user import User

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from app.services.auth_service import LocalUser

log = structlog.get_logger(__name__)

_bearer = HTTPBearer(auto_error=False)

_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Validate Bearer JWT and return the authenticated User.

    Usage:
        @router.get("/me")
        async def me(user: User = Depends(get_current_user)):
            ...
    """
    if credentials is None:
        raise _CREDENTIALS_EXCEPTION

    try:
        payload = decode_token(credentials.credentials)
    except JWTError as exc:
        log.warning("JWT decode failed", error=str(exc))
        raise _CREDENTIALS_EXCEPTION from exc

    if payload.type != "access":
        raise _CREDENTIALS_EXCEPTION

    user_id = uuid.UUID(payload.sub)
    user: User | LocalUser | None = None
    try:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
    except Exception as exc:
        log.warning("DB query failed in get_current_user, checking fallback store", error=str(exc))
        from app.services.auth_service import get_fallback_user_by_id
        user = get_fallback_user_by_id(user_id)

    if user is None:
        from app.services.auth_service import get_fallback_user_by_id
        user = get_fallback_user_by_id(user_id)

    if user is None:
        raise _CREDENTIALS_EXCEPTION

    return cast(User, user)
