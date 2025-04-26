from __future__ import annotations

from datetime import timedelta

from app.api.v1.schemas.token import AccessToken
from app.api.v1.schemas.user import UserCreate, UserOut
from app.core.config import settings
from app.db.session import get_session
from app.services.auth import AuthService
from fastapi import APIRouter, Body, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])


def _svc(db: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(db)


# ───────────────────── register ───────────────────────
@router.post("/register", response_model=UserOut, status_code=201)
async def register(user_in: UserCreate, svc: AuthService = Depends(_svc)):
    return await svc.register(user_in)


# ───────────────────── login ──────────────────────────
@router.post("/login", response_model=AccessToken)
async def login(
    response: Response,
    email: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    svc: AuthService = Depends(_svc),
):
    access, refresh = await svc.login(email, password)

    response.set_cookie(
        "refresh_token",
        refresh,
        max_age=int(
            timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES).total_seconds()
        ),
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )
    return AccessToken(access_token=access)


# ───────────────────── logout ──────────────────────────
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token", path="/")
    response.delete_cookie("refresh_token", path="/api/v1/auth")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ───────────────────── refresh ────────────────────────
@router.post("/refresh", response_model=AccessToken)
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(None, alias="refresh_token"),
    svc: AuthService = Depends(_svc),
):
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token",
        )

    access, new_refresh = await svc.refresh(refresh_token)

    response.set_cookie(
        "refresh_token",
        new_refresh,
        max_age=int(
            timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES).total_seconds()
        ),
        httponly=True,
        secure=True,
        samesite="lax",
        path="/api/v1/auth",
    )
    return AccessToken(access_token=access)
