# 审计问题清单

| 编号 | 优先级 | 模块 | 问题标题 | 现象 | 根因 | 影响 | 复现步骤 | 建议修复文件 | 建议修复方式 |
|------|--------|------|----------|------|------|------|----------|--------------|--------------|
| 1 | P0 | 后端 | 订单接口认证错误 | GET /api/v1/orders 返回 401 未认证错误 | 权限依赖配置问题或 token 验证失败 | 订单流程无法完成，用户无法查看订单 | 1. 登录获取 token<br>2. 使用 token 调用 GET /api/v1/orders | backend/app/api/v1/orders.py<br>backend/app/api/deps.py | 检查 orders.py 中的依赖配置，确保使用正确的认证依赖 |
| 2 | P0 | 后端 | 数据库依赖 | 后端服务依赖 MySQL 数据库，本地环境可能无法连接 | 配置文件默认使用 MySQL，需要实际数据库服务 | 服务启动后可能无法正常操作数据库 | 1. 启动后端服务<br>2. 尝试调用需要数据库的接口 | backend/app/core/config.py | 修改配置，支持 SQLite 作为默认数据库，或提供 Docker 启动脚本 |
| 3 | P1 | 管理后台 | Dashboard 使用 mock 数据 | Dashboard 页面显示 mock 数据，API 调用失败 | 后端 /admin/stats 接口不存在 | 管理后台无法查看真实数据统计 | 1. 登录管理后台<br>2. 访问 Dashboard 页面 | frontend-admin/src/views/dashboard/index.vue<br>backend/app/api/v1/dashboard.py | 实现后端 /admin/stats 接口，或修改前端使用现有 API |
| 4 | P1 | 前端商城 | 购物车使用本地 store | 购物车操作使用本地 store，未调用后端 API | 前端代码未实现购物车 API 调用 | 购物车数据无法持久化，用户切换设备后购物车丢失 | 1. 登录前端商城<br>2. 添加商品到购物车<br>3. 查看网络请求 | frontend-shop/src/stores/cart.ts<br>frontend-shop/src/api/cart.ts | 修改购物车逻辑，调用后端 /api/v1/carts 相关接口 |
| 5 | P1 | 后端 | deps.py 语法错误 | deps.py 第 74 行使用了错误的语法 | 代码语法错误 | 可能导致权限相关功能异常 | 1. 检查 deps.py 文件 | backend/app/api/deps.py | 修复第 74 行的语法错误，使用正确的 SQLAlchemy 查询语法 |
| 6 | P2 | 前端商城 | 商品详情页加入购物车 | 商品详情页加入购物车使用本地 store，未调用后端 API | 前端代码未实现购物车 API 调用 | 购物车数据无法持久化 | 1. 进入商品详情页<br>2. 点击"加入购物车"<br>3. 查看网络请求 | frontend-shop/src/views/ProductDetail/index.vue | 修改加入购物车逻辑，调用后端 /api/v1/carts/items 接口 |
| 7 | P2 | 管理后台 | token 字段不一致 | 部分代码使用 `token`，部分使用 `access_token` | 代码中 token 字段命名不统一 | 可能导致 token 存储和使用异常 | 1. 登录管理后台<br>2. 检查 localStorage 中的 token 字段 | frontend-admin/src/utils/auth.ts<br>frontend-admin/src/api/request.ts | 统一使用 `access_token` 字段 |
| 8 | P2 | 前端商城 | 商品搜索功能未实现 | 商品列表页搜索功能点击后无反应 | 搜索功能未实现 | 用户无法搜索商品 | 1. 进入商品列表页<br>2. 输入搜索关键词<br>3. 点击搜索按钮 | frontend-shop/src/views/ProductList/index.vue | 实现搜索功能，调用后端商品列表接口并传递 keyword 参数 |
| 9 | P3 | 前端 | 错误处理机制缺失 | 前端缺少统一的错误处理机制 | 代码中未实现全局错误处理 | 用户体验差，错误信息不友好 | 1. 故意触发错误（如无效登录）<br>2. 观察错误处理方式 | frontend-shop/src/api/request.ts<br>frontend-admin/src/api/request.ts | 实现全局错误处理，统一错误提示 |
| 10 | P3 | 后端 | API 文档不完善 | 缺少详细的 API 文档 | 未编写 API 文档 | 开发和调试困难 | 查看 /docs 页面 | backend/app/api/v1/ | 完善 API 文档注释，使用 FastAPI 的文档功能 |