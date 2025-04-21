from .landlord_detail import (
    LandlordDetailBase,
    LandlordDetailCreate,
    LandlordDetailOut,
    LandlordDetailUpdate,
)
from .token import AccessToken
from .user import UserBase, UserCreate, UserOut, UserUpdate

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
