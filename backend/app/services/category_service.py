from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from .base import BaseService
from ..models import Category
from ..schemas import CategoryCreate, CategoryUpdate


class CategoryService(BaseService[Category, CategoryCreate, CategoryUpdate]):
    def __init__(self):
        super().__init__(Category)

    async def get_with_children(self, db: AsyncSession, id: int) -> Optional[Category]:
        result = await db.execute(
            select(Category)
            .where(Category.id == id)
            .options(selectinload(Category.children))
        )
        return result.scalar_one_or_none()

    async def get_tree(self, db: AsyncSession) -> List[Category]:
        result = await db.execute(
            select(Category)
            .where(Category.parent_id.is_(None))
            .options(selectinload(Category.children))
            .order_by(Category.sort)
        )
        return result.scalars().all()

    async def get_by_parent(
        self, db: AsyncSession, parent_id: Optional[int] = None
    ) -> List[Category]:
        query = select(Category)
        if parent_id is None:
            query = query.where(Category.parent_id.is_(None))
        else:
            query = query.where(Category.parent_id == parent_id)
        query = query.order_by(Category.sort)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_active(self, db: AsyncSession) -> List[Category]:
        result = await db.execute(
            select(Category)
            .where(Category.status == 1)
            .order_by(Category.sort)
        )
        return result.scalars().all()


category_service = CategoryService()
