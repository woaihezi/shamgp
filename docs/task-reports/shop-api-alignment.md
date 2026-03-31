# Shop API Alignment - 前后端 API 对齐清单

**生成时间:** 2026-03-31  
**后端 Base URL:** `http://localhost:8000`  
**前端 Base URL:** `/api/v1`（via Vite proxy）

---

## 一、对齐总览

| 类别 | 前端路径 | 后端路径 | 状态 | 备注 |
|------|---------|---------|------|------|
| 认证注册 | `/api/v1/auth/register` | `/api/v1/auth/register` | ✅ 对齐 | |
| 认证登录 | `/api/v1/auth/login` | `/api/v1/auth/login` | ✅ 对齐 | |
| 认证用户信息 | `/api/v1/auth/userinfo` | `/api/v1/auth/userinfo` | ✅ 对齐 | |
| 认证登出 | `/api/v1/auth/logout` | `/api/v1/auth/logout` | ✅ 对齐 | |
| 购物车摘要 | `/api/v1/carts/summary` | `/api/v1/carts/summary` | ✅ 对齐 | |
| 购物车列表 | `/api/v1/carts/items` | `/api/v1/carts/items` | ✅ 对齐 | |
| 购物车添加 | `/api/v1/carts/items` | `/api/v1/carts/items` | ✅ 对齐 | |
| 购物车更新 | `/api/v1/carts/items/{id}` | `/api/v1/carts/items/{id}` | ✅ 对齐 | |
| 购物车删除 | `/api/v1/carts/items/{id}` | `/api/v1/carts/items/{id}` | ✅ 对齐 | |
| 购物车清空 | `/api/v1/carts/clear` | `/api/v1/carts/clear` | ✅ 对齐 | |
| 订单创建 | `/api/v1/orders/` | `/api/v1/orders/` | ✅ 对齐 | |
| 订单列表 | `/api/v1/orders/` | `/api/v1/orders/` | ✅ 对齐 | |
| 订单详情 | `/api/v1/orders/{id}` | `/api/v1/orders/{id}` | ✅ 对齐 | |
| 订单取消 | `/api/v1/orders/{id}/cancel` | `/api/v1/orders/{id}/cancel` | ✅ 对齐 | |
| 收货地址列表 | `/api/v1/orders/addresses` | `/api/v1/orders/addresses` | ✅ 对齐 | |
| 默认收货地址 | `/api/v1/orders/addresses/default` | `/api/v1/orders/addresses/default` | ✅ 对齐 | |
| 创建收货地址 | `/api/v1/orders/addresses` | `/api/v1/orders/addresses` | ✅ 对齐 | |
| 更新收货地址 | `/api/v1/orders/addresses/{id}` | `/api/v1/orders/addresses/{id}` | ✅ 对齐 | |
| 删除收货地址 | `/api/v1/orders/addresses/{id}` | `/api/v1/orders/addresses/{id}` | ✅ 对齐 | |
| 支付创建 | `/api/v1/payments/pay` | `/api/v1/payments/pay` | ✅ 对齐 | |
| 支付状态 | `/api/v1/payments/{orderId}/status` | `/api/v1/payments/{orderId}/status` | ✅ 对齐 | |
| 支付网关 | `/api/v1/payments/gateway` | `/api/v1/payments/gateway` | ✅ 对齐 | |
| 商品列表 | `/api/v1/products` | `/api/v1/products/simple` | ⚠️ 注意 | 见下方说明 |
| 商品详情 | `/api/v1/products/{id}` | `/api/v1/products/simple/{id}` | ⚠️ 注意 | 见下方说明 |
| 分类列表 | `/api/v1/categories` | `/api/v1/categories` | ✅ 对齐 | |
| 首页 Banner | `/api/v1/shop/home/banners` | `/api/v1/shop/home/banners` | ✅ 对齐 | |
| 可用优惠券 | `/api/v1/shop/home/coupons/available` | `/api/v1/shop/home/coupons/available` | ✅ 对齐 | |
| 首页楼层 | `/api/v1/shop/home/floors` | `/api/v1/shop/home/floors` | ✅ 对齐 | |
| 首页配置 | `/api/v1/shop/home/config` | `/api/v1/shop/home/config` | ✅ 对齐 | |

---

## 二、关键差异说明

### 2.1 商品 API（/products vs /products/simple）

**重要：** 后端的商品路由挂载在 `/products/simple` 路径下，而非 `/products`。

**后端路由注册（`api/v1/products.py`）：**
```python
router = APIRouter()  # 无 prefix，直接在路由上定义

@router.get("/simple")           # → /api/v1/products/simple
@router.get("/simple/{id}")      # → /api/v1/products/simple/{id}
```

