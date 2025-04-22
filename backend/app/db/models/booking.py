from datetime import date
from typing import TYPE_CHECKING

from app.core.enums import BookingStatus
from app.db.base import Base
from sqlalchemy import Date, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models import Transport, User


class Booking(Base):
    transport_id: Mapped[int] = mapped_column(
        ForeignKey("transports.id", ondelete="CASCADE"), nullable=False, index=True
    )
    renter_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, native_enum=False),
        default=BookingStatus.pending,
        nullable=False,
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    transport: Mapped["Transport"] = relationship(
        "Transport",
        back_populates="bookings",
        lazy="selectin",
    )
    renter: Mapped["User"] = relationship(
        "User",
        back_populates="bookings",
        lazy="selectin",
    )
