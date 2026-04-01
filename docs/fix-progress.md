# ShamGP 商城项目 - P0 修复进度

**开始时间**: 2026-04-01
**当前状态**: 已完成主要 P0 修复

---

## 修复进度

| 阶段 | 任务 | 状态 | 时间 |
|------|------|------|------|
| 1 | 创建 audit-fix-report.md | ✅ 完成 | 2026-04-01 |
| 2 | 修复 P0-A: 前端商城 API 路径重复拼接 | ✅ 完成 | 2026-04-01 |
| 3 | 修复 P0-B: 后端 router 重复 prefix | ✅ 完成 | 2026-04-01 |
| 4 | 修复 P0-C: 后台 token 键名不一致 | ✅ 完成 | 2026-04-01 |
| 5 | 修复 P0-D: 后台 dashboard mock 问题 | ✅ 完成 | 2026-04-01 |
| 6 | 修复 P0-E: 后端 admin 接口鉴权 | ✅ 完成 | 2026-04-01 |
| 7 | 修复 P0-F: 订单/库存链路 | ✅ 完成 | 2026-04-01 |
| 8 | 修复 P0-G: 优惠券协议对齐 | ⏳ 部分完成 | - |
| 9 | 修复 P0-H: 路由导入异常处理 | ✅ 完成 | 2026-04-01 |
| 10 | 修复 P1 问题 | ⏳ 待开始 | - |

---

## 已修复问题清单

### P0-A: 前端商城 API 路径重复拼接
**修复文件**:
- `frontend-shop/src/api/auth.ts`
- `frontend-shop/src/api/cart.ts`
- `frontend-shop/src/api/product.ts`
- `frontend-shop/src/api/order.ts`
- `frontend-shop/src/api/home.ts`

**修复内容**:
- 移除 `/api/v1` 重复前缀
- 统一使用相对路径

---

### P0-B: 后端 router 重复 prefix
**修复文件**:
- `backend/app/api/v1/shop/home.py`
- `backend/app/api/v1/dashboard.py`

**修复内容**:
- 移除 router 内部的 prefix 定义
- 统一由 api.py 管理 prefix

---

### P0-C & P0-D: 后台 token 键名不一致 & dashboard mock 问题
**修复文件**:
- `frontend-admin/src/views/dashboard/index.vue`

**修复内容**:
- 统一使用 `access_token`
- 移除 mock 数据回退逻辑
- 修正请求路径为 `/dashboard/stats`
- 接口失败时显示明确错误

---

### P0-E: 后端 admin 接口鉴权
**修复文件**:
- `backend/app/api/v1/dashboard.py`

**修复内容**:
- 为 dashboard 所有接口添加 `get_current_active_user` 鉴权依赖
- 确保后台接口不裸奔

---

### P0-F: 订单/库存链路真实错误
**修复文件**:
- `backend/app/services/order_service.py`

**修复内容**:
- 修复缺失的 `ProductSku` 导入
- 移除未使用的 `update` 导入

---

### P0-H: 路由导入失败被静默跳过
**修复文件**:
- `backend/app/api/v1/api.py`

**修复内容**:
- 添加严格模式开关 `API_STRICT_MODE`
- 路由加载成功时打印日志
- 失败时打印完整堆栈跟踪
- 严格模式下抛出异常而非静默跳过

---

## 修复日志

### 2026-04-01
- ✅ 创建 audit-fix-report.md
- ✅ 修复 P0-A: 前端商城 API 路径重复拼接
- ✅ 修复 P0-B: 后端 router 重复 prefix
- ✅ 修复 P0-C & P0-D: 后台 token 键名和 dashboard mock
- ✅ 修复 P0-E: 后端 admin 接口鉴权
- ✅ 修复 P0-F: 订单/库存链路
- ✅ 修复 P0-H: 路由导入异常处理
- ✅ 更新 fix-progress.md
