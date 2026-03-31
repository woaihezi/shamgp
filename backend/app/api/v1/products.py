from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...schemas.product import Product, ProductCreate, ProductUpdate, ProductSimple
from ...schemas.common import ResponseModel, ListResponseModel, PageResult
from ...services.simple_product_service import SimpleProductService
from ...api.deps import get_current_active_user
from ...models.user import User

router = APIRouter(tags=["商品管理"])


@router.get("/simple", response_model=ListResponseModel[ProductSimple])
async def get_simple_products(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    status: Optional[int] = Query(None, description="状态"),
    keyword: Optional[str] = Query(None, description="关键词"),
    db: AsyncSession = Depends(get_db)
):
    """获取简单商品列表（公开，无需认证）"""
    skip = (page - 1) * page_size
    service = SimpleProductService(db)
    items, total = await service.get_multi(
        category_id=category_id,
        status=status,
        keyword=keyword,
        skip=skip,
        limit=page_size
    )
    return ListResponseModel(
        data=[ProductSimple.model_validate(item) for item in items],
        total=total
    )


@router.get("/simple/{id}", response_model=ResponseModel[Product])
async def get_simple_product(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取简单商品详情（公开，无需认证）"""
    service = SimpleProductService(db)
    product = await service.get(id=id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return ResponseModel(data=Product.model_validate(product))


# --- 商城端别名路由（匹配前端 /api/v1/products 路径）---
@router.get("", response_model=ResponseModel[PageResult[ProductSimple]])
async def get_shop_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    keyword: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """商城商品列表（公开）"""
    skip = (page - 1) * page_size
    service = SimpleProductService(db)
    items, total = await service.get_multi(
        category_id=category_id,
        status=1,
        keyword=keyword,
        skip=skip,
        limit=page_size
    )
    return ResponseModel(data=PageResult(
        items=[ProductSimple.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size
    ))


@router.get("/{id}", response_model=ResponseModel[Product])
async def get_shop_product(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    """商城商品详情（公开）"""
    service = SimpleProductService(db)
    product = await service.get(id=id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return ResponseModel(data=Product.model_validate(product))


@router.post("/simple", response_model=ResponseModel[Product])
async def create_simple_product(
    obj_in: ProductCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """创建简单商品（需要登录）"""
    service = SimpleProductService(db)
    product = await service.create(obj_in=obj_in)
    return ResponseModel(data=Product.model_validate(product))


@router.put("/simple/{id}", response_model=ResponseModel[Product])
async def update_simple_product(
    id: int,
    obj_in: ProductUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新简单商品（需要登录）"""
    service = SimpleProductService(db)
    product = await service.get(id=id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    updated = await service.update(product, obj_in)
    return ResponseModel(data=Product.model_validate(updated))
