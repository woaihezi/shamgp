from pydantic import BaseModel, Field
from typing import Optional
from .common import TimestampSchema


class ProductImageBase(BaseModel):
    spu_id: int = Field(..., description="SPU ID")
    image_url: str = Field(..., max_length=255, description="图片URL")
    image_type: int = Field(default=0, description="图片类型: 0-轮播图, 1-详情图")
    sort: int = Field(default=0, description="排序")


class ProductImageCreate(ProductImageBase):
    pass


class ProductImageUpdate(ProductImageBase):
    spu_id: Optional[int] = Field(None, description="SPU ID")
    image_url: Optional[str] = Field(None, max_length=255, description="图片URL")


class ProductImage(ProductImageBase, TimestampSchema):
    id: int = Field(description="图片ID")

    class Config:
        from_attributes = True
