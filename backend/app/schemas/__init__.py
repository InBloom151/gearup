from .user import UserBase, UserCreate, UserUpdate, UserInDBBase, UserOut
from .landlord_detail import (
    LandlordDetailBase,
    LandlordDetailCreate,
    LandlordDetailUpdate,
    LandlordDetailInDBBase,
    LandlordDetailOut,
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserInDBBase",
    "UserOut",
    "LandlordDetailBase",
    "LandlordDetailCreate",
    "LandlordDetailUpdate",
    "LandlordDetailInDBBase",
    "LandlordDetailOut",
]

UserOut.model_rebuild()
LandlordDetailOut.model_rebuild()