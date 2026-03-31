# 系统架构规划

## 1. 项目概述

### 1.1 项目目标
构建一个可扩展的电商业务平台，同时支持：
- 电商前台（用户端）
- 电商后台（管理端）
- 通用管理模块（用户、角色、菜单、日志、配置、文件、报表等）

平台需要具备高度可扩展性，便于后续增加 AI 助手、Excel 导入导出、可视化大屏、工作流、CRM/OA/工单等业务子系统。

### 1.2 技术栈

#### 前端技术栈
- **前端后台**: Vue 3 + Vite + TypeScript + Element Plus + ECharts + Pinia + Vue Router + Axios
- **前端商城**: Vue 3 + Vite + TypeScript

#### 后端技术栈
- **框架**: FastAPI
- **ORM**: SQLAlchemy 2.0 (异步)
- **数据验证**: Pydantic v2
- **认证**: JWT (PyJWT / python-jose)
- **数据库**: PostgreSQL (主) / MySQL (兼容)

#### 部署
- Docker / Docker Compose

## 2. 系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                          客户端层                                 │
├─────────────────────────────────┬───────────────────────────────┤
│     前端商城 (Vue3 + TS)        │   前端后台 (Vue3 + TS + EP)   │
│    (C端用户访问)                 │   (B端管理员访问)              │
└─────────────────────────────────┴───────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                         API 网关层 (Nginx)                       │
│              (路由分发、静态资源服务、负载均衡)                   │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                        后端服务层 (FastAPI)                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ 用户模块 │  │ 商品模块 │  │ 订单模块 │  │ 支付模块 │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ 权限模块 │  │ 日志模块 │  │ 文件模块 │  │ 配置模块 │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                         数据存储层                                 │
├─────────────────────────────────┬───────────────────────────────┤
│   PostgreSQL / MySQL (主数据库) │   Redis (缓存/会话)            │
└─────────────────────────────────┴───────────────────────────────┘
```

### 2.2 核心设计原则

#### 2.2.1 分层架构
系统采用经典的分层架构设计：

```
┌─────────────────────────────────┐
│      Presentation Layer         │  (API 路由层 - routers)
├─────────────────────────────────┤
│      Business Logic Layer       │  (业务逻辑层 - services)
├─────────────────────────────────┤
│      Data Access Layer          │  (数据访问层 - models/repositories)
├─────────────────────────────────┤
│      Database Layer             │  (数据库层 - PostgreSQL/MySQL)
└─────────────────────────────────┘
```

#### 2.2.2 模块化设计
- 核心模块独立，低耦合高内聚
- 清晰的模块边界，便于并行开发
- 通用模块可复用于其他业务系统

#### 2.2.3 前后端分离
- RESTful API 设计
- 统一的数据响应格式
- JWT 无状态认证

## 3. 项目目录结构

### 3.1 根目录结构

```
shamgp/
├── docs/                           # 项目文档
│   ├── architecture-overview.md    # 本文档
│   ├── module-plan.md             # 模块规划
│   ├── database-design.md         # 数据库设计
│   ├── api-convention.md          # API 规范
│   ├── frontend-spec.md           # 前端规范
│   ├── backend-spec.md            # 后端规范
│   ├── task-splitting-plan.md     # 任务拆分
│   └── integration-plan.md        # 集成方案
├── backend/                        # 后端服务
│   ├── app/                        # 应用代码
│   │   ├── api/                    # API 路由
│   │   │   ├── v1/                 # API v1 版本
│   │   │   │   ├── admin/          # 后台管理 API
│   │   │   │   └── shop/           # 商城 API
│   │   ├── core/                   # 核心配置
│   │   ├── models/                 # 数据库模型
│   │   ├── schemas/                # Pydantic 模型
│   │   ├── services/               # 业务逻辑
│   │   ├── utils/                  # 工具函数
│   │   └── tests/                  # 测试
│   ├── alembic/                    # 数据库迁移
│   ├── Dockerfile
│   └── requirements.txt
├── frontend-admin/                 # 前端后台
│   ├── src/
│   │   ├── api/                    # API 请求
│   │   ├── assets/                 # 静态资源
│   │   ├── components/             # 公共组件
│   │   ├── layouts/                # 布局组件
│   │   ├── router/                 # 路由
│   │   ├── stores/                 # Pinia 状态管理
│   │   ├── utils/                  # 工具函数
│   │   ├── views/                  # 页面视图
│   │   └── types/                  # TypeScript 类型
│   ├── Dockerfile
│   └── package.json
├── frontend-shop/                  # 前端商城
│   ├── src/
│   │   ├── api/                    # API 请求
│   │   ├── assets/                 # 静态资源
│   │   ├── components/             # 公共组件
│   │   ├── layouts/                # 布局组件
│   │   ├── router/                 # 路由
│   │   ├── stores/                 # Pinia 状态管理
│   │   ├── utils/                  # 工具函数
│   │   ├── views/                  # 页面视图
│   │   └── types/                  # TypeScript 类型
│   ├── Dockerfile
│   └── package.json
├── docker/                         # Docker 相关
│   ├── nginx/                      # Nginx 配置
│   └── postgres/                   # PostgreSQL 配置
├── docker-compose.yml
└── README.md
```

### 3.2 后端目录详解

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI 应用入口
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                # 依赖注入
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py             # API 路由聚合
│   │       ├── admin/             # 后台管理 API
│   │       │   ├── __init__.py
│   │       │   ├── users.py       # 用户管理
│   │       │   ├── roles.py       # 角色管理
│   │       │   ├── menus.py       # 菜单管理
│   │       │   ├── permissions.py # 权限管理
│   │       │   ├── products.py    # 商品管理
│   │       │   ├── orders.py      # 订单管理
│   │       │   ├── categories.py  # 分类管理
│   │       │   ├── logs.py        # 日志管理
│   │       │   ├── files.py       # 文件管理
│   │       │   └── configs.py     # 配置管理
│   │       └── shop/              # 商城 API
│   │           ├── __init__.py
│   │           ├── auth.py        # 认证
│   │           ├── products.py    # 商品
│   │           ├── cart.py        # 购物车
│   │           ├── orders.py      # 订单
│   │           ├── users.py       # 用户中心
│   │           └── payments.py    # 支付
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # 配置管理
│   │   ├── security.py            # 安全相关 (JWT, 密码)
│   │   ├── database.py            # 数据库连接
│   │   ├── redis.py               # Redis 连接
│   │   ├── dependencies.py        # 全局依赖
│   │   └── exceptions.py          # 自定义异常
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                # 基础模型
│   │   ├── user.py                # 用户模型
│   │   ├── role.py                # 角色模型
│   │   ├── menu.py                # 菜单模型
│   │   ├── permission.py          # 权限模型
│   │   ├── product.py             # 商品模型
│   │   ├── category.py            # 分类模型
│   │   ├── order.py               # 订单模型
│   │   ├── cart.py                # 购物车模型
│   │   ├── file.py                # 文件模型
│   │   ├── log.py                 # 日志模型
│   │   └── config.py              # 配置模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── common.py              # 通用 Schema
│   │   ├── user.py                # 用户 Schema
│   │   ├── role.py                # 角色 Schema
│   │   ├── product.py             # 商品 Schema
│   │   ├── order.py               # 订单 Schema
│   │   └── ...
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base.py                # 基础 Service
│   │   ├── user_service.py        # 用户 Service
│   │   ├── product_service.py     # 商品 Service
│   │   ├── order_service.py       # 订单 Service
│   │   └── ...
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── datetime_util.py       # 日期工具
│   │   ├── string_util.py         # 字符串工具
│   │   ├── file_util.py           # 文件工具
│   │   └── logger.py              # 日志工具
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_api/
│       └── test_services/
├── alembic/
│   ├── versions/
│   └── env.py
├── .env.example
├── Dockerfile
└── requirements.txt
```

