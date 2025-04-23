from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from .transport import TransportOut


class TransportPhotoBase(BaseModel):
    transport_id: int
    url: str


class TransportPhotoCreate(TransportPhotoBase):
    pass


class TransportPhotoUpdate(BaseModel):
    url: Optional[str] = None


class TransportPhotoInDB(TransportPhotoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = dict(from_attributes=True)


class TransportPhotoOut(TransportPhotoInDB):
    transport: Optional[TransportOut] = None
