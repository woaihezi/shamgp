from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.shipping_rule import ShippingRule


async def calculate_freight(db: AsyncSession, region: Optional[str], order_amount: float) -> float:
    """
    计算运费
    1. 查找匹配的运费规则
    2. 检查是否包邮（满free_threshold）
    3. 返回运费
    """
    # 查找适用的规则（优先按地区，再按全国默认）
    result = await db.execute(
        select(ShippingRule).where(ShippingRule.status == 1).order_by(
            # 有地区的优先
            ShippingRule.region.desc()
        )
    )
    rules = list(result.scalars().all())

    applicable_rule = None
    for rule in rules:
        if rule.region is None:
            # 全国默认规则，暂存
            if applicable_rule is None or applicable_rule.region is not None:
                applicable_rule = rule
        elif region and rule.region:
            # 地区匹配
            regions = [r.strip() for r in rule.region.split(',')]
            if any(r in region for r in regions):
                applicable_rule = rule
                break

    if not applicable_rule:
        return 0.0

    # 包邮检查
    if applicable_rule.free_threshold > 0 and order_amount >= float(applicable_rule.free_threshold):
        return 0.0

    # 计算运费（简化版，按首重计算）
    fee = float(applicable_rule.first_weight_fee)
    return fee


def calculate_freight_sync(region: Optional[str], order_amount: float) -> float:
    """同步版本，用于直接SQL查询"""
    import sqlite3
    import os

    db_path = os.path.join(os.path.dirname(__file__), 'shop_db.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 查找规则
    cur.execute("SELECT id, name, region, first_weight_fee, extra_weight_fee, free_threshold FROM shipping_rules WHERE status = 1 ORDER BY region DESC")
    rules = cur.fetchall()
    conn.close()

    applicable = None
    for rule in rules:
        if rule[2] is None:  # 全国默认
            if applicable is None:
                applicable = rule
        elif region and rule[2]:
            if any(r.strip() in region for r in rule[2].split(',')):
                applicable = rule
                break

    if not applicable:
        return 0.0

    if applicable[5] > 0 and order_amount >= applicable[5]:
        return 0.0

    return applicable[3]
