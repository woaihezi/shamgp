from sqlalchemy import Column, BigInteger, Integer, String, Numeric, DateTime, SmallInteger, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base, TimestampMixin


class Coupon(Base, TimestampMixin):
    __tablename__ = "coupons"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="优惠券名称")
    code = Column(String(50), nullable=False, unique=True, comment="优惠券码")
    type = Column(SmallInteger, nullable=False, default=1, comment="类型：1满减 2折扣 3无门槛")
    满减金额 = Column(Numeric(10, 2), nullable=False, default=0, comment="满减金额（满X减Y）")
    折扣 = Column(Numeric(5, 2), nullable=True, comment="折扣率，如 0.9 表示9折")
    门槛金额 = Column(Numeric(10, 2), nullable=False, default=0, comment="使用门槛（满X可用）")
    total_count = Column(Integer, nullable=False, default=0, comment="发放总量，0不限")
    remain_count = Column(Integer, nullable=False, default=0, comment="剩余数量")
    per_user_limit = Column(Integer, nullable=False, default=1, comment="每人限领数量")
    start_time = Column(DateTime, nullable=True, comment="开始时间")
    end_time = Column(DateTime, nullable=True, comment="结束时间")
    status = Column(SmallInteger, nullable=False, default=1, comment="状态：0禁用 1启用")
    description = Column(Text, nullable=True, comment="描述")
