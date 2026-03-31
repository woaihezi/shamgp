from sqlalchemy import Column, String, Integer, SmallInteger, Text, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"
    
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(100), nullable=True)
    brief = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    cover_image = Column(String(255), nullable=True)
    images = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False, default=0.00)
    original_price = Column(Numeric(10, 2), nullable=True)
    cost_price = Column(Numeric(10, 2), nullable=True)
    stock = Column(Integer, nullable=False, default=0)
    sales = Column(Integer, nullable=False, default=0, index=True)
    views = Column(Integer, nullable=False, default=0)
    is_hot = Column(Boolean, default=False)
    is_new = Column(Boolean, default=False)
    is_recommend = Column(Boolean, default=False)
    status = Column(SmallInteger, default=0, index=True)
    sort = Column(Integer, default=0)
    
    category = relationship("ProductCategory", backref="products")
