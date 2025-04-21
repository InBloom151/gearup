from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.core.enums import EntityTypes
from pydantic import BaseModel, Field

from .user import UserInDB


class LandlordDetailBase(BaseModel):
    entity_type: EntityTypes
    company_name: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    address: Optional[str] = None
    additional_info: Optional[str] = Field(None, max_length=500)


class LandlordDetailCreate(LandlordDetailBase):
    user_id: int


class LandlordDetailUpdate(BaseModel):
    entity_type: Optional[EntityTypes] = None
    company_name: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    address: Optional[str] = None
    additional_info: Optional[str] = None


class LandlordDetailInDB(LandlordDetailBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = dict(from_attributes=True)


class LandlordDetailOut(LandlordDetailInDB):
    user: Optional[UserInDB] = None
