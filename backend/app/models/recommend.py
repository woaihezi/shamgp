from sqlalchemy import Column, BigInteger, String, Integer, Text, SmallInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin


class AdSpace(Base, IDMixin, TimestampMixin):
    __tablename__ = "ad_spaces"

    name = Column(String(100), nullable=False, comment="广告位名称")
    code = Column(String(50), nullable=False, unique=True, comment="广告位编码")
    width = Column(Integer, comment="宽度")
    height = Column(Integer, comment="高度")
    description = Column(Text, comment="描述")
    status = Column(SmallInteger, nullable=False, default=1, comment="状态：0-禁用，1-启用")

    ads = relationship("Ad", back_populates="ad_space")


class Ad(Base, IDMixin, TimestampMixin):
    __tablename__ = "ads"

    ad_space_id = Column(BigInteger, ForeignKey("ad_spaces.id"), nullable=False, comment="广告位ID")
    title = Column(String(200), nullable=False, comment="广告标题")
    image_url = Column(String(255), nullable=False, comment="图片URL")
    link_url = Column(String(255), comment="跳转链接")
    sort = Column(Integer, nullable=False, default=0, comment="排序")
    status = Column(SmallInteger, nullable=False, default=1, comment="状态：0-禁用，1-启用")
    start_time = Column(DateTime, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    click_count = Column(Integer, nullable=False, default=0, comment="点击次数")
    description = Column(Text, comment="描述")

    ad_space = relationship("AdSpace", back_populates="ads")


class Floor(Base, IDMixin, TimestampMixin):
    __tablename__ = "floors"

    name = Column(String(100), nullable=False, comment="楼层名称")
    code = Column(String(50), nullable=False, unique=True, comment="楼层编码")
    title = Column(String(200), comment="楼层标题")
    subtitle = Column(String(200), comment="楼层副标题")
    sort = Column(Integer, nullable=False, default=0, comment="排序")
    status = Column(SmallInteger, nullable=False, default=1, comment="状态：0-禁用，1-启用")
    style = Column(SmallInteger, nullable=False, default=1, comment="样式类型：1-单排，2-双排，3-网格")

    floor_products = relationship("FloorProduct", back_populates="floor")


class FloorProduct(Base, IDMixin):
    __tablename__ = "floor_products"

    floor_id = Column(BigInteger, ForeignKey("floors.id"), nullable=False, comment="楼层ID")
    product_id = Column(BigInteger, nullable=False, comment="商品ID")
    sort = Column(Integer, nullable=False, default=0, comment="排序")
    created_at = Column(DateTime, nullable=False, comment="创建时间")

    floor = relationship("Floor", back_populates="floor_products")
