-- =============================================
-- 商品中心数据库初始化脚本
-- 包含：分类、品牌、商品SPU、商品SKU、商品图片、库存记录
-- =============================================

-- 创建分类表
CREATE TABLE IF NOT EXISTS categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id BIGINT,
    sort INTEGER DEFAULT 0,
    icon VARCHAR(255),
    description TEXT,
    status INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

COMMENT ON TABLE categories IS '商品分类表';
COMMENT ON COLUMN categories.name IS '分类名称';
COMMENT ON COLUMN categories.parent_id IS '父分类ID';
COMMENT ON COLUMN categories.sort IS '排序';
COMMENT ON COLUMN categories.icon IS '分类图标';
COMMENT ON COLUMN categories.description IS '分类描述';
COMMENT ON COLUMN categories.status IS '状态: 0-禁用, 1-启用';

-- 创建品牌表
CREATE TABLE IF NOT EXISTS brands (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    logo VARCHAR(255),
    description TEXT,
    sort INTEGER DEFAULT 0,
    status INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE brands IS '品牌表';
COMMENT ON COLUMN brands.name IS '品牌名称';
COMMENT ON COLUMN brands.logo IS '品牌Logo';
COMMENT ON COLUMN brands.description IS '品牌描述';
COMMENT ON COLUMN brands.sort IS '排序';
COMMENT ON COLUMN brands.status IS '状态: 0-禁用, 1-启用';

-- 创建商品SPU表
CREATE TABLE IF NOT EXISTS product_spus (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    subtitle VARCHAR(500),
    category_id BIGINT NOT NULL,
    brand_id BIGINT,
    main_image VARCHAR(255),
    description TEXT,
    unit VARCHAR(50),
    status INTEGER DEFAULT 0,
    sort INTEGER DEFAULT 0,
    sales_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (brand_id) REFERENCES brands(id)
);

COMMENT ON TABLE product_spus IS '商品SPU表';
COMMENT ON COLUMN product_spus.name IS '商品名称';
COMMENT ON COLUMN product_spus.subtitle IS '副标题';
COMMENT ON COLUMN product_spus.category_id IS '分类ID';
COMMENT ON COLUMN product_spus.brand_id IS '品牌ID';
COMMENT ON COLUMN product_spus.main_image IS '主图';
COMMENT ON COLUMN product_spus.description IS '商品详情';
COMMENT ON COLUMN product_spus.unit IS '单位';
COMMENT ON COLUMN product_spus.status IS '状态: 0-下架, 1-上架';
COMMENT ON COLUMN product_spus.sort IS '排序';
COMMENT ON COLUMN product_spus.sales_count IS '销量';
COMMENT ON COLUMN product_spus.view_count IS '浏览量';

-- 创建商品SKU表
CREATE TABLE IF NOT EXISTS product_skus (
    id BIGSERIAL PRIMARY KEY,
    spu_id BIGINT NOT NULL,
    sku_code VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    specs TEXT,
    image VARCHAR(255),
    price DECIMAL(10,2) NOT NULL,
    original_price DECIMAL(10,2),
    cost_price DECIMAL(10,2),
    status INTEGER DEFAULT 1,
    sort INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (spu_id) REFERENCES product_spus(id) ON DELETE CASCADE
);

COMMENT ON TABLE product_skus IS '商品SKU表';
COMMENT ON COLUMN product_skus.spu_id IS 'SPU ID';
COMMENT ON COLUMN product_skus.sku_code IS 'SKU编码';
COMMENT ON COLUMN product_skus.name IS 'SKU名称';
COMMENT ON COLUMN product_skus.specs IS '规格JSON';
COMMENT ON COLUMN product_skus.image IS 'SKU图片';
COMMENT ON COLUMN product_skus.price IS '价格';
COMMENT ON COLUMN product_skus.original_price IS '原价';
COMMENT ON COLUMN product_skus.cost_price IS '成本价';
COMMENT ON COLUMN product_skus.status IS '状态: 0-禁用, 1-启用';
COMMENT ON COLUMN product_skus.sort IS '排序';

-- 创建商品图片表
CREATE TABLE IF NOT EXISTS product_images (
    id BIGSERIAL PRIMARY KEY,
    spu_id BIGINT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    image_type INTEGER DEFAULT 0,
    sort INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (spu_id) REFERENCES product_spus(id) ON DELETE CASCADE
);

COMMENT ON TABLE product_images IS '商品图片表';
COMMENT ON COLUMN product_images.spu_id IS 'SPU ID';
COMMENT ON COLUMN product_images.image_url IS '图片URL';
COMMENT ON COLUMN product_images.image_type IS '图片类型: 0-轮播图, 1-详情图';
COMMENT ON COLUMN product_images.sort IS '排序';

-- 创建库存记录表
CREATE TABLE IF NOT EXISTS inventory_records (
    id BIGSERIAL PRIMARY KEY,
    sku_id BIGINT NOT NULL UNIQUE,
    total_stock INTEGER DEFAULT 0,
    available_stock INTEGER DEFAULT 0,
    locked_stock INTEGER DEFAULT 0,
    warning_stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sku_id) REFERENCES product_skus(id) ON DELETE CASCADE
);

