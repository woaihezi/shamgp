# API 对齐报告

**检查日期**: 2026-03-31  
**项目名称**: ShamGP 商城项目

---

## 前端商城 API 检查

| 前端文件路径                      | 前端调用路径                                   | 后端真实路径          | HTTP 方法           | 是否对齐  | 修复说明                                      |
| --------------------------------- | ---------------------------------------------- | --------------------- | ------------------- | --------- | --------------------------------------------- |
| frontend-shop/src/api/auth.ts     | /auth/login                                    | /api/v1/auth/login    | POST                | ✅ 是     | -                                             |
| frontend-shop/src/api/auth.ts     | /auth/register                                 | /api/v1/auth/register | POST                | ✅ 是     | -                                             |
| frontend-shop/src/api/auth.ts     | /auth/userinfo                                 | /api/v1/auth/userinfo | GET                 | ✅ 是     | -                                             |
| frontend-shop/src/api/auth.ts     | /auth/logout                                   | /api/v1/auth/logout   | POST                | ✅ 是     | -                                             |
| frontend-shop/src/api/product.ts  | /api/v1/shop-products/shop/categories          | /api/v1/categories    | GET                 | ❌ 否     | 前端调用路径错误，应改为 /api/v1/categories   |
| frontend-shop/src/api/product.ts  | /api/v1/shop-products/shop/products/simple     | /api/v1/products      | GET                 | ❌ 否     | 前端调用路径错误，应改为 /api/v1/products     |
| frontend-shop/src/api/product.ts  | /api/v1/shop-products/shop/products/simple/:id | /api/v1/products/:id  | GET                 | ❌ 否     | 前端调用路径错误，应改为 /api/v1/products/:id |
| frontend-shop/src/api/category.ts | 需要检查                                       | /api/v1/categories    | GET                 | ⚠️ 待确认 | -                                             |
| frontend-shop/src/api/cart.ts     | 需要检查                                       | /api/v1/carts         | GET/POST/PUT/DELETE | ⚠️ 待确认 | -                                             |
| frontend-shop/src/api/order.ts    | 需要检查                                       | /api/v1/orders        | GET/POST            | ⚠️ 待确认 | -                                             |

---

## 前端管理后台 API 检查

| 前端文件路径                      | 前端调用路径 | 后端真实路径       | HTTP 方法           | 是否对齐  | 修复说明 |
| --------------------------------- | ------------ | ------------------ | ------------------- | --------- | -------- |
| frontend-admin/src/api/auth.ts    | 需要检查     | /api/v1/auth/login | POST                | ⚠️ 待确认 | -        |
| frontend-admin/src/api/product.ts | 需要检查     | /api/v1/products   | GET/POST/PUT/DELETE | ⚠️ 待确认 | -        |
| frontend-admin/src/api/order.ts   | 需要检查     | /api/v1/orders     | GET/PUT             | ⚠️ 待确认 | -        |

---

## 后端已注册路由清单

| 路由前缀              | 说明       | 状态      |
| --------------------- | ---------- | --------- |
| /api/v1/auth          | 认证相关   | ✅ 已注册 |
| /api/v1/carts         | 购物车     | ✅ 已注册 |
| /api/v1/orders        | 订单       | ✅ 已注册 |
| /api/v1/products      | 商品       | ✅ 已注册 |
| /api/v1/shop-products | 商城商品   | ✅ 已注册 |
| /api/v1/categories    | 分类       | ✅ 已注册 |
| /api/v1/users         | 用户       | ✅ 已注册 |
| /api/v1/dashboard     | 仪表盘     | ✅ 已注册 |
| /api/v1/inventory     | 库存       | ✅ 已注册 |
| /api/v1/logs          | 日志       | ✅ 已注册 |
| /api/v1/menus         | 菜单       | ✅ 已注册 |
| /api/v1/system-config | 系统配置   | ✅ 已注册 |
| /api/v1/uploads       | 上传       | ✅ 已注册 |
| /api/v1/coupons       | 优惠券     | ✅ 已注册 |
| /api/v1/roles         | 角色       | ✅ 已注册 |
| /api/v1/payments      | 支付       | ✅ 已注册 |
| /api/v1/admin/banners | 横幅管理   | ✅ 已注册 |
| /api/v1/admin/coupons | 优惠券管理 | ✅ 已注册 |
| /api/v1/shop/coupons  | 商城优惠券 | ✅ 已注册 |
| /api/v1/shop/home     | 商城首页   | ✅ 已注册 |

---

## 需要修复的项

### 1. 前端商城 product.ts 路径修复

- **问题**: 前端调用 `/api/v1/shop-products/shop/*` 但后端没有该路径
- **修复**: 修改 `frontend-shop/src/api/product.ts` 中的 API 路径

### 2. 其他 API 文件检查

- 需要检查 category.ts, cart.ts, order.ts 等文件的路径是否正确

---

## 备注

- 部分路由只有骨架实现（如 dashboard, payments, uploads），已在 api.py 中标记为"已注册但待完善"
- 建议优先修复 product.ts 的路径问题，然后测试首页数据加载
