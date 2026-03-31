# 数据库核心表设计

## 1. 设计原则

### 1.1 数据库兼容性
- 优先遵循 PostgreSQL 规范设计
- 保持与 MySQL 兼容性（避免使用 PostgreSQL 特有语法）
- 使用通用数据类型

### 1.2 命名规范
- 表名：小写字母 + 下划线，复数形式（如 `users`, `orders`）
- 字段名：小写字母 + 下划线（如 `user_name`, `created_at`）
- 索引名：`idx_表名_字段名`（如 `idx_users_email`）
- 外键名：`fk_表名_关联表名`（如 `fk_orders_user_id`）

### 1.3 通用字段
所有表都包含以下字段：
- `id`: 主键（BIGINT / BIGSERIAL）
- `created_at`: 创建时间（TIMESTAMP）
- `updated_at`: 更新时间（TIMESTAMP）
- `is_deleted`: 逻辑删除标记（BOOLEAN，默认 false）

---

## 2. 通用管理模块表设计

### 2.1 用户表 (users)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| username | VARCHAR(50) | NO | | 用户名（唯一） |
| password | VARCHAR(255) | NO | | 密码（加密存储） |
| email | VARCHAR(100) | YES | NULL | 邮箱 |
| phone | VARCHAR(20) | YES | NULL | 手机号 |
| nickname | VARCHAR(50) | YES | NULL | 昵称 |
| avatar | VARCHAR(255) | YES | NULL | 头像URL |
| gender | SMALLINT | YES | 0 | 性别：0-未知，1-男，2-女 |
| status | SMALLINT | NO | 1 | 状态：0-禁用，1-启用 |
| user_type | SMALLINT | NO | 1 | 用户类型：1-普通用户，2-管理员 |
| last_login_at | TIMESTAMP | YES | NULL | 最后登录时间 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |
| updated_at | TIMESTAMP | NO | NOW() | 更新时间 |
| is_deleted | BOOLEAN | NO | false | 逻辑删除 |

**索引**:
- `UNIQUE INDEX idx_users_username ON users(username)`
- `INDEX idx_users_email ON users(email)`
- `INDEX idx_users_phone ON users(phone)`
- `INDEX idx_users_status ON users(status)`

---

### 2.2 角色表 (roles)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| name | VARCHAR(50) | NO | | 角色名称 |
| code | VARCHAR(50) | NO | | 角色编码（唯一） |
| description | VARCHAR(255) | YES | NULL | 角色描述 |
| sort | INT | NO | 0 | 排序 |
| status | SMALLINT | NO | 1 | 状态：0-禁用，1-启用 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |
| updated_at | TIMESTAMP | NO | NOW() | 更新时间 |
| is_deleted | BOOLEAN | NO | false | 逻辑删除 |

**索引**:
- `UNIQUE INDEX idx_roles_code ON roles(code)`
- `INDEX idx_roles_status ON roles(status)`

---

### 2.3 权限表 (permissions)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| parent_id | BIGINT | YES | 0 | 父权限ID |
| name | VARCHAR(50) | NO | | 权限名称 |
| code | VARCHAR(100) | NO | | 权限编码（唯一） |
| type | SMALLINT | NO | 1 | 类型：1-菜单，2-按钮，3-接口 |
| path | VARCHAR(255) | YES | NULL | 路由路径 |
| icon | VARCHAR(50) | YES | NULL | 图标 |
| sort | INT | NO | 0 | 排序 |
| status | SMALLINT | NO | 1 | 状态：0-禁用，1-启用 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |
| updated_at | TIMESTAMP | NO | NOW() | 更新时间 |
| is_deleted | BOOLEAN | NO | false | 逻辑删除 |

**索引**:
- `UNIQUE INDEX idx_permissions_code ON permissions(code)`
- `INDEX idx_permissions_parent_id ON permissions(parent_id)`
- `INDEX idx_permissions_type ON permissions(type)`

---

### 2.4 用户角色关联表 (user_roles)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| user_id | BIGINT | NO | | 用户ID |
| role_id | BIGINT | NO | | 角色ID |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |

**索引**:
- `UNIQUE INDEX idx_user_roles_user_role ON user_roles(user_id, role_id)`
- `INDEX idx_user_roles_user_id ON user_roles(user_id)`
- `INDEX idx_user_roles_role_id ON user_roles(role_id)`

**外键**:
- `fk_user_roles_user_id -> users(id)`
- `fk_user_roles_role_id -> roles(id)`

---

