from .user import UserBase, UserCreate, UserUpdate, UserOut
from .landlord_detail import (
    LandlordDetailBase,
    LandlordDetailCreate,
    LandlordDetailUpdate,
    LandlordDetailOut,
)
from .token import TokenPair, TokenRefresh

__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserOut",
    "LandlordDetailBase",
    "LandlordDetailCreate",
    "LandlordDetailUpdate",
    "LandlordDetailOut",
    "TokenPair",
    "TokenRefresh",
]

UserOut.model_rebuild()
LandlordDetailOut.model_rebuild()