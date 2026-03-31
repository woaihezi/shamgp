from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .common import BaseSchema, PageResult


class CouponBase(BaseModel):
    name: str
    code: str
    type: str = "discount"
    discount_value: float
    min_order_amount: float = 0
    max_discount_amount: Optional[float] = None
    start_date: datetime
    end_date: datetime
    status: str = "active"
    total_count: int = 0
    per_user_limit: int = 1
    is_public: bool = True


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    total_count: Optional[int] = None


class CouponSchema(BaseSchema, CouponBase):
    used_count: int = 0


class CouponReceiveRecord(BaseSchema):
    id: int
    user_id: int
    coupon_id: int
    status: str = "active"


class CouponReceiveRecordCreate(BaseModel):
    coupon_id: int


# Backward compatibility
Coupon = CouponSchema
CouponPageResult = PageResult[CouponSchema]
CouponReceiveRecordPageResult = PageResult[CouponReceiveRecord]
