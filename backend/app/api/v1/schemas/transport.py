from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from .category import CategoryOut
    from .transport_photo import TransportPhotoOut
    from .user import UserOut


class TransportBase(BaseModel):
    landlord_id: int
    category_id: int
    title: str
    description: Optional[str] = None
    price_per_day: Optional[Decimal] = None
    price_per_month: Optional[Decimal] = None
    price_per_year: Optional[Decimal] = None


class TransportCreate(TransportBase):
    pass


class TransportUpdate(BaseModel):
    landlord_id: Optional[int] = None
    category_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price_per_day: Optional[Decimal] = None
    price_per_month: Optional[Decimal] = None
    price_per_year: Optional[Decimal] = None


class TransportInDB(TransportBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = dict(from_attributes=True)


class TransportOut(TransportInDB):
    landlord: Optional[UserOut] = None
    category: Optional[CategoryOut] = None
    photos: Optional[list[TransportPhotoOut]] = None
