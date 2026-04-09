
from typing import List
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from ..schemas.dashboard import (
    DashboardStats,
    SalesTrendResponse,
    SalesTrendItem,
    UserGrowthResponse,
    UserGrowthItem,
    OrderStats,
    OrderStatsResponse
)
from ..models.user import User
from ..models.order import Order, OrderItem
from ..models.product import Product
from ..models.product_sku import ProductSku


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_stats(self) -> DashboardStats:
        stats = DashboardStats()
        
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        
        # 总用户数
        result = await self.db.execute(select(func.count(User.id)))
        stats.total_users = result.scalar() or 0
        
        # 今日新增用户
        result = await self.db.execute(
            select(func.count(User.id)).where(User.created_at >= today_start)
        )
        stats.today_users = result.scalar() or 0
        
        # 总订单数
        result = await self.db.execute(select(func.count(Order.id)))
        stats.total_orders = result.scalar() or 0
        
        # 今日订单数
        result = await self.db.execute(
            select(func.count(Order.id)).where(Order.created_at >= today_start)
        )
        stats.today_orders = result.scalar() or 0
        
        # 总商品数
        result = await self.db.execute(select(func.count(Product.id)))
        stats.total_products = result.scalar() or 0
        
        # 在售商品数
        result = await self.db.execute(
            select(func.count(Product.id)).where(Product.status == 1)
        )
        stats.on_sale_products = result.scalar() or 0
        
        # 总销售额
        result = await self.db.execute(
            select(func.sum(Order.pay_amount))
        )
        stats.total_sales = result.scalar() or 0.0
        
        # 今日销售额
        result = await self.db.execute(
            select(func.sum(Order.pay_amount)).where(Order.created_at >= today_start)
        )
        stats.today_sales = result.scalar() or 0.0
        
        return stats

    async def get_sales_trend(self, days: int = 7) -> SalesTrendResponse:
        trend = []
        total_amount = 0.0
        total_orders = 0
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=days - 1 - i))
            date_start = datetime.combine(date.date(), datetime.min.time())
            date_end = datetime.combine(date.date(), datetime.max.time())
            
            # 查询当天销售额
            amount_result = await self.db.execute(
                select(func.sum(Order.pay_amount)).where(
                    and_(Order.created_at >= date_start, Order.created_at <= date_end)
                )
            )
            amount = amount_result.scalar() or 0.0
            
            # 查询当天订单数
            order_result = await self.db.execute(
                select(func.count(Order.id)).where(
                    and_(Order.created_at >= date_start, Order.created_at <= date_end)
                )
            )
            order_count = order_result.scalar() or 0
            
            trend.append(SalesTrendItem(
                date=date.strftime("%Y-%m-%d"), 
                amount=amount, 
                order_count=order_count
            ))
            total_amount += amount
            total_orders += order_count
        
        return SalesTrendResponse(trend=trend, total_amount=total_amount, total_orders=total_orders)

    async def get_user_growth(self, days: int = 7) -> UserGrowthResponse:
        growth = []
        cumulative = 0
        
        # 获取总用户数作为初始累积值
        total_result = await self.db.execute(select(func.count(User.id)))
        total_users = total_result.scalar() or 0
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=days - 1 - i))
            date_start = datetime.combine(date.date(), datetime.min.time())
            date_end = datetime.combine(date.date(), datetime.max.time())
            
            # 查询当天新增用户数
            result = await self.db.execute(
                select(func.count(User.id)).where(
                    and_(User.created_at >= date_start, User.created_at <= date_end)
                )
            )
            count = result.scalar() or 0
            
            cumulative += count
            growth.append(UserGrowthItem(
                date=date.strftime("%Y-%m-%d"), 
                count=count, 
                cumulative=total_users - (total_users - cumulative)
            ))
        
        return UserGrowthResponse(growth=growth, total_users=total_users)

    async def get_order_stats(self) -> OrderStatsResponse:
        # 查询各状态订单数
        pending_result = await self.db.execute(
            select(func.count(Order.id)).where(Order.status == "pending_payment")
        )
        paid_result = await self.db.execute(
            select(func.count(Order.id)).where(Order.status == "paid")
        )
        shipped_result = await self.db.execute(
            select(func.count(Order.id)).where(Order.status == "shipped")
        )
        completed_result = await self.db.execute(
            select(func.count(Order.id)).where(Order.status == "completed")
        )
        cancelled_result = await self.db.execute(
            select(func.count(Order.id)).where(Order.status == "cancelled")
        )
        
        stats = OrderStats(
            pending_payment=pending_result.scalar() or 0,
            paid=paid_result.scalar() or 0,
            shipped=shipped_result.scalar() or 0,
            completed=completed_result.scalar() or 0,
            cancelled=cancelled_result.scalar() or 0
        )
        
        # 查询最近订单
        recent_orders_result = await self.db.execute(
            select(Order.id, Order.order_no, Order.total_amount, Order.status)
            .order_by(Order.created_at.desc())
            .limit(5)
        )
        recent_orders = []
        for order in recent_orders_result.all():
            recent_orders.append({
                "id": order.id,
                "order_no": order.order_no,
                "total_amount": float(order.total_amount),
                "status": order.status
            })
        
        return OrderStatsResponse(stats=stats, recent_orders=recent_orders)
