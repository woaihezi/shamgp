# 数据模型关系说明

本文档描述 ShamGP 商城核心数据库表结构与关系，基于 `backend/app/models/` 真实代码生成。

---

## 一、核心实体

```
User ─────┬───── Address（收货地址）
          ├───── UserCoupon（用户优惠券） ── Coupon
          ├───── Favorite（收藏）─────────── Product
          ├───── BrowseHistory（浏览历史）── Product
          ├───── CartItem（购物车）
          ├───── Order（订单）────────────── OrderItem
          └───── user_role ─── Role ──── menu（权限）

Product ──┬───── ProductCategory（分类）
          ├───── Brand（品牌）
          ├───── ProductSpu ──┬── ProductSku（SKU变体）
          │                   └── ProductImage（商品图片）
          └───── OrderItem

Order ────┬───── OrderItem（订单项）── ProductSku
          ├───── Address（收货地址）
          ├───── OrderStatusLog（状态变更日志）
          └───── Refund（退款）

Floor ────┴───── FloorProduct（楼层商品关联）── Product
AdSpace ──┴───── Ad（广告位）
```

---

## 二、核心表结构

### users（用户表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 用户ID |
| username | VARCHAR(50) | 用户名，唯一 |
| email | VARCHAR(100) | 邮箱 |
| password_hash | VARCHAR(255) | 密码（bcrypt） |
| nickname | VARCHAR(50) | 昵称 |
| phone | VARCHAR(20) | 手机号 |
| avatar | VARCHAR(500) | 头像URL |
| status | SMALLINT | 状态：0禁用 1启用 |
| created_at | DATETIME | 创建时间 |

### product_categories（商品分类）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 分类ID |
| name | VARCHAR(100) | 分类名称 |
| parent_id | INTEGER FK | 父分类ID（支持多级） |
| icon | VARCHAR(500) | 图标URL |
| sort | INTEGER | 排序 |
| status | SMALLINT | 状态 |

### product_spus（商品SPU）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | SPU ID |
| name | VARCHAR(200) | 商品名称 |
| subtitle | VARCHAR(500) | 副标题 |
| category_id | INTEGER FK | 分类ID |
| brand_id | INTEGER FK | 品牌ID |
| main_image | VARCHAR(500) | 主图URL |
| images | TEXT | 多图JSON数组 |
| description | TEXT | 详情描述 |
| status | SMALLINT | 0下架 1上架 |
| sales_count | INTEGER | 销量 |
| view_count | INTEGER | 浏览量 |
| is_recommend | SMALLINT | 是否推荐 |
| is_new | SMALLINT | 是否新品 |
| is_hot | SMALLINT | 是否热销 |

### product_skus（商品SKU）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | SKU ID |
| spu_id | INTEGER FK | SPU ID |
| sku_code | VARCHAR(50) | SKU编码 |
| name | VARCHAR(200) | SKU名称（可区别规格） |
| specs | TEXT | 规格JSON `{"颜色":"黑色","容量":"256G"}` |
| image | VARCHAR(500) | SKU图片 |
| price | DECIMAL(10,2) | 售价 |
| original_price | DECIMAL(10,2) | 原价 |
| cost_price | DECIMAL(10,2) | 成本价 |
| stock | INTEGER | 库存 |
| status | SMALLINT | 状态 |

### product_images（商品图片）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 图片ID |
| spu_id | INTEGER FK | SPU ID |
| image_url | VARCHAR(500) | 图片URL |
| image_type | SMALLINT | 0主图 1详情图 2其他 |
| sort | INTEGER | 排序 |

### orders（订单）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 订单ID |
| order_no | VARCHAR(50) | 订单编号 |
| user_id | INTEGER FK | 用户ID |
| address_id | INTEGER FK | 收货地址ID |
| total_amount | DECIMAL(10,2) | 订单总额 |
| freight_amount | DECIMAL(10,2) | 运费 |
| discount_amount | DECIMAL(10,2) | 优惠金额 |
| pay_amount | DECIMAL(10,2) | 实付金额 |
| status | VARCHAR(50) | 订单状态 |
| pay_time | DATETIME | 支付时间 |
| shipped_time | DATETIME | 发货时间 |
| completed_time | DATETIME | 完成时间 |

### coupons（优惠券）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 优惠券ID |
| name | VARCHAR(100) | 优惠券名称 |
| code | VARCHAR(50) | 优惠券码，唯一 |
| type | SMALLINT | 1满减 2折扣 3无门槛 |
| 满减金额 | DECIMAL(10,2) | 满减金额 |
| 折扣 | DECIMAL(5,2) | 折扣率 |
| 门槛金额 | DECIMAL(10,2) | 使用门槛 |
| total_count | INTEGER | 发放总量（0不限） |
| remain_count | INTEGER | 剩余数量 |
| per_user_limit | INTEGER | 每人限领 |
| start_time | DATETIME | 开始时间 |
| end_time | DATETIME | 结束时间 |
| status | SMALLINT | 状态 |

### user_coupons（用户优惠券）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 记录ID |
| user_id | INTEGER FK | 用户ID |
| coupon_id | INTEGER FK | 优惠券ID |
| status | SMALLINT | 0未使用 1已使用 2已过期 |
| used_at | DATETIME | 使用时间 |
| order_id | INTEGER | 关联订单ID |

### favorites（收藏）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 收藏ID |
| user_id | INTEGER FK | 用户ID |
| product_id | INTEGER FK | 商品ID |
| created_at | DATETIME | 收藏时间 |

### browse_histories（浏览历史）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 记录ID |
| user_id | INTEGER FK | 用户ID |
| product_id | INTEGER FK | 商品ID |
| browse_time | DATETIME | 浏览时间 |

### order_status_logs（订单状态日志）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 日志ID |
| order_id | INTEGER FK | 订单ID |
| old_status | VARCHAR(50) | 原状态 |
| new_status | VARCHAR(50) | 新状态 |
| operator_type | VARCHAR(20) | 操作者类型 |
| operator_id | INTEGER | 操作者ID |
| remark | TEXT | 备注 |
| created_at | DATETIME | 操作时间 |

### inventory_records（库存变动记录）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 记录ID |
| sku_id | INTEGER FK | SKU ID |
| order_id | INTEGER FK | 订单ID（可空） |
| change_type | VARCHAR(20) | 变动类型 |
| quantity_change | INTEGER | 变动数量 |
| before_stock | INTEGER | 变动前库存 |
| after_stock | INTEGER | 变动后库存 |
| reason | VARCHAR(200) | 变动原因 |
| created_at | DATETIME | 变动时间 |

---

## 三、订单状态流转

```
pending_payment（待支付）
    ↓ 支付
paid（已支付）
    ↓ 发货
shipped（已发货）
    ↓ 确认收货
completed（已完成）
    ↓ 退款/取消
canceled（已取消）
refunded（已退款）
```

每次状态变更均写入 `order_status_logs` 表。

---

*本文档基于 `backend/app/models/` 真实代码生成