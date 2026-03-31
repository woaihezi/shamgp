# 购物车接口

本文档描述 ShamGP 商城购物车相关的所有 API 接口，基于真实代码生成。

> **代码位置**: `backend/app/api/v1/carts.py`  
> **路由前缀**: `/api/v1/carts`

---

## 获取购物车商品列表

获取当前用户的全部购物车商品（含选中状态）。

**请求**: `GET /api/v1/carts/items`

**认证**: 必须登录（JWT）

### 响应示例

```json
{
  "code": 200,
  "data": [
    {
      "id": 10,
      "user_id": 1,
      "product_id": 5,
      "sku_id": 101,
      "quantity": 2,
      "selected": true,
      "product_name": "iPhone 15 Pro",
      "product_image": "https://example.com/iphone15.jpg",
      "product_price": 7999.00,
      "created_at": "2026-03-20T10:30:00Z"
    }
  ]
}
```

### 对应后端代码

- **路由**: `backend/app/api/v1/carts.py` — `GET /items`
- **Service**: `backend/app/services/cart_service.py` — `CartService.get_cart_items()`

---

## 获取购物车摘要

获取当前用户购物车的汇总信息（总商品数、总数量、选中商品的总金额）。

**请求**: `GET /api/v1/carts/summary`

**认证**: 必须登录（JWT）

### 响应示例

```json
{
  "code": 200,
  "data": {
    "total_items": 3,
    "total_quantity": 5,
    "total_amount": 25997.00,
    "selected_items": [
      {
        "id": 10,
        "product_id": 5,
        "sku_id": 101,
        "quantity": 2,
        "selected": true,
        "product_name": "iPhone 15 Pro",
        "product_image": "https://example.com/iphone15.jpg",
        "product_price": 7999.00
      }
    ]
  }
}
```

### 业务说明

- `total_items`：购物车中不同商品（SKU）种类数
- `total_quantity`：所有商品的数量总和
- `total_amount`：**仅统计 `selected=true` 的商品**，即用户勾选待结算的金额
- `selected_items`：返回所有选中的商品完整信息（含 product_name、product_image）

### 对应后端代码

- **路由**: `backend/app/api/v1/carts.py` — `GET /summary`
- **Service**: `backend/app/services/cart_service.py` — `CartService.get_cart_summary()`

---

## 添加商品到购物车

将商品（或指定 SKU）加入购物车。如果该用户已存在相同商品+SKU 的记录，则**累加数量**而非新建记录。

**请求**: `POST /api/v1/carts/items`

**认证**: 必须登录（JWT）

### 请求体

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| product_id | integer | 是 | 商品 ID |
| sku_id | integer | 否 | SKU ID（多规格商品必填） |
| quantity | integer | 是 | 数量，必须 ≥ 1 |

### 请求示例

```json
{
  "product_id": 5,
  "sku_id": 101,
  "quantity": 1
}
```

### 响应示例（200）

```json
{
  "code": 200,
  "data": {
    "id": 11,
    "user_id": 1,
    "product_id": 5,
    "sku_id": 101,
    "quantity": 1,
    "selected": true
  }
}
```

### 业务逻辑

1. 查询是否存在 `user_id + product_id + sku_id` 相同且 `is_deleted=False` 的记录
2. 如果存在 → `quantity += 新增数量`，更新该记录
3. 如果不存在 → 新建 CartItem，`selected` 默认 `true`
4. 两种情况均返回 `201 Created`（实际代码未显式设置，在响应模型中隐含）

### 对应后端代码

- **路由**: `backend/app/api/v1/carts.py` — `POST /items`
- **Service**: `backend/app/services/cart_service.py` — `CartService.add_item()`

---

## 更新购物车商品

更新指定购物车商品的数量或选中状态。

**请求**: `PUT /api/v1/carts/items/{item_id}`

**认证**: 必须登录（JWT）

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| item_id | integer | 是 | 购物车商品项 ID |

### 请求体（所有字段可选）

| 字段 | 类型 | 说明 |
|------|------|------|
| quantity | integer | 更新后的数量（≥ 1） |
| selected | boolean | 是否选中 |

### 请求示例

```json
{
  "quantity": 3,
  "selected": true
}
```

### 响应示例（200）

```json
{
  "code": 200,
  "data": {
    "id": 10,
    "user_id": 1,
    "product_id": 5,
    "sku_id": 101,
    "quantity": 3,
    "selected": true
  }
}
```

### 响应示例（404 — 记录不存在或不属于当前用户）

```json
{
  "code": 404,
  "message": "Cart item not found"
}
```

### 安全校验

更新前会验证 `item_id` + `user_id` + `is_deleted=False` 三重条件，防止越权操作。

### 对应后端代码

- **路由**: `backend/app/api/v1/carts.py` — `PUT /items/{item_id}`
- **Service**: `backend/app/services/cart_service.py` — `CartService.update_item()`

---

## 删除购物车商品

从购物车中移除指定的商品项（逻辑删除）。

**请求**: `DELETE /api/v1/carts/items/{item_id}`

**认证**: 必须登录（JWT）

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| item_id | integer | 是 | 购物车商品项 ID |

### 响应示例（200）

```json
{
  "code": 200,
  "message": "Item removed successfully"
}
```

### 响应示例（404）

```json
{
  "code": 404,
  "message": "Cart item not found"
}
```

### 业务逻辑

- 使用**逻辑删除**：`is_deleted = True`，而非物理删除
- 删除时验证归属：`user_id` 必须匹配

### 对应后端代码

- **路由**: `backend/app/api/v1/carts.py` — `DELETE /items/{item_id}`
- **Service**: `backend/app/services/cart_service.py` — `CartService.remove_item()`

---

## 清空购物车

将当前用户的全部购物车商品清空（逻辑删除全部）。

**请求**: `DELETE /api/v1/carts/clear`

**认证**: 必须登录（JWT）

### 响应示例（200）

```json
{
  "code": 200,
  "message": "Cart cleared successfully"
}
```

### 业务逻辑

- 将 `is_deleted = True` 作用于该用户**所有**未删除的购物车记录
- 使用批量 UPDATE 而非逐条操作

### 对应后端代码

- **路由**: `backend/app/api/v1/carts.py` — `DELETE /clear`
- **Service**: `backend/app/services/cart_service.py` — `CartService.clear_cart()`

---

## 购物车数据模型（CartItem）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigInteger | 主键，自增 |
| user_id | Integer | 用户 ID（外键 → users） |
| product_id | Integer | 商品 ID（外键 → products） |
| sku_id | Integer | SKU ID（可空） |
| quantity | Integer | 数量 |
| selected | Boolean | 是否选中结算，默认 true |
| is_deleted | Boolean | 逻辑删除标记 |

**唯一约束**: `(user_id, product_id, sku_id)` 组合唯一，防止同一用户重复添加相同商品+规格。

### 关联关系

```
User
└── cart_items → CartItem[]（一对多）

CartItem
└── product → Product（多对一）
```

### 与结算的关联

用户结算时，`OrderService.create_order()` 调用 `CartService.get_selected_items()` 获取 `selected=True` 且在指定 `item_ids` 列表中的购物车项，将这些项转为订单商品。
