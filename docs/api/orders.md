# 订单接口

本文档描述 ShamGP 商城订单相关的所有 API 接口，基于真实代码生成。

> **代码位置**: `backend/app/api/v1/orders.py`  
> **路由前缀**: `/api/v1/orders`

---

## 通用数据模型

### 订单状态（OrderStatus）

| 状态值 | 说明 |
|--------|------|
| `pending_payment` | 待付款 |
| `paid` | 已付款 |
| `shipped` | 已发货 |
| `completed` | 已完成 |
| `canceled` | 已取消 |
| `refunding` | 退款中 |
| `refunded` | 已退款 |

### 支付状态（PayStatus）

| 值 | 说明 |
|----|------|
| 0 | 未支付 |
| 1 | 已支付 |
| 2 | 已退款 |

---

## 地址管理

### 获取收货地址列表

**请求**: `GET /api/v1/orders/addresses`

**认证**: 必须登录

### 响应示例

```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "name": "张三",
      "phone": "13800138000",
      "province": "广东省",
      "city": "深圳市",
      "district": "南山区",
      "detail_address": "科技园路1号",
      "is_default": true
    }
  ]
}
```

---

### 获取默认收货地址

**请求**: `GET /api/v1/orders/addresses/default`

**认证**: 必须登录

### 响应示例（200）

```json
{
  "code": 200,
  "data": {
    "id": 1,
    "name": "张三",
    "phone": "13800138000",
    "province": "广东省",
    "city": "深圳市",
    "district": "南山区",
    "detail_address": "科技园路1号",
    "is_default": true
  }
}
```

### 响应示例（404 — 无默认地址）

```json
{
  "code": 404,
  "message": "Default address not found"
}
```

---

### 新增收货地址

**请求**: `POST /api/v1/orders/addresses`

**认证**: 必须登录

### 请求体

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 收货人姓名 |
| phone | string | 是 | 收货人电话 |
| province | string | 否 | 省份 |
| city | string | 否 | 城市 |
| district | string | 否 | 区县 |
| detail_address | string | 是 | 详细地址 |
| is_default | boolean | 否 | 是否默认 |

### 响应示例

```json
{
  "code": 200,
  "data": {
    "id": 2,
    "name": "李四",
    "phone": "13900139000",
    "province": "广东省",
    "city": "广州市",
    "district": "天河区",
    "detail_address": "体育西路123号",
    "is_default": false
  }
}
```

---

### 更新收货地址

**请求**: `PUT /api/v1/orders/addresses/{address_id}`

**认证**: 必须登录

### 请求体

同新增，支持部分字段更新。

### 响应示例

```json
{
  "code": 200,
  "data": { ... }
}
```

---

### 删除收货地址

**请求**: `DELETE /api/v1/orders/addresses/{address_id}`

**认证**: 必须登录

### 响应示例

```json
{
  "code": 200,
  "message": "Address deleted successfully"
}
```

---

## 创建订单

将购物车中选中的商品正式提交为订单，同时**扣减库存**。

**请求**: `POST /api/v1/orders/`

**认证**: 必须登录（JWT）

### 请求体

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| address_id | integer | 是 | 收货地址 ID |
| cart_item_ids | list[integer] | 是 | 购物车商品项 ID 列表（由前端传递选中的项） |
| remark | string | 否 | 订单备注 |

### 请求示例

```json
{
  "address_id": 1,
  "cart_item_ids": [10, 11],
  "remark": "请轻拿轻放"
}
```

### 响应示例（201）

```json
{
  "code": 200,
  "data": {
    "id": 100,
    "order_no": "ORD20260331102345ABCDEF",
    "user_id": 1,
    "total_amount": 15998.00,
    "pay_amount": 15998.00,
    "discount_amount": 0.00,
    "freight_amount": 0.00,
    "status": "pending_payment",
    "pay_status": 0,
    "consignee_name": "张三",
    "consignee_phone": "13800138000",
    "consignee_address": "广东省深圳市南山区科技园路1号",
    "remark": "请轻拿轻放",
    "items": [
      {
        "id": 200,
        "product_id": 5,
        "product_name": "iPhone 15 Pro",
        "product_image": "https://example.com/iphone15.jpg",
        "sku_id": 101,
        "price": 7999.00,
        "quantity": 2,
        "total_amount": 15998.00
      }
    ],
    "created_at": "2026-03-31T10:23:45Z"
  }
}
```

### 业务逻辑

`OrderService.create_order()` 执行以下操作：

1. **验证地址**：检查地址是否属于当前用户
2. **获取购物车项**：根据 `cart_item_ids` 获取 `selected=True` 的购物车项
3. **库存检查**：逐项检查商品库存是否充足，不足则抛出 `ValueError`
4. **扣减库存**：`product.stock -= quantity`，`product.sales += quantity`
5. **生成订单号**：格式 `ORD{YYYYMMDDHHMMSS}{6位随机字符串}`
6. **创建订单**：写入 `orders` 和 `order_items` 表
7. **清空购物车**：将已结算的购物车项标记 `is_deleted=True`

