# 数据库运行手册

## 数据库类型支持

项目支持以下数据库：
- SQLite (默认，推荐用于开发)
- MySQL 8.0+
- PostgreSQL 13+

---

## 一、SQLite 初始化步骤（推荐）

SQLite 是最简单的方式，无需额外安装数据库服务。

### 1.1 配置环境变量
在项目根目录创建 `.env` 文件：
```env
DB_TYPE=sqlite
DB_NAME=./shop.db
```

### 1.2 初始化数据库表
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python scripts/init_db.py
```

### 1.3 填充测试数据
```bash
python scripts/seed_data.py
```

### 1.4 验证
数据库文件会自动创建在 `backend/shop.db`

---

## 二、MySQL 初始化步骤

### 2.1 启动 MySQL 服务
使用 Docker：
```bash
docker run --name shamgp-mysql -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=shop_db -p 3306:3306 -d mysql:8.0
```

或使用本地 MySQL，创建数据库：
```sql
CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2.2 配置环境变量
```env
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=shop_db
```

### 2.3 初始化和填充数据
```bash
cd backend
python scripts/init_db.py
python scripts/seed_data.py
```

---

## 三、PostgreSQL 初始化步骤

### 3.1 启动 PostgreSQL 服务
使用 Docker：
```bash
docker run --name shamgp-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=shop_db -p 5432:5432 -d postgres:15
```

### 3.2 配置环境变量
```env
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=shop_db
```

### 3.3 初始化和填充数据
```bash
cd backend
python scripts/init_db.py
python scripts/seed_data.py
```

---

## 四、Alembic 使用方式

### 4.1 创建新迁移
```bash
cd backend
alembic revision --autogenerate -m "description of change"
```

### 4.2 应用迁移
```bash
alembic upgrade head
```

### 4.3 回滚迁移
```bash
alembic downgrade -1  # 回滚上一个版本
alembic downgrade base  # 回滚所有
```

### 4.4 查看迁移历史
```bash
alembic history
```

---

## 五、Seed 顺序

正确的执行顺序：
1. `init_db.py` - 创建数据库表结构
2. `seed_data.py` - 填充测试数据（包括用户、分类、商品等）
3. `seed_rbac.py` - 填充 RBAC 权限数据（可选）

---

## 六、常见报错处理

### 6.1 ModuleNotFoundError
**错误**: `No module named 'app'`
**解决**: 确保在 backend 目录下运行，或者设置 PYTHONPATH
```bash
cd backend
set PYTHONPATH=.  # Windows
export PYTHONPATH=.  # Linux/Mac
```

### 6.2 数据库连接失败
**错误**: `Can't connect to MySQL server`
**解决**: 
- 检查数据库服务是否启动
- 检查 .env 配置是否正确
- 检查防火墙设置

### 6.3 表已存在错误
**错误**: `Table already exists`
**解决**: 删除数据库文件或清空数据库后重新运行 init_db.py

### 6.4 外键约束错误
**解决**: 确保 seed 顺序正确，先创建主表数据再创建从表数据

---

## 七、默认测试账号

初始化后可以使用以下账号登录：

**管理员账号**:
- 用户名: admin
- 密码: admin123

**测试用户账号**:
- 用户名: testuser
- 密码: user123
