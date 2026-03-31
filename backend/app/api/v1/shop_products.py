from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...schemas.product import Product, ProductSimple
from ...schemas.common import ResponseModel, ListResponseModel, PageResult
from ...services.simple_product_service import SimpleProductService

router = APIRouter(prefix="/shop", tags=["商城商品"])


@router.get("/products/simple", response_model=ListResponseModel[ProductSimple])
async def get_shop_simple_products(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    keyword: Optional[str] = Query(None, description="关键词"),
    db: AsyncSession = Depends(get_db)
):
    """获取商城简单商品列表（只显示已上架）"""
    skip = (page - 1) * page_size
    service = SimpleProductService(db)
    items, total = await service.get_multi(
        category_id=category_id,
        status=1,
        keyword=keyword,
        skip=skip,
        limit=page_size
    )
    return ListResponseModel(
        data=[ProductSimple.model_validate(item) for item in items],
        total=total
    )


@router.get("/products/simple/{id}", response_model=ResponseModel[Product])
async def get_shop_simple_product(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取商城简单商品详情"""
    service = SimpleProductService(db)
    product = await service.get(id=id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    if product.status != 1:
        raise HTTPException(status_code=404, detail="商品已下架")
    return ResponseModel(data=Product.model_validate(product))
