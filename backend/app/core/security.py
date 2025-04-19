from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt, JWTError
from passlib.context import CryptContext
import uuid

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ───────── password ──────────────────────────────────────────────────
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ───────── jwt ───────────────────────────────────────────────────────
def _jwt_encode(payload: dict[str, Any]) -> str:
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def _jwt_decode(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None

def create_jwt(
    *,
    sub: str,
    token_type: str,
    ttl: int,
) -> str:
    now = datetime.now(timezone.utc)

    return _jwt_encode(
        {
            "sub": sub,
            "type": token_type,
            "iat": now,
            "exp": now + timedelta(minutes=ttl),
            "jti": str(uuid.uuid4()),
        }
    )