from typing import TYPE_CHECKING

from app.db.base import Base
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models import Transport


class TransportPhoto(Base):
    transport_id: Mapped[int] = mapped_column(
        ForeignKey("transports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    url: Mapped[str] = mapped_column(String(256), nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    transport: Mapped["Transport"] = relationship(
        "Transport",
        back_populates="photos",
        lazy="selectin",
    )
