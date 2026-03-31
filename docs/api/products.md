# 商品相关接口

本文档描述 ShamGP 商城商品相关的所有 API 接口，基于真实代码生成。

> **代码位置**: `backend/app/api/v1/shop_products.py`  
> **路由前缀**: `/api/v1/shop-products`

---

## 获取商城商品列表

获取已上架的商城商品列表，支持分页、分类筛选和关键词搜索。

**请求**: `GET /api/v1/shop-products/products/simple`

**认证**: 否（公开接口）

### Query 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | integer | 否 | 1 | 页码，从 1 开始 |
| page_size | integer | 否 | 20 | 每页数量，最大 100 |
| category_id | integer | 否 | - | 分类 ID 筛选 |
| keyword | string | 否 | - | 关键词，匹配商品名称或副标题 |

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
      "is_new": false,
      "status": 1,
      "sort": 0
    }
  ],
  "total": 156
}
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 商品 ID |
| name | string | 商品名称 |
| brief | string | 商品简介 |
| cover_image | string | 封面图 URL |
| price | float | 销售价格 |
| original_price | float | 原价 |
| stock | integer | 库存数量 |
| sales | integer | 销量 |
| views | integer | 浏览量 |
| is_hot | boolean | 是否热门 |
| is_new | boolean | 是否新品 |
| status | integer | 状态：0-下架，1-上架 |
| category_id | integer | 分类 ID |

### 对应后端代码

- **路由**: `backend/app/api/v1/shop_products.py` — `GET /shop/products/simple`
- **Service**: `backend/app/services/simple_product_service.py` — `SimpleProductService.get_multi()`
- **模型**: `backend/app/models/product_spu.py` — `ProductSpu`

---

## 获取商城商品详情

获取单个商品的完整信息，包含 SKU 列表。

**请求**: `GET /api/v1/shop-products/products/simple/{id}`

**认证**: 否（公开接口）

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 商品 ID |

### 响应示例（200）

```json
{
  "code": 200,
  "data": {
    "id": 1,
    "category_id": 5,
    "name": "iPhone 15 Pro",
    "subtitle": "钛金属边框，A17 Pro 芯片",
    "code": "SKU-001",
    "brief": "全新苹果手机",
    "description": "<p>商品详情HTML内容...</p>",
    "cover_image": "https://example.com/iphone15.jpg",
    "images": "[\"https://example.com/1.jpg\", \"https://example.com/2.jpg\"]",
    "price": 7999.00,
    "original_price": 8999.00,
    "cost_price": 6500.00,
    "stock": 100,
    "sales": 520,
    "views": 2341,
    "is_hot": true,
    "is_new": false,
    "is_recommend": true,
    "status": 1,
    "sort": 0,
    "category": {
      "id": 5,
      "name": "手机数码"
    },
    "skus": [
      {
        "id": 101,
        "sku_code": "IP15P-256-B",
        "specs": "{\"颜色\": \"黑色\", \"内存\": \"256GB\"}",
        "specs_text": "黑色 / 256GB",
        "price": 7999.00,
        "original_price": 8999.00,
        "stock": 50
      }
    ]
  }
}
```

### 响应示例（404 — 商品不存在或已下架）

```json
{
  "code": 404,
  "message": "商品不存在"
}
```

### 副作用

调用此接口会**自动将商品的 `view_count` 浏览量 +1**。

### 对应后端代码

- **路由**: `backend/app/api/v1/shop_products.py` — `GET /shop/products/simple/{id}`
- **Service**: `backend/app/services/simple_product_service.py` — `SimpleProductService.get()`
- **模型**: `backend/app/models/product_spu.py` — `ProductSpu`

---

## 商品数据模型（ProductSpu）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigInteger | 主键，自增 |
| name | String(200) | 商品名称 |
| subtitle | String(500) | 副标题 |
| category_id | BigInteger | 分类 ID（外键 → product_categories） |
| brand_id | BigInteger | 品牌 ID（外键 → brands） |
| main_image | String(255) | 主图 |
| description | Text | 商品详情（富文本 HTML） |
| unit | String(50) | 单位 |
| status | Integer | 状态：0-下架，1-上架 |
| sort | Integer | 排序 |
| sales_count | Integer | 销量 |
| view_count | Integer | 浏览量 |

### 关联关系

```
ProductSpu
├── category → ProductCategory（多对一）
├── brand → Brand（多对一）
├── skus → ProductSku[]（一对多，含 InventoryRecord）
└── images → ProductImage[]（一对多）
```

### SKU 与库存模型

SKU（Stock Keeping Unit）用于标识同一商品的不同规格（如颜色、内存）。

库存由 `InventoryRecord` 独立表维护：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigInteger | 主键 |
| sku_id | BigInteger | SKU ID（外键，唯一） |
| total_stock | Integer | 总库存 |
| available_stock | Integer | 可用库存 |
| locked_stock | Integer | 锁定库存（下单未付款） |
| warning_stock | Integer | 预警库存 |

---

## 业务逻辑说明

### 商品查询逻辑（SimpleProductService）

1. **状态过滤**：商城列表只返回 `status=1`（已上架）的商品
2. **分类筛选**：`category_id` 精确匹配
3. **关键词搜索**：使用 `LIKE %keyword%` 匹配 `name` 或 `subtitle`
4. **排序规则**：`sort` 升序 → `id` 降序（最新优先）
5. **预加载**：查询时 `joinedload` 加载 category，避免 N+1

### 商城与后台商品的关系

ShamGP 项目中有两套商品相关代码：

| 路径 | 用途 | 模型 |
|------|------|------|
| `app/api/v1/shop_products.py` | C 端商城 | `ProductSpu`（SPU 模型） |
| `app/api/v1/products.py` | B 端管理后台 | `Product`（简单商品模型） |

两者使用不同的 Service 和 Schema，路由前缀分别为 `/shop-products` 和 `/products`。
