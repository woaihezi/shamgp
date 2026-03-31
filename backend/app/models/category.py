from sqlalchemy import Column, String, Integer, SmallInteger, Text
from .base import BaseModel


class ProductCategory(BaseModel):
    __tablename__ = "product_categories"
    
    parent_id = Column(Integer, default=0, index=True)
    name = Column(String(50), nullable=False)
    code = Column(String(50), nullable=True)
    image = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    sort = Column(Integer, default=0)
    level = Column(SmallInteger, default=1, index=True)
    status = Column(SmallInteger, default=1, index=True)
