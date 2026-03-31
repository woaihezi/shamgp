from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import BaseService
from ..models import InventoryRecord
from ..schemas import InventoryRecordCreate, InventoryRecordUpdate


class InventoryService(BaseService[InventoryRecord, InventoryRecordCreate, InventoryRecordUpdate]):
    def __init__(self):
        super().__init__(InventoryRecord)

    async def get_by_sku(self, db: AsyncSession, sku_id: int) -> Optional[InventoryRecord]:
        result = await db.execute(
            select(InventoryRecord).where(InventoryRecord.sku_id == sku_id)
        )
        return result.scalar_one_or_none()

    async def adjust_stock(
        self,
        db: AsyncSession,
        sku_id: int,
        quantity: int,
        is_add: bool = True
    ) -> Optional[InventoryRecord]:
        inventory = await self.get_by_sku(db, sku_id)
        if inventory:
            if is_add:
                inventory.total_stock += quantity
                inventory.available_stock += quantity
            else:
                inventory.total_stock -= quantity
                inventory.available_stock -= quantity
            await db.commit()
            await db.refresh(inventory)
        return inventory

    async def lock_stock(
        self,
        db: AsyncSession,
        sku_id: int,
        quantity: int
    ) -> Optional[InventoryRecord]:
        inventory = await self.get_by_sku(db, sku_id)
        if inventory and inventory.available_stock >= quantity:
            inventory.available_stock -= quantity
            inventory.locked_stock += quantity
            await db.commit()
            await db.refresh(inventory)
        return inventory

    async def unlock_stock(
        self,
        db: AsyncSession,
        sku_id: int,
        quantity: int
    ) -> Optional[InventoryRecord]:
        inventory = await self.get_by_sku(db, sku_id)
        if inventory and inventory.locked_stock >= quantity:
            inventory.available_stock += quantity
            inventory.locked_stock -= quantity
            await db.commit()
            await db.refresh(inventory)
        return inventory

    async def deduct_stock(
        self,
        db: AsyncSession,
        sku_id: int,
        quantity: int
    ) -> Optional[InventoryRecord]:
        inventory = await self.get_by_sku(db, sku_id)
        if inventory and inventory.locked_stock >= quantity:
            inventory.total_stock -= quantity
            inventory.locked_stock -= quantity
            await db.commit()
            await db.refresh(inventory)
        return inventory


inventory_service = InventoryService()
