# 系统结构说明

本文档描述 ShamGP 商城系统的整体架构，基于真实代码生成。

---

## 一、技术架构

```
┌─────────────────────────────────────────┐
│           前端 Vue 3 (localhost:5173)    │
│   frontend-shop (商城) / frontend-admin  │
└──────────────────┬──────────────────────┘
                   │ HTTP / SSE / WebSocket
                   │ JWT Auth
┌──────────────────▼──────────────────────┐
│          后端 FastAPI (localhost:8000)   │
│   backend/app/api/v1/                   │
│   - 商城 API (shop)                     │
│   - 管理后台 API (admin)                 │
│   - 通用 API (common)                   │
└──────────────────┬──────────────────────┘
                   │ SQLAlchemy 2.0 Async
┌──────────────────▼──────────────────────┐
│         SQLite (开发) / MySQL / PG      │
│              shop_db.db                 │
└─────────────────────────────────────────┘
```

---

## 二、后端目录结构

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py              # 路由汇总注册
│   │       ├── shop/               # 商城前端 API
│   │       │   ├── home.py         # 首页数据
│   │       │   ├── cart.py         # 购物车
│   │       │   ├── orders.py       # 订单
│   │       │   ├── products.py     # 商品
│   │       │   └── ...
│   │       ├── admin/              # 管理后台 API
│   │       └── common/             # 通用 API
│   ├── models/                     # SQLAlchemy 模型
│   │   ├── user.py                 # 用户/角色/权限
│   │   ├── product.py              # 商品/SPU/SKU
│   │   ├── order.py                # 订单/订单项
│   │   ├── coupon.py               # 优惠券/用户优惠券
│   │   ├── favorite.py             # 收藏
│   │   ├── browse_history.py       # 浏览历史
│   │   ├── order_status_log.py     # 订单状态日志
│   │   └── ...
│   ├── services/                   # 业务逻辑层
│   │   ├── product_service.py
│   │   ├── cart_service.py
│   │   ├── order_service.py
│   │   ├── favorite_service.py
│   │   └── ...
│   ├── deps/                       # 依赖注入（鉴权/DB）
│   │   └── auth.py
│   └── core/
│       ├── config.py               # 配置管理
│       └── database.py             # 数据库连接
├── scripts/
│   ├── init_db.py                  # 建表脚本
│   └── seed_real_data.py           # 种子数据
└── shop_db.db                      # SQLite 数据库
```

---

## 三、前端目录结构

```
frontend-shop/
├── src/
│   ├── api/                        # API 调用层
│   │   ├── request.ts              # Axios 实例 + 拦截器
│   │   ├── product.ts              # 商品 API
│   │   ├── cart.ts                 # 购物车 API
│   │   ├── order.ts                # 订单 API
│   │   ├── coupon.ts               # 优惠券 API
│   │   └── home.ts                 # 首页 API
│   ├── views/                      # 页面组件
│   │   ├── Home/                   # 首页
│   │   ├── Product/
│   │   │   ├── ProductList.vue     # 商品列表
│   │   │   └── ProductDetail.vue   # 商品详情
│   │   ├── Cart/                   # 购物车
│   │   ├── checkout/               # 结算页
│   │   └── User/                   # 用户中心
│   ├── stores/                     # Pinia 状态管理
│   │   ├── cart.ts
│   │   └── auth.ts
│   └── router/
│       └── index.ts                # 路由守卫
```

---

## 四、核心模块说明

| 模块 | 技术栈 | 状态 |
|------|--------|------|
| 用户认证 | FastAPI + JWT + bcrypt | ✅ 完整 |
| 商品管理 | Product/SPU/SKU 三层模型 | ✅ 完整 |
| 购物车 | 前端 Pinia + 后端 CartService | ✅ 完整 |
| 订单 | OrderService + 状态机 | ✅ 完整 |
| 优惠券 | Coupon + UserCoupon 表 | ✅ 完整 |
| 收藏 | FavoriteService | ✅ 完整 |
| 浏览历史 | BrowseHistoryService | ✅ 完整 |
| 楼层推荐 | Floor/FloorProduct | ✅ 完整 |
| RAG / AI | 未接入 | ❌ 未实现 |
| 支付 | 未接入 | ❌ 未实现 |
| Docker 部署 | docker-compose 骨架 | ⚠️ 骨架 |

---

## 五、数据库

- **开发**: SQLite (`shop_db.db`)
- **生产**: MySQL / PostgreSQL（修改 `DATABASE_URL` 环境变量）
- **ORM**: SQLAlchemy 2.0（异步）
- **迁移**: 直接 SQL / 脚本，未使用 Alembic

---

*本文档基于 `backend/app/` 和 `frontend-shop/src/` 真实代码生成