from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from ...schemas import (
    Category, CategoryTree, Brand,
    ProductSpu, ProductSpuSimple, ProductSku,
    ProductImage, ResponseBase, PageResult
)
from ...services import (
    category_service, brand_service,
    product_spu_service, product_sku_service,
    product_image_service
)

router = APIRouter(prefix="/shop", tags=["商城商品"])


@router.get("/categories", response_model=ResponseBase[List[CategoryTree]])
async def get_shop_categories():
    """获取前台分类树"""
    categories = await category_service.get_tree()
    return ResponseBase(data=categories)


@router.get("/brands", response_model=ResponseBase[List[Brand]])
async def get_shop_brands():
    """获取前台品牌列表"""
    brands = await brand_service.get_active()
    return ResponseBase(data=brands)


@router.get("/products", response_model=ResponseBase[PageResult[ProductSpuSimple]])
async def get_shop_products(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    brand_id: Optional[int] = Query(None, description="品牌ID"),
    keyword: Optional[str] = Query(None, description="关键词")
):
    """获取前台商品列表（只显示已上架）"""
    skip = (page - 1) * page_size
    items, total = await product_spu_service.get_multi_with_filters(
        category_id=category_id,
        brand_id=brand_id,
        status=1,
        keyword=keyword,
        skip=skip,
        limit=page_size
    )
    
    for item in items:
        if item.skus:
            prices = [sku.price for sku in item.skus if sku.status == 1]
            if prices:
                item.min_price = float(min(prices))
                item.max_price = float(max(prices))
    
    return ResponseBase(data=PageResult(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    ))


@router.get("/products/{id}", response_model=ResponseBase[ProductSpu])
async def get_shop_product(id: int):
    """获取前台商品详情"""
    spu = await product_spu_service.get_with_details(id=id)
    if not spu:
        raise HTTPException(status_code=404, detail="商品不存在")
    if spu.status != 1:
        raise HTTPException(status_code=404, detail="商品已下架")
    return ResponseBase(data=spu)


@router.get("/products/{spu_id}/skus", response_model=ResponseBase[List[ProductSku]])
async def get_shop_product_skus(spu_id: int):
    """获取商品SKU列表"""
    skus = await product_sku_service.get_by_spu(spu_id=spu_id)
    skus = [sku for sku in skus if sku.status == 1]
    return ResponseBase(data=skus)


@router.get("/products/{spu_id}/images", response_model=ResponseBase[List[ProductImage]])
async def get_shop_product_images(spu_id: int, image_type: Optional[int] = None):
    """获取商品图片"""
    images = await product_image_service.get_by_spu(spu_id=spu_id, image_type=image_type)
    return ResponseBase(data=images)
