from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload, joinedload
from decimal import Decimal
from .base import BaseService
from ..models import ProductSpu, ProductSku, ProductImage, Category, Brand
from ..schemas import ProductSpuCreate, ProductSpuUpdate


class ProductSpuService(BaseService[ProductSpu, ProductSpuCreate, ProductSpuUpdate]):
    def __init__(self):
        super().__init__(ProductSpu)

    async def get_with_details(self, db: AsyncSession, id: int) -> Optional[ProductSpu]:
        result = await db.execute(
            select(ProductSpu)
            .where(ProductSpu.id == id)
            .options(
                joinedload(ProductSpu.category),
                joinedload(ProductSpu.brand),
                selectinload(ProductSpu.skus).selectinload(ProductSku.inventory),
                selectinload(ProductSpu.images)
            )
        )
        spu = result.scalar_one_or_none()
        if spu:
            spu.view_count += 1
            await db.commit()
        return spu

    async def get_simple_with_prices(
        self, db: AsyncSession, id: int
    ) -> Optional[ProductSpu]:
        result = await db.execute(
            select(ProductSpu)
            .where(ProductSpu.id == id)
            .options(
                joinedload(ProductSpu.category),
                joinedload(ProductSpu.brand),
                selectinload(ProductSpu.skus)
            )
        )
        return result.scalar_one_or_none()

    async def get_multi_with_filters(
        self,
        db: AsyncSession,
        *,
        category_id: Optional[int] = None,
        brand_id: Optional[int] = None,
        status: Optional[int] = None,
        keyword: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[ProductSpu], int]:
        query = select(ProductSpu)
        conditions = []

        if category_id is not None:
            conditions.append(ProductSpu.category_id == category_id)
        if brand_id is not None:
            conditions.append(ProductSpu.brand_id == brand_id)
        if status is not None:
            conditions.append(ProductSpu.status == status)
        if keyword:
            conditions.append(
                or_(
                    ProductSpu.name.contains(keyword),
                    ProductSpu.subtitle.contains(keyword)
                )
            )

        if conditions:
            query = query.where(and_(*conditions))

        query = query.options(
            joinedload(ProductSpu.category),
            joinedload(ProductSpu.brand),
            selectinload(ProductSpu.skus)
        ).order_by(ProductSpu.sort, ProductSpu.id.desc())

        count_query = select(func.count()).select_from(ProductSpu)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        result = await db.execute(query.offset(skip).limit(limit))
        items = result.scalars().unique().all()

        return items, total

    async def publish(self, db: AsyncSession, id: int) -> Optional[ProductSpu]:
        spu = await self.get(db, id=id)
        if spu:
            spu.status = 1
            await db.commit()
            await db.refresh(spu)
        return spu

    async def unpublish(self, db: AsyncSession, id: int) -> Optional[ProductSpu]:
        spu = await self.get(db, id=id)
        if spu:
            spu.status = 0
            await db.commit()
            await db.refresh(spu)
        return spu

    async def get_multi_by_ids(self, db: AsyncSession, ids: List[int]) -> List[ProductSpu]:
        if not ids:
            return []
        result = await db.execute(select(ProductSpu).where(ProductSpu.id.in_(ids)))
        return list(result.scalars().all())


product_spu_service = ProductSpuService()
