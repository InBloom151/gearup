from __future__ import annotations

from app.api.v1.schemas.user import UserCreate, UserOut
from app.core import security
from app.core.config import settings
from app.repositories.user import UserRepository
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    # ────── registration ──────────────────────────────────────────
    async def register(self, data: UserCreate) -> UserOut:
        if await self.repo.get_user_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        data.password = security.hash_password(data.password)
        user = await self.repo.create_user(data)
        return user

    # ────── login / refresh helpers ───────────────────────────────
    async def login(self, email: str, password: str) -> tuple[str, str]:
        user = await self.repo.get_user_by_email(email)
        if not user or not security.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        return self._issue_tokens(email)

    async def refresh(self, refresh_token: str | None) -> tuple[str, str]:
        payload = security._jwt_decode(refresh_token or "")
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        email: str | None = payload.get("sub")
        if not email or not await self.repo.get_user_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return self._issue_tokens(email)

    # ────── internal ──────────────────────────────────────────────
    def _issue_tokens(self, email: str) -> tuple[str, str]:
        access = security.create_jwt(
            sub=email, token_type="access", ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh = security.create_jwt(
            sub=email, token_type="refresh", ttl=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        return access, refresh
