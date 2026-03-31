from pydantic import BaseModel, Field
from typing import Optional
from .common import TimestampSchema


class InventoryRecordBase(BaseModel):
    sku_id: int = Field(..., description="SKU ID")
    total_stock: int = Field(default=0, description="总库存")
    available_stock: int = Field(default=0, description="可用库存")
    locked_stock: int = Field(default=0, description="锁定库存")
    warning_stock: int = Field(default=0, description="预警库存")


class InventoryRecordCreate(InventoryRecordBase):
    pass


class InventoryRecordUpdate(InventoryRecordBase):
    sku_id: Optional[int] = Field(None, description="SKU ID")
    total_stock: Optional[int] = Field(None, description="总库存")
    available_stock: Optional[int] = Field(None, description="可用库存")
    locked_stock: Optional[int] = Field(None, description="锁定库存")
    warning_stock: Optional[int] = Field(None, description="预警库存")


class InventoryRecord(InventoryRecordBase, TimestampSchema):
    id: int = Field(description="库存记录ID")

    class Config:
        from_attributes = True
