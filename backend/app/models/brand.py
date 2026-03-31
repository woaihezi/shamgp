from sqlalchemy import Column, BigInteger, String, Integer, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Brand(Base, TimestampMixin):
    __tablename__ = "brands"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="品牌名称")
    logo = Column(String(255), nullable=True, comment="品牌Logo")
    description = Column(Text, nullable=True, comment="品牌描述")
    sort = Column(Integer, default=0, comment="排序")
    status = Column(Integer, default=1, comment="状态: 0-禁用, 1-启用")

    spus = relationship("ProductSpu", back_populates="brand")
