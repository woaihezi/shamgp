# API 清单

## 后端 API 清单

### 已注册的 API 路由（api.py）

| 模块 | 路由前缀 | 文件名 | 状态 |
|------|----------|--------|------|
| 认证 | `/api/v1/auth` | `app/api/v1/auth.py` | ✅ 已完成 |
| 购物车 | `/api/v1/carts` | `app/api/v1/carts.py` | ✅ 已完成 |
| 订单 | `/api/v1/orders` | `app/api/v1/orders.py` | ✅ 已完成 |
| 商品 | `/api/v1/products` | `app/api/v1/products.py` | ✅ 已完成 |
| 商城商品 | `/api/v1/shop-products` | `app/api/v1/shop_products.py` | ⚠️ 需确认 |
| 优惠券 | `/api/v1/coupons` | `app/api/v1/coupons.py` | ✅ 已完成 |
| 角色权限 | `/api/v1/roles` | `app/api/v1/roles.py` | ⚠️ 需确认 |
| 支付 | `/api/v1/payments` | `app/api/v1/payments.py` | ⚠️ 骨架 |

### 存在但未注册的 API 路由

| 模块 | 路由前缀 | 文件名 | 状态 |
|------|----------|--------|------|
| 分类 | `/api/v1/categories` | `app/api/v1/categories.py` | ❌ 未注册 |
| 用户 | `/api/v1/users` | `app/api/v1/users.py` | ❌ 未注册 |
| 仪表盘 | `/api/v1/dashboard` | `app/api/v1/dashboard.py` | ❌ 未注册 |
| 库存 | `/api/v1/inventory` | `app/api/v1/inventory.py` | ❌ 未注册 |
| 日志 | `/api/v1/logs` | `app/api/v1/logs.py` | ❌ 未注册 |
| 菜单 | `/api/v1/menus` | `app/api/v1/menus.py` | ❌ 未注册 |
| 系统配置 | `/api/v1/system-config` | `app/api/v1/system_config.py` | ❌ 未注册 |
| 上传 | `/api/v1/uploads` | `app/api/v1/uploads.py` | ❌ 未注册 |
| 管理后台-横幅 | `/api/v1/admin/banners` | `app/api/v1/admin/banners.py` | ❌ 未注册 |
| 管理后台-优惠券 | `/api/v1/admin/coupons` | `app/api/v1/admin/coupons.py` | ❌ 未注册 |
| 商城-优惠券 | `/api/v1/shop/coupons` | `app/api/v1/shop/coupons.py` | ❌ 未注册 |
| 商城-首页 | `/api/v1/shop/home` | `app/api/v1/shop/home.py` | ❌ 未注册 |

---

## 认证 API (/api/v1/auth)

| 方法 | 路径 | 功能 | 状态 |
|------|------|------|------|
| POST | `/login` | 用户登录 | ✅ |
| GET | `/userinfo` | 获取当前用户信息 | ✅ |
| POST | `/logout` | 退出登录 | ✅ |

---

## 购物车 API (/api/v1/carts)

| 方法 | 路径 | 功能 | 状态 |
|------|------|------|------|
| GET | `/` | 获取购物车列表 | ✅ |
| POST | `/` | 添加购物车项 | ✅ |
| PUT | `/{item_id}` | 更新购物车项 | ✅ |
| DELETE | `/{item_id}` | 删除购物车项 | ✅ |

---

## 订单 API (/api/v1/orders)

| 方法 | 路径 | 功能 | 状态 |
|------|------|------|------|
| GET | `/addresses` | 获取地址列表 | ✅ |
| GET | `/addresses/default` | 获取默认地址 | ✅ |
| POST | `/addresses` | 创建地址 | ✅ |
| PUT | `/addresses/{address_id}` | 更新地址 | ✅ |
| DELETE | `/addresses/{address_id}` | 删除地址 | ✅ |
| POST | `/` | 创建订单 | ✅ |
| GET | `/` | 获取订单列表 | ✅ |
| GET | `/{order_id}` | 获取订单详情 | ✅ |
| PUT | `/{order_id}/status` | 更新订单状态 | ✅ |
| POST | `/{order_id}/cancel` | 取消订单 | ✅ |
| POST | `/refunds` | 申请退款 | ✅ |
| GET | `/refunds` | 获取退款列表 | ✅ |
| GET | `/refunds/{refund_id}` | 获取退款详情 | ✅ |
| GET | `/admin/` | 管理员获取订单列表 | ✅ |
| GET | `/admin/{order_id}` | 管理员获取订单详情 | ✅ |
| PUT | `/admin/{order_id}/status` | 管理员更新订单状态 | ✅ |

---

## 商品 API (/api/v1/products)

| 方法 | 路径 | 功能 | 状态 |
|------|------|------|------|
| GET | `/simple` | 获取简单商品列表（公开） | ✅ |
| GET | `/simple/{id}` | 获取简单商品详情（公开） | ✅ |
| POST | `/simple` | 创建简单商品 | ✅ |
| PUT | `/simple/{id}` | 更新简单商品 | ✅ |

---

## 前端商城 API 封装 (frontend-shop/src/api/)

| 文件 | 功能 | 状态 | API 路径匹配 |
|------|------|------|-------------|
| `auth.ts` | 认证相关 | ✅ | `/api/v1/auth` |
| `cart.ts` | 购物车相关 | ✅ | `/api/v1/carts` |
| `category.ts` | 分类相关 | ⚠️ | 路径可能不匹配 |
| `home.ts` | 首页相关 | ⚠️ | 需确认 |
| `order.ts` | 订单相关 | ✅ | `/api/v1/orders` |
| `payment.ts` | 支付相关 | ⚠️ | 骨架 |
| `product.ts` | 商品相关 | ⚠️ | 路径不匹配（调用 `/shop-products/shop`） |

---

## 管理后台 API 封装 (frontend-admin/src/api/)

| 文件 | 功能 | 状态 |
|------|------|------|
| `auth.ts` | 认证相关 | ✅ |
| `file.ts` | 文件相关 | ⚠️ |
| `marketing.ts` | 营销相关 | ⚠️ |
| `order.ts` | 订单相关 | ⚠️ |
| `product.ts` | 商品相关 | ⚠️ |
| `report.ts` | 报表相关 | ⚠️ |
| `request.ts` | 请求封装 | ✅ |
| `setting.ts` | 设置相关 | ⚠️ |

---

## API 问题汇总

1. **大量 API 路由未注册** - 至少 10+ 个路由文件存在但未在 api.py 中注册
2. **前后端 API 路径不匹配** - 前端商城调用 `/api/v1/shop-products/shop/` 但后端没有该路由
3. **管理后台 API 路径不明确** - 缺少 `/admin/*` 前缀的统一管理
4. **部分 API 只有骨架** - dashboard, payments, uploads 等
