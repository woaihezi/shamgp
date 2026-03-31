
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


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_stats(self) -> DashboardStats:
        stats = DashboardStats()
        
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        
        stats.total_users = 100
        stats.today_users = 5
        stats.total_orders = 500
        stats.today_orders = 20
        stats.total_products = 300
        stats.on_sale_products = 250
        stats.total_sales = 150000.0
        stats.today_sales = 5000.0
        
        return stats

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
        stats = OrderStats(
            pending_payment=5,
            paid=15,
            shipped=8,
            completed=472,
            cancelled=20
        )
        
        recent_orders = [
            {"id": 1, "order_no": "ORD001", "total_amount": 199.0, "status": "completed"},
            {"id": 2, "order_no": "ORD002", "total_amount": 299.0, "status": "shipped"},
            {"id": 3, "order_no": "ORD003", "total_amount": 99.0, "status": "paid"},
        ]
        
        return OrderStatsResponse(stats=stats, recent_orders=recent_orders)