### 3.3 前端后台目录详解

```
frontend-admin/
├── public/
│   └── favicon.ico
├── src/
│   ├── main.ts                    # 入口文件
│   ├── App.vue                    # 根组件
│   ├── api/
│   │   ├── index.ts               # Axios 实例配置
│   │   ├── request.ts             # 请求封装
│   │   ├── user.ts                # 用户 API
│   │   ├── product.ts             # 商品 API
│   │   ├── order.ts               # 订单 API
│   │   └── ...
│   ├── assets/
│   │   ├── images/
│   │   ├── styles/
│   │   │   └── index.scss
│   ├── components/
│   │   ├── common/                # 通用组件
│   │   │   ├── SvgIcon/
│   │   │   ├── Upload/
│   │   │   └── ...
│   │   └── business/              # 业务组件
│   ├── layouts/
│   │   ├── index.vue              # 主布局
│   │   ├── components/
│   │   │   ├── Sidebar.vue        # 侧边栏
│   │   │   ├── Header.vue         # 顶部栏
│   │   │   └── TagsView.vue       # 标签栏
│   ├── router/
│   │   ├── index.ts               # 路由配置
│   │   └── modules/               # 路由模块
│   ├── stores/
│   │   ├── index.ts
│   │   ├── modules/
│   │   │   ├── user.ts            # 用户状态
│   │   │   ├── app.ts             # 应用状态
│   │   │   ├── permission.ts      # 权限状态
│   │   │   └── tagsView.ts        # 标签页状态
│   ├── utils/
│   │   ├── request.ts             # 请求工具
│   │   ├── auth.ts                # 认证工具
│   │   ├── storage.ts             # 存储工具
│   │   └── validate.ts            # 验证工具
│   ├── views/
│   │   ├── login/                 # 登录页
│   │   ├── dashboard/             # 仪表盘
│   │   ├── system/                # 系统管理
│   │   │   ├── user/
│   │   │   ├── role/
│   │   │   ├── menu/
│   │   │   ├── log/
│   │   │   └── config/
│   │   ├── product/               # 商品管理
│   │   ├── order/                 # 订单管理
│   │   └── ...
│   ├── types/
│   │   ├── api.ts                 # API 类型
│   │   ├── user.ts                # 用户类型
│   │   └── ...
│   └── env.d.ts
├── .env.development
├── .env.production
├── Dockerfile
├── vite.config.ts
├── tsconfig.json
└── package.json
```

