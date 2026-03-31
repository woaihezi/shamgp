from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.services.favorite_service import favorite_service
from app.services.product_service import product_spu_service

router = APIRouter()


@router.post("", response_model=dict)
async def add_favorite(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorite = await favorite_service.add_favorite(db, current_user.id, product_id)
    return {"code": 200, "data": favorite}


@router.delete("/{product_id}", response_model=dict)
async def remove_favorite(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await favorite_service.remove_favorite(db, current_user.id, product_id)
    return {"code": 200, "message": "已取消收藏"}


@router.get("", response_model=dict)
async def get_favorites(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorites = await favorite_service.get_user_favorites(db, current_user.id)
    product_ids = [f.product_id for f in favorites]
    products = []
    if product_ids:
        for pid in product_ids:
            product = await product_spu_service.get(db, pid)
            if product:
                products.append(product)
    return {"code": 200, "data": products}
