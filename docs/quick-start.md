# 快速开始指南

本指南将帮助你在 5 分钟内启动 ShamGP 商城项目。

---

## 一、环境准备

### 1.1 必需软件

- **Node.js**: 18.0 或更高版本
- **Python**: 3.10 或更高版本
- **Git**: 用于克隆代码（可选）

### 1.2 验证环境

打开终端，运行以下命令验证环境：

```bash
# 检查 Node.js 版本
node --version

# 检查 Python 版本
python --version

# 或
python3 --version
```

---

## 二、获取项目代码

### 2.1 克隆项目（如果使用 Git）

```bash
git clone <repository-url>
cd shamgp
```

### 2.2 或直接下载项目

如果你已经有项目代码，直接进入项目目录即可。

---

## 三、后端启动

### 3.1 进入后端目录

```bash
cd backend
```

### 3.2 创建虚拟环境

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.3 安装依赖

```bash
pip install -r requirements.txt
```

### 3.4 初始化数据库

项目默认使用 SQLite，无需额外安装数据库服务。

```bash
# 创建数据库表
python scripts/init_db.py

# 插入测试数据
python scripts/seed_data.py
```

成功后你会看到：
```
Creating database tables...
Database tables created successfully!
Seeding data...
Data seeded successfully!

Default admin account:
  Username: admin
  Password: admin123

Test user account:
  Username: testuser
  Password: user123
```

### 3.5 启动后端服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

或者使用项目提供的启动脚本：

**Windows:**
```powershell
python run_server.ps1
```

看到以下输出表示启动成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
```

### 3.6 验证后端

打开浏览器访问：
- **健康检查**: http://localhost:8000/health
- **API 文档**: http://localhost:8000/docs
- **根路径**: http://localhost:8000/

---

## 四、前端管理后台启动

### 4.1 打开新终端

保持后端服务运行，打开一个新的终端窗口。

### 4.2 进入管理后台目录

```bash
cd frontend-admin
```

### 4.3 安装依赖

```bash
npm install
```

### 4.4 启动开发服务器

```bash
npm run dev
```

看到以下输出表示启动成功：
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### 4.5 访问管理后台

打开浏览器访问：http://localhost:3000

**登录账号：**
- 用户名: `admin`
- 密码: `admin123`

---

## 五、前端商城启动

### 5.1 打开新终端

保持后端和管理后台运行，再打开一个新的终端窗口。

### 5.2 进入商城目录

```bash
cd frontend-shop
```

### 5.3 安装依赖

```bash
npm install
```

### 5.4 启动开发服务器

```bash
npm run dev
```

看到以下输出表示启动成功：
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3001/
  ➜  Network: use --host to expose
```

### 5.5 访问商城

打开浏览器访问：http://localhost:3001

**测试账号：**
- 用户名: `testuser`
- 密码: `user123`

或者注册一个新账号。

---

## 六、服务地址汇总

| 服务 | 地址 | 说明 |
|------|------|------|
| 后端 API | http://localhost:8000 | FastAPI 服务 |
| API 文档 | http://localhost:8000/docs | Swagger UI |
| 管理后台 | http://localhost:3000 | Vue 3 + Element Plus |
| 前端商城 | http://localhost:3001 | Vue 3 |

---

## 七、快速测试流程

### 7.1 测试后端 API

使用 Swagger UI 测试：
1. 访问 http://localhost:8000/docs
2. 点击 `/auth/login` 接口
3. 点击 "Try it out"
4. 输入：
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
5. 点击 "Execute"
6. 复制返回的 `access_token`

### 7.2 测试管理后台

1. 访问 http://localhost:3000
2. 使用 admin/admin123 登录
3. 浏览 Dashboard、商品管理、订单管理等页面

### 7.3 测试前端商城

1. 访问 http://localhost:3001
2. 浏览首页、商品列表
3. 注册或登录账号
4. 添加商品到购物车
5. 查看购物车

---

## 八、常见问题快速解决

### Q: 后端启动失败，提示 "No module named 'xxx'"
A: 确保已激活虚拟环境并安装了所有依赖：
```bash
# Windows
.\venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
```

### Q: 前端启动失败，提示 "port already in use"
A: 修改端口或关闭占用端口的程序。在 `vite.config.ts` 中修改端口，或使用：
```bash
npm run dev -- --port 3002
```

### Q: 前端无法连接后端 API
A: 确保：
1. 后端服务已启动在 http://localhost:8000
2. 检查浏览器控制台的网络请求
3. 确认 vite.config.ts 中的 proxy 配置正确

### Q: 数据库错误
A: 删除数据库文件重新初始化：
```bash
# Windows
del backend\shop_db.db

# Linux/Mac
rm backend/shop_db.db

# 重新初始化
cd backend
python scripts/init_db.py
python scripts/seed_data.py
```

---

## 九、下一步

- 阅读 [API 接口总览](./api-overview.md) 了解所有 API
- 阅读 [数据库设计](./database-design.md) 了解数据库结构
- 阅读 [开发指南](./dev-db-init-guide.md) 了解更多开发细节
- 阅读 [部署指南](./deployment.md) 了解如何部署到生产环境

---

## 十、需要帮助？

查看 [常见问题 FAQ](./faq.md) 或 [项目审计报告](./project-audit-report.md) 了解更多信息。

---

*文档更新时间: 2026-04-01*
