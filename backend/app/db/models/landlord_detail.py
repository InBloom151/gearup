from __future__ import annotations

from typing import TYPE_CHECKING

from app.core.enums import EntityTypes
from app.db.base import Base
from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models import User


class LandlordDetail(Base):

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    entity_type: Mapped[EntityTypes] = mapped_column(
        Enum(EntityTypes, native_enum=False)
    )
    company_name: Mapped[str | None] = mapped_column(String(128))
    registration_number: Mapped[str | None] = mapped_column(String(64))
    tax_id: Mapped[str | None] = mapped_column(String(64))
    address: Mapped[str | None] = mapped_column(String(256))
    additional_info: Mapped[str | None] = mapped_column(Text)

    user: Mapped["User"] = relationship(
        back_populates="landlord_detail",
        lazy="selectin",
    )
