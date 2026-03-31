from datetime import datetime, UTC
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, or_
from decimal import Decimal

from app.models.coupon import Coupon, CouponReceiveRecord
from app.schemas.coupon import CouponCreate, CouponUpdate, CouponReceiveRecordCreate
from .base import BaseService


class CouponService(BaseService[Coupon]):
    def __init__(self):
        super().__init__(Coupon)

    async def get_multi_paginated(
        self, db: AsyncSession, *, page: int = 1, page_size: int = 10, status: Optional[int] = None
    ) -> tuple[List[Coupon], int]:
        query = select(Coupon)
        if status is not None:
            query = query.where(Coupon.status == status)
        query = query.order_by(Coupon.created_at.desc())
        
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        result = await db.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def get_available_coupons(self, db: AsyncSession) -> List[Coupon]:
        now = datetime.now(UTC)
        query = select(Coupon).where(
            and_(
                Coupon.status == 1,
                Coupon.valid_start_time <= now,
                Coupon.valid_end_time >= now,
                Coupon.used_count < Coupon.total_count,
            )
        ).order_by(Coupon.sort.asc() if hasattr(Coupon, 'sort') else Coupon.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())


class CouponReceiveRecordService(BaseService[CouponReceiveRecord]):
    def __init__(self):
        super().__init__(CouponReceiveRecord)

    async def receive_coupon(
        self, db: AsyncSession, user_id: int, coupon_id: int
    ) -> Optional[CouponReceiveRecord]:
        coupon_service = CouponService()
        coupon = await coupon_service.get(db, coupon_id)
        
        if not coupon:
            return None
        
        now = datetime.now(UTC)
        
        if coupon.status != 1:
            return None
        if coupon.valid_start_time > now or coupon.valid_end_time < now:
            return None
        if coupon.used_count >= coupon.total_count:
            return None
        
        existing_count = await self.get_user_coupon_count(db, user_id, coupon_id)
        if existing_count >= coupon.per_limit:
            return None
        
        receive_data = {
            "user_id": user_id,
            "coupon_id": coupon_id,
            "status": 1,
            "received_time": now,
            "expire_time": coupon.valid_end_time,
        }
        
        record = await self.create(db, receive_data)
        return record

    async def get_user_coupon_count(self, db: AsyncSession, user_id: int, coupon_id: int) -> int:
        query = select(func.count(CouponReceiveRecord.id)).where(
            and_(
                CouponReceiveRecord.user_id == user_id,
                CouponReceiveRecord.coupon_id == coupon_id,
            )
        )
        result = await db.execute(query)
        return result.scalar() or 0

    async def get_user_coupons(
        self, db: AsyncSession, user_id: int, status: Optional[int] = None
    ) -> List[CouponReceiveRecord]:
        query = select(CouponReceiveRecord).where(CouponReceiveRecord.user_id == user_id)
        if status is not None:
            query = query.where(CouponReceiveRecord.status == status)
        query = query.order_by(CouponReceiveRecord.received_time.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    async def use_coupon(
        self, db: AsyncSession, record_id: int, order_id: int
    ) -> Optional[CouponReceiveRecord]:
        record = await self.get(db, record_id)
        if not record or record.status != 1:
            return None
        
        now = datetime.now(UTC)
        update_data = {
            "status": 2,
            "order_id": order_id,
            "used_time": now,
        }
        
        return await self.update(db, record, update_data)

    async def calculate_discount(
        self, db: AsyncSession, record_id: int, order_amount: Decimal
    ) -> Optional[Decimal]:
        record = await self.get(db, record_id)
        if not record or record.status != 1:
            return None
        
        coupon_service = CouponService()
        coupon = await coupon_service.get(db, record.coupon_id)
        if not coupon:
            return None
        
        if order_amount < coupon.min_amount:
            return None
        
        if coupon.type == 1:
            return min(coupon.discount_value, order_amount)
        elif coupon.type == 2:
            return order_amount * (1 - coupon.discount_value)
        elif coupon.type == 3:
            return min(coupon.discount_value, order_amount)
        
        return None


coupon_service = CouponService()
coupon_receive_record_service = CouponReceiveRecordService()
