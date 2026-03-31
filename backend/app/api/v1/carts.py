from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ...core.database import get_db
from ...schemas.cart import CartItemCreate, CartItemUpdate, CartItemSchema, CartSummary
from ...services.cart_service import CartService
from ...schemas.common import ResponseModel
from ...api.deps import get_current_active_user
from ...models.user import User

router = APIRouter()


@router.get("/summary", response_model=ResponseModel[CartSummary])
async def get_cart_summary(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = CartService(db)
    summary = await service.get_cart_summary(current_user.id)
    return ResponseModel(data=summary)


@router.get("/items", response_model=ResponseModel[List[CartItemSchema]])
async def get_cart_items(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = CartService(db)
    items = await service.get_cart_items(current_user.id)
    return ResponseModel(data=[CartItemSchema.model_validate(item) for item in items])


@router.post("/items", response_model=ResponseModel[CartItemSchema])
async def add_cart_item(
    cart_item_in: CartItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = CartService(db)
    item = await service.add_item(current_user.id, cart_item_in)
    return ResponseModel(data=CartItemSchema.model_validate(item))


@router.put("/items/{item_id}", response_model=ResponseModel[CartItemSchema])
async def update_cart_item(
    item_id: int,
    cart_item_in: CartItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = CartService(db)
    item = await service.update_item(current_user.id, item_id, cart_item_in)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return ResponseModel(data=CartItemSchema.model_validate(item))


@router.delete("/items/{item_id}", response_model=ResponseModel)
async def remove_cart_item(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = CartService(db)
    success = await service.remove_item(current_user.id, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return ResponseModel(message="Item removed successfully")


@router.delete("/clear", response_model=ResponseModel)
async def clear_cart(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = CartService(db)
    await service.clear_cart(current_user.id)
    return ResponseModel(message="Cart cleared successfully")
