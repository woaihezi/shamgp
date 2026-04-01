# ShamGP 商城项目 - P0 优先修复审计报告

**审计时间**: 2026-04-01
**审计范围**: woaihezi/shamgp 仓库
**目标**: P0 优先真实修复，前后端主链路可运行、可联调、可验收

---

## 一、审计问题汇总

### P0 问题（必须优先修复）

| 编号 | 问题 | 严重程度 | 状态 |
|------|------|---------|------|
| P0-A | 前端商城 API 路径重复拼接问题 | 🔴 严重 | 待修复 |
| P0-B | 后端 router 重复 prefix 问题 | 🔴 严重 | 待修复 |
| P0-C | 后台 token 键名不一致问题 | 🔴 严重 | 待修复 |
| P0-D | 后台 dashboard mock 掩盖真实故障问题 | 🔴 严重 | 待修复 |
| P0-E | 后端 admin 接口鉴权缺失问题 | 🟠 高 | 待修复 |
| P0-F | 订单/库存链路真实错误修复 | 🟠 高 | 待修复 |
| P0-G | 优惠券前后端协议对齐 | 🟠 高 | 待修复 |
| P0-H | 路由导入失败被静默跳过 | 🟠 高 | 待修复 |

### P1 问题（顺手修复）

| 编号 | 问题 | 严重程度 | 状态 |
|------|------|---------|------|
| P1-1 | README 与真实启动方式对齐 | 🟡 中 | 待修复 |
| P1-2 | 环境变量收口 | 🟡 中 | 待修复 |
| P1-3 | 商品列表页最小可用 | 🟡 中 | 待修复 |

---

## 二、详细问题分析

### P0-A: 前端商城 API 路径重复拼接问题

**问题描述**:
- `frontend-shop/src/api/request.ts` 已设置 `baseURL = '/api/v1'`
- 但业务 API 文件中仍有 `/api/v1/...` 的重复拼接
- 导致实际请求变成 `/api/v1/api/v1/...`

**受影响文件**:
- `frontend-shop/src/api/auth.ts`: 第 20, 24, 28, 32 行
- `frontend-shop/src/api/cart.ts`: 第 36-41 行
- `frontend-shop/src/api/product.ts`: 第 137-146 行
- `frontend-shop/src/api/order.ts`: 第 83-104 行
- `frontend-shop/src/api/home.ts`: 第 3, 66, 69, 72, 75, 81, 84 行

**修复方案**:
- 保留 `request.ts` 的 `baseURL = '/api/v1'`
- 所有业务 API 文件改为相对路径

---

### P0-B: 后端 router 重复 prefix 问题

**问题描述**:
- `backend/app/api/v1/api.py` 在 `include_router` 时传了 `prefix`
- 但部分 router 文件内部也定义了 `prefix`
- 导致双重叠加

**受影响文件**:
- `backend/app/api/v1/shop/home.py`: 第 14 行 `prefix="/home"`
- `backend/app/api/v1/dashboard.py`: 第 14 行 `prefix="/dashboard"`

**修复方案**:
- 统一只在 `api.py` 中传 prefix
- 移除各 router 文件内部的 prefix 定义

---

### P0-C: 后台 token 键名不一致问题

**问题描述**:
- 项目中同时使用 `token` 和 `access_token`
- `frontend-admin/src/views/dashboard/index.vue`: 第 126, 146 行使用 `localStorage.getItem('token')`
- `frontend-admin/src/api/request.ts`: 第 12 行使用 `localStorage.getItem('access_token')`
- `frontend-admin/src/utils/auth.ts`: 不确定使用哪个

**修复方案**:
- 全项目统一只使用 `access_token`
- 修复 dashboard 页面和其他相关文件

---

### P0-D: 后台 dashboard mock 掩盖真实故障问题

**问题描述**:
- `frontend-admin/src/views/dashboard/index.vue` 在 API 失败时静默使用 mock 数据
- 没有显示错误状态，用户不知道真实接口是否可用
- 请求路径 `/admin/stats` 与后端真实路径 `/dashboard/stats` 不匹配

**修复方案**:
- 去掉 mock 数据回退逻辑
- 接口失败时显示明确错误提示
- 修正请求路径

---

### P0-E: 后端 admin 接口鉴权缺失问题

**问题描述**:
- 检查发现部分 admin 接口没有添加鉴权依赖
- 需要确保后台接口不裸奔

**需要检查的接口**:
- `dashboard`
- `orders admin`
- `inventory`
- `logs`
- `system_config`
- `menus`
- `uploads`
- `admin/coupons`
- `admin/banners`

**修复方案**:
- 应加登录鉴权的加 `Depends(get_current_active_user)`
- 应加权限控制的加 `require_permissions(...)`

---

### P0-F: 订单/库存链路真实错误修复

**问题描述**:
- `backend/app/services/order_service.py` 存在导入问题
- 第 210 行使用了 `ProductSku` 但没有导入
- 库存扣减逻辑需要验证

**修复方案**:
- 修复缺失导入
- 验证 `create_order` / `cancel_order` / `deduct_stock_for_order` 是否可真实执行

---

### P0-G: 优惠券前后端协议对齐

**问题描述**:
- 前端和后端优惠券接口协议不一致
- `frontend-shop/src/api/home.ts` 第 84 行 `receiveCoupon` 还在传 `user_id`
- 应该基于当前登录用户获取

**修复方案**:
- 统一路径、参数、user_id 获取方式
- 优先保证最小可用链路：查询可领取、查询我的优惠券、下单使用

---

### P0-H: 路由导入失败被静默跳过

**问题描述**:
- `backend/app/api/v1/api.py` 第 7-14 行 `_include_router` 会吞异常
- 导致服务启动了但接口没挂上

**修复方案**:
- 开发环境：打印完整错误并明确标识失败模块
- 至少提供一个严格模式开关

---

## 三、修复计划

### 修复顺序
1. ✅ 创建 audit-fix-report.md
2. ⏳ 修复 P0-A: 前端商城 API 路径重复拼接
3. ⏳ 修复 P0-B: 后端 router 重复 prefix
4. ⏳ 修复 P0-C: 后台 token 键名不一致
5. ⏳ 修复 P0-D: 后台 dashboard mock 问题
6. ⏳ 修复 P0-E: 后端 admin 接口鉴权
7. ⏳ 修复 P0-F: 订单/库存链路
8. ⏳ 修复 P0-G: 优惠券协议对齐
9. ⏳ 修复 P0-H: 路由导入异常处理
10. ⏳ 修复 P1 问题
11. ⏳ 验证并更新 docs/fix-progress.md
12. ⏳ 输出最终修复报告

---

*文档创建时间: 2026-04-01*
