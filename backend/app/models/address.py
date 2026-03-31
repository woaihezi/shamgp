from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class Address(BaseModel):
    __tablename__ = "addresses"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    consignee_name = Column(String(50), nullable=False)
    consignee_phone = Column(String(20), nullable=False)
    province = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    detail_address = Column(String(200), nullable=False)
    zip_code = Column(String(10), nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)
    
    user = relationship("User", backref="addresses")
