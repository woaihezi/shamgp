from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from .base import BaseService
from ..models.favorite import Favorite


class FavoriteService(BaseService):
    def __init__(self):
        super().__init__(Favorite)

    async def get_user_favorites(self, db: AsyncSession, user_id: int) -> List[Favorite]:
        result = await db.execute(
            select(Favorite).where(Favorite.user_id == user_id).order_by(Favorite.created_at.desc())
        )
        return list(result.scalars().all())

    async def add_favorite(self, db: AsyncSession, user_id: int, product_id: int) -> Favorite:
        # 检查是否已收藏
        result = await db.execute(
            select(Favorite).where(Favorite.user_id == user_id, Favorite.product_id == product_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            return existing
        favorite = Favorite(user_id=user_id, product_id=product_id)
        db.add(favorite)
        await db.commit()
        await db.refresh(favorite)
        return favorite

    async def remove_favorite(self, db: AsyncSession, user_id: int, product_id: int) -> bool:
        result = await db.execute(
            delete(Favorite).where(Favorite.user_id == user_id, Favorite.product_id == product_id)
        )
        await db.commit()
        return result.rowcount > 0


favorite_service = FavoriteService()
