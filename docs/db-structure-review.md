# 数据库结构审查

## 数据库模型清单

### 核心业务模型

| 模型名 | 表名 | 文件 | 状态 | 说明 |
|--------|------|------|------|------|
| User | users | `app/models/user.py` | ✅ | 用户模型 |
| Product | products | `app/models/product.py` | ✅ | 商品模型（简单版） |
| ProductSpu | product_spus | `app/models/product_spu.py` | ✅ | 商品 SPU |
| ProductSku | product_skus | `app/models/product_sku.py` | ✅ | 商品 SKU |
| ProductCategory | product_categories | `app/models/category.py` | ✅ | 商品分类 |
| ProductBrand | product_brands | `app/models/brand.py` | ✅ | 商品品牌 |
| ProductImage | product_images | `app/models/product_image.py` | ✅ | 商品图片 |
| Order | orders | `app/models/order.py` | ✅ | 订单 |
| OrderItem | order_items | `app/models/order.py` | ✅ | 订单项 |
| Refund | refunds | `app/models/order.py` | ✅ | 退款 |
| CartItem | cart_items | `app/models/cart.py` | ✅ | 购物车项 |
| Address | addresses | `app/models/address.py` | ✅ | 收货地址 |
| Coupon | coupons | `app/models/coupon.py` | ✅ | 优惠券 |
| Banner | banners | `app/models/banner.py` | ✅ | 横幅广告 |

### 系统管理模型

| 模型名 | 表名 | 文件 | 状态 | 说明 |
|--------|------|------|------|------|
| Role | roles | `app/models/role.py` | ✅ | 角色 |
| Permission | permissions | `app/models/permission.py` | ✅ | 权限 |
| Menu | menus | `app/models/menu.py` | ✅ | 菜单 |
| Log | logs | `app/models/log.py` | ✅ | 日志 |
| File | files | `app/models/file.py` | ✅ | 文件 |
| SystemConfig | system_configs | `app/models/system_config.py` | ✅ | 系统配置 |
| InventoryRecord | inventory_records | `app/models/inventory_record.py` | ✅ | 库存记录 |
| Recommend | recommends | `app/models/recommend.py` | ✅ | 推荐 |

### 总计：约 20+ 个数据模型

---

## 模型关系图（简要）

```
User (用户)
  ├── orders (订单)
  ├── cart_items (购物车)
  ├── addresses (地址)
  ├── refunds (退款)
  └── roles (角色)

ProductCategory (分类)
  └── products (商品)

Product (商品)
  ├── order_items (订单项)
  └── cart_items (购物车项)

Order (订单)
  ├── order_items (订单项)
  └── refunds (退款)

Role (角色)
  ├── permissions (权限)
  └── users (用户)
```

---

## 数据库迁移

| 项目 | 状态 | 位置 | 说明 |
|------|------|------|------|
| Alembic 配置 | ✅ 存在 | `alembic.ini` | 配置文件完整 |
| 迁移脚本目录 | ✅ 存在 | `alembic/` | 目录结构完整 |
| env.py | ✅ 存在 | `alembic/env.py` | 配置文件 |
| 迁移版本 | ⚠️ 需确认 | `alembic/versions/` | 需要检查是否有迁移文件 |

---

## 初始化脚本

| 脚本 | 位置 | 状态 | 说明 |
|------|------|------|------|
| init_db.py | `backend/scripts/init_db.py` | ✅ 存在 | 数据库初始化 |
| seed_data.py | `backend/scripts/seed_data.py` | ✅ 存在 | 数据填充 |
| seed_rbac.py | `backend/scripts/seed_rbac.py` | ✅ 存在 | RBAC 数据 |
| create_addresses.py | `backend/scripts/create_addresses.py` | ✅ 存在 | 创建地址 |

---

## 数据库配置

### 支持的数据库类型

| 数据库 | 驱动 | 状态 |
|--------|------|------|
| SQLite | aiosqlite | ✅ 默认 |
| MySQL | aiomysql | ✅ 支持 |
| PostgreSQL | asyncpg | ✅ 支持 |

### 配置文件

- `app/core/config.py` - 数据库连接配置
- `.env.example` - 环境变量示例

---

## 数据库设计评估

### 优点

1. ✅ **模型设计完整** - 覆盖了电商核心业务所需的所有表
2. ✅ **使用 Async SQLAlchemy** - 支持异步操作，性能好
3. ✅ **有基础模型 (BaseModel)** - 统一的字段（id, created_at, updated_at, is_deleted）
4. ✅ **软删除支持** - 使用 is_deleted 字段
5. ✅ **迁移工具配置** - Alembic 已配置
6. ✅ **多数据库支持** - 支持 SQLite、MySQL、PostgreSQL

### 待完善

1. ⚠️ **迁移版本缺失** - 需要确认是否有实际的迁移文件
2. ⚠️ **索引设计** - 需要检查索引是否合理
3. ⚠️ **外键约束** - 需要确认外键关系是否完善
4. ⚠️ **初始化脚本** - 需要测试初始化脚本是否可用

---

## 环境变量使用

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| DB_TYPE | 数据库类型 | sqlite |
| DB_HOST | 数据库主机 | localhost |
| DB_PORT | 数据库端口 | 3306 |
| DB_USER | 数据库用户 | root |
| DB_PASSWORD | 数据库密码 | password |
| DB_NAME | 数据库名 | shop_db |
| SECRET_KEY | JWT 密钥 | your-secret-key-here |
| ALGORITHM | JWT 算法 | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token 过期时间 | 10080 (7天) |
