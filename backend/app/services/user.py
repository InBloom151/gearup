from __future__ import annotations

from app.api.v1.schemas import (
    LandlordDetailCreate,
    LandlordDetailOut,
    LandlordDetailUpdate,
    UserOut,
    UserUpdate,
)
from app.repositories.user import UserRepository
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def update_user(self, data: UserUpdate, user_id: int) -> UserOut:
        user = await self.repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return await self.repo.update_user(user, data)

    async def delete_user(self, user_id: int) -> None:
        user = await self.repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        await self.repo.delete_user(user)

    async def create_landlord_detail(
        self, data: LandlordDetailCreate
    ) -> LandlordDetailOut:
        if await self.repo.get_landlord_by_user_id(data.user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a landlord",
            )
        landlord_detail = await self.repo.create_landlord(data)
        return landlord_detail

    async def update_landlord_detail(
        self, data: LandlordDetailUpdate, user_id: int
    ) -> LandlordDetailOut:
        landlord_detail = await self.repo.get_landlord_by_user_id(user_id)

        if not landlord_detail:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="LandlordDetail not found",
            )

        if landlord_detail.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID doesn`t match the credentials",
            )

        return await self.repo.update_landlord(landlord_detail, data)
