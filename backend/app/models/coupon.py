from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.models.base import BaseModel


class Coupon(BaseModel):
    __tablename__ = "coupons"

    name = Column(String(100), nullable=False, comment="优惠券名称")
    code = Column(String(50), unique=True, nullable=False, comment="优惠券码")
    type = Column(String(20), nullable=False, default="discount", comment="类型: discount=折扣, fixed=满减")
    discount_value = Column(Float, nullable=False, comment="优惠值")
    min_order_amount = Column(Float, default=0, comment="最低订单金额")
    max_discount_amount = Column(Float, nullable=True, comment="最高优惠金额")
    start_date = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    end_date = Column(DateTime(timezone=True), nullable=False, comment="结束时间")
    status = Column(String(20), default="active", comment="状态")
    total_count = Column(Integer, default=0)
    used_count = Column(Integer, default=0)
    per_user_limit = Column(Integer, default=1)
    is_public = Column(Boolean, default=True)
