from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from .transport import TransportOut


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryInDB(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = dict(from_attributes=True)


class CategoryOut(CategoryInDB):
    transports: Optional[list[TransportOut]] = None
