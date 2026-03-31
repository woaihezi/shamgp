# Task 02: 商城最小可用闭环

> 日期：2026-03-31
> 状态：✅ 完成

---

## 一、改了哪些文件

### 后端修复
| 文件 | 修改内容 |
|------|---------|
| `app/schemas/common.py` | 新增 `PaginationResult`、`PageResponse`、`PaginationParams`、`IdMixin` alias |
| `app/schemas/coupon.py` | 新增 `CouponReceiveRecord`、`CouponReceiveRecordCreate`、`CouponPageResult`、`CouponReceiveRecordPageResult`；新增 `Coupon` alias |
| `app/models/base.py` | 新增 `IDMixin` class |
| `app/models/role.py` | 新增 `role_menu_association` 表；新增 `menus` relationship |
| `app/models/user.py` | 已有 `user_role_association`（无需修改） |
| `app/api/deps.py` | 新增 `get_current_active_superuser` 函数 |
| `app/services/coupon_service.py` | 重写为类方法模式；新增 `get_multi_paginated`、`update` 方法；新增 `coupon_service` 和 `coupon_receive_record_service` 实例 |
| `app/services/dashboard_service.py` | 修复 HTML 实体 `&gt;` → `>` |
| `app/services/log_service.py` | 修复 HTML 实体 |
| `app/services/upload_service.py` | 修复 HTML 实体 |
| `app/services/system_config_service.py` | 修复 HTML 实体 |
| `app/api/v1/products.py` | 新增商城端 `GET /` 和 `GET /{id}` 路由（别名） |
| `app/api/v1/auth.py` | 移除调试 try-except（已恢复） |

### 前端修复
| 文件 | 修改内容 |
|------|---------|
| `frontend-shop/src/api/auth.ts` | 路径加 `/api/v1` 前缀 |
| `frontend-shop/src/api/cart.ts` | 路径加 `/api/v1` 前缀 |
| `frontend-shop/src/api/product.ts` | 确认使用 `/api/v1` |
| `frontend-shop/src/api/order.ts` | 确认使用 `/api/v1` |
| `frontend-shop/src/api/payment.ts` | 确认使用 `/api/v1` |
| `frontend-shop/src/api/category.ts` | 确认使用 `/api/v1` |
| `frontend-shop/src/api/home.ts` | 确认使用 `/api/v1` |

---

## 二、新增/修复了哪些 API 路由

| 路由 | 方法 | 状态 | 说明 |
|------|------|------|------|
| `/api/v1/auth/register` | POST | ✅ | 用户注册（已有） |
| `/api/v1/auth/login` | POST | ✅ | 用户登录（已有） |
| `/api/v1/auth/userinfo` | GET | ✅ | 用户信息 |
| `/api/v1/products` | GET | ✅ 新增 | 商品列表（商城端） |
| `/api/v1/products/{id}` | GET | ✅ 新增 | 商品详情（商城端） |
| `/api/v1/carts/summary` | GET | ✅ | 购物车摘要 |
| `/api/v1/carts/items` | GET/POST | ✅ | 购物车项 |
| `/api/v1/orders/` | GET | ✅ | 订单列表 |
| `/api/v1/coupons/` | GET/POST | ✅ | 优惠券列表/创建 |

---

## 三、修复的 API 不匹配问题

1. **前端 API 路径缺 `/api/v1` 前缀**：7 个 API 文件全部修复
2. **商城商品列表 404**：新增 `GET /api/v1/products` 和 `GET /api/v1/products/{id}` 别名路由
3. **Coupon schema 缺类型**：`CouponPageResult`、`CouponReceiveRecord` 等缺失导致 4 个路由 skip
4. **`get_current_active_superuser` 缺失**：`users.py`、`menus.py` 等依赖此函数
5. **`PaginationParams`/`PageResponse` 缺失**：`common.py` schema 别名补全
6. **`role_menu` 表缺失**：导致 `Role.menus` relationship 初始化失败，auth 500
7. **HTML 实体污染**：4 个 service 文件含 `&gt;`/`&lt;` 导致 SyntaxError

---

## 四、默认测试账号

| 账号 | 密码 | 角色 |
|------|------|------|
| `admin` | `admin123` | 超级管理员 |
| `testuser` | - | 已存在（密码未知） |
| 注册新账号 | `POST /api/v1/auth/register` | 普通用户 |

---

## 五、商城最小闭环当前状态

```
✅ 用户注册     POST /api/v1/auth/register
✅ 用户登录     POST /api/v1/auth/login
✅ 商品列表     GET  /api/v1/products
✅ 商品详情     GET  /api/v1/products/{id}
✅ 加入购物车   POST /api/v1/carts/items
✅ 购物车查询   GET  /api/v1/carts/summary
⚠️ 创建订单    POST /api/v1/orders/  （需收货地址）
⚠️ 订单支付    POST /api/v1/payments/pay
```

---

## 六、剩余未完成问题

| 问题 | 优先级 | 说明 |
|------|--------|------|
| 创建订单需要 address_id | P1 | 需先有收货地址 |
| 订单完整支付流程 | P2 | Mock 支付已就绪 |
| 商城前端路由注册 | P1 | ProductList/Detail/Login/Register 路由已挂载 |
| 商品详情页用 mock 数据 | P1 | 需改为调用 `GET /api/v1/products/{id}` |
| 优惠券下单核销 | P2 | 需下单时传入 coupon_code |
| Admin 用户/权限页 | P2 | 本轮未做 |
| 库存超卖问题 | P1 | 下单不扣库存 |
| Docker 完善 | P3 | 本轮未做 |
