# 任务报告：订单中心任务

## 任务信息

- **任务编号**: 05
- **任务名称**: 订单中心任务
- **负责人**:
- **创建时间**: 2026-03-31
- **完成时间**: 2026-03-31

## 任务目标

搭建商城用户下单流程以及后台订单管理能力。

## 完成了什么

### 1. 后端基础结构

- 创建了后端项目结构和配置文件
- 配置了 FastAPI + SQLAlchemy 2.0 异步架构
- 创建了 requirements.txt 依赖文件
- 实现了核心配置模块（config.py, database.py）

### 2. 数据库模型

创建了完整的数据库模型：

- `base.py` - 基础模型（包含时间戳和软删除）
- `user.py` - 用户模型
- `category.py` - 商品分类模型
- `product.py` - 商品模型
- `cart.py` - 购物车模型
- `address.py` - 收货地址模型
- `order.py` - 订单、订单项、退款模型

**订单状态设计**:

- pending_payment - 待付款
- paid - 已付款（待发货）
- shipped - 已发货（待收货）
- completed - 已完成
- canceled - 已取消
- refunding - 退款中
- refunded - 已退款

### 3. Pydantic Schemas

创建了完整的请求/响应模型：

- `common.py` - 通用响应模型、分页参数
- `cart.py` - 购物车相关 Schema
- `address.py` - 地址相关 Schema
- `order.py` - 订单相关 Schema

### 4. 服务层（Service）

实现了业务逻辑层：

- `cart_service.py` - 购物车服务
- `address_service.py` - 地址服务
- `order_service.py` - 订单服务（含订单创建、状态流转、退款）

### 5. API 路由

创建了完整的 API 接口：

- `carts.py` - 购物车接口
- `orders.py` - 订单和地址接口（包含商城端和管理端）

### 6. 数据库 SQL 脚本

- `sql/init.sql` - 完整的数据库初始化脚本
- 包含测试数据（用户、分类、商品、地址）

### 7. 前端商城

实现了完整的商城前端功能：

- **购物车页面** (`frontend-shop/src/views/cart/CartList.vue`)
  - 商品添加/删除/数量修改
  - 商品选中/取消选中
  - 购物车清空
  - 演示商品一键添加
- **结算页面** (`frontend-shop/src/views/checkout/Checkout.vue`)
  - 收货地址选择
  - 商品清单展示
  - 订单备注
  - 金额明细
- **订单列表** (`frontend-shop/src/views/order/OrderList.vue`)
  - 订单状态筛选
  - 订单列表展示
  - 模拟支付
  - 取消订单
- **订单详情** (`frontend-shop/src/views/order/OrderDetail.vue`)
  - 订单详情展示
  - 订单操作（支付、取消、收货、退款）
  - 退款申请
- API 封装 (`cart.ts`, `order.ts`, `request.ts`)

### 8. 前端后台

实现了后台管理功能：

- **订单管理页面** (`frontend-admin/src/views/order/OrderList.vue`)
  - 订单列表展示（含分页）
  - 订单状态筛选
  - 订单详情查看
  - 发货操作
  - 完成订单操作
- API 封装 (`order.ts`, `request.ts`)
- 基础路由和布局

## 改了哪些文件

### 新建文件 - 后端

- `backend/requirements.txt`
- `backend/app/__init__.py`
- `backend/app/core/__init__.py`
- `backend/app/core/config.py`
- `backend/app/core/database.py`
- `backend/app/models/__init__.py`
- `backend/app/models/base.py`
- `backend/app/models/user.py`
- `backend/app/models/category.py`
- `backend/app/models/product.py`
- `backend/app/models/cart.py`
- `backend/app/models/address.py`
- `backend/app/models/order.py`
- `backend/app/schemas/__init__.py`
- `backend/app/schemas/common.py`
- `backend/app/schemas/cart.py`
- `backend/app/schemas/address.py`
- `backend/app/schemas/order.py`
- `backend/app/services/__init__.py`
- `backend/app/services/cart_service.py`
- `backend/app/services/address_service.py`
- `backend/app/services/order_service.py`
- `backend/app/api/__init__.py`
- `backend/app/api/v1/__init__.py`
- `backend/app/api/v1/carts.py`
- `backend/app/api/v1/orders.py`
- `backend/app/utils/__init__.py`

### 新建文件 - SQL

- `sql/init.sql`

### 新建文件 - 前端商城

- `frontend-shop/package.json`
- `frontend-shop/vite.config.ts`
- `frontend-shop/tsconfig.json`
- `frontend-shop/tsconfig.node.json`
- `frontend-shop/index.html`
- `frontend-shop/src/main.ts`
- `frontend-shop/src/App.vue`
- `frontend-shop/src/router/index.ts`
- `frontend-shop/src/api/request.ts`
- `frontend-shop/src/api/cart.ts`
- `frontend-shop/src/api/order.ts`
- `frontend-shop/src/views/Home.vue`
- `frontend-shop/src/views/cart/CartList.vue`
- `frontend-shop/src/views/checkout/Checkout.vue`
- `frontend-shop/src/views/order/OrderList.vue`
- `frontend-shop/src/views/order/OrderDetail.vue`

