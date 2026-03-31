from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import BaseService
from ..models import ProductImage
from ..schemas import ProductImageCreate, ProductImageUpdate


class ProductImageService(BaseService[ProductImage, ProductImageCreate, ProductImageUpdate]):
    def __init__(self):
        super().__init__(ProductImage)

    async def get_by_spu(self, db: AsyncSession, spu_id: int, image_type: Optional[int] = None) -> List[ProductImage]:
        query = select(ProductImage).where(ProductImage.spu_id == spu_id)
        if image_type is not None:
            query = query.where(ProductImage.image_type == image_type)
        query = query.order_by(ProductImage.sort)
        result = await db.execute(query)
        return result.scalars().all()


product_image_service = ProductImageService()
