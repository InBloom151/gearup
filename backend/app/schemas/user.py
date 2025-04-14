from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, EmailStr

if TYPE_CHECKING:
    from .landlord_detail import LandlordDetailOut

class UserRole(Enum):
    client = "client"
    landlord = "landlord"

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    role: UserRole
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[UserRole] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserOut(UserInDBBase):
    landlord_details: Optional["LandlordDetailOut"] = None