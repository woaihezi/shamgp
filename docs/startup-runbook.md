# ShamGP 商城项目 - 启动运行手册

**更新时间**: 2026-04-01

---

## 新机器如何拉起项目

### 一、环境准备

**必需软件**:
- Node.js 18+
- Python 3.10+
- Git

---

### 二、后端启动

#### 1. 克隆项目
```bash
git clone <repository-url>
cd shamgp
```

#### 2. 配置环境变量（可选）
```bash
cp .env.example .env
# 编辑 .env（开发环境使用默认 SQLite，可不用修改）
```

#### 3. 初始化后端
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
```

#### 4. 启动后端服务
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**验证后端启动成功**:
- 访问 http://localhost:8000/health
- 期望返回: `{"status":"healthy"}`
- API 文档: http://localhost:8000/docs

---

### 三、管理后台启动

```bash
cd frontend-admin
npm install
npm run dev
```

**访问地址**: http://localhost:3000

**默认账号**:
- 用户名: `admin`
- 密码: `admin123`

---

### 四、前端商城启动

```bash
cd frontend-shop
npm install
npm run dev
```

**访问地址**: http://localhost:3001

**默认测试账号**:
- 用户名: `testuser`
- 密码: `user123`

或使用注册功能创建新账号

---

### 五、验证最小闭环

#### 方式 1：手动验证
1. 登录 testuser / user123
2. 浏览商品列表
3. 加购物车
4. 创建收货地址
5. 创建订单
6. 验证库存扣减

#### 方式 2：使用验证脚本（PowerShell）
```powershell
cd scripts
.\verify-minimal.ps1
```

---

### 六、服务地址汇总

| 服务 | 地址 | 说明 |
|------|------|------|
| 后端 API | http://localhost:8000 | FastAPI 服务 |
| API 文档 | http://localhost:8000/docs | Swagger UI |
| 管理后台 | http://localhost:3000 | Vue 3 + Element Plus |
| 前端商城 | http://localhost:3001 | Vue 3 |

---

### 七、常见问题

#### Q: 后端启动时提示端口被占用？
A: 修改启动命令的 `--port` 参数，或关闭占用 8000 端口的程序

#### Q: 数据库文件在哪？
A: SQLite 数据库文件在 `backend/shop_db.db`

#### Q: 如何重置数据库？
A: 删除 `backend/shop_db.db`，然后重新运行 `python scripts/init_db.py` 和 `python scripts/seed_data.py`

#### Q: npm install 很慢？
A: 可以使用淘宝镜像：`npm config set registry https://registry.npmmirror.com`
