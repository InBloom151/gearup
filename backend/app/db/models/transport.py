from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from app.db.base import Base
from sqlalchemy import DECIMAL, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models import Category, User


class Transport(Base):
    landlord_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            ForeignKey("categories.id", ondelete="RESTRICT"),
            nullable=False,
            index=True,
        )
    )

    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price_per_day: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=True)
    price_per_month: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=True)
    price_per_year: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=True)

    landlord: Mapped["User"] = relationship(
        "User",
        back_populates="transports",
        lazy="selectin",
    )
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="categories",
        lazy="selectin",
    )
