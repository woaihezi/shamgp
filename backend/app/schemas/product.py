from typing import Optional
from pydantic import Field
from app.schemas.common import BaseSchema


class ProductBase(BaseSchema):
    category_id: int = Field(..., description="分类ID")
    name: str = Field(..., max_length=200, description="商品名称")
    code: Optional[str] = Field(None, max_length=100, description="商品编码")
    brief: Optional[str] = Field(None, max_length=500, description="简介")
    description: Optional[str] = Field(None, description="详情")
    cover_image: Optional[str] = Field(None, max_length=255, description="封面图")
    images: Optional[str] = Field(None, description="图片列表(JSON)")
    price: float = Field(..., description="价格")
    original_price: Optional[float] = Field(None, description="原价")
    cost_price: Optional[float] = Field(None, description="成本价")
    stock: int = Field(default=0, description="库存")
    sales: int = Field(default=0, description="销量")
    views: int = Field(default=0, description="浏览量")
    is_hot: bool = Field(default=False, description="是否热门")
    is_new: bool = Field(default=False, description="是否新品")
    is_recommend: bool = Field(default=False, description="是否推荐")
    status: int = Field(default=0, description="状态: 0-下架, 1-上架")
    sort: int = Field(default=0, description="排序")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    category_id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[float] = None


class ProductSimple(ProductBase):
    id: int


class Product(ProductSimple):
    pass
