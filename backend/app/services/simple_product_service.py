from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload, joinedload
from decimal import Decimal

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class SimpleProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: int) -> Optional[Product]:
        result = await self.db.execute(
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.id == id)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        *,
        category_id: Optional[int] = None,
        status: Optional[int] = None,
        keyword: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Product], int]:
        query = select(Product)
        conditions = []

        if category_id is not None:
            conditions.append(Product.category_id == category_id)
        if status is not None:
            conditions.append(Product.status == status)
        if keyword:
            conditions.append(
                or_(
                    Product.name.contains(keyword),
                    Product.brief.contains(keyword)
                )
            )

        if conditions:
            query = query.where(and_(*conditions))

        query = query.options(
            joinedload(Product.category)
        ).order_by(Product.sort, Product.id.desc())

        count_query = select(func.count()).select_from(Product)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        result = await self.db.execute(query.offset(skip).limit(limit))
        items = result.scalars().unique().all()

        return items, total

    async def create(self, obj_in: ProductCreate) -> Product:
        db_obj = Product(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: Product, obj_in: ProductUpdate) -> Product:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def remove(self, id: int) -> Optional[Product]:
        result = await self.get(id=id)
        if result:
            result.is_deleted = True
            await self.db.commit()
        return result