### 订单号格式

```
ORD + 年月日时分秒 + 6位随机大写字母数字
例：ORD20260331102345ABCDEF
```

### 对应后端代码

- **路由**: `backend/app/api/v1/orders.py` — `POST /`
- **Service**: `backend/app/services/order_service.py` — `OrderService.create_order()`

---

## 获取订单列表

获取当前用户的订单列表，支持状态筛选和分页。

**请求**: `GET /api/v1/orders/`

**认证**: 必须登录（JWT）

### Query 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| status | string | 否 | - | 订单状态筛选 |
| page | integer | 否 | 1 | 页码 |
| page_size | integer | 否 | 20 | 每页数量 |

### 响应示例

```json
{
  "code": 200,
  "data": [
    {
      "id": 100,
      "order_no": "ORD20260331102345ABCDEF",
      "total_amount": 15998.00,
      "pay_amount": 15998.00,
      "status": "paid",
      "pay_status": 1,
      "created_at": "2026-03-31T10:23:45Z"
    }
  ],
  "total": 15
}
```

### 对应后端代码

- **路由**: `backend/app/api/v1/orders.py` — `GET /`
- **Service**: `backend/app/services/order_service.py` — `OrderService.get_orders()`

---

## 获取订单详情

获取单个订单的完整信息（含订单明细）。

**请求**: `GET /api/v1/orders/{order_id}`

**认证**: 必须登录（JWT）

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| order_id | integer | 是 | 订单 ID |

### 响应示例

```json
{
  "code": 200,
  "data": {
    "id": 100,
    "order_no": "ORD20260331102345ABCDEF",
    "user_id": 1,
    "total_amount": 15998.00,
    "pay_amount": 15998.00,
    "discount_amount": 0.00,
    "freight_amount": 0.00,
    "status": "paid",
    "pay_status": 1,
    "pay_time": "2026-03-31T10:30:00Z",
    "consignee_name": "张三",
    "consignee_phone": "13800138000",
    "consignee_address": "广东省深圳市南山区科技园路1号",
    "remark": "请轻拿轻放",
    "items": [
      {
        "id": 200,
        "product_id": 5,
        "product_name": "iPhone 15 Pro",
        "product_image": "https://example.com/iphone15.jpg",
        "sku_id": 101,
        "price": 7999.00,
        "quantity": 2,
        "total_amount": 15998.00
      }
    ]
  }
}
```

### 权限校验

订单必须属于当前登录用户，否则返回 404（防止信息泄露）。

### 对应后端代码

- **路由**: `backend/app/api/v1/orders.py` — `GET /{order_id}`
- **Service**: `backend/app/services/order_service.py` — `OrderService.get_order()`

---

## 更新订单状态

**请求**: `PUT /api/v1/orders/{order_id}/status`

**认证**: 必须登录（JWT）

### 请求体

```json
{
  "status": "shipped"
}
```

### 状态自动联动

| 新状态 | 副作用 |
|--------|--------|
| `paid` | `pay_status → 1`，`pay_time → NOW()` |
| `shipped` | `delivery_time → NOW()` |
| `completed` | `receive_time → NOW()` |
| `canceled` | `cancel_time → NOW()` |
| `refunded` | `pay_status → 2`，`refund_time → NOW()` |

### 响应示例

```json
{
  "code": 200,
  "data": { ... }
}
```

---

## 取消订单

用户主动取消订单（仅允许待付款状态的订单）。

**请求**: `POST /api/v1/orders/{order_id}/cancel`

**认证**: 必须登录（JWT）

### Query 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cancel_reason | string | 是 | 取消原因 |

### 响应示例（200）

```json
{
  "code": 200,
  "data": {
    "id": 100,
    "status": "canceled",
    "cancel_time": "2026-03-31T10:35:00Z",
    "cancel_reason": "不想要了"
  }
}
```

### 响应示例（400 — 订单无法取消）

```json
{
  "code": 400,
  "message": "Order cannot be cancelled"
}
```

### 业务逻辑

1. 检查订单状态必须为 `pending_payment`（待付款）
2. 逐项回滚库存：`product.stock += quantity`，`product.sales -= quantity`
3. 将订单状态更新为 `canceled`，记录 `cancel_time` 和 `cancel_reason`

### 对应后端代码

- **Service**: `backend/app/services/order_service.py` — `OrderService.cancel_order()`

---

## 申请退款

用户针对已支付或已发货的订单申请退款。

**请求**: `POST /api/v1/orders/refunds`

**认证**: 必须登录（JWT）

### 请求体

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| order_id | integer | 是 | 订单 ID |
| order_item_id | integer | 否 | 指定某项商品退款（为空则退整单） |
| refund_reason | string | 是 | 退款原因 |
| refund_type | string | 是 | 退款类型 |

### 响应示例