### 2.5 角色权限关联表 (role_permissions)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| role_id | BIGINT | NO | | 角色ID |
| permission_id | BIGINT | NO | | 权限ID |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |

**索引**:
- `UNIQUE INDEX idx_role_perms_role_perm ON role_permissions(role_id, permission_id)`
- `INDEX idx_role_perms_role_id ON role_permissions(role_id)`
- `INDEX idx_role_perms_perm_id ON role_permissions(permission_id)`

**外键**:
- `fk_role_perms_role_id -> roles(id)`
- `fk_role_perms_perm_id -> permissions(id)`

---

### 2.6 菜单表 (menus)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| parent_id | BIGINT | YES | 0 | 父菜单ID |
| name | VARCHAR(50) | NO | | 菜单名称 |
| path | VARCHAR(255) | YES | NULL | 路由路径 |
| component | VARCHAR(255) | YES | NULL | 组件路径 |
| icon | VARCHAR(50) | YES | NULL | 图标 |
| redirect | VARCHAR(255) | YES | NULL | 重定向路径 |
| sort | INT | NO | 0 | 排序 |
| visible | BOOLEAN | NO | true | 是否显示 |
| status | SMALLINT | NO | 1 | 状态：0-禁用，1-启用 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |
| updated_at | TIMESTAMP | NO | NOW() | 更新时间 |
| is_deleted | BOOLEAN | NO | false | 逻辑删除 |

**索引**:
- `INDEX idx_menus_parent_id ON menus(parent_id)`
- `INDEX idx_menus_sort ON menus(sort)`

---

### 2.7 操作日志表 (operation_logs)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| user_id | BIGINT | YES | NULL | 操作用户ID |
| username | VARCHAR(50) | YES | NULL | 操作用户名 |
| module | VARCHAR(50) | YES | NULL | 操作模块 |
| operation | VARCHAR(50) | YES | NULL | 操作类型 |
| method | VARCHAR(10) | YES | NULL | 请求方法 |
| url | VARCHAR(255) | YES | NULL | 请求URL |
| ip | VARCHAR(50) | YES | NULL | IP地址 |
| params | TEXT | YES | NULL | 请求参数 |
| result | TEXT | YES | NULL | 返回结果 |
| status | SMALLINT | NO | 1 | 状态：0-失败，1-成功 |
| error_msg | TEXT | YES | NULL | 错误信息 |
| cost_time | INT | YES | NULL | 耗时（毫秒） |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |

**索引**:
- `INDEX idx_op_logs_user_id ON operation_logs(user_id)`
- `INDEX idx_op_logs_module ON operation_logs(module)`
- `INDEX idx_op_logs_created_at ON operation_logs(created_at)`

---

### 2.8 系统配置表 (system_configs)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| group_name | VARCHAR(50) | YES | NULL | 配置分组 |
| config_key | VARCHAR(100) | NO | | 配置键（唯一） |
| config_value | TEXT | YES | NULL | 配置值 |
| config_type | VARCHAR(20) | NO | 'string' | 配置类型：string, int, bool, json |
| description | VARCHAR(255) | YES | NULL | 配置描述 |
| sort | INT | NO | 0 | 排序 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |
| updated_at | TIMESTAMP | NO | NOW() | 更新时间 |

**索引**:
- `UNIQUE INDEX idx_configs_key ON system_configs(config_key)`
- `INDEX idx_configs_group ON system_configs(group_name)`

---

### 2.9 文件表 (files)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| user_id | BIGINT | YES | NULL | 上传用户ID |
| original_name | VARCHAR(255) | NO | | 原始文件名 |
| file_name | VARCHAR(255) | NO | | 存储文件名 |
| file_path | VARCHAR(500) | NO | | 文件路径 |
| file_url | VARCHAR(500) | NO | | 文件访问URL |
| file_size | BIGINT | NO | 0 | 文件大小（字节） |
| file_type | VARCHAR(100) | YES | NULL | MIME类型 |
| file_ext | VARCHAR(20) | YES | NULL | 文件扩展名 |
| storage_type | VARCHAR(20) | NO | 'local' | 存储类型：local, oss, minio |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |

**索引**:
- `INDEX idx_files_user_id ON files(user_id)`
- `INDEX idx_files_created_at ON files(created_at)`

---

## 3. 电商业务模块表设计

