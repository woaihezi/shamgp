# 收藏接口

本文档描述 ShamGP 商城收藏相关的所有 API 接口，基于真实代码生成。

> **代码位置**: `backend/app/api/v1/favorites.py`  
> **路由前缀**: `/api/v1/favorites`

---

## 添加收藏

将指定商品添加到用户收藏列表。如果已收藏则直接返回，不重复创建。

**请求**: `POST /api/v1/favorites`

**认证**: 必须登录（JWT）

### Query 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| product_id | integer | 是 | 商品 ID |

### 响应示例（200）

```json
{
  "code": 200,
  "data": {
    "id": 5,
    "user_id": 1,
    "product_id": 10,
    "created_at": "2026-03-31T11:00:00Z"
  }
}
```

### 业务逻辑

1. 检查是否已存在 `user_id + product_id` 相同的收藏记录
2. 如果已存在 → 直接返回该记录（幂等，不报错）
3. 如果不存在 → 新建 `Favorite` 记录

### 对应后端代码

- **路由**: `backend/app/api/v1/favorites.py` — `POST /`
- **Service**: `backend/app/services/favorite_service.py` — `FavoriteService.add_favorite()`

---

## 取消收藏

将指定商品从用户收藏列表中移除。

**请求**: `DELETE /api/v1/favorites/{product_id}`

**认证**: 必须登录（JWT）

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| product_id | integer | 是 | 商品 ID |

### 响应示例（200）

```json
{
  "code": 200,
  "message": "已取消收藏"
}
```

### 业务逻辑

根据 `user_id + product_id` 执行物理删除（`DELETE` 语句），返回删除行数（`rowcount > 0` 表示成功）。

### 对应后端代码

- **路由**: `backend/app/api/v1/favorites.py` — `DELETE /{product_id}`
- **Service**: `backend/app/services/favorite_service.py` — `FavoriteService.remove_favorite()`

---

## 获取收藏列表

获取当前用户的全部收藏商品。

**请求**: `GET /api/v1/favorites`

**认证**: 必须登录（JWT）

### 响应示例

```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "category_id": 5,
      "name": "iPhone 15 Pro",
      "code": "SKU-001",
      "brief": "全新苹果手机",
      "cover_image": "https://example.com/iphone15.jpg",
      "price": 7999.00,
      "original_price": 8999.00,
      "stock": 100,
      "sales": 520,
      "views": 2340,
      "is_hot": true,
      "status": 1,
      "category": {
        "id": 5,
        "name": "手机数码"
      }
    }
  ]
}
```

### 业务逻辑

1. 查询用户所有收藏记录，返回 `Favorite` 列表
2. 提取所有 `product_id`
3. 批量调用 `product_spu_service.get_multi_by_ids()` 获取商品详情
4. 按收藏时间倒序排列（`created_at DESC`）

### 对应后端代码

- **路由**: `backend/app/api/v1/favorites.py` — `GET /`
- **Service**: `backend/app/services/favorite_service.py` — `FavoriteService.get_user_favorites()`

---

## Favorite 数据模型

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigInteger | 主键，自增 |
| user_id | Integer | 用户 ID（外键 → users） |
| product_id | Integer | 商品 ID（外键 → products） |
| created_at | DateTime | 收藏时间 |

### 索引

- `INDEX idx_favorites_user_id(user_id)`
- `INDEX idx_favorites_product_id(product_id)`

### 关联关系

```
User
└── favorites → Favorite[]（一对多）

Favorite
├── user → User（多对一）
└── product → Product（多对一）
```
