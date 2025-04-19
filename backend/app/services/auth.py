from __future__ import annotations

from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.user import UserRepository
from app.core import security
from app.core.config import settings
from app.api.v1.schemas import UserCreate, UserOut, TokenPair

class AuthService:

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    # ────── registration ──────────────────────────────────────────
    async def register(self, data: UserCreate) -> UserOut:
        if await self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        data.password = security.hash_password(data.password)
        user = await self.repo.create(data)
        return UserOut.model_validate(user, from_attributes=True)

    # ────── login ─────────────────────────────────────────────────
    async def login(self, email: str, password: str) -> TokenPair:
        user = await self.repo.get_by_email(email)
        if not user or not security.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        return self._issue_tokens(user.email)

    # ────── refresh ───────────────────────────────────────────────
    async def refresh(self, refresh_token: str) -> TokenPair:
        payload = security._jwt_decode(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid refresh token",
            )

        email = payload.get("sub")
        if not email or not await self.repo.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return self._issue_tokens(email)

    # ────── helpers ───────────────────────────────────────────────
    def _issue_tokens(self, email: str) -> TokenPair:
        access = security.create_jwt(
            sub=email,
            token_type="access",
            ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        refresh = security.create_jwt(
            sub=email,
            token_type="refresh",
            ttl=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )

        return TokenPair(
            access_token=access,
            refresh_token=refresh,
            token_type="bearer",
        )
