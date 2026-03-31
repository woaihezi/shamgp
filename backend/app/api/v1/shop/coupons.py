from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import ResponseModel
from app.schemas.coupon import (
    Coupon, CouponReceiveRecord, CouponReceiveRecordCreate
)
from app.services.coupon_service import coupon_service, coupon_receive_record_service

router = APIRouter(prefix="/coupons", tags=["shop-coupons"])


@router.get("/available", response_model=ResponseModel[list[Coupon]])
async def get_available_coupons(
    db: AsyncSession = Depends(get_db),
):
    coupons = await coupon_service.get_available_coupons(db)
    return ResponseModel(data=coupons)


@router.get("/my", response_model=ResponseModel[list[CouponReceiveRecord]])
async def get_my_coupons(
    user_id: int = Query(..., description="用户ID"),
    status: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    coupons = await coupon_receive_record_service.get_user_coupons(db, user_id, status=status)
    return ResponseModel(data=coupons)


@router.post("/receive", response_model=ResponseModel[CouponReceiveRecord])
async def receive_coupon(
    coupon_in: CouponReceiveRecordCreate,
    user_id: int = Query(..., description="用户ID"),
    db: AsyncSession = Depends(get_db),
):
    record = await coupon_receive_record_service.receive_coupon(db, user_id, coupon_in.coupon_id)
    if not record:
        raise HTTPException(status_code=400, detail="Failed to receive coupon")
    return ResponseModel(data=record)


@router.post("/use/{record_id}", response_model=ResponseModel[CouponReceiveRecord])
async def use_coupon(
    record_id: int,
    order_id: int = Query(..., description="订单ID"),
    db: AsyncSession = Depends(get_db),
):
    record = await coupon_receive_record_service.use_coupon(db, record_id, order_id)
    if not record:
        raise HTTPException(status_code=400, detail="Failed to use coupon")
    return ResponseModel(data=record)


@router.get("/calculate-discount/{record_id}")
async def calculate_discount(
    record_id: int,
    order_amount: float = Query(..., description="订单金额"),
    db: AsyncSession = Depends(get_db),
):
    from decimal import Decimal
    discount = await coupon_receive_record_service.calculate_discount(
        db, record_id, Decimal(str(order_amount))
    )
    if discount is None:
        raise HTTPException(status_code=400, detail="Invalid coupon or order amount")
    return ResponseModel(data={"discount": float(discount)})
