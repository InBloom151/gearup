from __future__ import annotations

from app.api.deps.auth import get_current_user
from app.api.v1.schemas import (
    LandlordDetailCreate,
    LandlordDetailCreateIn,
    LandlordDetailOut,
    LandlordDetailUpdate,
    UserOut,
    UserUpdate,
)
from app.db.models import User
from app.db.session import get_session
from app.services.user import UserService
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/user", tags=["user"])


def _svc(db: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(db)


"""-------------PUT-------------"""


@router.get("/get_current_user", response_model=UserOut)
async def get_current_user(
    user: User = Depends(get_current_user),
) -> UserOut:
    return user


"""------------POST------------"""


@router.post("/create_landlord_detail", response_model=LandlordDetailOut)
async def create_landlord_detail(
    data: LandlordDetailCreateIn,
    user: User = Depends(get_current_user),
    svc: UserService = Depends(_svc),
):
    landlord_data = LandlordDetailCreate(user_id=user.id, **data.model_dump())
    return await svc.create_landlord_detail(landlord_data)


"""-------------PUT-------------"""


@router.put("/update_user", response_model=UserOut)
async def update_user(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    svc: UserService = Depends(_svc),
):
    return await svc.update_user(data, user.id)


@router.put("/update_landlord_detail", response_model=LandlordDetailOut)
async def update_landlord_detail(
    data: LandlordDetailUpdate,
    user: User = Depends(get_current_user),
    svc: UserService = Depends(_svc),
):
    return await svc.update_landlord_detail(data, user.id)


"""------------DELETE------------"""


@router.delete("/delete_user", response_class=Response)
async def delete_user(
    user: User = Depends(get_current_user),
    svc: UserService = Depends(_svc),
) -> None:
    await svc.delete_user(user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
