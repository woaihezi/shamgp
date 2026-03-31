from sqlalchemy import Column, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class InventoryRecord(Base, TimestampMixin):
    __tablename__ = "inventory_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sku_id = Column(BigInteger, ForeignKey("product_skus.id"), nullable=False, unique=True, comment="SKU ID")
    total_stock = Column(Integer, default=0, comment="总库存")
    available_stock = Column(Integer, default=0, comment="可用库存")
    locked_stock = Column(Integer, default=0, comment="锁定库存")
    warning_stock = Column(Integer, default=0, comment="预警库存")

    sku = relationship("ProductSku", back_populates="inventory")
