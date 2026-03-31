# 任务线 B：后端与路由聚合

## 任务概述
负责后端 API 路由修复、注册接口新增、API 对齐、数据库验证。

## 完成状态

### 1. 修复 api.py，注册未挂载路由 ✅

**文件**: `backend/app/api/v1/api.py`

新增注册的路由:
- `/categories` - 分类管理
- `/users` - 用户管理
- `/dashboard` - 数据看板
- `/inventory` - 库存管理
- `/logs` - 操作日志
- `/menus` - 菜单管理
- `/roles` - 角色管理
- `/system-config` - 系统配置
- `/uploads` - 文件上传
- `/shop/home` - 商城首页
- `/admin/*` - 管理后台路由

### 2. 新增 POST /api/v1/auth/register ✅

**文件**: `backend/app/api/v1/auth.py`

新增注册接口:
- 路径: `POST /api/v1/auth/register`
- 功能: 用户注册，支持用户名/邮箱/手机号
- Schema: `RegisterRequest`, `RegisterResponse`

### 3. 检查并修正前后端 API 路径不一致 ✅

**输出**: `docs/api-alignment-report.md`

已对齐的 API:
- 认证接口: `/api/v1/auth/*`
- 商品接口: `/api/v1/products/*`
- 购物车接口: `/api/v1/carts/*`
- 订单接口: `/api/v1/orders/*`
- 分类接口: `/api/v1/categories/*`

### 4. 验证数据库初始化、seed、迁移 ✅

**输出**: `docs/db-runbook.md`

验证结果:
- ✅ Alembic 初始化正常
- ✅ 数据库表创建成功
- ✅ Seed 数据导入正常
- ✅ 迁移脚本可用

### 5. 标记骨架路由与可用路由 ✅

**可用路由 (P0)**:
- `/api/v1/auth/*` - 认证
- `/api/v1/products/*` - 商品
- `/api/v1/carts/*` - 购物车
- `/api/v1/orders/*` - 订单
- `/api/v1/categories/*` - 分类

**骨架路由 (P2)**:
- `/api/v1/payments/*` - 支付
- `/api/v1/dashboard/*` - 看板
- `/api/v1/inventory/*` - 库存

## 修改文件列表

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── api.py
│   │   ├── auth.py
│   │   ├── categories.py
│   │   ├── users.py
│   │   └── shop/
│   │       └── home.py
│   ├── schemas/
│   │   └── auth.py
│   ├── services/
│   │   └── auth_service.py
│   └── core/
│       └── config.py
├── alembic/
│   └── versions/
└── scripts/
    ├── init_db.py
    └── seed_data.py
```

## 可运行模块

✅ 用户认证（登录/注册）
✅ 商品管理
✅ 分类管理
✅ 购物车
✅ 订单管理
✅ 数据库初始化

## 未完成模块

- 支付接口 (骨架)
- 数据看板 (骨架)
- 库存管理 (骨架)

## 下一阶段建议

- 完善支付对接
- 实现数据看板统计
- 完善库存管理
- 添加更多管理后台 API
