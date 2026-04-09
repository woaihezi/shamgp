# 开发指南

本文档介绍如何在本地环境中设置和开发 ShamGP 商城项目。

---

## 一、环境准备

### 1.1 系统要求

- **操作系统**: Windows 10+ / macOS 10.15+ / Ubuntu 20.04+
- **Node.js**: 18.0+ (用于前端开发)
- **Python**: 3.10+ (用于后端开发)
- **数据库**: MySQL 8.0+ 或 PostgreSQL 13+ 或 SQLite (默认)
- **Git**: 2.20+ (版本控制)

### 1.2 工具推荐

- **代码编辑器**: VS Code (推荐) 或 PyCharm
- **数据库工具**: Navicat / DBeaver / phpMyAdmin
- **API 测试工具**: Postman / Insomnia
- **终端**: Windows Terminal (Windows) / iTerm2 (macOS) / GNOME Terminal (Linux)

---

## 二、项目结构

```
├── backend/          # 后端代码 (FastAPI + SQLAlchemy)
├── frontend-admin/   # 管理后台 (Vue 3 + Element Plus)
├── frontend-shop/    # 前端商城 (Vue 3 + Element Plus)
├── docs/             # 项目文档
├── sql/              # SQL 脚本
└── docker-compose.yml # Docker 配置
```

---

## 三、后端开发环境搭建

### 3.1 克隆代码

```bash
# 克隆仓库
git clone <repository-url> shamgp
cd shamgp
```

### 3.2 配置环境变量

```bash
# 进入后端目录
cd backend

# 复制环境变量文件
cp .env.example .env

# 编辑 .env 文件
# 可以使用默认配置，SQLite 作为默认数据库
```

### 3.3 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3.4 初始化数据库

```bash
# 激活虚拟环境（如果还没有激活）
source venv/bin/activate

# 初始化数据库
python scripts/init_db.py

# 填充初始数据
python scripts/seed_data.py

# 填充 RBAC 数据
python scripts/seed_rbac.py
```

### 3.5 启动开发服务器

```bash
# 激活虚拟环境（如果还没有激活）
source venv/bin/activate

# 启动开发服务器
uvicorn app.main:app --reload --port 8000

# 访问 Swagger UI: http://localhost:8000/docs
# 访问 ReDoc: http://localhost:8000/redoc
```

---

## 四、前端开发环境搭建

### 4.1 管理后台

```bash
# 进入管理后台目录
cd frontend-admin

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问: http://localhost:3000
```

### 4.2 前端商城

```bash
# 进入前端商城目录
cd frontend-shop

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问: http://localhost:3001
```

---

## 五、数据库操作

### 5.1 使用 SQLite (默认)

SQLite 是默认的数据库，无需额外配置，适合开发和测试。

### 5.2 使用 MySQL

1. **修改 .env 文件**:
   ```env
   DB_TYPE=mysql
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=shop_db
   ```

