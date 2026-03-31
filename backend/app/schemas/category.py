from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .common import TimestampSchema


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100, description="分类名称")
    parent_id: Optional[int] = Field(None, description="父分类ID")
    sort: int = Field(default=0, description="排序")
    icon: Optional[str] = Field(None, max_length=255, description="分类图标")
    description: Optional[str] = Field(None, description="分类描述")
    status: int = Field(default=1, description="状态: 0-禁用, 1-启用")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = Field(None, max_length=100, description="分类名称")


class Category(CategoryBase, TimestampSchema):
    id: int = Field(description="分类ID")

    class Config:
        from_attributes = True


class CategoryTree(Category):
    children: List["CategoryTree"] = Field(default_factory=list, description="子分类")


CategoryTree.model_rebuild()
