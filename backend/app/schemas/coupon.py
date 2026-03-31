from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from .common import IDMixin, TimestampMixin, PageResult


class CouponBase(BaseModel):
    name: str = Field(..., max_length=100, description="优惠券名称")
    type: int = Field(1, description="优惠券类型：1-满减券，2-折扣券，3-无门槛券")
    discount_value: Decimal = Field(..., description="优惠值")
    min_amount: Decimal = Field(Decimal("0"), description="最低使用金额")
    total_count: int = Field(0, description="发放总量")
    per_limit: int = Field(1, description="每人限领数量")
    valid_start_time: datetime = Field(..., description="有效期开始时间")
    valid_end_time: datetime = Field(..., description="有效期结束时间")
    status: int = Field(1, description="状态：0-禁用，1-启用")
    description: Optional[str] = Field(None, description="优惠券描述")


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    type: Optional[int] = None
    discount_value: Optional[Decimal] = None
    min_amount: Optional[Decimal] = None
    total_count: Optional[int] = None
    per_limit: Optional[int] = None
    valid_start_time: Optional[datetime] = None
    valid_end_time: Optional[datetime] = None
    status: Optional[int] = None
    description: Optional[str] = None


class Coupon(CouponBase, IDMixin, TimestampMixin):
    used_count: int = Field(0, description="已使用数量")

    model_config = ConfigDict(from_attributes=True)


class CouponPageResult(PageResult[Coupon]):
    pass


class CouponReceiveRecordBase(BaseModel):
    user_id: int = Field(..., description="用户ID")
    coupon_id: int = Field(..., description="优惠券ID")
    status: int = Field(1, description="状态：1-未使用，2-已使用，3-已过期")
    order_id: Optional[int] = Field(None, description="使用订单ID")
    used_time: Optional[datetime] = Field(None, description="使用时间")
    received_time: datetime = Field(..., description="领取时间")
    expire_time: datetime = Field(..., description="过期时间")


class CouponReceiveRecordCreate(BaseModel):
    coupon_id: int


class CouponReceiveRecord(CouponReceiveRecordBase, IDMixin, TimestampMixin):
    model_config = ConfigDict(from_attributes=True)


class CouponReceiveRecordPageResult(PageResult[CouponReceiveRecord]):
    pass
