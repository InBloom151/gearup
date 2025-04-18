from __future__ import annotations
from datetime import datetime
from app.core.enums import UserRole
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    role: UserRole
    phone: Optional[str] = Field(None, max_length=32)

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[UserRole] = None
    phone: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)


class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = dict(from_attributes=True)

class UserOut(UserInDB):
    landlord_detail: Optional["LandlordDetailOut"] = None