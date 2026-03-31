from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from decimal import Decimal
from .common import TimestampSchema
from .inventory_record import InventoryRecord


class ProductSkuBase(BaseModel):
    spu_id: int = Field(..., description="SPU ID")
    sku_code: str = Field(..., max_length=100, description="SKU编码")
    name: str = Field(..., max_length=200, description="SKU名称")
    specs: Optional[Any] = Field(None, description="规格JSON")
    image: Optional[str] = Field(None, max_length=255, description="SKU图片")
    price: Decimal = Field(..., ge=0, description="价格")
    original_price: Optional[Decimal] = Field(None, ge=0, description="原价")
    cost_price: Optional[Decimal] = Field(None, ge=0, description="成本价")
    status: int = Field(default=1, description="状态: 0-禁用, 1-启用")
    sort: int = Field(default=0, description="排序")


class ProductSkuCreate(ProductSkuBase):
    pass


class ProductSkuUpdate(ProductSkuBase):
    spu_id: Optional[int] = Field(None, description="SPU ID")
    sku_code: Optional[str] = Field(None, max_length=100, description="SKU编码")
    name: Optional[str] = Field(None, max_length=200, description="SKU名称")
    price: Optional[Decimal] = Field(None, ge=0, description="价格")


class ProductSku(ProductSkuBase, TimestampSchema):
    id: int = Field(description="SKU ID")
    inventory: Optional[InventoryRecord] = Field(None, description="库存信息")

    class Config:
        from_attributes = True