COMMENT ON TABLE inventory_records IS '库存记录表';
COMMENT ON COLUMN inventory_records.sku_id IS 'SKU ID';
COMMENT ON COLUMN inventory_records.total_stock IS '总库存';
COMMENT ON COLUMN inventory_records.available_stock IS '可用库存';
COMMENT ON COLUMN inventory_records.locked_stock IS '锁定库存';
COMMENT ON COLUMN inventory_records.warning_stock IS '预警库存';

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_categories_parent_id ON categories(parent_id);
CREATE INDEX IF NOT EXISTS idx_categories_status ON categories(status);
CREATE INDEX IF NOT EXISTS idx_brands_status ON brands(status);
CREATE INDEX IF NOT EXISTS idx_product_spus_category_id ON product_spus(category_id);
CREATE INDEX IF NOT EXISTS idx_product_spus_brand_id ON product_spus(brand_id);
CREATE INDEX IF NOT EXISTS idx_product_spus_status ON product_spus(status);
CREATE INDEX IF NOT EXISTS idx_product_skus_spu_id ON product_skus(spu_id);
CREATE INDEX IF NOT EXISTS idx_product_skus_sku_code ON product_skus(sku_code);
CREATE INDEX IF NOT EXISTS idx_product_skus_status ON product_skus(status);
CREATE INDEX IF NOT EXISTS idx_product_images_spu_id ON product_images(spu_id);
CREATE INDEX IF NOT EXISTS idx_inventory_records_sku_id ON inventory_records(sku_id);

-- =============================================
-- 插入示例数据
-- =============================================

-- 插入分类数据
INSERT INTO categories (name, parent_id, sort, status) VALUES
('电子产品', NULL, 1, 1),
('服装', NULL, 2, 1),
('食品', NULL, 3, 1),
('手机', 1, 1, 1),
('电脑', 1, 2, 1),
('男装', 2, 1, 1),
('女装', 2, 2, 1);

-- 插入品牌数据
INSERT INTO brands (name, sort, status) VALUES
('Apple', 1, 1),
('Samsung', 2, 1),
('华为', 3, 1),
('Nike', 4, 1),
('小米', 5, 1);

-- 插入商品SPU数据
INSERT INTO product_spus (name, subtitle, category_id, brand_id, main_image, unit, status, sort) VALUES
('iPhone 15 Pro', '苹果最新款手机', 4, 1, NULL, '台', 1, 1),
('Samsung Galaxy S24', '三星旗舰手机', 4, 2, NULL, '台', 1, 2),
('华为Mate 60', '华为旗舰手机', 4, 3, NULL, '台', 1, 3),
('MacBook Pro 14', '苹果笔记本电脑', 5, 1, NULL, '台', 1, 4),
('Nike Air Max', '经典运动鞋', 6, 4, NULL, '双', 1, 5);

-- 插入商品SKU数据
INSERT INTO product_skus (spu_id, sku_code, name, specs, price, original_price, status, sort) VALUES
(1, 'SKU001', 'iPhone 15 Pro 128GB 黑色', '{"颜色":"黑色","存储":"128GB"}', 7999.00, 8999.00, 1, 1),
(1, 'SKU002', 'iPhone 15 Pro 256GB 白色', '{"颜色":"白色","存储":"256GB"}', 8999.00, 9999.00, 1, 2),
(2, 'SKU003', 'Samsung Galaxy S24 128GB 黑色', '{"颜色":"黑色","存储":"128GB"}', 6999.00, 7999.00, 1, 1),
(3, 'SKU004', '华为Mate 60 256GB 黑色', '{"颜色":"黑色","存储":"256GB"}', 5999.00, 6999.00, 1, 1),
(4, 'SKU005', 'MacBook Pro 14 M3 512GB', '{"CPU":"M3","存储":"512GB"}', 14999.00, 16999.00, 1, 1),
(5, 'SKU006', 'Nike Air Max 42码 黑色', '{"颜色":"黑色","尺码":"42"}', 899.00, 1099.00, 1, 1);

-- 插入库存数据
INSERT INTO inventory_records (sku_id, total_stock, available_stock, locked_stock, warning_stock) VALUES
(1, 100, 95, 5, 10),
(2, 80, 78, 2, 10),
(3, 50, 48, 2, 10),
(4, 120, 115, 5, 10),
(5, 30, 28, 2, 5),
(6, 200, 190, 10, 20);

-- 插入商品图片数据
INSERT INTO product_images (spu_id, image_url, image_type, sort) VALUES
(1, '/images/iphone15-pro-1.jpg', 0, 1),
(1, '/images/iphone15-pro-2.jpg', 0, 2),
(2, '/images/samsung-s24-1.jpg', 0, 1),
(3, '/images/huawei-mate60-1.jpg', 0, 1),
(4, '/images/macbook-pro-1.jpg', 0, 1),
(5, '/images/nike-airmax-1.jpg', 0, 1);
