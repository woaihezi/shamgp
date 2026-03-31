# 商城项目

一个现代化的电商平台项目，包含管理后台、前端商城和后端 API。

## 技术栈

### 前端管理后台 (frontend-admin)
- Vue 3
- Vite
- TypeScript
- Element Plus
- ECharts
- Pinia
- Vue Router
- Axios

### 前端商城 (frontend-shop)
- Vue 3
- Vite
- TypeScript
- Pinia
- Vue Router
- Axios

### 后端 (backend)
- FastAPI
- SQLAlchemy
- JWT
- Pydantic

### 数据库
- MySQL / PostgreSQL

## 项目结构

```
shamgp/
├── frontend-admin/       # 管理后台
├── frontend-shop/        # 前端商城
├── backend/              # 后端 API
├── docs/                 # 文档
├── sql/                  # SQL 脚本
├── scripts/              # 脚本文件
├── docker/               # Docker 配置
├── .env.example          # 环境变量示例
├── docker-compose.yml    # Docker Compose 配置
└── README.md             # 项目说明
```

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.10+
- Docker (可选)

### 1. 克隆项目

```bash
git clone <repository-url>
cd shamgp
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置
```

### 3. 启动数据库 (使用 Docker)

```bash
docker-compose up -d mysql
```

### 4. 启动后端

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

后端 API 文档: http://localhost:8000/docs

### 5. 启动管理后台

```bash
cd frontend-admin
npm install
npm run dev
```

访问: http://localhost:3000

### 6. 启动前端商城

```bash
cd frontend-shop
npm install
npm run dev
```

访问: http://localhost:3001

## 使用 Docker Compose 启动

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 开发指南

详细开发指南请参考 `docs/` 目录下的文档。

## 许可证

MIT
