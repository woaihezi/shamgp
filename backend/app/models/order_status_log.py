from sqlalchemy import Column, BigInteger, Integer, ForeignKey, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class OrderStatusLog(Base):
    __tablename__ = "order_status_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    operator_type = Column(String(20), default="system")  # system/user/admin
    operator_id = Column(Integer, nullable=True)
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", backref="status_logs")
