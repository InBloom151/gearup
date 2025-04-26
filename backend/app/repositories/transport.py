from typing import List

from app.api.v1.schemas import TransportCreate, TransportUpdate
from app.db.models import Transport
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TransportRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, transport_id: int) -> Transport | None:
        stmt = select(Transport).where(Transport.id == transport_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: TransportCreate) -> Transport:
        transport = Transport(**data.model_dump())
        self.session.add(transport)
        await self.session.commit()
        await self.session.refresh(transport)
        return transport

    async def update(self, transport: Transport, data: TransportUpdate) -> Transport:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(transport, key, value)
        await self.session.commit()
        await self.session.refresh(transport)
        return transport

    async def delete(self, transport: Transport) -> None:
        await self.session.delete(transport)
        await self.session.commit()

    async def get_user_transport(self, transport_id) -> List[Transport]:
        stmt = select(Transport).where(Transport.id == transport_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
