from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models.user import User
from app.models.coupon import Coupon
from app.schemas.coupon import CouponCreate, CouponUpdate, CouponSchema
from app.schemas.common import ResponseModel, ListResponseModel
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=ListResponseModel[dict])
async def list_coupons(
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """List coupons (public)"""
    query = select(Coupon).where(Coupon.is_deleted == False, Coupon.status == "active")
    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar()
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    coupons = result.scalars().all()
    return ListResponseModel(
        data=[{
            "id": c.id, "name": c.name, "code": c.code, "type": c.type,
            "discount_value": c.discount_value, "min_order_amount": c.min_order_amount,
            "max_discount_amount": c.max_discount_amount,
            "start_date": str(c.start_date), "end_date": str(c.end_date),
            "total_count": c.total_count, "used_count": c.used_count,
        } for c in coupons],
        total=total or 0
    )


@router.post("/", response_model=ResponseModel[dict])
async def create_coupon(
    coupon_in: CouponCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create coupon (admin only)"""
    coupon = Coupon(**coupon_in.model_dump())
    db.add(coupon)
    await db.commit()
    await db.refresh(coupon)
    return ResponseModel(data={"id": coupon.id, "name": coupon.name})


@router.post("/verify", response_model=ResponseModel[dict])
async def verify_coupon(
    code: str = Query(..., description="优惠券码"),
    order_amount: float = Query(..., description="订单金额"),
    db: AsyncSession = Depends(get_db),
):
    """Verify if a coupon is valid for an order amount"""
    from app.services.coupon_service import CouponService
    service = CouponService(db)
    result = await service.verify_coupon(code, order_amount)
    return ResponseModel(data=result)
