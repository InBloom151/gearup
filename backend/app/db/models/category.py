from typing import TYPE_CHECKING, Optional

from app.db.base import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models import Transport


class Category(Base):
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    transports: Mapped[list["Transport"]] = relationship(
        "Transport",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    # parent_id: Mapped[Optional[int]] = mapped_column(
    #     ForeignKey("categories.id", ondelete="SET NULL"),
    #     nullable=True,
    # )

    # parent: Mapped[Optional["Category"]] = relationship(
    #     "Category",
    #     remote_side=["Category.id"],
    #     backref=backref("children", lazy="selectin"),
    #     lazy="selectin",
    # )
