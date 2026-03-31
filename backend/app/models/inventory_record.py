from sqlalchemy import Column, BigInteger, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class InventoryRecord(Base, TimestampMixin):
    __tablename__ = "inventory_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sku_id = Column(BigInteger, ForeignKey("product_skus.id"), nullable=False, unique=True, comment="SKU ID")
    order_id = Column(BigInteger, nullable=True, comment="关联订单ID")
    change_type = Column(String(50), nullable=True, comment="变动类型：order_deduct-订单扣减, refund_add-退款归还, manual-手动调整")
    quantity_change = Column(Integer, default=0, comment="变动数量（正数为增加，负数为减少）")
    total_stock = Column(Integer, default=0, comment="总库存")
    available_stock = Column(Integer, default=0, comment="可用库存")
    locked_stock = Column(Integer, default=0, comment="锁定库存")
    warning_stock = Column(Integer, default=0, comment="预警库存")

    sku = relationship("ProductSku", back_populates="inventory")
