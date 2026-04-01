# API 接口总览

本文档提供 ShamGP 商城项目所有 API 接口的完整总览。

---

## 一、基础信息

### 1.1 API 基础路径
- **开发环境**: `http://localhost:8000/api/v1`
- **生产环境**: `https://your-domain.com/api/v1`

### 1.2 响应格式
所有 API 响应统一使用以下格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

**分页响应格式**：
```json
{
  "code": 200,
  "message": "success",
  "data": [],
  "total": 100,
  "page": 1,
  "page_size": 20
}
```

### 1.3 状态码说明

| HTTP 状态码 | code | 说明 |
|------------|------|------|
| 200 | 200 | 成功 |
| 400 | 400 | 请求参数错误 |
| 401 | 401 | 未认证 |
| 403 | 403 | 无权限 |
| 404 | 404 | 资源不存在 |
| 500 | 500 | 服务器内部错误 |

### 1.4 认证方式

使用 JWT Bearer Token 认证：

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 二、API 模块总览

### 2.1 认证模块 (Auth)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 用户注册 | POST | `/auth/register` | 否 | 注册新用户 |
| 用户登录 | POST | `/auth/login` | 否 | 用户登录获取 Token |
| 获取用户信息 | GET | `/auth/userinfo` | 是 | 获取当前登录用户信息 |
| 退出登录 | POST | `/auth/logout` | 是 | 退出登录 |
| 获取菜单树 | GET | `/auth/menu-tree` | 是 | 获取用户菜单树 |
| 获取路由 | GET | `/auth/routers` | 是 | 获取用户路由 |

**详细文档**: [auth.md](./api/auth.md)

---

### 2.2 用户模块 (Users)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 获取用户列表 | GET | `/users/` | 是(管理员) | 获取用户列表 |
| 获取用户详情 | GET | `/users/{id}` | 是 | 获取用户详情 |
| 创建用户 | POST | `/users/` | 是(管理员) | 创建新用户 |
| 更新用户 | PUT | `/users/{id}` | 是 | 更新用户信息 |
| 删除用户 | DELETE | `/users/{id}` | 是(管理员) | 删除用户 |

---

### 2.3 商品模块 (Products)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 获取商品列表(简单) | GET | `/products/simple` | 否 | 获取简单商品列表 |
| 获取商品详情(简单) | GET | `/products/simple/{id}` | 否 | 获取简单商品详情 |
| 创建商品(简单) | POST | `/products/simple` | 是(管理员) | 创建简单商品 |
| 更新商品(简单) | PUT | `/products/simple/{id}` | 是(管理员) | 更新简单商品 |
| 删除商品(简单) | DELETE | `/products/simple/{id}` | 是(管理员) | 删除简单商品 |
| 商城商品列表 | GET | `/products/` | 否 | 商城端商品列表 |
| 商城商品详情 | GET | `/products/{id}` | 否 | 商城端商品详情 |

**详细文档**: [products.md](./api/products.md)

---

### 2.4 分类模块 (Categories)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 获取分类列表 | GET | `/categories/` | 否 | 获取分类列表 |
| 获取分类详情 | GET | `/categories/{id}` | 否 | 获取分类详情 |
| 创建分类 | POST | `/categories/` | 是(管理员) | 创建分类 |
| 更新分类 | PUT | `/categories/{id}` | 是(管理员) | 更新分类 |
| 删除分类 | DELETE | `/categories/{id}` | 是(管理员) | 删除分类 |

---

### 2.5 购物车模块 (Carts)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 获取购物车摘要 | GET | `/carts/summary` | 是 | 获取购物车摘要 |
| 获取购物车项 | GET | `/carts/items` | 是 | 获取购物车项列表 |
| 添加购物车项 | POST | `/carts/items` | 是 | 添加商品到购物车 |
| 更新购物车项 | PUT | `/carts/items/{item_id}` | 是 | 更新购物车项 |
| 删除购物车项 | DELETE | `/carts/items/{item_id}` | 是 | 删除购物车项 |
| 清空购物车 | DELETE | `/carts/clear` | 是 | 清空购物车 |

**详细文档**: [cart.md](./api/cart.md)

---

### 2.6 订单模块 (Orders)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 获取订单列表 | GET | `/orders/` | 是 | 获取当前用户订单列表 |
| 获取订单详情 | GET | `/orders/{order_id}` | 是 | 获取订单详情 |
| 创建订单 | POST | `/orders/` | 是 | 创建新订单 |
| 取消订单 | PUT | `/orders/{order_id}/cancel` | 是 | 取消订单 |
| 管理后台订单列表 | GET | `/orders/admin/` | 是(管理员) | 管理后台订单列表 |
| 更新订单状态 | PUT | `/orders/admin/{id}/status` | 是(管理员) | 更新订单状态 |

