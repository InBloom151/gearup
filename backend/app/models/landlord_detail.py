from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base

class EntityType(PyEnum):
    individual = "individual"
    legal = "legal"

class LandlordDetail(Base): #TODO
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    entity_type = Column(Enum(EntityType), nullable=False)
    company_name = Column(String, nullable=True)
    registration_number = Column(String, nullable=True)
    tax_id = Column(String, nullable=True)
    address = Column(String, nullable=True)
    additional_info = Column(Text, nullable=True)

    user = relationship("User", back_populates="landlord_details")