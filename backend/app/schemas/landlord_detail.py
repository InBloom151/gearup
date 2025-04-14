from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, EmailStr

if TYPE_CHECKING:
    from .user import UserInDBBase

class EntityType(str, Enum):
    individual = "individual"
    legal = "legal"

class LandlordDetailBase(BaseModel):
    entity_type: EntityType
    company_name: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    address: Optional[str] = None
    additional_info: Optional[str] = None

class LandlordDetailCreate(LandlordDetailBase):
    user_id: int

class LandlordDetailUpdate(BaseModel):
    entity_type: Optional[EntityType] = None
    company_name: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    address: Optional[str] = None
    additional_info: Optional[str] = None

class LandlordDetailInDBBase(LandlordDetailBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LandlordDetailOut(LandlordDetailInDBBase):
    user: Optional["UserInDBBase"] = None