2. **创建数据库**:
   ```sql
   CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **重新初始化数据库**:
   ```bash
   python scripts/init_db.py
   python scripts/seed_data.py
   ```

### 5.3 使用 PostgreSQL

1. **修改 .env 文件**:
   ```env
   DB_TYPE=postgresql
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_NAME=shop_db
   ```

2. **创建数据库**:
   ```sql
   CREATE DATABASE shop_db;
   ```

3. **重新初始化数据库**:
   ```bash
   python scripts/init_db.py
   python scripts/seed_data.py
   ```

---

## 六、开发流程

### 6.1 代码风格

- **后端**: 遵循 PEP 8 规范，使用 Black 进行代码格式化
- **前端**: 遵循 ESLint 规则，使用 Prettier 进行代码格式化

### 6.2 提交规范

使用 Conventional Commits 规范:

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码风格调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建或依赖更新

### 6.3 分支管理

- `main`: 主分支，用于发布
- `develop`: 开发分支，集成所有功能
- `feature/*`: 功能分支，用于开发新功能
- `fix/*`: 修复分支，用于修复 bug

### 6.4 开发步骤

1. **创建分支**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **开发功能**:
   - 编写代码
   - 添加测试
   - 运行测试

3. **提交代码**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

4. **推送到远程**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **创建 Pull Request**:
   - 描述功能或修复
   - 关联相关 issue

---

## 七、测试

### 7.1 后端测试

```bash
# 进入后端目录
cd backend

# 安装测试依赖
pip install pytest pytest-asyncio aiosqlite

# 运行测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/unit/test_user_service.py
```

### 7.2 前端测试

```bash
# 进入前端目录
cd frontend-admin # 或 frontend-shop

# 运行测试
npm test

# 构建测试
npm run build
```

---

## 八、常见问题

### 8.1 后端启动失败

- **端口占用**: 检查 8000 端口是否被占用
  ```bash
  lsof -i :8000
  ```

- **数据库连接失败**: 检查数据库配置和服务状态
  ```bash
  sudo systemctl status mysql # 或 postgresql
  ```

- **依赖缺失**: 重新安装依赖
  ```bash
  pip install -r requirements.txt
  ```

### 8.2 前端启动失败

- **依赖缺失**: 重新安装依赖
  ```bash
  npm install
  ```

- **端口占用**: 检查 3000/3001 端口是否被占用
  ```bash
  lsof -i :3000
  ```

- **Node.js 版本问题**: 确保使用 Node.js 18.0+
  ```bash
  node --version
  ```

### 8.3 数据库初始化失败

- **权限不足**: 检查数据库用户权限
- **数据库不存在**: 先创建数据库
- **SQL 语法错误**: 检查 SQL 脚本

---

## 九、Docker 开发环境

### 9.1 使用 Docker Compose

```bash
# 在项目根目录
cd /path/to/shamgp

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 停止服务
docker-compose down
```

### 9.2 访问服务

- **管理后台**: http://localhost:3000
- **前端商城**: http://localhost:3001
- **后端 API**: http://localhost:8000
- **数据库**: localhost:3306 (MySQL)

---

## 十、API 开发

### 10.1 添加新 API

1. **创建路由**:
   - 在 `backend/app/api/v1/` 目录下创建新的路由文件
   - 在 `backend/app/api/v1/api.py` 中注册路由

2. **创建服务**:
   - 在 `backend/app/services/` 目录下创建新的服务文件
   - 实现业务逻辑

3. **创建模型**:
   - 在 `backend/app/models/` 目录下创建新的模型文件
   - 定义数据库表结构

4. **创建 schema**:
   - 在 `backend/app/schemas/` 目录下创建新的 schema 文件
   - 定义请求和响应的数据结构

### 10.2 测试 API

- **Swagger UI**: http://localhost:8000/docs
- **Postman**: 创建请求并测试
- **curl**: 命令行测试
  ```bash
  curl -X GET http://localhost:8000/api/v1/products/simple
  ```

---

## 十一、前端开发

### 11.1 添加新页面

1. **创建组件**:
   - 在 `frontend-admin/src/views/` 或 `frontend-shop/src/views/` 目录下创建新的页面组件

2. **注册路由**:
   - 在 `frontend-admin/src/router/index.ts` 或 `frontend-shop/src/router/index.ts` 中注册路由

3. **添加 API 调用**:
   - 在 `frontend-admin/src/api/` 或 `frontend-shop/src/api/` 目录下创建或修改 API 文件

4. **添加样式**:
   - 在组件中添加样式，或在 `src/styles/` 目录下添加全局样式

### 11.2 状态管理

- **Vuex**: 用于全局状态管理
- **Pinia**: 推荐使用，更简洁的状态管理方案

---

## 十二、部署到生产环境

参考 [部署指南](./deployment.md) 文档。

---

## 十三、开发工具推荐

### 13.1 VS Code 插件

- **Python**: Python 语言支持
- **Pylance**: Python 类型检查
- **Black Formatter**: 代码格式化
- **Prettier**: 前端代码格式化
- **ESLint**: 前端代码检查
- **Volar**: Vue 3 支持
- **Docker**: Docker 支持
- **GitLens**: Git 增强

### 13.2 其他工具

- **Postman**: API 测试
- **DBeaver**: 数据库管理
- **Figma**: 设计工具
- **GitHub Desktop**: Git 客户端

---

## 十四、团队协作

### 14.1 代码 review

- 每次提交前运行测试
- 提交 Pull Request 后进行代码 review
- 确保代码符合项目规范

### 14.2 文档更新

- 功能变更时更新相关文档
- 保持 API 文档与代码同步
- 记录重要的设计决策

### 14.3 问题跟踪

- 使用 GitHub Issues 或 Jira 跟踪任务和 bug
- 定期进行 sprint 规划
- 保持任务状态更新

---

*文档更新时间: 2026-04-09*