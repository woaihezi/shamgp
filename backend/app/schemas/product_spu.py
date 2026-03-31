from pydantic import BaseModel, Field
from typing import Optional, List
from .common import TimestampSchema
from .product_sku import ProductSku
from .product_image import ProductImage
from .category import Category
from .brand import Brand


class ProductSpuBase(BaseModel):
    name: str = Field(..., max_length=200, description="商品名称")
    subtitle: Optional[str] = Field(None, max_length=500, description="副标题")
    category_id: int = Field(..., description="分类ID")
    brand_id: Optional[int] = Field(None, description="品牌ID")
    main_image: Optional[str] = Field(None, max_length=255, description="主图")
    description: Optional[str] = Field(None, description="商品详情")
    unit: Optional[str] = Field(None, max_length=50, description="单位")
    status: int = Field(default=0, description="状态: 0-下架, 1-上架")
    sort: int = Field(default=0, description="排序")


class ProductSpuCreate(ProductSpuBase):
    pass


class ProductSpuUpdate(ProductSpuBase):
    name: Optional[str] = Field(None, max_length=200, description="商品名称")
    category_id: Optional[int] = Field(None, description="分类ID")


class ProductSpu(ProductSpuBase, TimestampSchema):
    id: int = Field(description="SPU ID")
    sales_count: int = Field(default=0, description="销量")
    view_count: int = Field(default=0, description="浏览量")
    category: Optional[Category] = Field(None, description="分类信息")
    brand: Optional[Brand] = Field(None, description="品牌信息")
    skus: List[ProductSku] = Field(default_factory=list, description="SKU列表")
    images: List[ProductImage] = Field(default_factory=list, description="商品图片")

    class Config:
        from_attributes = True


class ProductSpuSimple(ProductSpuBase, TimestampSchema):
    id: int = Field(description="SPU ID")
    sales_count: int = Field(default=0, description="销量")
    view_count: int = Field(default=0, description="浏览量")
    category: Optional[Category] = Field(None, description="分类信息")
    brand: Optional[Brand] = Field(None, description="品牌信息")
    min_price: Optional[float] = Field(None, description="最低价格")
    max_price: Optional[float] = Field(None, description="最高价格")

    class Config:
        from_attributes = True
