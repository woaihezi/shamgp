
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class DashboardStats(BaseModel):
    total_users: int = Field(default=0, description="用户总数")
    today_users: int = Field(default=0, description="今日新增用户")
    total_orders: int = Field(default=0, description="订单总数")
    today_orders: int = Field(default=0, description="今日订单数")
    total_products: int = Field(default=0, description="商品总数")
    on_sale_products: int = Field(default=0, description="上架商品数")
    total_sales: float = Field(default=0.0, description="销售总额")
    today_sales: float = Field(default=0.0, description="今日销售额")


class SalesTrendItem(BaseModel):
    date: str = Field(description="日期")
    amount: float = Field(default=0.0, description="销售额")
    order_count: int = Field(default=0, description="订单数")


class SalesTrendResponse(BaseModel):
    trend: List[SalesTrendItem] = Field(description="销售趋势数据")
    total_amount: float = Field(default=0.0, description="总销售额")
    total_orders: int = Field(default=0, description="总订单数")


class UserGrowthItem(BaseModel):
    date: str = Field(description="日期")
    count: int = Field(default=0, description="新增用户数")
    cumulative: int = Field(default=0, description="累计用户数")


class UserGrowthResponse(BaseModel):
    growth: List[UserGrowthItem] = Field(description="用户增长数据")
    total_users: int = Field(default=0, description="总用户数")


class OrderStats(BaseModel):
    pending_payment: int = Field(default=0, description="待支付")
    paid: int = Field(default=0, description="已支付")
    shipped: int = Field(default=0, description="已发货")
    completed: int = Field(default=0, description="已完成")
    cancelled: int = Field(default=0, description="已取消")


class OrderStatsResponse(BaseModel):
    stats: OrderStats = Field(description="订单状态统计")
    recent_orders: List[dict] = Field(default_factory=list, description="最近订单")
