from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ...models import Base
from ...schemas import (
    Category, CategoryCreate, CategoryUpdate, CategoryTree,
    ResponseBase, PageParams, PageResult
)
from ...services import category_service

router = APIRouter(prefix="/categories", tags=["商品分类管理"])


@router.get("/tree", response_model=ResponseBase[List[CategoryTree]])
async def get_category_tree():
    """获取分类树结构"""
    categories = await category_service.get_tree()
    return ResponseBase(data=categories)


@router.get("", response_model=ResponseBase[List[Category]])
async def get_categories(
    parent_id: Optional[int] = Query(None, description="父分类ID")
):
    """获取分类列表"""
    categories = await category_service.get_by_parent(parent_id=parent_id)
    return ResponseBase(data=categories)


@router.get("/{id}", response_model=ResponseBase[Category])
async def get_category(id: int):
    """获取分类详情"""
    category = await category_service.get(id=id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    return ResponseBase(data=category)


@router.post("", response_model=ResponseBase[Category])
async def create_category(obj_in: CategoryCreate):
    """创建分类"""
    category = await category_service.create(obj_in=obj_in)
    return ResponseBase(data=category)


@router.put("/{id}", response_model=ResponseBase[Category])
async def update_category(id: int, obj_in: CategoryUpdate):
    """更新分类"""
    category = await category_service.get(id=id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    category = await category_service.update(db_obj=category, obj_in=obj_in)
    return ResponseBase(data=category)


@router.delete("/{id}", response_model=ResponseBase[Category])
async def delete_category(id: int):
    """删除分类"""
    category = await category_service.remove(id=id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    return ResponseBase(data=category)