**详细文档**: [orders.md](./api/orders.md)

---

### 2.7 优惠券模块 (Coupons)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 获取优惠券列表 | GET | `/coupons/` | 否 | 获取优惠券列表 |
| 获取优惠券详情 | GET | `/coupons/{id}` | 否 | 获取优惠券详情 |
| 领取优惠券 | POST | `/coupons/{id}/receive` | 是 | 领取优惠券 |
| 我的优惠券 | GET | `/coupons/my` | 是 | 获取我的优惠券 |
| 创建优惠券 | POST | `/coupons/` | 是(管理员) | 创建优惠券 |

**详细文档**: [coupons.md](./api/coupons.md)

---

### 2.8 收藏模块 (Favorites)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 获取收藏列表 | GET | `/favorites/` | 是 | 获取收藏列表 |
| 添加收藏 | POST | `/favorites/` | 是 | 添加收藏 |
| 删除收藏 | DELETE | `/favorites/{id}` | 是 | 删除收藏 |

**详细文档**: [favorites.md](./api/favorites.md)

---

### 2.9 浏览历史模块 (Browse History)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 获取浏览历史 | GET | `/browse-history/` | 是 | 获取浏览历史 |
| 清除浏览历史 | DELETE | `/browse-history/clear` | 是 | 清除浏览历史 |

**详细文档**: [browse-history.md](./api/browse-history.md)

---

### 2.10 角色权限模块 (Roles & Permissions)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 获取角色列表 | GET | `/roles/` | 是(管理员) | 获取角色列表 |
| 创建角色 | POST | `/roles/` | 是(管理员) | 创建角色 |
| 更新角色 | PUT | `/roles/{id}` | 是(管理员) | 更新角色 |
| 删除角色 | DELETE | `/roles/{id}` | 是(管理员) | 删除角色 |

---

### 2.11 仪表盘模块 (Dashboard)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 获取统计数据 | GET | `/dashboard/stats` | 是(管理员) | 获取仪表盘统计数据 |

---

### 2.12 支付模块 (Payments)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 支付订单 | POST | `/payments/pay` | 是 | 支付订单 |
| 支付回调 | POST | `/payments/callback` | 否 | 支付回调 |

---

### 2.13 文件上传模块 (Uploads)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 上传文件 | POST | `/uploads/` | 是 | 上传文件 |

---

### 2.14 系统配置模块 (System Config)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 获取系统配置 | GET | `/system-config/` | 是(管理员) | 获取系统配置 |
| 更新系统配置 | PUT | `/system-config/` | 是(管理员) | 更新系统配置 |

---

### 2.15 商城专属模块 (Shop)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 首页数据 | GET | `/shop/home` | 否 | 获取首页数据 |
| 商城商品列表 | GET | `/shop/products/simple` | 否 | 商城商品列表 |
| 商城商品详情 | GET | `/shop/products/simple/{id}` | 否 | 商城商品详情 |
| 商城优惠券列表 | GET | `/shop/coupons/` | 否 | 商城优惠券列表 |

---

### 2.16 管理后台专属模块 (Admin)

| 接口 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| Banner 管理 | GET/POST/PUT/DELETE | `/admin/banners/` | 是(管理员) | Banner 管理 |
| 优惠券管理 | GET/POST/PUT/DELETE | `/admin/coupons/` | 是(管理员) | 优惠券管理 |

---

## 三、测试账号

### 3.1 管理员账号
- **用户名**: `admin`
- **密码**: `admin123`
- **角色**: 系统管理员

### 3.2 测试用户账号
- **用户名**: `testuser`
- **密码**: `user123`
- **角色**: 普通用户

---

## 四、快速测试

### 4.1 使用 curl 测试

```bash
# 健康检查
curl http://localhost:8000/health

# 用户登录
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 获取商品列表（无需认证）
curl http://localhost:8000/api/v1/products/simple

# 获取购物车（需要认证）
curl http://localhost:8000/api/v1/carts/items \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 4.2 使用 Swagger UI

访问 http://localhost:8000/docs 可以使用 Swagger UI 进行交互式测试。

---

## 五、错误处理

### 5.1 通用错误响应

```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

### 5.2 验证错误响应

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "username"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

---

*文档更新时间: 2026-04-01*