### 3.1 商品分类表 (product_categories)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| parent_id | BIGINT | YES | 0 | 父分类ID |
| name | VARCHAR(50) | NO | | 分类名称 |
| code | VARCHAR(50) | YES | NULL | 分类编码 |
| image | VARCHAR(255) | YES | NULL | 分类图片 |
| description | VARCHAR(255) | YES | NULL | 分类描述 |
| sort | INT | NO | 0 | 排序 |
| level | SMALLINT | NO | 1 | 分类层级 |
| status | SMALLINT | NO | 1 | 状态：0-禁用，1-启用 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |
| updated_at | TIMESTAMP | NO | NOW() | 更新时间 |
| is_deleted | BOOLEAN | NO | false | 逻辑删除 |

**索引**:
- `INDEX idx_categories_parent_id ON product_categories(parent_id)`
- `INDEX idx_categories_level ON product_categories(level)`
- `INDEX idx_categories_status ON product_categories(status)`

---

### 3.2 商品表 (products)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| category_id | BIGINT | NO | | 分类ID |
| name | VARCHAR(200) | NO | | 商品名称 |
| code | VARCHAR(100) | YES | NULL | 商品编码 |
| brief | VARCHAR(500) | YES | NULL | 商品简介 |
| description | TEXT | YES | NULL | 商品详情 |
| cover_image | VARCHAR(255) | YES | NULL | 封面图 |
| images | TEXT | YES | NULL | 商品图片（JSON数组） |
| price | DECIMAL(10,2) | NO | 0.00 | 销售价格 |
| original_price | DECIMAL(10,2) | YES | NULL | 原价 |
| cost_price | DECIMAL(10,2) | YES | NULL | 成本价 |
| stock | INT | NO | 0 | 库存数量 |
| sales | INT | NO | 0 | 销量 |
| views | INT | NO | 0 | 浏览量 |
| is_hot | BOOLEAN | NO | false | 是否热门 |
| is_new | BOOLEAN | NO | false | 是否新品 |
| is_recommend | BOOLEAN | NO | false | 是否推荐 |
| status | SMALLINT | NO | 0 | 状态：0-下架，1-上架 |
| sort | INT | NO | 0 | 排序 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |
| updated_at | TIMESTAMP | NO | NOW() | 更新时间 |
| is_deleted | BOOLEAN | NO | false | 逻辑删除 |

**索引**:
- `INDEX idx_products_category_id ON products(category_id)`
- `INDEX idx_products_status ON products(status)`
- `INDEX idx_products_sales ON products(sales)`
- `INDEX idx_products_created_at ON products(created_at)`

---

### 3.3 商品SKU表 (product_skus)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| product_id | BIGINT | NO | | 商品ID |
| sku_code | VARCHAR(100) | YES | NULL | SKU编码 |
| specs | VARCHAR(500) | YES | NULL | 规格（JSON） |
| specs_text | VARCHAR(500) | YES | NULL | 规格文本 |
| image | VARCHAR(255) | YES | NULL | SKU图片 |
| price | DECIMAL(10,2) | NO | 0.00 | SKU价格 |
| original_price | DECIMAL(10,2) | YES | NULL | SKU原价 |
| stock | INT | NO | 0 | 库存 |
| sales | INT | NO | 0 | 销量 |
| status | SMALLINT | NO | 1 | 状态：0-禁用，1-启用 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |
| updated_at | TIMESTAMP | NO | NOW() | 更新时间 |

**索引**:
- `INDEX idx_product_skus_product_id ON product_skus(product_id)`

---

### 3.4 购物车表 (cart_items)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| user_id | BIGINT | NO | | 用户ID |
| product_id | BIGINT | NO | | 商品ID |
| sku_id | BIGINT | YES | NULL | SKU ID |
| quantity | INT | NO | 1 | 数量 |
| selected | BOOLEAN | NO | true | 是否选中 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |
| updated_at | TIMESTAMP | NO | NOW() | 更新时间 |

**索引**:
- `UNIQUE INDEX idx_cart_user_product_sku ON cart_items(user_id, product_id, sku_id)`
- `INDEX idx_cart_user_id ON cart_items(user_id)`

---

