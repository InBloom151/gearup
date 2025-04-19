from .user import UserBase, UserCreate, UserUpdate, UserOut
from .landlord_detail import (
    LandlordDetailBase,
    LandlordDetailCreate,
    LandlordDetailUpdate,
    LandlordDetailOut,
)
from .token import AccessToken

__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserOut",
    "LandlordDetailBase",
    "LandlordDetailCreate",
    "LandlordDetailUpdate",
    "LandlordDetailOut",
    "AccessToken",
]

UserOut.model_rebuild()
LandlordDetailOut.model_rebuild()