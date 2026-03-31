from sqlalchemy import Column, BigInteger, String, Integer, Text, SmallInteger
from .base import Base, IDMixin, TimestampMixin


class Banner(Base, IDMixin, TimestampMixin):
    __tablename__ = "banners"

    title = Column(String(200), nullable=False, comment="轮播图标题")
    image_url = Column(String(255), nullable=False, comment="图片URL")
    link_url = Column(String(255), comment="跳转链接")
    sort = Column(Integer, nullable=False, default=0, comment="排序")
    status = Column(SmallInteger, nullable=False, default=1, comment="状态：0-禁用，1-启用")
    platform = Column(SmallInteger, nullable=False, default=1, comment="平台：1-PC端，2-移动端，3-全部")
    description = Column(Text, comment="描述")
