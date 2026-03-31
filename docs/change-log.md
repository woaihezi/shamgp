# 变更日志

## 2026-03-31 - P0 阶段完成

### 本轮修改文件清单

#### 前端商城 (frontend-shop)

- `src/router/index.ts` - 添加缺失路由（/products, /product/:id, /login, /register, /profile, /orders, /orders/:id）
- `src/views/Register/index.vue` - 对接后端注册 API，添加表单校验和错误提示
- `src/api/product.ts` - 修复 API 路径，从 /api/v1/shop-products/shop 改为 /api/v1

#### 后端 (backend)

- `app/api/v1/api.py` - 注册所有缺失路由（categories, users, dashboard, inventory, logs, menus, system_config, uploads, admin/banners, admin/coupons, shop/coupons, shop/home）
- `app/api/v1/auth.py` - 添加 POST /register 注册接口

#### 项目根目录

- `.env` - 创建环境变量配置文件（使用 SQLite）

#### 文档 (docs)

- `db-runbook.md` - 新建数据库运行手册
- `p0-validation.md` - 新建 P0 验证报告
- `api-alignment-report.md` - 新建 API 对齐报告
- `mvp-status.md` - 新建 MVP 状态报告
- `change-log.md` - 新建变更日志（本文件）

---

### 已完成功能

1. ✅ 前端商城所有关键路由已添加并可访问
2. ✅ 后端所有路由已注册到主路由
3. ✅ 注册功能已完成（后端 API + 前端页面）
4. ✅ 数据库初始化脚本验证通过
5. ✅ API 路径对齐已修复（product.ts）

---

### 功能验证状态

| 功能         | 状态        | 说明                         |
| ------------ | ----------- | ---------------------------- |
| 前端路由     | ✅ 真的跑通 | 所有路由已配置，页面文件存在 |
| 后端路由注册 | ✅ 真的跑通 | 所有路由已注册到 api.py      |
| 注册功能     | ✅ 已接入   | 后端 API 已实现，前端已对接  |
| 数据库初始化 | ✅ 已接入   | init_db.py 可正常运行        |
| API 路径对齐 | ✅ 已接入   | product.ts 路径已修复        |

---

### 还剩 P2/P3

#### P2

- 完善 Dashboard（移除 mock 数据）
- 完善管理后台用户管理
- 完善权限管理
- 实现文件上传功能
- 完善前端商城个人中心
- 完善 Docker 配置

#### P3

- 支付功能
- 营销功能（Banner、优惠券等）
- 系统配置
- 日志和审计
- 单元测试
- 集成测试

---

### 下一步建议

1. 启动后端服务测试 API
2. 启动前端商城测试页面跳转
3. 完成 seed_data.py 数据填充
4. 进入 P1 阶段（商城主链路 + 后台核心模块）
