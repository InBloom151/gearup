from app.api.v1.schemas import TransportPhotoCreate, TransportPhotoUpdate
from app.db.models import TransportPhoto
from sqlalchemy.ext.asyncio import AsyncSession


class TransportPhotoRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: TransportPhotoCreate) -> TransportPhoto:
        photo = TransportPhoto(**data.model_dump())
        self.session.add(photo)
        await self.session.commit()
        await self.session.refresh(photo)
        return photo

    async def update(
        self, transport_photo: TransportPhoto, data: TransportPhotoUpdate
    ) -> TransportPhoto:
        for key, value in data.model_dump().items():
            setattr(key, value, transport_photo)
        await self.session.commit()
        await self.session.refresh(transport_photo)
        return transport_photo

    async def delete(self, transport_photo: TransportPhoto) -> None:
        await self.session.delete(transport_photo)
        await self.session.commit()
