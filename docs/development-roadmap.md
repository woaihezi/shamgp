# 开发路线图

本文档按优先级分阶段规划项目开发任务。

---

## 阶段总览

| 阶段 | 目标 | 预计工作量 |
|------|------|------------|
| P0 | 修复可运行性，确保项目能跑通 | 2-3 天 |
| P1 | 完成商城主流程 MVP | 5-7 天 |
| P2 | 补后台管理和数据统计 | 4-5 天 |
| P3 | 做权限、日志、上传、支付、部署优化 | 7-10 天 |

---

## P0 - 先修复可运行性

**目标**: 确保项目基本可运行，核心链路能走通

### 任务清单

| 序号 | 任务 | 详细说明 | 代码位置 | 预计时间 |
|------|------|----------|----------|----------|
| 1 | 注册所有后端 API 路由 | 在 api.py 中注册所有未注册的路由（categories, users, dashboard, inventory, logs, menus, system_config, uploads, admin, shop） | `backend/app/api/v1/api.py` | 0.5 天 |
| 2 | 统一前后端 API 路径 | 修复前端商城的 API 路径，确保与后端匹配 | `frontend-shop/src/api/product.ts` | 0.5 天 |
| 3 | 实现用户注册 API | 添加用户注册接口 | `backend/app/api/v1/auth.py` | 0.5 天 |
| 4 | 测试数据库初始化 | 测试并完善 init_db.py 和 seed_data.py，确保能正常初始化数据库 | `backend/scripts/` | 0.5 天 |
| 5 | 补充前端商城基础路由 | 添加商品列表、商品详情、登录、注册的路由占位 | `frontend-shop/src/router/index.ts` | 0.5 天 |
| 6 | 验证后端 API 可访问 | 启动后端，通过 Swagger UI 测试核心 API | `backend/` | 0.5 天 |

**P0 阶段合计**: 约 3 天

---

## P1 - 完成商城主流程 MVP

**目标**: 用户可以浏览商品、加购物车、下单、查看订单

### 任务清单

| 序号 | 任务 | 详细说明 | 代码位置 | 预计时间 |
|------|------|----------|----------|----------|
| 7 | 创建前端商城登录页 | 实现登录页面，对接后端登录 API | `frontend-shop/src/views/Login/` | 0.5 天 |
| 8 | 创建前端商城注册页 | 实现注册页面，对接后端注册 API | `frontend-shop/src/views/Register/` | 0.5 天 |
| 9 | 创建前端商城商品列表页 | 实现商品列表，支持筛选、搜索、分页 | `frontend-shop/src/views/ProductList/` | 1 天 |
| 10 | 创建前端商城商品详情页 | 实现商品详情展示，加入购物车功能 | `frontend-shop/src/views/ProductDetail/` | 1 天 |
| 11 | 完善购物车功能 | 完善购物车页面，实现添加、修改、删除 | `frontend-shop/src/views/cart/` | 0.5 天 |
| 12 | 完善结账和下单流程 | 完善结账页面，确保下单流程正常 | `frontend-shop/src/views/checkout/` | 0.5 天 |
| 13 | 完善订单列表和详情 | 确保订单列表和详情页正常工作 | `frontend-shop/src/views/order/` | 0.5 天 |
| 14 | 管理后台商品管理 | 实现商品的增删改查 | `frontend-admin/src/views/product/` | 1 天 |
| 15 | 管理后台分类管理 | 实现分类的增删改查，支持多级分类 | `frontend-admin/src/views/product/CategoryList.vue` | 0.5 天 |
| 16 | 管理后台订单管理 | 实现订单列表、详情、状态更新 | `frontend-admin/src/views/orders/` | 0.5 天 |

**P1 阶段合计**: 约 6.5 天

---

## P2 - 补后台管理和数据统计

**目标**: 完善后台管理功能，添加数据统计

### 任务清单

