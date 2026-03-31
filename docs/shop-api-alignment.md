# 商城前后端 API 对齐清单

> 更新：2026-03-31

---

## 后端路由注册（`/api/v1` 前缀）

| 后端路径 | 方法 | 认证 | 前端对应 | 状态 |
|---------|------|------|---------|------|
| `/auth/register` | POST | 否 | `POST /api/v1/auth/register` | ✅ |
| `/auth/login` | POST | 否 | `POST /api/v1/auth/login` | ✅ |
| `/auth/userinfo` | GET | JWT | `GET /api/v1/auth/userinfo` | ✅ |
| `/auth/logout` | POST | JWT | `POST /api/v1/auth/logout` | ✅ |
| `/products` | GET | 否 | `GET /api/v1/products` | ✅ 新增 |
| `/products/{id}` | GET | 否 | `GET /api/v1/products/{id}` | ✅ 新增 |
| `/products/simple` | GET | 否 | （Admin 端） | ✅ |
| `/categories` | GET | 否 | `GET /api/v1/categories` | ✅ |
| `/carts/summary` | GET | JWT | `GET /api/v1/carts/summary` | ✅ |
| `/carts/items` | GET | JWT | `GET /api/v1/carts/items` | ✅ |
| `/carts/items` | POST | JWT | `POST /api/v1/carts/items` | ✅ |
| `/carts/items/{id}` | PUT | JWT | `PUT /api/v1/carts/items/{id}` | ✅ |
| `/carts/items/{id}` | DELETE | JWT | `DELETE /api/v1/carts/items/{id}` | ✅ |
| `/carts/clear` | DELETE | JWT | `DELETE /api/v1/carts/clear` | ✅ |
| `/orders/` | GET | JWT | `GET /api/v1/orders/` | ✅ |
| `/orders/` | POST | JWT | `POST /api/v1/orders/` | ✅ |
| `/orders/{id}` | GET | JWT | `GET /api/v1/orders/{id}` | ✅ |
| `/addresses` | GET | JWT | （Shop 未对接） | ⚠️ |
| `/coupons/` | GET | JWT | `GET /api/v1/coupons/` | ✅ |
| `/coupons/` | POST | JWT | `POST /api/v1/coupons/` | ✅ |
| `/coupons/verify` | POST | 否 | （优惠券核销） | ⚠️ |
| `/payments/pay` | POST | JWT | （下单后支付） | ⚠️ |
| `/home/banners` | GET | 否 | `GET /api/v1/home/banners` | ⚠️ 待对接 |
| `/home/coupons/available` | GET | 否 | `GET /api/v1/home/coupons/available` | ⚠️ 待对接 |

---

## 前端 API 文件路径映射

| 前端文件 | API 路径 | 后端路径 | 状态 |
|---------|---------|---------|------|
| `src/api/auth.ts` | `/api/v1/auth/*` | `/auth/*` | ✅ |
| `src/api/cart.ts` | `/api/v1/carts/*` | `/carts/*` | ✅ |
| `src/api/product.ts` | `/api/v1/products` | `/products` | ✅ |
| `src/api/order.ts` | `/api/v1/orders/*` | `/orders/*` | ✅ |
| `src/api/payment.ts` | `/api/v1/payments/*` | `/payments/*` | ✅ |
| `src/api/category.ts` | `/api/v1/categories` | `/categories` | ✅ |
| `src/api/home.ts` | `/api/v1/home/*` | `/home/*` | ⚠️ |

---

## Token 存储

| 位置 | 字段名 | 状态 |
|------|--------|------|
| `localStorage` | `access_token` | ✅ 统一 |
| `user store` (Pinia) | `token` → `access_token` | ✅ |

---

## 待解决不匹配

1. **收货地址 API**：`POST /api/v1/orders/` 需要 `address_id`，但前端 Shop 尚未实现地址管理
2. **优惠券核销**：下单时需传入 `coupon_code`，前后端尚未联调
3. **支付回调**：Mock 支付已就绪，真实支付待接入
