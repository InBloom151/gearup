from __future__ import annotations

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import UserCreate, UserOut, TokenPair, TokenRefresh
from app.db.session import get_session
from app.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

def _svc(db: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(db)

@router.post(
    "/register",
    response_model=UserOut,
    status_code=201
)
async def register(user_in: UserCreate, svc: AuthService = Depends(_svc)):
    return await svc.register(user_in)

@router.post("/login", response_model=TokenPair)
async def login(
    email: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    svc: AuthService = Depends(_svc),
):
    return await svc.login(email, password)

@router.post("/refresh", response_model=TokenPair)
async def refresh(token_in: TokenRefresh, svc: AuthService = Depends(_svc)):
    return await svc.refresh(token_in.refresh_token)