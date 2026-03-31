-- ========================================
-- Shamgp Shopping Platform Database Schema
-- ========================================

-- Enable timezone support
SET TIME ZONE 'UTC';

-- ========================================
-- 1. 通用管理模块表
-- ========================================

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    nickname VARCHAR(50),
    avatar VARCHAR(255),
    gender SMALLINT DEFAULT 0,
    status SMALLINT DEFAULT 1,
    user_type SMALLINT DEFAULT 1,
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);

-- 商品分类表
CREATE TABLE IF NOT EXISTS product_categories (
    id BIGSERIAL PRIMARY KEY,
    parent_id INTEGER DEFAULT 0,
    name VARCHAR(50) NOT NULL,
    code VARCHAR(50),
    image VARCHAR(255),
    description VARCHAR(255),
    sort INTEGER DEFAULT 0,
    level SMALLINT DEFAULT 1,
    status SMALLINT DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_categories_parent_id ON product_categories(parent_id);
CREATE INDEX IF NOT EXISTS idx_categories_level ON product_categories(level);
CREATE INDEX IF NOT EXISTS idx_categories_status ON product_categories(status);

-- 商品表
CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(100),
    brief VARCHAR(500),
    description TEXT,
    cover_image VARCHAR(255),
    images TEXT,
    price NUMERIC(10,2) DEFAULT 0.00 NOT NULL,
    original_price NUMERIC(10,2),
    cost_price NUMERIC(10,2),
    stock INTEGER DEFAULT 0 NOT NULL,
    sales INTEGER DEFAULT 0 NOT NULL,
    views INTEGER DEFAULT 0 NOT NULL,
    is_hot BOOLEAN DEFAULT FALSE,
    is_new BOOLEAN DEFAULT FALSE,
    is_recommend BOOLEAN DEFAULT FALSE,
    status SMALLINT DEFAULT 0,
    sort INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
CREATE INDEX IF NOT EXISTS idx_products_sales ON products(sales);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at);

-- ========================================
-- 2. 订单中心模块表
-- ========================================

-- 购物车表
CREATE TABLE IF NOT EXISTS cart_items (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    sku_id INTEGER,
    quantity INTEGER DEFAULT 1 NOT NULL,
    selected BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_cart_user_product_sku ON cart_items(user_id, product_id, sku_id);
CREATE INDEX IF NOT EXISTS idx_cart_user_id ON cart_items(user_id);

-- 收货地址表
CREATE TABLE IF NOT EXISTS addresses (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    consignee_name VARCHAR(50) NOT NULL,
    consignee_phone VARCHAR(20) NOT NULL,
    province VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    district VARCHAR(50) NOT NULL,
    detail_address VARCHAR(200) NOT NULL,
    zip_code VARCHAR(10),
    is_default BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_addresses_user_id ON addresses(user_id);

-- 订单表
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    order_no VARCHAR(64) NOT NULL,
    user_id INTEGER NOT NULL,
    total_amount NUMERIC(10,2) DEFAULT 0.00 NOT NULL,
    pay_amount NUMERIC(10,2) DEFAULT 0.00 NOT NULL,
    discount_amount NUMERIC(10,2) DEFAULT 0.00,
    freight_amount NUMERIC(10,2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'pending_payment' NOT NULL,
    pay_status SMALLINT DEFAULT 0 NOT NULL,
    pay_time TIMESTAMP WITH TIME ZONE,
    pay_type VARCHAR(20),
    consignee_name VARCHAR(50) NOT NULL,
    consignee_phone VARCHAR(20) NOT NULL,
    consignee_address VARCHAR(500) NOT NULL,
    remark VARCHAR(500),
    cancel_time TIMESTAMP WITH TIME ZONE,
    cancel_reason VARCHAR(255),
    delivery_time TIMESTAMP WITH TIME ZONE,
    receive_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_orders_order_no ON orders(order_no);
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);

-- 订单项表
CREATE TABLE IF NOT EXISTS order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    product_image VARCHAR(255),
    sku_id INTEGER,
    sku_specs VARCHAR(500),
    price NUMERIC(10,2) NOT NULL,
    quantity INTEGER NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);

-- 退款表
CREATE TABLE IF NOT EXISTS refunds (
    id BIGSERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    order_item_id INTEGER,
    refund_no VARCHAR(64) NOT NULL,
    user_id INTEGER NOT NULL,
    refund_amount NUMERIC(10,2) NOT NULL,
    refund_reason VARCHAR(500) NOT NULL,
    refund_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    audit_time TIMESTAMP WITH TIME ZONE,
    audit_user_id INTEGER,
    audit_remark VARCHAR(500),
    refund_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_refunds_refund_no ON refunds(refund_no);
CREATE INDEX IF NOT EXISTS idx_refunds_order_id ON refunds(order_id);
CREATE INDEX IF NOT EXISTS idx_refunds_user_id ON refunds(user_id);
CREATE INDEX IF NOT EXISTS idx_refunds_status ON refunds(status);

-- ========================================
-- 3. 初始化测试数据
-- ========================================

-- 插入测试用户
INSERT INTO users (username, password, email, nickname, status, user_type) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyTjY5cFvXy', 'admin@example.com', '管理员', 1, 2),
('testuser', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyTjY5cFvXy', 'test@example.com', '测试用户', 1, 1)
ON CONFLICT DO NOTHING;

-- 插入测试分类
INSERT INTO product_categories (parent_id, name, code, sort, level, status) VALUES
(0, '电子产品', 'electronics', 1, 1, 1),
(0, '服装鞋帽', 'clothing', 2, 1, 1),
(1, '手机', 'phones', 1, 2, 1),
(1, '电脑', 'computers', 2, 2, 1)
ON CONFLICT DO NOTHING;

-- 插入测试商品
INSERT INTO products (category_id, name, price, stock, status, is_hot, is_new) VALUES
(3, 'iPhone 15 Pro', 8999.00, 100, 1, true, true),
(3, 'Samsung Galaxy S24', 6999.00, 50, 1, true, false),
(4, 'MacBook Pro 14', 14999.00, 30, 1, false, true),
(4, 'ThinkPad X1 Carbon', 9999.00, 20, 1, false, false)
ON CONFLICT DO NOTHING;

-- 插入测试地址
INSERT INTO addresses (user_id, consignee_name, consignee_phone, province, city, district, detail_address, is_default) VALUES
(2, '张三', '13800138000', '北京市', '北京市', '朝阳区', '建国路88号SOHO现代城A座1001室', true),
(2, '李四', '13900139000', '上海市', '上海市', '浦东新区', '陆家嘴环路1000号恒生银行大厦', false)
ON CONFLICT DO NOTHING;