```json
{
  "code": 200,
  "data": {
    "id": 50,
    "order_id": 100,
    "refund_no": "REF20260331104000GHIJKL",
    "user_id": 1,
    "refund_amount": 15998.00,
    "refund_reason": "商品损坏",
    "refund_type": "退货退款",
    "status": "pending"
  }
}
```

### 退款号格式

```
REF{YYYYMMDDHHMMSS}{6位随机大写字母数字}
```

### 退款金额计算

- 不指定 `order_item_id` → 退整单实付金额 `order.pay_amount`
- 指定 `order_item_id` → 退该明细的小计金额 `order_item.total_amount`

### 申请后状态变更

申请退款后，订单状态自动变为 `refunding`（退款中）。

### 对应后端代码

- **路由**: `backend/app/api/v1/orders.py` — `POST /refunds`
- **Service**: `backend/app/services/order_service.py` — `OrderService.create_refund()`

---

## 获取退款记录

**请求**: `GET /api/v1/orders/refunds`

**认证**: 必须登录（JWT）

### Query 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| order_id | integer | 否 | 按订单 ID 筛选 |

### 响应示例

```json
{
  "code": 200,
  "data": [
    {
      "id": 50,
      "order_id": 100,
      "refund_no": "REF20260331104000GHIJKL",
      "refund_amount": 15998.00,
      "refund_reason": "商品损坏",
      "status": "pending"
    }
  ]
}
```

---

## 获取单个退款记录

**请求**: `GET /api/v1/orders/refunds/{refund_id}`

**认证**: 必须登录（JWT）

### 响应示例（200）

```json
{
  "code": 200,
  "data": { ... }
}
```

---

## 订单数据模型

### Order 主表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| order_no | String(64) | 订单号（唯一，索引） |
| user_id | Integer | 用户 ID（外键 → users） |
| total_amount | Numeric(10,2) | 订单总金额 |
| pay_amount | Numeric(10,2) | 实付金额 |
| discount_amount | Numeric(10,2) | 优惠金额 |
| freight_amount | Numeric(10,2) | 运费 |
| status | String(20) | 订单状态（索引） |
| pay_status | SmallInteger | 支付状态 |
| pay_time | DateTime | 支付时间 |
| pay_type | String(20) | 支付方式 |
| consignee_name | String(50) | 收货人姓名 |
| consignee_phone | String(20) | 收货人电话 |
| consignee_address | String(500) | 收货地址（省市区+详情拼接） |
| remark | String(500) | 订单备注 |
| cancel_time | DateTime | 取消时间 |
| cancel_reason | String(255) | 取消原因 |
| delivery_time | DateTime | 发货时间 |
| receive_time | DateTime | 收货时间 |

### OrderItem 订单明细表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| order_id | Integer | 订单 ID（外键 → orders） |
| product_id | Integer | 商品 ID（外键 → products） |
| product_name | String(200) | 商品名称（下单快照） |
| product_image | String(255) | 商品图片（下单快照） |
| sku_id | Integer | SKU ID |
| sku_specs | String(500) | SKU 规格文本（下单快照） |
| price | Numeric(10,2) | 单价（下单快照） |
| quantity | Integer | 数量 |
| total_amount | Numeric(10,2) | 小计金额 |

### Refund 退款表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| order_id | Integer | 订单 ID（外键 → orders） |
| order_item_id | Integer | 订单明细 ID（可空） |
| refund_no | String(64) | 退款号（唯一） |
| user_id | Integer | 用户 ID（外键 → users） |
| refund_amount | Numeric(10,2) | 退款金额 |
| refund_reason | String(500) | 退款原因 |
| refund_type | String(20) | 退款类型 |
| status | String(20) | 退款状态 |
| audit_time | DateTime | 审核时间 |
| audit_user_id | Integer | 审核人 ID |
| audit_remark | String(500) | 审核备注 |
| refund_time | DateTime | 退款时间 |

### OrderStatusLog 订单状态日志表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| order_id | Integer | 订单 ID（外键 → orders） |
| old_status | String(50) | 原状态（可空） |
| new_status | String(50) | 新状态 |
| operator_type | String(20) | 操作者类型：system / user / admin |
| operator_id | Integer | 操作者 ID |
| remark | Text | 备注 |
| created_at | DateTime | 操作时间 |

---

## 管理员接口（Admin）

> **路由前缀**: `/api/v1/orders/admin/`

以下接口为管理端专用，**不需要用户认证**（但需要后台鉴权，本文档不详述）。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/` | 获取所有订单（支持分页+状态筛选） |
| GET | `/admin/{order_id}` | 获取指定订单详情 |
| PUT | `/admin/{order_id}/status` | 修改订单状态（发货/完成等） |

### 管理员更新订单状态

```http
PUT /api/v1/orders/admin/{order_id}/status
Content-Type: application/json

{
  "status": "shipped"
}
```

---

## 支付接口

**状态**: 未实现

支付接口（`app/api/v1/payments.py`）已注册到路由，但具体支付逻辑（微信支付/支付宝等）尚未实现。订单创建后 `pay_status` 默认为 `0`（未支付），暂无主动触发支付的 API。
