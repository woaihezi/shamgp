from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .base import BaseService
from ..models import ProductSku
from ..schemas import ProductSkuCreate, ProductSkuUpdate


class ProductSkuService(BaseService[ProductSku, ProductSkuCreate, ProductSkuUpdate]):
    def __init__(self):
        super().__init__(ProductSku)

    async def get_by_spu(self, db: AsyncSession, spu_id: int) -> List[ProductSku]:
        result = await db.execute(
            select(ProductSku)
            .where(ProductSku.spu_id == spu_id)
            .options(selectinload(ProductSku.inventory))
            .order_by(ProductSku.sort)
        )
        return result.scalars().all()

    async def get_by_code(self, db: AsyncSession, sku_code: str) -> Optional[ProductSku]:
        result = await db.execute(
            select(ProductSku)
            .where(ProductSku.sku_code == sku_code)
            .options(selectinload(ProductSku.inventory))
        )
        return result.scalar_one_or_none()


product_sku_service = ProductSkuService()
