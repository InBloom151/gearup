from .booking import BookingBase, BookingCreate, BookingInDB, BookingOut, BookingUpdate
from .category import (
    CategoryBase,
    CategoryCreate,
    CategoryInDB,
    CategoryOut,
    CategoryUpdate,
)
from .landlord_detail import (
    LandlordDetailBase,
    LandlordDetailCreate,
    LandlordDetailCreateIn,
    LandlordDetailOut,
    LandlordDetailUpdate,
)
from .token import AccessToken
from .transport import (
    TransportBase,
    TransportCreate,
    TransportInDB,
    TransportOut,
    TransportUpdate,
)
from .transport_photo import (
    TransportPhotoBase,
    TransportPhotoCreate,
    TransportPhotoInDB,
    TransportPhotoOut,
    TransportPhotoUpdate,
)
from .user import UserBase, UserCreate, UserOut, UserUpdate

__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserOut",
    "LandlordDetailBase",
    "LandlordDetailCreate",
    "LandlordDetailCreateIn",
    "LandlordDetailUpdate",
    "LandlordDetailOut",
    "AccessToken",
    "TransportBase",
    "TransportCreate",
    "TransportUpdate",
    "TransportInDB",
    "TransportOut",
    "BookingBase",
    "BookingCreate",
    "BookingUpdate",
    "BookingInDB",
    "BookingOut",
    "CategoryBase",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryInDB",
    "CategoryOut",
    "TransportPhotoBase",
    "TransportPhotoCreate",
    "TransportPhotoUpdate",
    "TransportPhotoInDB",
    "TransportPhotoOut",
]

UserOut.model_rebuild()
LandlordDetailOut.model_rebuild()
TransportOut.model_rebuild()
BookingOut.model_rebuild()
CategoryOut.model_rebuild()
TransportPhotoOut.model_rebuild()
