from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ...core.database import get_db
from ...schemas.cart import CartItemCreate, CartItemUpdate, CartItemSchema, CartSummary
from ...services.cart_service import CartService
from ...schemas.common import ResponseModel

router = APIRouter()


@router.get("/summary", response_model=ResponseModel[CartSummary])
async def get_cart_summary(
    user_id: int = 1, 
    db: AsyncSession = Depends(get_db)
):
    service = CartService(db)
    summary = await service.get_cart_summary(user_id)
    return ResponseModel(data=summary)


@router.get("/items", response_model=ResponseModel[List[CartItemSchema]])
async def get_cart_items(
    user_id: int = 1, 
    db: AsyncSession = Depends(get_db)
):
    service = CartService(db)
    items = await service.get_cart_items(user_id)
    return ResponseModel(data=[CartItemSchema.model_validate(item) for item in items])


@router.post("/items", response_model=ResponseModel[CartItemSchema])
async def add_cart_item(
    cart_item_in: CartItemCreate,
    user_id: int = 1, 
    db: AsyncSession = Depends(get_db)
):
    service = CartService(db)
    item = await service.add_item(user_id, cart_item_in)
    return ResponseModel(data=CartItemSchema.model_validate(item))


@router.put("/items/{item_id}", response_model=ResponseModel[CartItemSchema])
async def update_cart_item(
    item_id: int,
    cart_item_in: CartItemUpdate,
    user_id: int = 1, 
    db: AsyncSession = Depends(get_db)
):
    service = CartService(db)
    item = await service.update_item(user_id, item_id, cart_item_in)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return ResponseModel(data=CartItemSchema.model_validate(item))


@router.delete("/items/{item_id}", response_model=ResponseModel)
async def remove_cart_item(
    item_id: int,
    user_id: int = 1, 
    db: AsyncSession = Depends(get_db)
):
    service = CartService(db)
    success = await service.remove_item(user_id, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return ResponseModel(message="Item removed successfully")


@router.delete("/clear", response_model=ResponseModel)
async def clear_cart(
    user_id: int = 1, 
    db: AsyncSession = Depends(get_db)
):
    service = CartService(db)
    await service.clear_cart(user_id)
    return ResponseModel(message="Cart cleared successfully")
