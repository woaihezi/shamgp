from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import (
    InventoryRecord, InventoryRecordCreate, InventoryRecordUpdate,
    ResponseBase
)
from ...services import inventory_service
from ...core.database import get_db
from ...api.deps import get_current_active_user
from ...models.user import User

router = APIRouter(prefix="/inventory", tags=["库存管理"])


@router.get("/sku/{sku_id}", response_model=ResponseBase[InventoryRecord])
async def get_inventory(sku_id: int):
    """获取SKU库存"""
    inventory = await inventory_service.get_by_sku(sku_id=sku_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    return ResponseBase(data=inventory)


@router.post("", response_model=ResponseBase[InventoryRecord])
async def create_inventory(obj_in: InventoryRecordCreate):
    """创建库存记录"""
    inventory = await inventory_service.create(obj_in=obj_in)
    return ResponseBase(data=inventory)


@router.put("/{id}", response_model=ResponseBase[InventoryRecord])
async def update_inventory(id: int, obj_in: InventoryRecordUpdate):
    """更新库存记录"""
    inventory = await inventory_service.get(id=id)
    if not inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    inventory = await inventory_service.update(db_obj=inventory, obj_in=obj_in)
    return ResponseBase(data=inventory)


@router.delete("/{id}", response_model=ResponseBase[InventoryRecord])
async def delete_inventory(id: int):
    """删除库存记录"""
    inventory = await inventory_service.remove(id=id)
    if not inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    return ResponseBase(data=inventory)


@router.post("/sku/{sku_id}/adjust", response_model=ResponseBase[InventoryRecord])
async def adjust_stock(sku_id: int, quantity: int, is_add: bool = True):
    """调整库存"""
    inventory = await inventory_service.adjust_stock(
        sku_id=sku_id,
        quantity=quantity,
        is_add=is_add
    )
    if not inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    return ResponseBase(data=inventory)


@router.post("/sku/{sku_id}/lock", response_model=ResponseBase[InventoryRecord])
async def lock_stock(sku_id: int, quantity: int):
    """锁定库存"""
    inventory = await inventory_service.lock_stock(
        sku_id=sku_id,
        quantity=quantity
    )
    if not inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在或库存不足")
    return ResponseBase(data=inventory)


@router.post("/sku/{sku_id}/unlock", response_model=ResponseBase[InventoryRecord])
async def unlock_stock(sku_id: int, quantity: int):
    """解锁库存"""
    inventory = await inventory_service.unlock_stock(
        sku_id=sku_id,
        quantity=quantity
    )
    if not inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    return ResponseBase(data=inventory)


@router.post("/sku/{sku_id}/deduct", response_model=ResponseBase[InventoryRecord])
async def deduct_stock(sku_id: int, quantity: int):
    """扣减库存"""
    inventory = await inventory_service.deduct_stock(
        sku_id=sku_id,
        quantity=quantity
    )
    if not inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    return ResponseBase(data=inventory)
