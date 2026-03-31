from sqlalchemy import Column, BigInteger, Integer, ForeignKey, DateTime, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base, TimestampMixin


class UserCoupon(Base, TimestampMixin):
    __tablename__ = "user_coupons"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    coupon_id = Column(BigInteger, ForeignKey("coupons.id"), nullable=False, index=True)
    status = Column(SmallInteger, nullable=False, default=0, comment="状态：0未使用 1已使用 2已过期")
    used_at = Column(DateTime, nullable=True, comment="使用时间")
    order_id = Column(Integer, nullable=True, comment="关联订单ID")

    user = relationship("User", backref="user_coupons")
    coupon = relationship("Coupon", backref="user_coupons")
