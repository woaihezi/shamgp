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

    async def deduct_stock_for_order(
        self,
        db: AsyncSession,
        sku_id: int,
        quantity: int,
        order_id: int
    ) -> dict:
        """
        真实扣减 SKU 库存（下单时调用）
        使用乐观锁：UPDATE ... WHERE stock >= quantity
        """
        from ..models.product_sku import ProductSku
        from ..models.inventory_record import InventoryRecord

        # 先查当前库存
        result = await db.execute(
            select(ProductSku).where(ProductSku.id == sku_id)
        )
        sku = result.scalar_one_or_none()
        if not sku:
            return {"success": False, "error": "SKU不存在"}

        old_stock = sku.stock or 0
        if old_stock < quantity:
            return {"success": False, "error": f"库存不足（当前{old_stock}，需要{quantity}）"}

        # 乐观锁扣减：UPDATE SET stock = stock - quantity WHERE id = ? AND stock >= quantity
        update_result = await db.execute(
            update(ProductSku)
            .where(ProductSku.id == sku_id, ProductSku.stock >= quantity)
            .values(stock=ProductSku.stock - quantity)
        )

        if update_result.rowcount == 0:
            # 并发冲突，库存被其他请求改掉了
            await db.rollback()
            return {"success": False, "error": "库存不足（并发冲突）"}

        new_stock = old_stock - quantity

        # 写入库存变动记录（更新已有记录或创建新记录）
        inv_result = await db.execute(
            select(InventoryRecord).where(InventoryRecord.sku_id == sku_id)
        )
        inv_record = inv_result.scalar_one_or_none()

        if inv_record:
            inv_record.order_id = order_id
            inv_record.change_type = "order_deduct"
            inv_record.quantity_change = -quantity
            inv_record.total_stock = new_stock
            inv_record.available_stock = new_stock
            inv_record.locked_stock = 0
        else:
            record = InventoryRecord(
                sku_id=sku_id,
                order_id=order_id,
                change_type="order_deduct",
                quantity_change=-quantity,
                total_stock=new_stock,
                available_stock=new_stock,
                locked_stock=0,
                warning_stock=0,
            )
            db.add(record)

        await db.flush()

        return {"success": True, "old_stock": old_stock, "new_stock": new_stock}


inventory_service = InventoryService()
