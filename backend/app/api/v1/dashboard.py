
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.database import get_db
from ...schemas.common import ResponseModel
from ...schemas.dashboard import (
    DashboardStats,
    SalesTrendResponse,
    UserGrowthResponse,
    OrderStatsResponse
)
from ...services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["仪表盘"])


@router.get("/stats", response_model=ResponseModel[DashboardStats])
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    service = DashboardService(db)
    stats = await service.get_stats()
    return ResponseModel(data=stats)


@router.get("/sales-trend", response_model=ResponseModel[SalesTrendResponse])
async def get_sales_trend(
    days: int = Query(7, ge=1, le=365, description="天数"),
    db: AsyncSession = Depends(get_db)
):
    service = DashboardService(db)
    trend = await service.get_sales_trend(days)
    return ResponseModel(data=trend)


@router.get("/user-growth", response_model=ResponseModel[UserGrowthResponse])
async def get_user_growth(
    days: int = Query(7, ge=1, le=365, description="天数"),
    db: AsyncSession = Depends(get_db)
):
    service = DashboardService(db)
    growth = await service.get_user_growth(days)
    return ResponseModel(data=growth)


@router.get("/order-stats", response_model=ResponseModel[OrderStatsResponse])
async def get_order_stats(db: AsyncSession = Depends(get_db)):
    service = DashboardService(db)
    stats = await service.get_order_stats()
    return ResponseModel(data=stats)
