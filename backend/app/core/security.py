"""
OZARK — Core Security: Password Hashing + JWT

Uses:
  - passlib[bcrypt] for password hashing (bcrypt cost factor 12)
  - python-jose for JWT encoding / decoding
"""

import time
import uuid
from typing import Literal

from jose import JWTError, jwt
import bcrypt

from app.core.config import settings
from app.schemas.auth import TokenPayload

# ── Password Hashing ───────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    """Return a bcrypt hash of the plain-text password."""
    pwd_bytes = plain.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Constant-time comparison of plain password against its hash."""
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


# ── JWT ────────────────────────────────────────────────────────────────────────

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 30          # 30 minutes
REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 days


def _create_token(
    subject: str | uuid.UUID,
    token_type: Literal["access", "refresh"],
    expires_in: int,
) -> str:
    now = int(time.time())
    payload = {
        "sub": str(subject),
        "type": token_type,
        "iat": now,
        "exp": now + expires_in,
        "jti": str(uuid.uuid4()),  # unique token ID (enables revocation later)
    }
    return jwt.encode(payload, settings.APP_SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: str | uuid.UUID) -> str:
    return _create_token(user_id, "access", ACCESS_TOKEN_EXPIRE_SECONDS)


def create_refresh_token(user_id: str | uuid.UUID) -> str:
    return _create_token(user_id, "refresh", REFRESH_TOKEN_EXPIRE_SECONDS)


def decode_token(token: str) -> TokenPayload:
    """
    Decode and validate a JWT.

    Raises:
        jose.JWTError — on any verification failure (expired, bad sig, etc.)
    """
    payload = jwt.decode(token, settings.APP_SECRET_KEY, algorithms=[ALGORITHM])
    return TokenPayload(**payload)
