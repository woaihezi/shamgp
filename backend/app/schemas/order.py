from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from .common import BaseSchema
from ..models.order import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int
    product_name: str
    product_image: Optional[str] = None
    sku_id: Optional[int] = None
    sku_specs: Optional[str] = None
    price: float
    quantity: int
    total_amount: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemSchema(BaseSchema, OrderItemBase):
    order_id: int


class OrderBase(BaseModel):
    remark: Optional[str] = Field(None, max_length=500)


class OrderCreate(BaseModel):
    address_id: int
    cart_item_ids: List[int]
    remark: Optional[str] = Field(None, max_length=500)


class OrderUpdate(BaseModel):
    remark: Optional[str] = Field(None, max_length=500)
    consignee_name: Optional[str] = Field(None, max_length=50)
    consignee_phone: Optional[str] = Field(None, max_length=20)
    consignee_address: Optional[str] = Field(None, max_length=500)


class OrderStatusUpdate(BaseModel):
    status: str


class OrderSchema(BaseSchema):
    order_no: str
    user_id: int
    total_amount: float
    pay_amount: float
    discount_amount: float
    freight_amount: float
    status: str
    pay_status: int
    pay_time: Optional[datetime] = None
    pay_type: Optional[str] = None
    consignee_name: str
    consignee_phone: str
    consignee_address: str
    remark: Optional[str] = None
    cancel_time: Optional[datetime] = None
    cancel_reason: Optional[str] = None
    delivery_time: Optional[datetime] = None
    receive_time: Optional[datetime] = None
    
    items: List[OrderItemSchema] = []


class OrderStatusLogSchema(BaseModel):
    id: int
    order_id: int
    old_status: Optional[str] = None
    new_status: str
    operator_type: str
    operator_id: Optional[int] = None
    remark: Optional[str] = None
    created_at: datetime


class OrderDetailSchema(OrderSchema):
    status_logs: List[OrderStatusLogSchema] = []


class RefundBase(BaseModel):
    refund_reason: str = Field(..., min_length=1, max_length=500)
    refund_type: str


class RefundCreate(RefundBase):
    order_id: int
    order_item_id: Optional[int] = None


class RefundSchema(BaseSchema, RefundBase):
    order_id: int
    order_item_id: Optional[int] = None
    refund_no: str
    user_id: int
    refund_amount: float
    status: str
    audit_time: Optional[datetime] = None
    audit_user_id: Optional[int] = None
    audit_remark: Optional[str] = None
    refund_time: Optional[datetime] = None
