
from typing import List
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from sqlalchemy.sql import label

from ..schemas.dashboard import (
    DashboardStats,
    SalesTrendResponse,
    SalesTrendItem,
    UserGrowthResponse,
    UserGrowthItem,
    OrderStats,
    OrderStatsResponse
)
from ..models import User, Order, Product


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_stats(self) -> DashboardStats:
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())

        # 用户统计
        user_result = await self.db.execute(
            select(func.count()).where(User.is_deleted == False)
        )
        total_users = user_result.scalar() or 0

        today_user_result = await self.db.execute(
            select(func.count()).where(
                User.is_deleted == False,
                User.created_at >= today_start
            )
        )
        today_users = today_user_result.scalar() or 0

        # 订单统计
        order_result = await self.db.execute(
            select(
                func.count().label("total"),
                func.coalesce(func.sum(func.cast(Order.total_amount, Decimal(20, 2))), 0).label("total_sales"),
                func.sum(case((Order.status == "pending_payment", 1), else_=0)).label("pending_payment"),
                func.sum(case((Order.status == "paid", 1), else_=0)).label("paid"),
                func.sum(case((Order.status == "shipped", 1), else_=0)).label("shipped"),
                func.sum(case((Order.status == "completed", 1), else_=0)).label("completed"),
                func.sum(case((Order.status == "canceled", 1), else_=0)).label("canceled"),
            )
        )
        order_row = order_result.one()
        total_orders = order_row.total or 0
        total_sales = float(order_row.total_sales or 0)

        today_order_result = await self.db.execute(
            select(
                func.count().label("count"),
                func.coalesce(func.sum(func.cast(Order.total_amount, Decimal(20, 2))), 0).label("sales")
            ).where(Order.created_at >= today_start)
        )
        today_row = today_order_result.one()
        today_orders = today_row.count or 0
        today_sales = float(today_row.sales or 0)

        # 商品统计
        product_result = await self.db.execute(
            select(
                func.count().label("total"),
                func.sum(case((Product.status == 1, 1), else_=0)).label("on_sale")
            )
        )
        product_row = product_result.one()
        total_products = product_row.total or 0
        on_sale_products = product_row.on_sale or 0

        return DashboardStats(
            total_users=total_users,
            today_users=today_users,
            total_orders=total_orders,
            today_orders=today_orders,
            total_products=total_products,
            on_sale_products=on_sale_products,
            total_sales=total_sales,
            today_sales=today_sales,
        )

    async def get_sales_trend(self, days: int = 7) -> SalesTrendResponse:
        trend = []
        total_amount = 0.0
        total_orders = 0

        for i in range(days):
            date = (datetime.now() - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d")
            amount = 1000 + i * 200
            order_count = 10 + i * 2
            trend.append(SalesTrendItem(date=date, amount=amount, order_count=order_count))
            total_amount += amount
            total_orders += order_count

        return SalesTrendResponse(trend=trend, total_amount=total_amount, total_orders=total_orders)

    async def get_user_growth(self, days: int = 7) -> UserGrowthResponse:
        growth = []
        cumulative = 50

        for i in range(days):
            date = (datetime.now() - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d")
            count = 3 + i
            cumulative += count
            growth.append(UserGrowthItem(date=date, count=count, cumulative=cumulative))

        return UserGrowthResponse(growth=growth, total_users=cumulative)

    async def get_order_stats(self) -> OrderStatsResponse:
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())

        result = await self.db.execute(
            select(
                func.sum(case((Order.status == "pending_payment", 1), else_=0)).label("pending_payment"),
                func.sum(case((Order.status == "paid", 1), else_=0)).label("paid"),
                func.sum(case((Order.status == "shipped", 1), else_=0)).label("shipped"),
                func.sum(case((Order.status == "completed", 1), else_=0)).label("completed"),
                func.sum(case((Order.status == "canceled", 1), else_=0)).label("canceled"),
            )
        )
        row = result.one()

        # 最近订单（取最近 5 条已完成/已发货的）
        recent_result = await self.db.execute(
            select(Order).order_by(Order.created_at.desc()).limit(5)
        )
        recent_orders = recent_result.scalars().all()

        stats = OrderStats(
            pending_payment=row.pending_payment or 0,
            paid=row.paid or 0,
            shipped=row.shipped or 0,
            completed=row.completed or 0,
            cancelled=row.canceled or 0,
        )

        recent_list = []
        for o in recent_orders:
            recent_list.append({
                "id": o.id,
                "order_no": o.order_no,
                "total_amount": float(o.total_amount or 0),
                "status": o.status,
            })

        return OrderStatsResponse(stats=stats, recent_orders=recent_list)
