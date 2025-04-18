from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import DateTime, Integer

UTC_NOW: Annotated[datetime, mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
)] = ...

class Base(DeclarativeBase):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    created_at: Mapped[datetime] = UTC_NOW
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"