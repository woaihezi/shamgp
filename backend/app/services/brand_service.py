from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import BaseService
from ..models import Brand
from ..schemas import BrandCreate, BrandUpdate


class BrandService(BaseService[Brand, BrandCreate, BrandUpdate]):
    def __init__(self):
        super().__init__(Brand)

    async def get_active(self, db: AsyncSession) -> List[Brand]:
        result = await db.execute(
            select(Brand)
            .where(Brand.status == 1)
            .order_by(Brand.sort)
        )
        return result.scalars().all()


brand_service = BrandService()
