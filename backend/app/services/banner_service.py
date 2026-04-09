from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models.banner import Banner
from app.schemas.banner import BannerCreate, BannerUpdate
from .base import BaseService


class BannerService(BaseService[Banner, BannerCreate, BannerUpdate]):
    def __init__(self):
        super().__init__(Banner)

    async def get_multi_paginated(
        self, db: AsyncSession, *, page: int = 1, page_size: int = 10, status: Optional[int] = None, platform: Optional[int] = None
    ) -> tuple[List[Banner], int]:
        query = select(Banner)
        if status is not None:
            query = query.where(Banner.status == status)
        if platform is not None:
            query = query.where(Banner.platform == platform)
        query = query.order_by(Banner.sort.asc(), Banner.created_at.desc())
        
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        result = await db.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def get_active_banners(self, db: AsyncSession, platform: Optional[int] = None) -> List[Banner]:
        query = select(Banner).where(Banner.status == 1)
        if platform is not None:
            query = query.where(and_(Banner.platform.in_([platform, 3])))
        query = query.order_by(Banner.sort.asc(), Banner.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())


banner_service = BannerService()
