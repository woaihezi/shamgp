from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import List, Optional
from ..models.cart import CartItem
from ..models.product import Product
from ..schemas.cart import CartItemCreate, CartItemUpdate, CartItemSchema, CartSummary


class CartService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_cart_items(self, user_id: int) -> List[CartItem]:
        result = await self.db.execute(
            select(CartItem).where(CartItem.user_id == user_id, CartItem.is_deleted == False)
        )
        return list(result.scalars().all())

    async def get_cart_summary(self, user_id: int) -> CartSummary:
        items = await self.get_cart_items(user_id)
        total_items = len(items)
        total_quantity = sum(item.quantity for item in items)
        total_amount = 0.0
        selected_items = []

        for item in items:
            if item.selected:
                result = await self.db.execute(select(Product).where(Product.id == item.product_id))
                product = result.scalar_one_or_none()
                if product:
                    total_amount += float(product.price) * item.quantity
                    item_schema = CartItemSchema.model_validate(item)
                    item_schema.product_name = product.name
                    item_schema.product_image = product.cover_image
                    item_schema.product_price = float(product.price)
                    selected_items.append(item_schema)

        return CartSummary(
            total_items=total_items,
            total_quantity=total_quantity,
            total_amount=total_amount,
            selected_items=selected_items
        )

    async def add_item(self, user_id: int, cart_item_in: CartItemCreate) -> CartItem:
        result = await self.db.execute(
            select(CartItem).where(
                CartItem.user_id == user_id,
                CartItem.product_id == cart_item_in.product_id,
                CartItem.sku_id == cart_item_in.sku_id,
                CartItem.is_deleted == False
            )
        )
        existing_item = result.scalar_one_or_none()

        if existing_item:
            existing_item.quantity += cart_item_in.quantity
            await self.db.commit()
            await self.db.refresh(existing_item)
            return existing_item
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_id=cart_item_in.product_id,
                sku_id=cart_item_in.sku_id,
                quantity=cart_item_in.quantity,
                selected=True
            )
            self.db.add(cart_item)
            await self.db.commit()
            await self.db.refresh(cart_item)
            return cart_item

    async def update_item(self, user_id: int, item_id: int, cart_item_in: CartItemUpdate) -> Optional[CartItem]:
        result = await self.db.execute(
            select(CartItem).where(
                CartItem.id == item_id,
                CartItem.user_id == user_id,
                CartItem.is_deleted == False
            )
        )
        cart_item = result.scalar_one_or_none()
        if not cart_item:
            return None

        update_data = cart_item_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(cart_item, field, value)

        await self.db.commit()
        await self.db.refresh(cart_item)
        return cart_item

    async def remove_item(self, user_id: int, item_id: int) -> bool:
        result = await self.db.execute(
            select(CartItem).where(
                CartItem.id == item_id,
                CartItem.user_id == user_id,
                CartItem.is_deleted == False
            )
        )
        cart_item = result.scalar_one_or_none()
        if not cart_item:
            return False

        cart_item.is_deleted = True
        await self.db.commit()
        return True

    async def clear_cart(self, user_id: int) -> None:
        await self.db.execute(
            update(CartItem)
            .where(CartItem.user_id == user_id, CartItem.is_deleted == False)
            .values(is_deleted=True)
        )
        await self.db.commit()

    async def get_selected_items(self, user_id: int, item_ids: List[int]) -> List[CartItem]:
        result = await self.db.execute(
            select(CartItem).where(
                CartItem.user_id == user_id,
                CartItem.id.in_(item_ids),
                CartItem.selected == True,
                CartItem.is_deleted == False
            )
        )
        return list(result.scalars().all())
