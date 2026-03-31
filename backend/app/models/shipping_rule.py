from sqlalchemy import Column, Integer, String, Numeric, DateTime, SmallInteger, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base, TimestampMixin


class ShippingRule(Base, TimestampMixin):
    __tablename__ = "shipping_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="规则名称")
    region = Column(String(200), nullable=True, comment="地区（为空表示全国）")
    first_weight = Column(Numeric(10, 2), nullable=False, default=1.0, comment="首重（kg）")
    first_weight_fee = Column(Numeric(10, 2), nullable=False, default=0.0, comment="首重费用")
    extra_weight = Column(Numeric(10, 2), nullable=False, default=1.0, comment="续重（kg）")
    extra_weight_fee = Column(Numeric(10, 2), nullable=False, default=0.0, comment="续重费用/kg")
    free_threshold = Column(Numeric(10, 2), nullable=False, default=0.0, comment="满X元包邮（0表示不包邮）")
    status = Column(SmallInteger, nullable=False, default=1, comment="状态：0禁用 1启用")
    description = Column(Text, nullable=True)