| 序号 | 任务 | 详细说明 | 代码位置 | 预计时间 |
|------|------|----------|----------|----------|
| 17 | 实现数据统计 API | 实现仪表盘统计接口（今日订单、销售额、用户数等） | `backend/app/api/v1/dashboard.py` | 1 天 |
| 18 | 完善管理后台 Dashboard | 对接真实 API，移除 mock 数据 | `frontend-admin/src/views/dashboard/` | 0.5 天 |
| 19 | 管理后台用户管理 | 实现用户列表、添加、编辑、禁用 | `frontend-admin/src/views/users/` | 1 天 |
| 20 | 管理后台权限管理 | 实现角色管理、权限分配 | `frontend-admin/src/views/permissions/` | 1 天 |
| 21 | 实现文件上传功能 | 实现图片上传 API 和前端对接 | `backend/app/api/v1/uploads.py`, `frontend-admin/src/api/file.ts` | 1 天 |
| 22 | 前端商城个人中心 | 实现个人中心，包含订单管理、地址管理 | `frontend-shop/src/views/Profile/` | 0.5 天 |

**P2 阶段合计**: 约 5 天

---

## P3 - 做权限、日志、上传、支付、部署优化

**目标**: 完善高级功能，优化部署

### 任务清单

| 序号 | 任务 | 详细说明 | 代码位置 | 预计时间 |
|------|------|----------|----------|----------|
| 23 | 完善 RBAC 权限控制 | 实现基于角色的权限控制，保护 API | `backend/app/api/deps.py`, `backend/app/core/` | 1.5 天 |
| 24 | 实现操作日志 | 记录用户操作、登录日志、数据变更 | `backend/app/api/v1/logs.py`, `backend/app/services/log_service.py` | 1 天 |
| 25 | 实现支付功能 | 对接支付宝/微信支付，实现支付回调 | `backend/app/api/v1/payments.py` | 2 天 |
| 26 | 营销功能完善 | 实现 Banner 管理、优惠券完善、推荐商品 | `backend/app/api/v1/admin/`, `frontend-admin/src/views/marketing/` | 1.5 天 |
| 27 | Docker 配置完善 | 添加 backend、frontend-admin、frontend-shop 服务，创建 Dockerfile | `docker-compose.yml`, `docker/` | 1.5 天 |
| 28 | 编写测试 | 添加单元测试和集成测试 | `backend/tests/`, `frontend-admin/tests/` | 2.5 天 |
| 29 | 项目文档完善 | 编写 API 文档、部署文档、开发指南 | `docs/` | 1 天 |

**P3 阶段合计**: 约 11 天

---

## 里程碑

### Milestone 1: 项目可运行 (P0 完成)
- 后端 API 完整注册并可访问
- 数据库可正常初始化
- 前后端 API 路径统一
- 预计时间: 3 天

### Milestone 2: 商城 MVP (P1 完成)
- 用户可以注册/登录
- 用户可以浏览商品列表和详情
- 用户可以加购物车、下单
- 用户可以查看订单
- 管理员可以管理商品、分类、订单
- 预计时间: 累计 9.5 天

### Milestone 3: 后台完善 (P2 完成)
- 数据统计看板可用
- 管理员可以管理用户和权限
- 文件上传功能可用
- 用户有个人中心
- 预计时间: 累计 14.5 天

### Milestone 4: 功能完备 (P3 完成)
- 权限控制完善
- 日志系统完善
- 支付功能可用
- 营销功能完善
- Docker 部署可用
- 测试覆盖
- 文档完善
- 预计时间: 累计 25.5 天

---

## 依赖关系

```
P0 (必须先完成)
  ↓
P1 (依赖 P0)
  ↓
P2 (依赖 P1)
  ↓
P3 (依赖 P2)
```

## 下一步行动

请参考 [dev-gap-list.md](./dev-gap-list.md) 查看详细的缺口清单，以及 [下一步最值得先做的 10 个任务](#下一步最值得先做的-10-个任务)。