**前端当前 `product.ts` 使用的路径：**
```typescript
const API_BASE = '/api/v1'
getProducts: () => request.get(`${API_BASE}/products/simple`, ...)
// ✅ 正确映射到后端 /api/v1/products/simple
getProduct: (id) => request.get(`${API_BASE}/products/simple/${id}`)
// ✅ 正确映射到后端 /api/v1/products/simple/{id}
```

### 2.2 商城首页 API

**后端路由挂载（`api/v1/shop/home.py`）：**
```python
router = APIRouter(prefix="/shop/home", tags=["商城首页"])  
# → /api/v1/shop/home/...
```

**前端 `home.ts` 使用的 BASE_URL：**
```typescript
const BASE_URL = '/api/v1/shop'
// ✅ 正确映射到后端 /api/v1/shop/home/...
```

---

## 三、认证要求对照

| API | 认证要求 | 前端 Header |
|-----|---------|-------------|
| `POST /api/v1/auth/register` | ❌ 公开 | - |
| `POST /api/v1/auth/login` | ❌ 公开 | - |
| `GET /api/v1/auth/userinfo` | ✅ Bearer Token | `Authorization: Bearer {access_token}` |
| `POST /api/v1/auth/logout` | ❌ 公开 | - |
| `GET /api/v1/products/simple` | ❌ 公开 | - |
| `GET /api/v1/products/simple/{id}` | ❌ 公开 | - |
| `GET /api/v1/carts/summary` | ✅ Bearer Token | `Authorization: Bearer {access_token}` |
| `GET /api/v1/carts/items` | ✅ Bearer Token | `Authorization: Bearer {access_token}` |
| `POST /api/v1/carts/items` | ✅ Bearer Token | `Authorization: Bearer {access_token}` |
| `PUT /api/v1/carts/items/{id}` | ✅ Bearer Token | `Authorization: Bearer {access_token}` |
| `DELETE /api/v1/carts/items/{id}` | ✅ Bearer Token | `Authorization: Bearer {access_token}` |
| `DELETE /api/v1/carts/clear` | ✅ Bearer Token | `Authorization: Bearer {access_token}` |
| `POST /api/v1/orders/` | ✅ Bearer Token | `Authorization: Bearer {access_token}` |
| `GET /api/v1/orders/` | ✅ Bearer Token | `Authorization: Bearer {access_token}` |
| `GET /api/v1/orders/{id}` | ✅ Bearer Token | `Authorization: Bearer {access_token}` |
| `POST /api/v1/orders/{id}/cancel` | ✅ Bearer Token | `Authorization: Bearer {access_token}` |

> **Token 存储位置:** `localStorage.access_token`  
> **Token 格式:** JWT Bearer Token  
> **请求拦截器:** `frontend-shop/src/api/request.ts` 自动附加 Authorization header

---

## 四、数据模型映射

### 4.1 商品数据结构

**后端返回（`ProductSpu`）：**
```typescript
{
  id: number
  name: string
  subtitle?: string
  category_id?: number
  brand_id?: number
  cover_image?: string       // ← 前端应使用此字段
  main_image?: string        // ← 备用
  description?: string
  unit?: string
  status?: number
  sales?: number
  sales_count?: number
  view_count?: number
  price?: number             // ← SPU 价格（可能有 SKU 价格）
  original_price?: number
  min_price?: number         // ← SKU 最低价
  max_price?: number
  is_hot?: boolean
  is_new?: boolean
  created_at?: string
  updated_at?: string
  category?: Category
  brand?: Brand
  skus?: ProductSku[]
  images?: ProductImage[]
}
```

**前端 `ProductSpu` 类型（`api/product.ts`）：** ✅ 与后端完全匹配

**前端 `ProductList/index.vue` 兼容处理：**
```typescript
// 图片字段
product.cover_image || product.mainImage

// 价格字段
product.price || product.minPrice || 0

// 库存字段
(product as any).stock || (product as any).inventory?.available_stock || 99
```

### 4.2 购物车数据结构

**后端 `CartItem` 字段：** `id, user_id, product_id, sku_id, quantity, selected, created_at, updated_at`  
**前端 `cart.ts` 接口字段：** ✅ 兼容

---

## 五、响应格式统一

所有 API 统一响应格式（通过 `request.ts` 拦截器标准化）：

```typescript
// 成功
{ code: 200, message: "success", data: T }

// 失败
{ code: xxx, message: "错误信息", data: null }
```

后端中间件处理：
- `res.code !== 200` → 抛出 `Promise.reject`
- 拦截器统一返回 `{ code: 200, message: 'success', data: res }` 格式
