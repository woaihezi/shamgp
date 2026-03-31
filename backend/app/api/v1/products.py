from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import (
    ProductSpu, ProductSpuCreate, ProductSpuUpdate, ProductSpuSimple,
    ProductSku, ProductSkuCreate, ProductSkuUpdate,
    ProductImage, ProductImageCreate, ProductImageUpdate,
    Brand, BrandCreate, BrandUpdate,
    ResponseBase, PageParams, PageResult
)
from ...services import (
    product_spu_service, product_sku_service,
    product_image_service, brand_service
)

router = APIRouter(tags=["商品管理"])


@router.get("/brands", response_model=ResponseBase[List[Brand]])
async def get_brands():
    """获取品牌列表"""
    brands = await brand_service.get_active()
    return ResponseBase(data=brands)


@router.get("/brands/{id}", response_model=ResponseBase[Brand])
async def get_brand(id: int):
    """获取品牌详情"""
    brand = await brand_service.get(id=id)
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    return ResponseBase(data=brand)


@router.post("/brands", response_model=ResponseBase[Brand])
async def create_brand(obj_in: BrandCreate):
    """创建品牌"""
    brand = await brand_service.create(obj_in=obj_in)
    return ResponseBase(data=brand)


@router.put("/brands/{id}", response_model=ResponseBase[Brand])
async def update_brand(id: int, obj_in: BrandUpdate):
    """更新品牌"""
    brand = await brand_service.get(id=id)
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    brand = await brand_service.update(db_obj=brand, obj_in=obj_in)
    return ResponseBase(data=brand)


@router.delete("/brands/{id}", response_model=ResponseBase[Brand])
async def delete_brand(id: int):
    """删除品牌"""
    brand = await brand_service.remove(id=id)
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    return ResponseBase(data=brand)


@router.get("/spus", response_model=ResponseBase[PageResult[ProductSpuSimple]])
async def get_spus(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    brand_id: Optional[int] = Query(None, description="品牌ID"),
    status: Optional[int] = Query(None, description="状态"),
    keyword: Optional[str] = Query(None, description="关键词")
):
    """获取商品SPU列表"""
    skip = (page - 1) * page_size
    items, total = await product_spu_service.get_multi_with_filters(
        category_id=category_id,
        brand_id=brand_id,
        status=status,
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


@router.get("/spus/{id}", response_model=ResponseBase[ProductSpu])
async def get_spu(id: int):
    """获取商品SPU详情"""
    spu = await product_spu_service.get_with_details(id=id)
    if not spu:
        raise HTTPException(status_code=404, detail="商品不存在")
    return ResponseBase(data=spu)


@router.post("/spus", response_model=ResponseBase[ProductSpu])
async def create_spu(obj_in: ProductSpuCreate):
    """创建商品SPU"""
    spu = await product_spu_service.create(obj_in=obj_in)
    return ResponseBase(data=spu)


@router.put("/spus/{id}", response_model=ResponseBase[ProductSpu])
async def update_spu(id: int, obj_in: ProductSpuUpdate):
    """更新商品SPU"""
    spu = await product_spu_service.get(id=id)
    if not spu:
        raise HTTPException(status_code=404, detail="商品不存在")
    spu = await product_spu_service.update(db_obj=spu, obj_in=obj_in)
    return ResponseBase(data=spu)


@router.delete("/spus/{id}", response_model=ResponseBase[ProductSpu])
async def delete_spu(id: int):
    """删除商品SPU"""
    spu = await product_spu_service.remove(id=id)
    if not spu:
        raise HTTPException(status_code=404, detail="商品不存在")
    return ResponseBase(data=spu)


@router.post("/spus/{id}/publish", response_model=ResponseBase[ProductSpu])
async def publish_spu(id: int):
    """上架商品"""
    spu = await product_spu_service.publish(id=id)
    if not spu:
        raise HTTPException(status_code=404, detail="商品不存在")
    return ResponseBase(data=spu)


@router.post("/spus/{id}/unpublish", response_model=ResponseBase[ProductSpu])
async def unpublish_spu(id: int):
    """下架商品"""
    spu = await product_spu_service.unpublish(id=id)
    if not spu:
        raise HTTPException(status_code=404, detail="商品不存在")
    return ResponseBase(data=spu)


@router.get("/spus/{spu_id}/skus", response_model=ResponseBase[List[ProductSku]])
async def get_skus(spu_id: int):
    """获取SKU列表"""
    skus = await product_sku_service.get_by_spu(spu_id=spu_id)
    return ResponseBase(data=skus)


@router.get("/skus/{id}", response_model=ResponseBase[ProductSku])
async def get_sku(id: int):
    """获取SKU详情"""
    sku = await product_sku_service.get(id=id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU不存在")
    return ResponseBase(data=sku)


@router.post("/skus", response_model=ResponseBase[ProductSku])
async def create_sku(obj_in: ProductSkuCreate):
    """创建SKU"""
    sku = await product_sku_service.create(obj_in=obj_in)
    return ResponseBase(data=sku)


@router.put("/skus/{id}", response_model=ResponseBase[ProductSku])
async def update_sku(id: int, obj_in: ProductSkuUpdate):
    """更新SKU"""
    sku = await product_sku_service.get(id=id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU不存在")
    sku = await product_sku_service.update(db_obj=sku, obj_in=obj_in)
    return ResponseBase(data=sku)


@router.delete("/skus/{id}", response_model=ResponseBase[ProductSku])
async def delete_sku(id: int):
    """删除SKU"""
    sku = await product_sku_service.remove(id=id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU不存在")
    return ResponseBase(data=sku)


@router.get("/spus/{spu_id}/images", response_model=ResponseBase[List[ProductImage]])
async def get_images(spu_id: int, image_type: Optional[int] = None):
    """获取商品图片"""
    images = await product_image_service.get_by_spu(spu_id=spu_id, image_type=image_type)
    return ResponseBase(data=images)


@router.post("/images", response_model=ResponseBase[ProductImage])
async def create_image(obj_in: ProductImageCreate):
    """创建商品图片"""
    image = await product_image_service.create(obj_in=obj_in)
    return ResponseBase(data=image)


@router.put("/images/{id}", response_model=ResponseBase[ProductImage])
async def update_image(id: int, obj_in: ProductImageUpdate):
    """更新商品图片"""
    image = await product_image_service.get(id=id)
    if not image:
        raise HTTPException(status_code=404, detail="图片不存在")
    image = await product_image_service.update(db_obj=image, obj_in=obj_in)
    return ResponseBase(data=image)


@router.delete("/images/{id}", response_model=ResponseBase[ProductImage])
async def delete_image(id: int):
    """删除商品图片"""
    image = await product_image_service.remove(id=id)
    if not image:
        raise HTTPException(status_code=404, detail="图片不存在")
    return ResponseBase(data=image)
