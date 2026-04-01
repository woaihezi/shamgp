from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime
import random
import string
from ..models.order import Order, OrderItem, Refund, OrderStatus, PayStatus
from ..models.cart import CartItem
from ..models.address import Address
from ..models.product import Product, ProductSku
from ..schemas.order import OrderCreate, OrderUpdate, OrderSchema, OrderItemSchema, RefundCreate, RefundSchema
from .address_service import AddressService
from .cart_service import CartService
from .inventory_service import inventory_service


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _generate_order_no(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"ORD{timestamp}{random_str}"

    def _generate_refund_no(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"REF{timestamp}{random_str}"

    async def create_order(self, user_id: int, order_in: OrderCreate) -> Order:
        address = await AddressService(self.db).get_address(user_id, order_in.address_id)
        if not address:
            raise ValueError("Address not found")

        cart_items = await CartService(self.db).get_selected_items(user_id, order_in.cart_item_ids)
        if not cart_items:
            raise ValueError("No selected cart items")

        order_no = self._generate_order_no()
        total_amount = 0.0
        order_items = []

        for cart_item in cart_items:
            result = await self.db.execute(select(Product).where(Product.id == cart_item.product_id))
            product = result.scalar_one_or_none()
            if not product:
                continue
            if product.stock < cart_item.quantity:
                raise ValueError(f"Insufficient stock for product {product.name}")

            item_total = float(product.price) * cart_item.quantity
            total_amount += item_total

            order_item = OrderItem(
                product_id=product.id,
                product_name=product.name,
                product_image=product.cover_image,
                sku_id=cart_item.sku_id,
                price=product.price,
                quantity=cart_item.quantity,
                total_amount=item_total
            )
            order_items.append(order_item)
            product.stock -= cart_item.quantity
            product.sales += cart_item.quantity

        order = Order(
            order_no=order_no,
            user_id=user_id,
            total_amount=total_amount,
            pay_amount=total_amount,
            discount_amount=0,
            freight_amount=0,
            status=OrderStatus.PENDING_PAYMENT,
            pay_status=PayStatus.UNPAID,
            consignee_name=address.consignee_name,
            consignee_phone=address.consignee_phone,
            consignee_address=f"{address.province}{address.city}{address.district}{address.detail_address}",
            remark=order_in.remark,
            items=order_items
        )

        self.db.add(order)
        for cart_item in cart_items:
            cart_item.is_deleted = True

        await self.db.flush()  # flush without commit to get order.id

        # 扣减 SKU 库存
        from .inventory_service import inventory_service
        for item in order.items:
            sku_id = item.sku_id if item.sku_id else None
            if sku_id is None:
                # 没有 SKU，降级到产品级扣减（已在上方直接处理 product.stock）
                continue
            deduct_result = await inventory_service.deduct_stock_for_order(
                self.db, sku_id, item.quantity, order.id
            )
            if not deduct_result["success"]:
                await self.db.rollback()
                raise ValueError(f"SKU {sku_id} 库存不足：{deduct_result['error']}")

        # Eager load items before returning
        result = await self.db.execute(
            select(Order)
            .where(Order.id == order.id)
            .options(selectinload(Order.items))
        )
        order = result.scalar_one()

        await self.db.commit()
        return order

    async def get_orders(self, user_id: Optional[int] = None, status: Optional[str] = None, 
                        page: int = 1, page_size: int = 20) -> tuple[List[Order], int]:
        query = select(Order).where(Order.is_deleted == False)
        
        if user_id:
            query = query.where(Order.user_id == user_id)
        if status:
            query = query.where(Order.status == status)
        
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()

        query = query.order_by(Order.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        query = query.options(selectinload(Order.items))
        
        result = await self.db.execute(query)
        orders = list(result.scalars().all())
        
        return orders, total

    async def get_order(self, order_id: int, user_id: Optional[int] = None) -> Optional[Order]:
        query = select(Order).where(Order.id == order_id, Order.is_deleted == False)
        if user_id:
            query = query.where(Order.user_id == user_id)
        query = query.options(selectinload(Order.items))
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_order_by_no(self, order_no: str, user_id: Optional[int] = None) -> Optional[Order]:
        query = select(Order).where(Order.order_no == order_no, Order.is_deleted == False)
        if user_id:
            query = query.where(Order.user_id == user_id)
        query = query.options(selectinload(Order.items))
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_order_status(self, order_id: int, status: str, user_id: Optional[int] = None) -> Optional[Order]:
        order = await self.get_order(order_id, user_id)
        if not order:
            return None

        order.status = status
        
        if status == OrderStatus.PAID:
            order.pay_status = PayStatus.PAID
            order.pay_time = datetime.now()
        elif status == OrderStatus.SHIPPED:
            order.delivery_time = datetime.now()
        elif status == OrderStatus.COMPLETED:
            order.receive_time = datetime.now()
        elif status == OrderStatus.CANCELED:
            order.cancel_time = datetime.now()
        elif status == OrderStatus.REFUNDING:
            pass
        elif status == OrderStatus.REFUNDED:
            order.pay_status = PayStatus.REFUNDED
            order.refund_time = datetime.now()

        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def update_order(self, order_id: int, order_in: OrderUpdate, user_id: Optional[int] = None) -> Optional[Order]:
        order = await self.get_order(order_id, user_id)
        if not order:
            return None

        update_data = order_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(order, field, value)

        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def cancel_order(self, order_id: int, cancel_reason: str, user_id: Optional[int] = None) -> Optional[Order]:
        order = await self.get_order(order_id, user_id)
        if not order or order.status not in [OrderStatus.PENDING_PAYMENT]:
            return None

        for item in order.items:
            result = await self.db.execute(select(Product).where(Product.id == item.product_id))
            product = result.scalar_one_or_none()
            if product:
                product.stock += item.quantity
                product.sales -= item.quantity
            # 恢复 SKU 库存
            sku_id = item.sku_id if item.sku_id else None
            if sku_id is not None:
                inv_result = await self.db.execute(
                    select(ProductSku).where(ProductSku.id == sku_id)
                )
                sku = inv_result.scalar_one_or_none()
                if sku:
                    sku.stock = (sku.stock or 0) + item.quantity

        order.status = OrderStatus.CANCELED
        order.cancel_time = datetime.now()
        order.cancel_reason = cancel_reason

        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def create_refund(self, user_id: int, refund_in: RefundCreate) -> Refund:
        order = await self.get_order(refund_in.order_id, user_id)
        if not order or order.status not in [OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.COMPLETED]:
            raise ValueError("Order not eligible for refund")

        refund_no = self._generate_refund_no()
        refund_amount = order.pay_amount
        
        if refund_in.order_item_id:
            result = await self.db.execute(select(OrderItem).where(OrderItem.id == refund_in.order_item_id))
            order_item = result.scalar_one_or_none()
            if order_item and order_item.order_id == refund_in.order_id:
                refund_amount = float(order_item.total_amount)

        refund = Refund(
            order_id=refund_in.order_id,
            order_item_id=refund_in.order_item_id,
            refund_no=refund_no,
            user_id=user_id,
            refund_amount=refund_amount,
            refund_reason=refund_in.refund_reason,
            refund_type=refund_in.refund_type,
            status="pending"
        )

        self.db.add(refund)
        order.status = OrderStatus.REFUNDING
        
        await self.db.commit()
        await self.db.refresh(refund)
        return refund

    async def get_refunds(self, user_id: Optional[int] = None, order_id: Optional[int] = None) -> List[Refund]:
        query = select(Refund).where(Refund.is_deleted == False)
        if user_id:
            query = query.where(Refund.user_id == user_id)
        if order_id:
            query = query.where(Refund.order_id == order_id)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_refund(self, refund_id: int, user_id: Optional[int] = None) -> Optional[Refund]:
        query = select(Refund).where(Refund.id == refund_id, Refund.is_deleted == False)
        if user_id:
            query = query.where(Refund.user_id == user_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def add_status_log(
        self, db: AsyncSession, order_id: int, new_status: str,
        old_status: Optional[str] = None, operator_type: str = "system",
        operator_id: Optional[int] = None, remark: Optional[str] = None
    ):
        from ..models.order_status_log import OrderStatusLog
        log = OrderStatusLog(
            order_id=order_id,
            old_status=old_status,
            new_status=new_status,
            operator_type=operator_type,
            operator_id=operator_id,
            remark=remark
        )
        db.add(log)
        await db.commit()
        await db.refresh(log)
        return log
