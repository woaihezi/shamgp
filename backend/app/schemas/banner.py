from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from .common import IDMixin, TimestampMixin, PageResult


class BannerBase(BaseModel):
    title: str = Field(..., max_length=200, description="轮播图标题")
    image_url: str = Field(..., max_length=255, description="图片URL")
    link_url: Optional[str] = Field(None, max_length=255, description="跳转链接")
    sort: int = Field(0, description="排序")
    status: int = Field(1, description="状态：0-禁用，1-启用")
    platform: int = Field(1, description="平台：1-PC端，2-移动端，3-全部")
    description: Optional[str] = Field(None, description="描述")


class BannerCreate(BannerBase):
    pass


class BannerUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    image_url: Optional[str] = Field(None, max_length=255)
    link_url: Optional[str] = Field(None, max_length=255)
    sort: Optional[int] = None
    status: Optional[int] = None
    platform: Optional[int] = None
    description: Optional[str] = None


class Banner(BannerBase, IDMixin, TimestampMixin):
    model_config = ConfigDict(from_attributes=True)


class BannerPageResult(PageResult[Banner]):
    pass
