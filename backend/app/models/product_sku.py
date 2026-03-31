from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class ProductSku(Base, TimestampMixin):
    __tablename__ = "product_skus"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    spu_id = Column(BigInteger, ForeignKey("product_spus.id"), nullable=False, comment="SPU ID")
    sku_code = Column(String(100), nullable=False, unique=True, comment="SKU编码")
    name = Column(String(200), nullable=False, comment="SKU名称")
    specs = Column(Text, nullable=True, comment="规格JSON")
    image = Column(String(255), nullable=True, comment="SKU图片")
    price = Column(Numeric(10, 2), nullable=False, comment="价格")
    original_price = Column(Numeric(10, 2), nullable=True, comment="原价")
    cost_price = Column(Numeric(10, 2), nullable=True, comment="成本价")
    status = Column(Integer, default=1, comment="状态: 0-禁用, 1-启用")
    sort = Column(Integer, default=0, comment="排序")

    spu = relationship("ProductSpu", back_populates="skus")
    inventory = relationship("InventoryRecord", back_populates="sku", uselist=False)
