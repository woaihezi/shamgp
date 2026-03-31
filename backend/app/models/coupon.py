from sqlalchemy import Column, BigInteger, String, Integer, Numeric, Text, DateTime, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin


class Coupon(Base, IDMixin, TimestampMixin):
    __tablename__ = "coupons"

    name = Column(String(100), nullable=False, comment="优惠券名称")
    type = Column(SmallInteger, nullable=False, default=1, comment="优惠券类型：1-满减券，2-折扣券，3-无门槛券")
    discount_value = Column(Numeric(10, 2), nullable=False, comment="优惠值")
    min_amount = Column(Numeric(10, 2), default=0, comment="最低使用金额")
    total_count = Column(Integer, nullable=False, default=0, comment="发放总量")
    used_count = Column(Integer, nullable=False, default=0, comment="已使用数量")
    per_limit = Column(Integer, nullable=False, default=1, comment="每人限领数量")
    valid_start_time = Column(DateTime, nullable=False, comment="有效期开始时间")
    valid_end_time = Column(DateTime, nullable=False, comment="有效期结束时间")
    status = Column(SmallInteger, nullable=False, default=1, comment="状态：0-禁用，1-启用")
    description = Column(Text, comment="优惠券描述")

    receive_records = relationship("CouponReceiveRecord", back_populates="coupon")


class CouponReceiveRecord(Base, IDMixin, TimestampMixin):
    __tablename__ = "coupon_receive_records"

    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    coupon_id = Column(BigInteger, ForeignKey("coupons.id"), nullable=False, comment="优惠券ID")
    status = Column(SmallInteger, nullable=False, default=1, comment="状态：1-未使用，2-已使用，3-已过期")
    order_id = Column(BigInteger, comment="使用订单ID")
    used_time = Column(DateTime, comment="使用时间")
    received_time = Column(DateTime, nullable=False, comment="领取时间")
    expire_time = Column(DateTime, nullable=False, comment="过期时间")

    coupon = relationship("Coupon", back_populates="receive_records")
