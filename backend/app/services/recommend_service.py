from typing import List, Optional
from datetime import datetime, UTC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models.recommend import AdSpace, Ad, Floor, FloorProduct
from app.schemas.recommend import (
    AdSpaceCreate, AdSpaceUpdate,
    AdCreate, AdUpdate,
    FloorCreate, FloorUpdate,
    FloorProductCreate, FloorProductUpdate
)
from .base import BaseService


class AdSpaceService(BaseService[AdSpace]):
    def __init__(self):
        super().__init__(AdSpace)

    async def get_multi_paginated(
        self, db: AsyncSession, *, page: int = 1, page_size: int = 10, status: Optional[int] = None
    ) -> tuple[List[AdSpace], int]:
        query = select(AdSpace)
        if status is not None:
            query = query.where(AdSpace.status == status)
        query = query.order_by(AdSpace.created_at.desc())
        
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        result = await db.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def get_by_code(self, db: AsyncSession, code: str) -> Optional[AdSpace]:
        result = await db.execute(select(AdSpace).where(AdSpace.code == code))
        return result.scalar_one_or_none()


class AdService(BaseService[Ad]):
    def __init__(self):
        super().__init__(Ad)

    async def get_multi_paginated(
        self, db: AsyncSession, *, page: int = 1, page_size: int = 10, ad_space_id: Optional[int] = None, status: Optional[int] = None
    ) -> tuple[List[Ad], int]:
        query = select(Ad)
        if ad_space_id is not None:
            query = query.where(Ad.ad_space_id == ad_space_id)
        if status is not None:
            query = query.where(Ad.status == status)
        query = query.order_by(Ad.sort.asc(), Ad.created_at.desc())
        
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        result = await db.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def get_active_ads(self, db: AsyncSession, ad_space_id: int) -> List[Ad]:
        now = datetime.now(UTC)
        query = select(Ad).where(
            and_(
                Ad.ad_space_id == ad_space_id,
                Ad.status == 1,
                (Ad.start_time.is_(None) | (Ad.start_time <= now)),
                (Ad.end_time.is_(None) | (Ad.end_time >= now)),
            )
        ).order_by(Ad.sort.asc())
        result = await db.execute(query)
        return list(result.scalars().all())

    async def increment_click(self, db: AsyncSession, ad_id: int) -> Optional[Ad]:
        ad = await self.get(db, ad_id)
        if ad:
            ad.click_count += 1
            await db.commit()
            await db.refresh(ad)
        return ad


class FloorService(BaseService[Floor]):
    def __init__(self):
        super().__init__(Floor)

    async def get_multi_paginated(
        self, db: AsyncSession, *, page: int = 1, page_size: int = 10, status: Optional[int] = None
    ) -> tuple[List[Floor], int]:
        query = select(Floor)
        if status is not None:
            query = query.where(Floor.status == status)
        query = query.order_by(Floor.sort.asc(), Floor.created_at.desc())
        
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        result = await db.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def get_active_floors(self, db: AsyncSession) -> List[Floor]:
        query = select(Floor).where(Floor.status == 1).order_by(Floor.sort.asc())
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_by_code(self, db: AsyncSession, code: str) -> Optional[Floor]:
        result = await db.execute(select(Floor).where(Floor.code == code))
        return result.scalar_one_or_none()

    async def get_floor_product_map(self, db: AsyncSession) -> dict[int, List[dict]]:
        """
        获取所有启用楼层ID对应的商品ID列表
        返回 { floor_id: [{product_id: int, sort: int}, ...] }
        """
        from app.models.product import Product
        floors = await self.get_active_floors(db)
        floor_ids = [f.id for f in floors]
        if not floor_ids:
            return {}

        # 批量查询楼层商品关联
        fp_query = select(FloorProduct).where(FloorProduct.floor_id.in_(floor_ids)).order_by(FloorProduct.sort)
        fp_result = await db.execute(fp_query)
        floor_products = list(fp_result.scalars().all())

        # 提取所有product_id
        prod_ids = list(set(fp.product_id for fp in floor_products))
        if not prod_ids:
            return {fid: [] for fid in floor_ids}

        # 批量查询商品基本信息
        prod_query = select(Product.id, Product.cover_image, Product.price, Product.original_price, Product.name).where(Product.id.in_(prod_ids))
        prod_result = await db.execute(prod_query)
        prod_map = {row[0]: {"cover_image": row[1], "price": float(row[2]) if row[2] else 0, "original_price": float(row[3]) if row[3] else None, "name": row[4]} for row in prod_result.fetchall()}

        # 组装
        result: dict[int, List[dict]] = {fid: [] for fid in floor_ids}
        for fp in floor_products:
            prod_info = prod_map.get(fp.product_id)
            if prod_info:
                result[fp.floor_id].append({
                    "product_id": fp.product_id,
                    "sort": fp.sort,
                    **prod_info
                })

        return result


class FloorProductService(BaseService[FloorProduct]):
    def __init__(self):
        super().__init__(FloorProduct)

    async def get_by_floor_id(self, db: AsyncSession, floor_id: int) -> List[FloorProduct]:
        query = select(FloorProduct).where(FloorProduct.floor_id == floor_id).order_by(FloorProduct.sort.asc())
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_product_ids_by_floor_id(self, db: AsyncSession, floor_id: int) -> List[int]:
        query = select(FloorProduct.product_id).where(FloorProduct.floor_id == floor_id).order_by(FloorProduct.sort.asc())
        result = await db.execute(query)
        return list(result.scalars().all())


ad_space_service = AdSpaceService()
ad_service = AdService()
floor_service = FloorService()
floor_product_service = FloorProductService()
