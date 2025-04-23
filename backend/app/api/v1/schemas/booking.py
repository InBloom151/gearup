from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from app.core.enums import BookingStatus
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from .transport import TransportOut
    from .user import UserOut


class BookingBase(BaseModel):
    transport_id: int
    start_date: date
    end_date: date
    status: BookingStatus = Field(BookingStatus.pending)


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[BookingStatus] = None


class BookingInDB(BookingBase):
    id: int
    client_id: int
    created_at: datetime
    updated_at: datetime

    model_config = dict(from_attributes=True)


class BookingOut(BookingInDB):
    transport: Optional["TransportOut"] = None
    client: Optional[UserOut] = None
