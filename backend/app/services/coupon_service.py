from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime
from ..models.coupon import Coupon
from ..schemas.coupon import CouponCreate, CouponUpdate


class CouponService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_coupon(self, coupon_in: CouponCreate) -> Coupon:
        coupon = Coupon(**coupon_in.model_dump())
        self.db.add(coupon)
        await self.db.commit()
        await self.db.refresh(coupon)
        return coupon

    async def get_coupon(self, coupon_id: int) -> Optional[Coupon]:
        result = await self.db.execute(
            select(Coupon).where(Coupon.id == coupon_id, Coupon.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_coupon_by_code(self, code: str) -> Optional[Coupon]:
        result = await self.db.execute(
            select(Coupon).where(Coupon.code == code, Coupon.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def list_coupons(self, status: Optional[str] = None, page: int = 1, page_size: int = 20):
        query = select(Coupon).where(Coupon.is_deleted == False)
        if status:
            query = query.where(Coupon.status == status)
        query = query.order_by(Coupon.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_coupon(self, coupon_id: int, coupon_in: CouponUpdate) -> Optional[Coupon]:
        coupon = await self.get_coupon(coupon_id)
        if not coupon:
            return None
        for key, value in coupon_in.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(coupon, key, value)
        await self.db.commit()
        await self.db.refresh(coupon)
        return coupon

    async def verify_coupon(self, code: str, order_amount: float) -> dict:
        coupon = await self.get_coupon_by_code(code)
        if not coupon:
            return {"valid": False, "reason": "优惠券不存在"}
        if coupon.status != "active":
            return {"valid": False, "reason": "优惠券已停用"}
        now = datetime.now()
        if now < coupon.start_date or now > coupon.end_date:
            return {"valid": False, "reason": "优惠券已过期"}
        if order_amount < coupon.min_order_amount:
            return {"valid": False, "reason": f"订单金额需满{coupon.min_order_amount}元"}
        discount = coupon.discount_value
        if coupon.type == "discount":
            discount = order_amount * coupon.discount_value
            if coupon.max_discount_amount:
                discount = min(discount, coupon.max_discount_amount)
        return {"valid": True, "discount": round(discount, 2), "coupon_id": coupon.id}
