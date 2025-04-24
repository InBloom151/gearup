from __future__ import annotations

from app.api.v1.schemas import (
    LandlordDetailCreate,
    LandlordDetailUpdate,
    UserCreate,
    UserUpdate,
)
from app.db.models import LandlordDetail, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, data: UserCreate) -> User:
        values = data.model_dump(exclude={"password"})
        values["password_hash"] = data.password
        user = User(**values)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user: User, data: UserUpdate) -> User:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user: User) -> None:
        self.session.delete(user)
        await self.session.commit()

    async def get_landlord_by_user_id(self, user_id: int) -> LandlordDetail | None:
        stmt = select(LandlordDetail).where(LandlordDetail.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_landlord(self, data: LandlordDetailCreate) -> LandlordDetail:
        landlord_detail = LandlordDetail(**data.model_dump())
        self.session.add(landlord_detail)
        await self.session.commit()
        await self.session.refresh(landlord_detail)
        return landlord_detail

    async def update_landlord(
        self, landlord_detail: LandlordDetail, data: LandlordDetailUpdate
    ) -> LandlordDetail:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(landlord_detail, key, value)
        await self.session.commit()
        await self.session.refresh(landlord_detail)
        return landlord_detail
