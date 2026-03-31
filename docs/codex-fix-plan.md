# 修复计划

## 一、P0/P1 问题清单

| 编号 | 优先级 | 模块 | 问题标题 | 描述 |
|------|--------|------|----------|------|
| 1 | P0 | 后端 | 订单接口认证错误 | GET /api/v1/orders 返回 401 未认证错误 |
| 2 | P0 | 后端 | 数据库依赖 | 后端服务依赖 MySQL 数据库，本地环境可能无法连接 |
| 3 | P1 | 后端 | deps.py 语法错误 | deps.py 第 74 行使用了错误的语法 |
| 4 | P1 | 前端商城 | 购物车使用本地 store | 购物车操作使用本地 store，未调用后端 API |
| 5 | P1 | 管理后台 | Dashboard 使用 mock 数据 | Dashboard 页面显示 mock 数据，API 调用失败 |
| 6 | P2 | 管理后台 | token 字段不一致 | 部分代码使用 `token`，部分使用 `access_token` |
| 7 | P2 | 前端商城 | 商品详情页加入购物车 | 商品详情页加入购物车使用本地 store，未调用后端 API |

## 二、修复顺序

### 1. 后端启动与认证问题
- 修复 deps.py 语法错误
- 修复订单接口认证错误
- 优化数据库配置，支持本地开发环境

### 2. 商城主链路
- 修复前端购物车与后端 API 对接
- 修复商品详情页加入购物车功能
- 验证下单流程

### 3. 后台主链路
- 统一管理后台 token 字段
- 实现 Dashboard 数据接口或优化前端 mock 数据

## 三、每项涉及文件

### 1. 订单接口认证错误
- **涉及文件**：
  - backend/app/api/v1/orders.py
  - backend/app/api/deps.py
- **修复思路**：检查 orders.py 中的依赖配置，确保使用正确的认证依赖

### 2. 数据库依赖
- **涉及文件**：
  - backend/app/core/config.py
- **修复思路**：修改配置，支持 SQLite 作为默认数据库，或提供更灵活的数据库配置选项

### 3. deps.py 语法错误
- **涉及文件**：
  - backend/app/api/deps.py
- **修复思路**：修复第 74 行的语法错误，使用正确的 SQLAlchemy 查询语法

### 4. 前端购物车使用本地 store
- **涉及文件**：
  - frontend-shop/src/stores/cart.ts
  - frontend-shop/src/api/cart.ts
- **修复思路**：修改购物车逻辑，调用后端 /api/v1/carts 相关接口

### 5. Dashboard 使用 mock 数据
- **涉及文件**：
  - frontend-admin/src/views/dashboard/index.vue
  - backend/app/api/v1/dashboard.py
- **修复思路**：实现后端 /admin/stats 接口，或修改前端使用现有 API

### 6. token 字段不一致
- **涉及文件**：
  - frontend-admin/src/utils/auth.ts
  - frontend-admin/src/api/request.ts
- **修复思路**：统一使用 `access_token` 字段

### 7. 商品详情页加入购物车
- **涉及文件**：
  - frontend-shop/src/views/ProductDetail/index.vue
- **修复思路**：修改加入购物车逻辑，调用后端 /api/v1/carts/items 接口

## 四、修复目标

1. **P0 问题**：全部修复，确保核心流程可以正常运行
2. **P1 问题**：优先修复影响用户体验的问题
3. **P2 问题**：视时间情况进行修复

## 五、验证计划

每修复一项，立即进行验证：
- 后端接口验证：使用 curl 或浏览器测试 API 响应
- 前端功能验证：访问页面并测试功能
- 全链路验证：测试完整的业务流程

---

*修复计划结束*