from sqlalchemy import Column, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import BaseModel


class CartItem(BaseModel):
    __tablename__ = "cart_items"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    sku_id = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    selected = Column(Boolean, nullable=False, default=True)
    
    user = relationship("User", backref="cart_items")
    product = relationship("Product", backref="cart_items")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', 'sku_id', name='idx_cart_user_product_sku'),
    )
