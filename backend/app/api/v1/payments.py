"""
支付模块 Mock 实现
模拟微信支付 / 支付宝 沙箱流程
状态机: pending_payment → paid → shipped → completed
"""
from datetime import datetime
from typing import Optional
import hashlib
import time
import random
import string
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.order import Order, OrderStatus, PayStatus
from app.schemas.common import ResponseModel
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter(tags=["支付"])


def _generate_trade_no() -> str:
    """生成支付流水号"""
    return f"PAY{datetime.now().strftime('%Y%m%d%H%M%S')}{''.join(random.choices(string.digits, k=10))}"


def _mock_sign(params: dict) -> str:
    """模拟签名"""
    sorted_items = sorted(params.items(), key=lambda x: x[0])
    sign_str = "&".join(f"{k}={v}" for k, v in sorted_items)
    return hashlib.md5(sign_str.encode()).hexdigest()[:16]


@router.post("/pay")
async def create_payment(
    order_id: int = Query(..., description="订单ID"),
    pay_channel: str = Query("mock_wechat", description="支付渠道: mock_wechat / mock_alipay"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    创建支付订单（Mock）
    模拟用户打开微信/支付宝扫码页
    返回支付链接和二维码
    """
    # 查订单
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.is_deleted == False)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 只能是本人订单
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your order")

    # 只能是待支付状态
    if order.status != OrderStatus.PENDING_PAYMENT:
        raise HTTPException(status_code=400, detail=f"Order status is {order.status}, cannot pay")

    trade_no = _generate_trade_no()
    pay_amount = float(order.pay_amount)

    # 构建 Mock 支付页面 URL
    pay_url = (
        f"http://localhost:8000/api/v1/payments/gateway"
        f"?trade_no={trade_no}&order_no={order.order_no}"
        f"&amount={pay_amount:.2f}&channel={pay_channel}"
    )

    return ResponseModel(data={
        "trade_no": trade_no,
        "order_id": order.id,
        "order_no": order.order_no,
        "pay_amount": pay_amount,
        "pay_channel": pay_channel,
        "pay_url": pay_url,
        "qrcode_url": f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={pay_url}",
        "expire_at": datetime.now().timestamp() + 30 * 60,  # 30分钟过期
        "status": "pending",
    })


@router.get("/gateway")
async def mock_payment_gateway(
    trade_no: str = Query(...),
    order_no: str = Query(...),
    amount: str = Query(...),
    channel: str = Query(...),
    action: str = Query("pay", description="pay / cancel"),
    db: AsyncSession = Depends(get_db),
):
    """
    Mock 支付网关页面
    浏览器访问此 URL 会展示一个模拟支付确认页
    action=pay → 模拟支付成功
    action=cancel → 模拟取消
    """
    if action == "cancel":
        return ResponseModel(data={
            "status": "cancelled",
            "trade_no": trade_no,
            "message": "Payment cancelled by user"
        })

    # 模拟支付成功
    result = await db.execute(
        select(Order).where(Order.order_no == order_no, Order.is_deleted == False)
    )
    order = result.scalar_one_or_none()
    if not order:
        return ResponseModel(data={"status": "error", "message": "Order not found"})

    if order.status == OrderStatus.PAID:
        return ResponseModel(data={"status": "already_paid", "trade_no": trade_no, "order_no": order_no})

    order.status = OrderStatus.PAID
    order.pay_status = PayStatus.PAID
    order.pay_time = datetime.now()
    order.pay_type = channel

    await db.commit()

    return ResponseModel(data={
        "status": "success",
        "trade_no": trade_no,
        "order_no": order_no,
        "pay_amount": amount,
        "pay_channel": channel,
        "pay_time": order.pay_time.isoformat(),
        "message": "Payment successful"
    })


@router.post("/callback/{trade_no}")
async def payment_callback(
    trade_no: str,
    status: str = Query(..., description="success / failed"),
    db: AsyncSession = Depends(get_db),
):
    """
    支付回调（Mock）
    微信/支付宝服务端回调此接口
    """
    if status == "success":
        # 在真实系统中这里会根据 trade_no 查本地支付记录
        # 并验证签名，然后更新订单状态
        return ResponseModel(data={"received": True, "trade_no": trade_no})

    return ResponseModel(data={"received": True, "trade_no": trade_no, "note": "failed status noted"})


@router.get("/{order_id}/status")
async def get_payment_status(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """查询订单支付状态"""
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.is_deleted == False)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your order")

    status_map = {
        OrderStatus.PENDING_PAYMENT: "unpaid",
        OrderStatus.PAID: "paid",
        OrderStatus.SHIPPED: "shipped",
        OrderStatus.COMPLETED: "completed",
        OrderStatus.CANCELED: "cancelled",
        OrderStatus.REFUNDING: "refunding",
        OrderStatus.REFUNDED: "refunded",
    }

    return ResponseModel(data={
        "order_id": order.id,
        "order_no": order.order_no,
        "status": status_map.get(order.status, order.status),
        "pay_status": order.pay_status,
        "pay_time": order.pay_time.isoformat() if order.pay_time else None,
        "pay_type": order.pay_type,
        "pay_amount": float(order.pay_amount),
    })
