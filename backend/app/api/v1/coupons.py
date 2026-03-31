from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.coupon import Coupon
from app.models.user_coupon import UserCoupon

router = APIRouter()


@router.get("/available")
async def get_available_coupons(db: AsyncSession = Depends(get_db)):
    """获取当前可领取的优惠券"""
    now = datetime.now()
    result = await db.execute(
        select(Coupon).where(
            Coupon.status == 1,
            Coupon.remain_count > 0,
            (Coupon.start_time == None) | (Coupon.start_time <= now),
            (Coupon.end_time == None) | (Coupon.end_time >= now)
        ).order_by(Coupon.门槛金额)
    )
    coupons = result.scalars().all()
    return {"code": 200, "data": [
        {
            "id": c.id,
            "name": c.name,
            "code": c.code,
            "type": c.type,
            "满减金额": float(c.满减金额) if c.满减金额 else 0,
            "折扣": float(c.折扣) if c.折扣 else None,
            "门槛金额": float(c.门槛金额),
            "total_count": c.total_count,
            "remain_count": c.remain_count,
            "per_user_limit": c.per_user_limit,
            "start_time": c.start_time.isoformat() if c.start_time else None,
            "end_time": c.end_time.isoformat() if c.end_time else None,
            "description": c.description,
        }
        for c in coupons
    ]}


@router.post("/receive/{coupon_id}")
async def receive_coupon(
    coupon_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """领取优惠券"""
    result = await db.execute(select(Coupon).where(Coupon.id == coupon_id))
    coupon = result.scalar_one_or_none()
    if not coupon:
        return {"code": 404, "message": "优惠券不存在"}

    now = datetime.now()
    if coupon.start_time and coupon.start_time > now:
        return {"code": 400, "message": "优惠券尚未开始"}
    if coupon.end_time and coupon.end_time < now:
        return {"code": 400, "message": "优惠券已结束"}
    if coupon.remain_count <= 0:
        return {"code": 400, "message": "已领完"}

    uc_result = await db.execute(
        select(UserCoupon).where(
            UserCoupon.user_id == current_user.id,
            UserCoupon.coupon_id == coupon_id
        )
    )
    existing = uc_result.scalars().all()
    if len(existing) >= coupon.per_user_limit:
        return {"code": 400, "message": f"您已领取过该优惠券（限领{coupon.per_user_limit}张）"}

    coupon.remain_count = max(0, coupon.remain_count - 1)
    user_coupon = UserCoupon(
        user_id=current_user.id,
        coupon_id=coupon_id,
        status=0
    )
    db.add(user_coupon)
    await db.commit()
    await db.refresh(user_coupon)
    return {"code": 200, "message": "领取成功", "data": {"id": user_coupon.id}}


@router.get("/my")
async def get_my_coupons(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取我的优惠券"""
    result = await db.execute(
        select(UserCoupon, Coupon).join(Coupon).where(
            UserCoupon.user_id == current_user.id
        ).order_by(UserCoupon.created_at.desc())
    )
    rows = result.all()
    data = []
    for uc, c in rows:
        data.append({
            "id": uc.id,
            "coupon_id": c.id,
            "name": c.name,
            "code": c.code,
            "type": c.type,
            "满减金额": float(c.满减金额) if c.满减金额 else 0,
            "折扣": float(c.折扣) if c.折扣 else None,
            "门槛金额": float(c.门槛金额),
            "status": uc.status,
            "start_time": c.start_time.isoformat() if c.start_time else None,
            "end_time": c.end_time.isoformat() if c.end_time else None,
        })
    return {"code": 200, "data": data}


@router.post("/use")
async def use_coupon(
    coupon_id: int,
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """使用优惠券（结算时调用）"""
    result = await db.execute(
        select(UserCoupon).where(
            UserCoupon.id == coupon_id,
            UserCoupon.user_id == current_user.id,
            UserCoupon.status == 0
        )
    )
    uc = result.scalar_one_or_none()
    if not uc:
        return {"code": 400, "message": "优惠券不可用"}

    uc.status = 1
    uc.used_at = datetime.now()
    uc.order_id = order_id
    await db.commit()
    return {"code": 200, "message": "优惠券已使用"}
