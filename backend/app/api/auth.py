from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import (
    UserCreate,
    UserOut,
    Token,
    TokenRefresh,
)
from app.crud.user import create_user, get_user_by_email
from app.core.security import (
    verify_password,
    get_password_hash,
    create_token,
    decode_token,
)
from app.core.config import settings
from app.db.session import get_session

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = await get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user_in.password)
    user_in.password = hashed_password
    user = await create_user(db, user_in)
    return user

@router.post("/login", response_model=Token)
async def login(
    email: str = Body(...),
    password: str = Body(...),
    db: AsyncSession = Depends(get_session)
):
    user = await get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(
        data={"sub": user.email}, token_type="access", expires_delta=access_token_expires
    )
    refresh_token = create_token(
        data={"sub": user.email}, token_type="refresh", expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh(token_in: TokenRefresh, db: AsyncSession = Depends(get_session)):
    payload = decode_token(token_in.refresh_token)

    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = await get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    new_access_token = create_token(
        data={"sub": user.email}, token_type="access", expires_delta=access_token_expires
    )
    new_refresh_token = create_token(
        data={"sub": user.email}, token_type="refresh", expires_delta=refresh_token_expires
    )

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}