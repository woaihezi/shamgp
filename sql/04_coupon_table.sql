CREATE TABLE IF NOT EXISTS coupons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '优惠券名称',
    code VARCHAR(50) UNIQUE NOT NULL COMMENT '优惠券码',
    type VARCHAR(20) NOT NULL DEFAULT 'discount' COMMENT '类型: discount=折扣, fixed=满减',
    discount_value FLOAT NOT NULL COMMENT '优惠值(折扣率或满减金额)',
    min_order_amount FLOAT DEFAULT 0 COMMENT '最低订单金额',
    max_discount_amount FLOAT COMMENT '最高优惠金额(折扣时)',
    start_date TIMESTAMP NOT NULL COMMENT '开始时间',
    end_date TIMESTAMP NOT NULL COMMENT '结束时间',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态: active/inactive/expired',
    total_count INTEGER DEFAULT 0 COMMENT '总发放数量',
    used_count INTEGER DEFAULT 0 COMMENT '已使用数量',
    per_user_limit INTEGER DEFAULT 1 COMMENT '每人限领数量',
    is_public BOOLEAN DEFAULT TRUE COMMENT '是否公开领取',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);
