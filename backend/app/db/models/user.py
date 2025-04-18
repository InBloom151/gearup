from __future__ import annotations
from app.core.enums import UserRole

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum
from typing import Optional

from app.db.base import Base

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