# ShamGP 商城项目 - 路由映射表

**更新时间**: 2026-04-01

---

## 一、前端管理后台 (frontend-admin)

### 主要入口
- 首页: http://localhost:3000
- 登录页: http://localhost:3000/login
- Dashboard: http://localhost:3000/dashboard
- 订单管理: http://localhost:3000/orders

### 关键 API 路径（后端）
- POST `/api/v1/auth/login` - 登录
- GET `/api/v1/dashboard/stats` - Dashboard 统计
- GET `/api/v1/orders/admin/` - 订单列表（管理端）

---

## 二、前端商城 (frontend-shop)

### 主要入口
- 首页: http://localhost:3001
- 商品列表: http://localhost:3001/products
- 商品详情: http://localhost:3001/products/:id
- 购物车: http://localhost:3001/cart
- 结账: http://localhost:3001/checkout
- 订单列表: http://localhost:3001/orders
- 登录: http://localhost:3001/login
- 注册: http://localhost:3001/register

### 关键 API 路径（后端）
- POST `/api/v1/auth/login` - 登录
- POST `/api/v1/auth/register` - 注册
- GET `/api/v1/products/simple` - 商品列表（简单）
- GET `/api/v1/products` - 商品列表（商城，支持分页/搜索/分类）
- GET `/api/v1/products/:id` - 商品详情
- POST `/api/v1/carts/items` - 加购物车
- GET `/api/v1/carts/items` - 购物车列表
- GET `/api/v1/carts/summary` - 购物车摘要
- DELETE `/api/v1/carts/items/:id` - 删除购物车项
- GET `/api/v1/orders/addresses` - 收货地址列表
- POST `/api/v1/orders/addresses` - 创建收货地址
- POST `/api/v1/orders/` - 创建订单
- GET `/api/v1/orders/` - 订单列表

---

## 三、后端 API (backend)

### 公开接口（无需认证）
- GET `/health` - 健康检查
- GET `/api/v1/products/simple` - 简单商品列表
- GET `/api/v1/products/simple/:id` - 简单商品详情
- GET `/api/v1/products` - 商城商品列表
- GET `/api/v1/products/:id` - 商城商品详情
- POST `/api/v1/auth/login` - 登录
- POST `/api/v1/auth/register` - 注册

### 需要认证的接口
- GET `/api/v1/auth/userinfo` - 获取用户信息
- POST `/api/v1/auth/logout` - 登出
- POST `/api/v1/carts/items` - 加购物车
- GET `/api/v1/carts/items` - 购物车列表
- GET `/api/v1/carts/summary` - 购物车摘要
- PUT `/api/v1/carts/items/:id` - 更新购物车项
- DELETE `/api/v1/carts/items/:id` - 删除购物车项
- DELETE `/api/v1/carts/clear` - 清空购物车
- GET `/api/v1/orders/addresses` - 收货地址列表
- GET `/api/v1/orders/addresses/default` - 默认地址
- POST `/api/v1/orders/addresses` - 创建收货地址
- PUT `/api/v1/orders/addresses/:id` - 更新收货地址
- DELETE `/api/v1/orders/addresses/:id` - 删除收货地址
- POST `/api/v1/orders/` - 创建订单
- GET `/api/v1/orders/` - 订单列表
- GET `/api/v1/orders/:id` - 订单详情
- POST `/api/v1/orders/:id/cancel` - 取消订单

### 后台管理接口（需要认证）
- GET `/api/v1/dashboard/stats` - Dashboard 统计
- GET `/api/v1/dashboard/sales-trend` - 销售趋势
- GET `/api/v1/dashboard/user-growth` - 用户增长
- GET `/api/v1/dashboard/order-stats` - 订单统计
- GET `/api/v1/orders/admin/` - 订单列表（管理端）
- GET `/api/v1/inventory/*` - 库存管理
