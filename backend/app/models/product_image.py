from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class ProductImage(Base, TimestampMixin):
    __tablename__ = "product_images"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    spu_id = Column(BigInteger, ForeignKey("product_spus.id"), nullable=False, comment="SPU ID")
    image_url = Column(String(255), nullable=False, comment="图片URL")
    image_type = Column(Integer, default=0, comment="图片类型: 0-轮播图, 1-详情图")
    sort = Column(Integer, default=0, comment="排序")

    spu = relationship("ProductSpu", back_populates="images")