### 3.4 前端商城目录详解

```
frontend-shop/
├── public/
│   └── favicon.ico
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── api/
│   │   ├── index.ts
│   │   ├── auth.ts
│   │   ├── product.ts
│   │   ├── cart.ts
│   │   ├── order.ts
│   │   └── user.ts
│   ├── assets/
│   │   ├── images/
│   │   └── styles/
│   ├── components/
│   │   ├── common/
│   │   └── business/
│   ├── layouts/
│   │   ├── DefaultLayout.vue
│   │   └── components/
│   ├── router/
│   │   └── index.ts
│   ├── stores/
│   │   ├── modules/
│   │   │   ├── user.ts
│   │   │   ├── cart.ts
│   │   │   └── app.ts
│   ├── utils/
│   ├── views/
│   │   ├── Home/
│   │   ├── Product/
│   │   ├── Cart/
│   │   ├── Order/
│   │   ├── User/
│   │   └── Login/
│   └── types/
├── Dockerfile
├── vite.config.ts
└── package.json
```

## 4. 部署架构

### 4.1 Docker Compose 部署

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: shamgp
      POSTGRES_USER: shamgp
      POSTGRES_PASSWORD: shamgp123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://shamgp:shamgp123@postgres:5432/shamgp
      - REDIS_URL=redis://redis:6379

  frontend-admin:
    build: ./frontend-admin
    depends_on:
      - backend
    ports:
      - "3000:80"

  frontend-shop:
    build: ./frontend-shop
    depends_on:
      - backend
    ports:
      - "3001:80"

  nginx:
    image: nginx:alpine
    depends_on:
      - backend
      - frontend-admin
      - frontend-shop
    ports:
      - "80:80"
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf

volumes:
  postgres_data:
  redis_data:
```

## 5. 扩展能力设计

### 5.1 预留扩展点

| 扩展功能 | 预留位置 | 说明 |
|---------|---------|------|
| AI 助手 | backend/app/api/v1/ai/, frontend-admin/src/views/ai/ | 可插拔的 AI 模块 |
| Excel 导入导出 | backend/app/utils/excel.py, frontend-admin/src/components/Excel/ | 独立工具模块 |
| 可视化大屏 | frontend-admin/src/views/dashboard/big-screen/ | 大屏展示模块 |
| 工作流 | backend/app/services/workflow/, frontend-admin/src/views/workflow/ | 工作流引擎模块 |
| CRM | backend/app/api/v1/crm/, frontend-admin/src/views/crm/ | CRM 业务模块 |
| OA | backend/app/api/v1/oa/, frontend-admin/src/views/oa/ | OA 业务模块 |
| 工单 | backend/app/api/v1/ticket/, frontend-admin/src/views/ticket/ | 工单系统模块 |

### 5.2 插件化架构
核心业务模块采用插件化设计，便于后续扩展：
- 每个业务模块独立路由、独立 Service
- 通过配置动态加载/卸载模块
- 统一