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
- SQLAlchemy 2.0
- JWT
- Pydantic 2

### 数据库
- SQLite (默认开发环境)

## 项目结构

```
shamgp/
├── frontend-admin/       # 管理后台
├── frontend-shop/        # 前端商城
├── backend/              # 后端 API
├── docs/                 # 文档
├── scripts/              # 脚本文件
├── .env.example          # 环境变量示例
└── README.md             # 项目说明
```

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.10+

### 1. 克隆项目

```bash
git clone <repository-url>
cd shamgp
```

### 2. 启动后端

**注意：docker-compose.yml 只负责数据库，本项目默认使用 SQLite，无需额外启动数据库**

#### 安全配置（P0 必做）

- 必须在 `.env` 中设置强随机 `SECRET_KEY`（至少 32 位）。
- `CORS_ORIGINS` 必须是明确域名白名单，禁止使用 `*`。
- 若需要跨域携带凭据（Cookie/Authorization），`CORS_ALLOW_CREDENTIALS=true` 时同样不能使用 `*`。

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py

# 导入种子数据
python scripts/seed_data.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端 API 文档: http://localhost:8000/docs

### 3. 启动管理后台

```bash
cd frontend-admin
npm install
npm run dev
```

访问: http://localhost:3000

**默认账号**:
- 用户名: `admin`
- 密码: `admin123`

### 4. 启动前端商城

```bash
cd frontend-shop
npm install
npm run dev
```

访问: http://localhost:3001

**默认测试账号**:
- 用户名: `testuser`
- 密码: `user123`

或使用注册功能创建新账号

## 当前已验证功能

✅ **后端核心链路**:
- 用户注册/登录（JWT）
- 商品列表（简单商品）
- 购物车（加购、摘要、列表）
- 收货地址管理
- 订单创建
- 产品级库存扣减

✅ **管理后台**:
- 登录
- Dashboard（需要登录鉴权）

✅ **前端商城**:
- API 路径修复（无重复前缀）

## 当前已知限制

1. **SKU 库存链路**：仅验证了产品级库存扣减，未验证 SKU 级库存扣减
2. **后台权限**：仅添加了登录鉴权，未细分权限级别
3. **商品列表页**：搜索和分类过滤功能需要完善
4. **支付功能**：未实现
5. **订单状态流转**：仅创建订单，未实现支付、发货、收货等状态

## 开发指南

详细开发指南请参考 `docs/` 目录下的文档。

## 许可证

MIT
