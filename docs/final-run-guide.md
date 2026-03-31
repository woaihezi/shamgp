# 项目最终运行指南

## 环境要求

- Node.js 18+
- Python 3.10+
- MySQL 8.0+ 或 PostgreSQL 13+（可选，也可以使用 SQLite）
- Docker（可选，用于快速启动数据库）

## 1. 数据库准备（可选）

### 方式一：使用 Docker 启动 MySQL
```bash
docker run --name shamgp-mysql -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=shop_db -p 3306:3306 -d mysql:8.0
```

### 方式二：使用本地 MySQL
确保本地 MySQL 已启动，然后创建数据库：
```sql
CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 2. 后端启动

### 2.1 配置环境变量
项目根目录已有 `.env` 文件，根据实际情况修改数据库配置：
```env
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=shop_db
```

### 2.2 创建虚拟环境并安装依赖
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2.3 启动后端服务
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端 API 文档：http://localhost:8000/docs

健康检查：http://localhost:8000/health

## 3. 前端管理后台启动

```bash
cd frontend-admin
npm install
npm run dev
```

访问：http://localhost:3000

## 4. 前端商城启动

```bash
cd frontend-shop
npm install
npm run dev
```

访问：http://localhost:3001

## 5. 数据库初始化（可选）

如果需要初始化数据库表结构，可以执行 `sql/` 目录下的 SQL 脚本。

## 6. 服务说明

| 服务 | 地址 | 说明 |
|------|------|------|
| 后端 API | http://localhost:8000 | FastAPI 服务 |
| API 文档 | http://localhost:8000/docs | Swagger UI |
| 前端管理后台 | http://localhost:3000 | Vue 3 + Element Plus |
| 前端商城 | http://localhost:3001 | Vue 3 |

## 7. 常见问题

### 7.1 后端启动失败
- 检查 Python 版本是否为 3.10+
- 检查虚拟环境是否正确激活
- 检查 .env 文件配置是否正确
- 检查数据库服务是否启动

### 7.2 前端启动失败
- 检查 Node.js 版本是否为 18+
- 删除 node_modules 和 package-lock.json，重新 npm install
- 检查端口 3000/3001 是否被占用

### 7.3 前端无法请求后端 API
- 确认后端服务已启动
- 检查浏览器控制台是否有错误
- 确认 vite.config.ts 中的 proxy 配置正确
