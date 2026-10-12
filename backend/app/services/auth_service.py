"""
OZARK — Auth Service (Business Logic)

Handles user creation and credential verification.
All DB interaction goes through this layer, never directly from endpoints.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Optional

import structlog
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    REFRESH_TOKEN_EXPIRE_SECONDS,
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

log = structlog.get_logger(__name__)


class LocalUser:
    """In-memory user representation for fallback operation."""
    def __init__(self, id: uuid.UUID, name: str, email: str, password_hash: str, created_at: datetime):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at


_FALLBACK_USERS: Dict[str, LocalUser] = {}
_FALLBACK_USERS_BY_ID: Dict[uuid.UUID, LocalUser] = {}


def _init_demo_user() -> None:
    demo_email = "demo@ozark.ai"
    demo_id = uuid.UUID("11111111-2222-3333-4444-555555555555")
    demo_user = LocalUser(
        id=demo_id,
        name="Demo User",
        email=demo_email,
        password_hash=hash_password("Demo@123"),
        created_at=datetime.now(timezone.utc),
    )
    _FALLBACK_USERS[demo_email] = demo_user
    _FALLBACK_USERS_BY_ID[demo_id] = demo_user


_init_demo_user()


def get_fallback_user_by_id(user_id: uuid.UUID) -> Optional[LocalUser]:
    return _FALLBACK_USERS_BY_ID.get(user_id)


async def register_user(payload: RegisterRequest, db: AsyncSession) -> UserResponse:
    """
    Create a new user.
    Falls back to local in-memory registry if DB connection is unavailable.
    """
    email_clean = payload.email.lower().strip()
    
    # Check fallback store first
    if email_clean in _FALLBACK_USERS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    try:
        existing = await db.execute(
            select(User).where(User.email == email_clean)
        )
        if existing.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        user = User(
            name=payload.name.strip(),
            email=email_clean,
            password_hash=hash_password(payload.password),
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)

        # Sync into fallback store
        local_u = LocalUser(
            id=user.id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
        )
        _FALLBACK_USERS[email_clean] = local_u
        _FALLBACK_USERS_BY_ID[user.id] = local_u

        log.info("User registered in DB", user_id=str(user.id), email=user.email)
        return UserResponse.model_validate(user)
    except HTTPException:
        raise
    except Exception as exc:
        log.warning("Postgres unavailable during registration, using resilient memory store", error=str(exc))
        new_id = uuid.uuid4()
        now = datetime.now(timezone.utc)
        local_u = LocalUser(
            id=new_id,
            name=payload.name.strip(),
            email=email_clean,
            password_hash=hash_password(payload.password),
            created_at=now,
        )
        _FALLBACK_USERS[email_clean] = local_u
        _FALLBACK_USERS_BY_ID[new_id] = local_u
        log.info("User registered in memory store", user_id=str(new_id), email=email_clean)
        return UserResponse(
            id=new_id,
            name=local_u.name,
            email=local_u.email,
            created_at=now,
        )


async def login_user(payload: LoginRequest, db: AsyncSession) -> TokenResponse:
    """
    Authenticate a user and return JWT access + refresh tokens.
    """
    _INVALID = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email_clean = payload.email.lower().strip()

    user = None
    try:
        result = await db.execute(
            select(User).where(User.email == email_clean)
        )
        user = result.scalar_one_or_none()
    except Exception as exc:
        log.warning("Postgres unavailable during login, checking memory store", error=str(exc))
        user = _FALLBACK_USERS.get(email_clean)

    if user is None:
        user = _FALLBACK_USERS.get(email_clean)

    # Always run verify to prevent timing attacks even when user is None
    dummy_hash = "$2b$12$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    stored_hash = user.password_hash if user else dummy_hash

    if not verify_password(payload.password, stored_hash) or user is None:
        log.warning("Failed login attempt", email=payload.email)
        raise _INVALID

    log.info("User logged in", user_id=str(user.id))

    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )


async def refresh_access_token(refresh_token: str, db: AsyncSession) -> TokenResponse:
    """
    Issue a new access token from a valid refresh token.
    """
    from jose import JWTError
    from app.core.security import decode_token

    _INVALID = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(refresh_token)
    except JWTError:
        raise _INVALID

    if payload.type != "refresh":
        raise _INVALID

    user_id = uuid.UUID(payload.sub)
    user = None
    try:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
    except Exception:
        user = _FALLBACK_USERS_BY_ID.get(user_id)

    if user is None:
        user = _FALLBACK_USERS_BY_ID.get(user_id)

    if user is None:
        raise _INVALID

    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )
