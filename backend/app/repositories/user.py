from __future__ import annotations

from app.api.v1.schemas.user import UserCreate
from app.db.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: UserCreate) -> User:
        values = data.model_dump(exclude={"password"})
        values["password_hash"] = data.password
        user = User(**values)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
