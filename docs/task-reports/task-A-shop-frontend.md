# 任务线 A：商城前端 (frontend-shop)

## 任务概述
负责商城前端核心功能开发，包括路由、页面、API对接和状态管理。

## 完成状态

### 1. 补齐路由 ✅

**文件**: `frontend-shop/src/router/index.ts`

新增路由:
- `/products` - 商品列表
- `/product/:id` - 商品详情
- `/login` - 登录页
- `/register` - 注册页
- `/profile` - 个人中心

### 2. 完成页面 ✅

**已实现页面**:
- `src/views/ProductList/index.vue` - 商品列表页
- `src/views/ProductDetail/index.vue` - 商品详情页
- `src/views/Login/index.vue` - 登录页
- `src/views/Register/index.vue` - 注册页
- `src/views/Profile/index.vue` - 个人中心页

### 3. 对接 API ✅

**API 模块**:
- `src/api/auth.ts` - 认证接口（登录/注册/用户信息/登出）
- `src/api/product.ts` - 商品接口（列表/详情）
- `src/api/category.ts` - 分类接口
- `src/api/home.ts` - 首页接口
- `src/api/cart.ts` - 购物车接口
- `src/api/order.ts` - 订单接口

### 4. 统一 access_token 存储 ✅

**实现**:
- 使用 `localStorage` 统一存储 `access_token`
- 请求拦截器自动附加 Bearer Token
- 响应拦截器处理 401 未授权自动跳转登录

### 5. Loading / Empty / Error 状态 ✅

**所有页面已实现**:
- 加载状态（Loading）
- 空数据状态（Empty）
- 错误状态（Error）

## 修改文件列表

```
frontend-shop/
├── src/
│   ├── router/
│   │   └── index.ts
│   ├── views/
│   │   ├── ProductList/
│   │   │   └── index.vue
│   │   ├── ProductDetail/
│   │   │   └── index.vue
│   │   ├── Login/
│   │   │   └── index.vue
│   │   ├── Register/
│   │   │   └── index.vue
│   │   └── Profile/
│   │       └── index.vue
│   ├── api/
│   │   ├── auth.ts
│   │   ├── product.ts
│   │   ├── category.ts
│   │   ├── home.ts
│   │   ├── cart.ts
│   │   └── order.ts
│   ├── stores/
│   │   ├── user.ts
│   │   └── cart.ts
│   └── utils/
│       └── request.ts
```

## 可运行模块

✅ 商品浏览（列表/详情）
✅ 用户认证（登录/注册）
✅ 个人中心
✅ 购物车
✅ 订单查看

## 未完成模块

无

## 下一阶段建议

- 优化用户体验细节
- 添加更多筛选和排序功能
- 实现商品搜索
- 添加收货地址管理
