from enum import Enum as PyEnum

from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship

from app.db.base import Base

class UserRole(PyEnum):
    client = "client"
    landlord = "landlord"

class User(Base):
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=True)
    role = Column(Enum(UserRole), nullable=False)
    phone = Column(String, nullable=True)

    landlord_details = relationship("LandlordDetail", uselist=False, back_populates="user")