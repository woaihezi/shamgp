from sqlalchemy import Column, String, Integer, SmallInteger, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class OrderStatus:
    PENDING_PAYMENT = "pending_payment"
    PAID = "paid"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELED = "canceled"
    REFUNDING = "refunding"
    REFUNDED = "refunded"


class PayStatus:
    UNPAID = 0
    PAID = 1
    REFUNDED = 2


class Order(BaseModel):
    __tablename__ = "orders"
    
    order_no = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    pay_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    discount_amount = Column(Numeric(10, 2), default=0.00)
    freight_amount = Column(Numeric(10, 2), default=0.00)
    status = Column(String(20), nullable=False, default=OrderStatus.PENDING_PAYMENT, index=True)
    pay_status = Column(SmallInteger, nullable=False, default=PayStatus.UNPAID)
    pay_time = Column(DateTime(timezone=True), nullable=True)
    pay_type = Column(String(20), nullable=True)
    consignee_name = Column(String(50), nullable=False)
    consignee_phone = Column(String(20), nullable=False)
    consignee_address = Column(String(500), nullable=False)
    remark = Column(String(500), nullable=True)
    cancel_time = Column(DateTime(timezone=True), nullable=True)
    cancel_reason = Column(String(255), nullable=True)
    delivery_time = Column(DateTime(timezone=True), nullable=True)
    receive_time = Column(DateTime(timezone=True), nullable=True)
    
    user = relationship("User", backref="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(BaseModel):
    __tablename__ = "order_items"
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_name = Column(String(200), nullable=False)
    product_image = Column(String(255), nullable=True)
    sku_id = Column(Integer, nullable=True)
    sku_specs = Column(String(500), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", backref="order_items")


class Refund(BaseModel):
    __tablename__ = "refunds"
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id"), nullable=True)
    refund_no = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    refund_amount = Column(Numeric(10, 2), nullable=False)
    refund_reason = Column(String(500), nullable=False)
    refund_type = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    audit_time = Column(DateTime(timezone=True), nullable=True)
    audit_user_id = Column(Integer, nullable=True)
    audit_remark = Column(String(500), nullable=True)
    refund_time = Column(DateTime(timezone=True), nullable=True)
    
    order = relationship("Order", backref="refunds")
    user = relationship("User", backref="refunds")
