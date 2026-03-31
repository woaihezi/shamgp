from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.coupon import (
    Coupon, CouponCreate, CouponUpdate, CouponPageResult,
    CouponReceiveRecord, CouponReceiveRecordPageResult
)
from app.schemas.common import ResponseModel, PageParams
from app.services.coupon_service import coupon_service, coupon_receive_record_service

router = APIRouter(prefix="/coupons", tags=["admin-coupons"])


@router.get("", response_model=ResponseModel[CouponPageResult])
async def get_coupons(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    items, total = await coupon_service.get_multi_paginated(
        db, page=page, page_size=page_size, status=status
    )
    return ResponseModel(
        data=CouponPageResult(
            items=items,
            total=total,
            page=page,
            page_size=page_size
        )
    )


@router.get("/{coupon_id}", response_model=ResponseModel[Coupon])
async def get_coupon(coupon_id: int, db: AsyncSession = Depends(get_db)):
    coupon = await coupon_service.get(db, coupon_id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return ResponseModel(data=coupon)


@router.post("", response_model=ResponseModel[Coupon])
async def create_coupon(coupon_in: CouponCreate, db: AsyncSession = Depends(get_db)):
    coupon = await coupon_service.create(db, coupon_in.model_dump())
    return ResponseModel(data=coupon)


@router.put("/{coupon_id}", response_model=ResponseModel[Coupon])
async def update_coupon(
    coupon_id: int,
    coupon_in: CouponUpdate,
    db: AsyncSession = Depends(get_db),
):
    coupon = await coupon_service.get(db, coupon_id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    coupon = await coupon_service.update(db, coupon, coupon_in.model_dump(exclude_unset=True))
    return ResponseModel(data=coupon)


@router.delete("/{coupon_id}", response_model=ResponseModel[dict])
async def delete_coupon(coupon_id: int, db: AsyncSession = Depends(get_db)):
    coupon = await coupon_service.remove(db, coupon_id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return ResponseModel(data={"message": "Coupon deleted successfully"})


@router.get("/records/list", response_model=ResponseModel[CouponReceiveRecordPageResult])
async def get_coupon_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * page_size
    items = await coupon_receive_record_service.get_multi(db, skip=offset, limit=page_size)
    total = len(items)
    return ResponseModel(
        data=CouponReceiveRecordPageResult(
            items=items,
            total=total,
            page=page,
            page_size=page_size
        )
    )
