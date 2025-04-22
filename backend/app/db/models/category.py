from typing import Optional

from app.db.base import Base
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship


class Category(Base):
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parent_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )

    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        remote_side=[id],
        backref=backref("children", lazy="selectin"),
        lazy="selectin",
    )
