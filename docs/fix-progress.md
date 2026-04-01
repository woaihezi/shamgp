# ShamGP 商城项目 - P0 / P1 / P2 修复进度

**开始时间**: 2026-04-01
**当前状态**: 已完成 P0 修复和 P1/P2 收尾

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
| 10 | 打通最小下单闭环 | ✅ 完成 | 2026-04-01 |
| 11 | P1-1: README 与真实启动方式对齐 | ✅ 完成 | 2026-04-01 |
| 12 | P1-2: 环境变量收口 | ✅ 完成 | 2026-04-01 |
| 13 | P1-3: 商品列表页最小可用 | ✅ 完成 | 2026-04-01 |
| 14 | P2-1: 补最小 smoke 测试/验证脚本 | ✅ 完成 | 2026-04-01 |
| 15 | P2-2: 补文档 | ✅ 完成 | 2026-04-01 |

---

## 已修复问题清单（P0）

见 docs/audit-fix-report.md

---

## 已完成 P1/P2 收尾

### P1-1: README 与真实启动方式对齐
**修复文件**: `README.md`
**修复内容**:
- 明确数据库使用 SQLite（无需 docker-compose）
- 明确 docker-compose 只负责数据库（项目默认不使用）
- 添加真实已验证功能清单
- 添加当前已知限制
- 明确默认账号

---

### P1-2: 环境变量收口
**修复文件**: `.env.example`
**修复内容**:
- 统一 DB_TYPE 默认为 sqlite
- 添加 API_STRICT_MODE 配置
- 明确各配置项说明
- 与 backend/config.py 对齐

---

### P1-3: 商品列表页最小可用
**修复文件**: `frontend-shop/src/views/ProductList/index.vue`
**修复内容**:
- handleSearch 不再是空函数
- 关键词搜索已实现
- 分类过滤已实现
- 添加 loading 状态
- 明确说明当前为前端过滤

---

### P2-1: 补最小 smoke 测试/验证脚本
**新增文件**: `scripts/verify-minimal.ps1`
**内容**:
- 完整验证登录→商品→购物车→地址→创建订单
- 可复制执行的 PowerShell 脚本

---

### P2-2: 补文档
**新增/更新文件**:
- `docs/known-issues.md` - 已知问题清单
- `docs/startup-runbook.md` - 启动运行手册
- `docs/route-map.md` - 路由映射表
- `docs/auth-flow.md` - 认证流程

---

## 修复日志

### 2026-04-01
- ✅ 创建 audit-fix-report.md
- ✅ 修复 P0-A 到 P0-H
- ✅ 打通最小下单闭环（登录→商品→购物车→地址→创建订单→库存扣减）
- ✅ P1-1: 更新 README.md
- ✅ P1-2: 更新 .env.example
- ✅ P1-3: 修复 ProductList 组件
- ✅ P2-1: 创建 verify-minimal.ps1 验证脚本
- ✅ P2-2: 补充 known-issues.md、startup-runbook.md、route-map.md、auth-flow.md
- ✅ 更新 fix-progress.md
