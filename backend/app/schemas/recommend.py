from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from .common import IDMixin, TimestampMixin, PageResult


class AdSpaceBase(BaseModel):
    name: str = Field(..., max_length=100, description="广告位名称")
    code: str = Field(..., max_length=50, description="广告位编码")
    width: Optional[int] = Field(None, description="宽度")
    height: Optional[int] = Field(None, description="高度")
    description: Optional[str] = Field(None, description="描述")
    status: int = Field(1, description="状态：0-禁用，1-启用")


class AdSpaceCreate(AdSpaceBase):
    pass


class AdSpaceUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, max_length=50)
    width: Optional[int] = None
    height: Optional[int] = None
    description: Optional[str] = None
    status: Optional[int] = None


class AdSpace(AdSpaceBase, IDMixin, TimestampMixin):
    model_config = ConfigDict(from_attributes=True)


class AdSpacePageResult(PageResult[AdSpace]):
    pass


class AdBase(BaseModel):
    ad_space_id: int = Field(..., description="广告位ID")
    title: str = Field(..., max_length=200, description="广告标题")
    image_url: str = Field(..., max_length=255, description="图片URL")
    link_url: Optional[str] = Field(None, max_length=255, description="跳转链接")
    sort: int = Field(0, description="排序")
    status: int = Field(1, description="状态：0-禁用，1-启用")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    description: Optional[str] = Field(None, description="描述")


class AdCreate(AdBase):
    pass


class AdUpdate(BaseModel):
    ad_space_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=200)
    image_url: Optional[str] = Field(None, max_length=255)
    link_url: Optional[str] = Field(None, max_length=255)
    sort: Optional[int] = None
    status: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    description: Optional[str] = None


class Ad(AdBase, IDMixin, TimestampMixin):
    click_count: int = Field(0, description="点击次数")

    model_config = ConfigDict(from_attributes=True)


class AdPageResult(PageResult[Ad]):
    pass


class FloorBase(BaseModel):
    name: str = Field(..., max_length=100, description="楼层名称")
    code: str = Field(..., max_length=50, description="楼层编码")
    title: Optional[str] = Field(None, max_length=200, description="楼层标题")
    subtitle: Optional[str] = Field(None, max_length=200, description="楼层副标题")
    sort: int = Field(0, description="排序")
    status: int = Field(1, description="状态：0-禁用，1-启用")
    style: int = Field(1, description="样式类型：1-单排，2-双排，3-网格")


class FloorCreate(FloorBase):
    pass


class FloorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, max_length=50)
    title: Optional[str] = Field(None, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=200)
    sort: Optional[int] = None
    status: Optional[int] = None
    style: Optional[int] = None


class Floor(FloorBase, IDMixin, TimestampMixin):
    model_config = ConfigDict(from_attributes=True)


class FloorPageResult(PageResult[Floor]):
    pass


class FloorProductBase(BaseModel):
    floor_id: int = Field(..., description="楼层ID")
    product_id: int = Field(..., description="商品ID")
    sort: int = Field(0, description="排序")


class FloorProductCreate(FloorProductBase):
    pass


class FloorProductUpdate(BaseModel):
    floor_id: Optional[int] = None
    product_id: Optional[int] = None
    sort: Optional[int] = None


class FloorProduct(FloorProductBase, IDMixin):
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
