from sqlalchemy import Column, BigInteger, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class ProductSpu(Base, TimestampMixin):
    __tablename__ = "product_spus"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, comment="商品名称")
    subtitle = Column(String(500), nullable=True, comment="副标题")
    category_id = Column(BigInteger, ForeignKey("categories.id"), nullable=False, comment="分类ID")
    brand_id = Column(BigInteger, ForeignKey("brands.id"), nullable=True, comment="品牌ID")
    main_image = Column(String(255), nullable=True, comment="主图")
    description = Column(Text, nullable=True, comment="商品详情")
    unit = Column(String(50), nullable=True, comment="单位")
    status = Column(Integer, default=0, comment="状态: 0-下架, 1-上架")
    sort = Column(Integer, default=0, comment="排序")
    sales_count = Column(Integer, default=0, comment="销量")
    view_count = Column(Integer, default=0, comment="浏览量")

    category = relationship("Category", back_populates="spus")
    brand = relationship("Brand", back_populates="spus")
    skus = relationship("ProductSku", back_populates="spu", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="spu", cascade="all, delete-orphan")
