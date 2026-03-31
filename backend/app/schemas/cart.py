from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from .common import BaseSchema


class CartItemBase(BaseModel):
    product_id: int
    sku_id: Optional[int] = None
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None
    selected: Optional[bool] = None


class CartItemSchema(BaseSchema, CartItemBase):
    user_id: int
    selected: bool
    product_name: Optional[str] = None
    product_image: Optional[str] = None
    product_price: Optional[float] = None


class CartItemWithProduct(CartItemSchema):
    pass


class CartSummary(BaseModel):
    total_items: int
    total_quantity: int
    total_amount: float
    selected_items: List[CartItemSchema] = []
