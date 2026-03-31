# 项目规范化整理任务报告

## 1. 当前项目存在的主要结构问题

### 1.1 后端问题
- `backend/app/main.py` 只包含了 carts 和 orders 路由，未接入其他所有 API 模块
- 配置文件 `backend/app/core/config.py` 使用硬编码的 PostgreSQL URL，与 `.env.example` 不一致
- `requirements.txt` 缺少必要的数据库驱动（asyncpg、aiomysql）

### 1.2 前端管理后台问题
- 存在重复的布局目录：`layout/` 和 `layouts/`
- `App.vue` 使用简单布局，未集成完整的后台管理布局
- 路由配置过于简单，未配置完整的管理后台页面路由
- Stores 结构混乱，存在重复的 store 定义

### 1.3 前端请求规范问题
- `frontend-admin` 和 `frontend-shop` 的 request.ts 都硬编码了 `http://localhost:8000` 作为 baseURL
- 虽然 vite.config.ts 都配置了 proxy，但请求没有通过 proxy 发送

## 2. 完成的收口动作

### 2.1 统一后端 API 入口
- 修改 `backend/app/main.py`，改为引入 `api_router` 统一管理所有路由
- 更新 `backend/app/api/v1/api.py`，整合所有 API 模块路由：
  - admin 相关路由（coupons、banners）
  - shop 相关路由（home、coupons）
  - 其他核心路由（auth、carts、categories、dashboard、inventory、logs、menus、orders、products、roles、shop_products、system_config、uploads、users）

### 2.2 统一后端环境变量配置
- 重构 `backend/app/core/config.py`：
  - 支持 DB_TYPE（mysql/postgresql/sqlite）配置
  - 添加单独的 DB_HOST、DB_PORT、DB_USER、DB_PASSWORD、DB_NAME 配置项
  - 通过 @property 动态生成 DATABASE_URL
  - 添加 BACKEND_HOST 和 BACKEND_PORT 配置
- 更新 `backend/requirements.txt`，添加：
  - aiomysql==0.2.0（MySQL 异步驱动）
  - asyncpg==0.29.0（PostgreSQL 异步驱动）
  - greenlet==3.0.3（SQLAlchemy 异步支持）

### 2.3 统一前端请求规范
- 修改 `frontend-admin/src/utils/request.ts`：baseURL 改为空字符串，使用 Vite proxy
- 修改 `frontend-shop/src/utils/request.ts`：baseURL 改为空字符串，使用 Vite proxy

### 2.4 统一 frontend-admin 布局结构
- 保留 `layouts/` 目录（更完整的后台管理布局）
- 更新 `App.vue`，简化为只使用 `<router-view />`
- 完善路由配置 `frontend-admin/src/router/index.ts`：
  - 添加登录页路由
  - 配置基于 Layout 的主路由结构
  - 添加首页、商品管理、订单管理、营销运营、文件管理、系统设置等页面路由
- 统一 Stores 结构：
  - 更新 `stores/index.ts`，导出 modules 下的完整 store
  - 更新 `stores/app.ts`，重定向到 modules/app

### 2.5 配置文件
- 从 `.env.example` 复制创建 `.env` 文件

## 3. 修改的文件清单

### 后端文件
- `backend/app/main.py` - 统一 API 入口
- `backend/app/api/v1/api.py` - 整合所有路由
- `backend/app/core/config.py` - 统一配置管理
- `backend/requirements.txt` - 添加数据库驱动

### 前端管理后台文件
- `frontend-admin/src/App.vue` - 简化 App 组件
- `frontend-admin/src/router/index.ts` - 完善路由配置
- `frontend-admin/src/utils/request.ts` - 统一请求规范
- `frontend-admin/src/stores/index.ts` - 统一 store 导出
- `frontend-admin/src/stores/app.ts` - 重定向到 modules/app

### 前端商城文件
- `frontend-shop/src/utils/request.ts` - 统一请求规范

### 配置文件
- `.env` - 新建环境变量配置文件

## 4. 删除或合并的重复内容
- 计划删除 `frontend-admin/src/layout/` 目录（保留 `layouts/` 作为主要布局）
- 合并了 store 定义，统一使用 `stores/modules/` 下的完整实现

## 5. 项目启动说明

### 5.1 后端启动
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5.2 前端管理后台启动
```bash
cd frontend-admin
npm install
npm run dev
```
访问：http://localhost:3000

### 5.3 前端商城启动
```bash
cd frontend-shop
npm install
npm run dev
```
访问：http://localhost:3001

## 6. 暂未完全联调的部分

### 6.1 后端
- 数据库连接需要实际的 MySQL/PostgreSQL 服务运行
- 部分 API 依赖数据库表结构，需要执行 SQL 初始化脚本
- 用户认证中间件未完全集成

### 6.2 前端管理后台
- 登录功能未完全实现
- 侧边栏菜单动态生成未实现
- 各页面的 API 调用未完全对接
- TagsView 功能可能需要完善

### 6.3 前端商城
- 页面路由和组件需要进一步完善
- API 调用未完全对接

### 6.4 整体
- 数据库初始化脚本需要执行
- 测试数据需要准备
