-- ========================================
-- 营销与运营配置模块 - 数据库表结构
-- ========================================

-- 1. 优惠券表
CREATE TABLE IF NOT EXISTS coupons (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '优惠券名称',
    type TINYINT NOT NULL DEFAULT 1 COMMENT '优惠券类型：1-满减券，2-折扣券，3-无门槛券',
    discount_value DECIMAL(10,2) NOT NULL COMMENT '优惠值：满减券为减多少钱，折扣券为折扣（如0.8表示8折）',
    min_amount DECIMAL(10,2) DEFAULT 0 COMMENT '最低使用金额',
    total_count INT NOT NULL DEFAULT 0 COMMENT '发放总量',
    used_count INT NOT NULL DEFAULT 0 COMMENT '已使用数量',
    per_limit INT NOT NULL DEFAULT 1 COMMENT '每人限领数量',
    valid_start_time TIMESTAMP NOT NULL COMMENT '有效期开始时间',
    valid_end_time TIMESTAMP NOT NULL COMMENT '有效期结束时间',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态：0-禁用，1-启用',
    description TEXT COMMENT '优惠券描述',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_coupons_status ON coupons(status);
CREATE INDEX idx_coupons_valid_time ON coupons(valid_start_time, valid_end_time);

-- 2. 用户优惠券领取记录表
CREATE TABLE IF NOT EXISTS coupon_receive_records (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    coupon_id BIGINT NOT NULL COMMENT '优惠券ID',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态：1-未使用，2-已使用，3-已过期',
    order_id BIGINT COMMENT '使用订单ID',
    used_time TIMESTAMP COMMENT '使用时间',
    received_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '领取时间',
    expire_time TIMESTAMP NOT NULL COMMENT '过期时间',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_coupon_records_user_id ON coupon_receive_records(user_id);
CREATE INDEX idx_coupon_records_coupon_id ON coupon_receive_records(coupon_id);
CREATE INDEX idx_coupon_records_status ON coupon_receive_records(status);

-- 3. 首页轮播图表
CREATE TABLE IF NOT EXISTS banners (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL COMMENT '轮播图标题',
    image_url VARCHAR(255) NOT NULL COMMENT '图片URL',
    link_url VARCHAR(255) COMMENT '跳转链接',
    sort INT NOT NULL DEFAULT 0 COMMENT '排序，数字越小越靠前',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态：0-禁用，1-启用',
    platform TINYINT NOT NULL DEFAULT 1 COMMENT '平台：1-PC端，2-移动端，3-全部',
    description TEXT COMMENT '描述',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_banners_status ON banners(status);
CREATE INDEX idx_banners_sort ON banners(sort);
CREATE INDEX idx_banners_platform ON banners(platform);

-- 4. 广告位表
CREATE TABLE IF NOT EXISTS ad_spaces (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '广告位名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '广告位编码',
    width INT COMMENT '宽度（像素）',
    height INT COMMENT '高度（像素）',
    description TEXT COMMENT '描述',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态：0-禁用，1-启用',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ad_spaces_code ON ad_spaces(code);
CREATE INDEX idx_ad_spaces_status ON ad_spaces(status);

-- 5. 广告表
CREATE TABLE IF NOT EXISTS ads (
    id BIGSERIAL PRIMARY KEY,
    ad_space_id BIGINT NOT NULL COMMENT '广告位ID',
    title VARCHAR(200) NOT NULL COMMENT '广告标题',
    image_url VARCHAR(255) NOT NULL COMMENT '图片URL',
    link_url VARCHAR(255) COMMENT '跳转链接',
    sort INT NOT NULL DEFAULT 0 COMMENT '排序，数字越小越靠前',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态：0-禁用，1-启用',
    start_time TIMESTAMP COMMENT '开始时间',
    end_time TIMESTAMP COMMENT '结束时间',
    click_count INT NOT NULL DEFAULT 0 COMMENT '点击次数',
    description TEXT COMMENT '描述',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ads_ad_space_id ON ads(ad_space_id);
CREATE INDEX idx_ads_status ON ads(status);
CREATE INDEX idx_ads_sort ON ads(sort);
CREATE INDEX idx_ads_time ON ads(start_time, end_time);

-- 6. 首页楼层表
CREATE TABLE IF NOT EXISTS floors (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '楼层名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '楼层编码',
    title VARCHAR(200) COMMENT '楼层标题',
    subtitle VARCHAR(200) COMMENT '楼层副标题',
    sort INT NOT NULL DEFAULT 0 COMMENT '排序，数字越小越靠前',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态：0-禁用，1-启用',
    style TINYINT NOT NULL DEFAULT 1 COMMENT '样式类型：1-单排，2-双排，3-网格',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_floors_code ON floors(code);
CREATE INDEX idx_floors_status ON floors(status);
CREATE INDEX idx_floors_sort ON floors(sort);

-- 7. 楼层商品关联表
CREATE TABLE IF NOT EXISTS floor_products (
    id BIGSERIAL PRIMARY KEY,
    floor_id BIGINT NOT NULL COMMENT '楼层ID',
    product_id BIGINT NOT NULL COMMENT '商品ID',
    sort INT NOT NULL DEFAULT 0 COMMENT '排序，数字越小越靠前',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_floor_products_floor_id ON floor_products(floor_id);
CREATE INDEX idx_floor_products_product_id ON floor_products(product_id);
CREATE INDEX idx_floor_products_sort ON floor_products(sort);