### 新建/修改文件 - 前端后台

- `frontend-admin/vite.config.ts` (新建)
- `frontend-admin/src/main.ts`
- `frontend-admin/src/App.vue`
- `frontend-admin/src/router/index.ts`
- `frontend-admin/src/views/Home.vue` (新建)
- `frontend-admin/src/api/request.ts` (新建)
- `frontend-admin/src/api/order.ts` (新建)
- `frontend-admin/src/views/order/OrderList.vue` (新建)

### 新建文件 - 文档

- `docs/task-reports/task-05-order-center.md` (本文件)

## 功能特性

### 购物车功能

- ✅ 添加商品到购物车
- ✅ 修改购物车商品数量
- ✅ 删除购物车商品
- ✅ 商品选中/取消选中
- ✅ 清空购物车
- ✅ 购物车金额汇总

### 订单功能

- ✅ 创建订单（从购物车选中商品）
- ✅ 订单列表查询（支持状态筛选）
- ✅ 订单详情查看
- ✅ 订单状态流转
  - 待付款 → 已付款（模拟支付）
  - 已付款 → 已发货（后台发货）
  - 已发货 → 已完成（确认收货）
  - 待付款 → 已取消（取消订单）
- ✅ 订单取消（待付款状态）
- ✅ 库存扣减/回滚

### 收货地址功能

- ✅ 地址列表查询
- ✅ 默认地址管理
- ✅ 地址创建/更新/删除

### 退款功能（基础版）

- ✅ 退款申请（支持仅退款/退货退款）
- ✅ 退款状态跟踪
- ✅ 订单状态自动更新为退款中

### 后台管理功能

- ✅ 订单列表查询（分页）
- ✅ 订单详情查看
- ✅ 订单发货操作
- ✅ 订单完成操作
- ✅ 订单状态筛选

### 支付相关

- ✅ 预留支付状态字段
- ✅ 预留支付时间、支付方式字段
- ✅ 不强制接入真实支付（提供模拟支付）

## 技术架构

### 后端技术栈

- **框架**: FastAPI
- **ORM**: SQLAlchemy 2.0 (异步)
- **数据验证**: Pydantic v2
- **数据库**: PostgreSQL (兼容 MySQL)

### 前端技术栈

- **前端商城**: Vue 3 + Vite + TypeScript + Vue Router + Pinia + Axios
- **前端后台**: Vue 3 + Vite + TypeScript + Element Plus + Vue Router + Pinia + Axios

### 数据库设计

- 所有表包含基础字段：id, created_at, updated_at, is_deleted
- 支持逻辑删除
- 完整的索引设计
- 订单状态使用字符串存储，便于扩展

## 怎么测试

### 1. 数据库初始化

```bash
# 使用 PostgreSQL 客户端执行 sql/init.sql
psql -U postgres -d shamgp -f sql/init.sql
```

### 2. 后端启动

```bash
cd backend
pip install -r requirements.txt
# 配置好 .env 文件后启动
uvicorn app.main:app --reload --port 8000
```

### 3. 前端商城启动

```bash
cd frontend-shop
npm install
npm run dev
# 访问 http://localhost:3001
```

### 4. 前端后台启动

```bash
cd frontend-admin
npm install
npm run dev
# 访问 http://localhost:3000
```

### 5. 测试流程

1. 访问前端商城首页
2. 点击购物车，添加演示商品
3. 调整商品数量和选中状态
4. 点击去结算，选择收货地址
5. 提交订单
6. 在订单列表中模拟支付
7. 访问后台管理系统
8. 在订单管理中发货
9. 回到商城确认收货
10. （可选）申请退款

## 留了哪些坑

1. **权限认证**: 当前所有 API 都硬编码 user_id=1，需要接入真实的 JWT 认证
2. **商品中心**: 商品模型比较简单，缺少 SKU 规格、库存预警等功能
3. **支付集成**: 未接入真实的支付渠道（支付宝、微信支付等）
4. **物流跟踪**: 缺少物流信息和物流单号管理
5. **订单评价**: 缺少订单评价功能
6. **优惠券/活动**: 缺少优惠券和促销活动支持
7. **消息通知**: 缺少订单状态变更的消息通知
8. **数据统计**: 缺少订单统计报表
9. **库存并发**: 高并发场景下需要优化库存扣减逻辑（使用分布式锁）
10. **单元测试**: 缺少 API 和 Service 层的单元测试

## 验收标准检查

- ✅ 1. 商城用户可加入购物车
- ✅ 2. 可提交订单
- ✅ 3. 可查看订单列表和详情
- ✅ 4. 后台可管理订单
- ✅ 5. 订单状态结构清晰

所有验收标准已满足！