### 3.5 订单表 (orders)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| order_no | VARCHAR(64) | NO | | 订单号（唯一） |
| user_id | BIGINT | NO | | 用户ID |
| total_amount | DECIMAL(10,2) | NO | 0.00 | 订单总金额 |
| pay_amount | DECIMAL(10,2) | NO | 0.00 | 实付金额 |
| discount_amount | DECIMAL(10,2) | YES | 0.00 | 优惠金额 |
| freight_amount | DECIMAL(10,2) | YES | 0.00 | 运费 |
| status | SMALLINT | NO | 0 | 订单状态：0-待付款，1-待发货，2-已发货，3-已完成，4-已取消，5-已退款 |
| pay_status | SMALLINT | NO | 0 | 支付状态：0-未支付，1-已支付，2-已退款 |
| pay_time | TIMESTAMP | YES | NULL | 支付时间 |
| pay_type | VARCHAR(20) | YES | NULL | 支付方式 |
| consignee_name | VARCHAR(50) | NO | | 收货人姓名 |
| consignee_phone | VARCHAR(20) | NO | | 收货人电话 |
| consignee_address | VARCHAR(500) | NO | | 收货地址 |
| remark | VARCHAR(500) | YES | NULL | 订单备注 |
| cancel_time | TIMESTAMP | YES | NULL | 取消时间 |
| cancel_reason | VARCHAR(255) | YES | NULL | 取消原因 |
| delivery_time | TIMESTAMP | YES | NULL | 发货时间 |
| receive_time | TIMESTAMP | YES | NULL | 收货时间 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |
| updated_at | TIMESTAMP | NO | NOW() | 更新时间 |

**索引**:
- `UNIQUE INDEX idx_orders_order_no ON orders(order_no)`
- `INDEX idx_orders_user_id ON orders(user_id)`
- `INDEX idx_orders_status ON orders(status)`
- `INDEX idx_orders_created_at ON orders(created_at)`

---

### 3.6 订单明细表 (order_items)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| order_id | BIGINT | NO | | 订单ID |
| product_id | BIGINT | NO | | 商品ID |
| sku_id | BIGINT | YES | NULL | SKU ID |
| product_name | VARCHAR(200) | NO | | 商品名称 |
| product_image | VARCHAR(255) | YES | NULL | 商品图片 |
| sku_specs | VARCHAR(500) | YES | NULL | SKU规格 |
| price | DECIMAL(10,2) | NO | 0.00 | 单价 |
| quantity | INT | NO | 1 | 数量 |
| total_amount | DECIMAL(10,2) | NO | 0.00 | 小计金额 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |

**索引**:
- `INDEX idx_order_items_order_id ON order_items(order_id)`
- `INDEX idx_order_items_product_id ON order_items(product_id)`

---

### 3.7 收货地址表 (user_addresses)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| user_id | BIGINT | NO | | 用户ID |
| name | VARCHAR(50) | NO | | 收货人姓名 |
| phone | VARCHAR(20) | NO | | 收货人电话 |
| province | VARCHAR(50) | YES | NULL | 省份 |
| city | VARCHAR(50) | YES | NULL | 城市 |
| district | VARCHAR(50) | YES | NULL | 区县 |
| detail | VARCHAR(500) | NO | | 详细地址 |
| is_default | BOOLEAN | NO | false | 是否默认地址 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |
| updated_at | TIMESTAMP | NO | NOW() | 更新时间 |

**索引**:
- `INDEX idx_user_addresses_user_id ON user_addresses(user_id)`

---

### 3.8 商品评价表 (product_reviews)

| 字段名 | 类型 | 可空 | 默认值 | 说明 |
|-------|------|------|--------|------|
| id | BIGSERIAL | NO | | 主键 |
| product_id | BIGINT | NO | | 商品ID |
| order_id | BIGINT | NO | | 订单ID |
| user_id | BIGINT | NO | | 用户ID |
| rating | SMALLINT | NO | 5 | 评分：1-5星 |
| content | TEXT | YES | NULL | 评价内容 |
| images | TEXT | YES | NULL | 评价图片（JSON数组） |
| is_anonymous | BOOLEAN | NO | false | 是否匿名 |
| status | SMALLINT | NO | 1 | 状态：0-隐藏，1-显示 |
| created_at | TIMESTAMP | NO | NOW() | 创建时间 |

**索引**:
- `INDEX idx_reviews_product_id ON product_reviews(product_id)`
- `INDEX idx_reviews_user_id ON product_reviews(user_id)`

---

## 4. 数据库初始化脚本模板

### 4.1 PostgreSQL 建表脚本示例

```sql
-- 创建用户表
CREATE TABLE users (
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
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT false
);

CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_status ON users(status);
```

### 4.2 MySQL 建表脚本示例

```sql
-- 创建用户表
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    nickname VARCHAR(50),
    avatar VARCHAR(255),
    gender TINYINT DEFAULT 0,
    status TINYINT DEFAULT 1,
    user_type TINYINT DEFAULT 1,
    last_login_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT false
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_status ON users(status);
```
