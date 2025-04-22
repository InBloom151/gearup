from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from app.core.enums import UserRole
from app.db.base import Base
from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models import Booking, LandlordDetail, Transport


class User(Base):
    email: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    name: Mapped[str | None] = mapped_column(String(128))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, native_enum=False))
    phone: Mapped[str | None] = mapped_column(String(32))

    landlord_detail: Mapped[Optional["LandlordDetail"]] = relationship(
        back_populates="user",
        uselist=False,
        lazy="selectin",
    )
    transports: Mapped[List["Transport"]] = relationship(
        "Transport",
        back_populates="landlord",
        lazy="selectin",
    )
    bookings: Mapped[List["Booking"]] = relationship(
        "Booking",
        back_populates="renter",
        lazy="selectin",
    )
