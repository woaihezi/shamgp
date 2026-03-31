from pydantic import BaseModel, Field
from typing import Optional
from .common import TimestampSchema


class BrandBase(BaseModel):
    name: str = Field(..., max_length=100, description="品牌名称")
    logo: Optional[str] = Field(None, max_length=255, description="品牌Logo")
    description: Optional[str] = Field(None, description="品牌描述")
    sort: int = Field(default=0, description="排序")
    status: int = Field(default=1, description="状态: 0-禁用, 1-启用")


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BrandBase):
    name: Optional[str] = Field(None, max_length=100, description="品牌名称")


class Brand(BrandBase, TimestampSchema):
    id: int = Field(description="品牌ID")

    class Config:
        from_attributes = True
