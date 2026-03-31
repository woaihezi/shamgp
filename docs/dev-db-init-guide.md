# 开发环境数据库初始化指南

## 1. 概述

本指南介绍如何在开发环境中初始化数据库，包括创建表结构和插入测试数据。

## 2. 数据库配置

### 2.1 默认配置

项目默认使用 **SQLite** 作为开发数据库，配置如下：

```env
# .env 文件
DB_TYPE=sqlite
DB_NAME=shop_db
```

SQLite 数据库文件将存储在：`backend/shop_db.db`

### 2.2 切换到其他数据库

如需使用 PostgreSQL 或 MySQL，修改 `.env` 文件：

**PostgreSQL:**
```env
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=shop_db
```

**MySQL:**
```env
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=shop_db
```

## 3. 初始化步骤

### 3.1 准备 Python 环境

首先，确保你在 backend 目录下，并已创建虚拟环境：

```bash
cd backend

# 创建虚拟环境（如果还没有）
python -m venv venv

# 激活虚拟环境
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3.2 创建数据库表

运行初始化脚本创建所有数据库表：

```bash
python scripts/init_db.py
```

成功后会看到：
```
Creating database tables...
Database tables created successfully!
```

### 3.3 插入种子数据

运行种子数据脚本，插入测试数据：

```bash
python scripts/seed_data.py
```

成功后会看到：
```
Seeding data...
Data seeded successfully!

Default admin account:
  Username: admin
  Password: admin123

Test user account:
  Username: testuser
  Password: user123
```

## 4. 种子数据内容

种子数据脚本会创建以下内容：

### 4.1 用户数据

**管理员账号：**
- 用户名：admin
- 密码：admin123
- 角色：系统管理员
- 邮箱：admin@shamgp.com

**测试用户账号：**
- 用户名：testuser
- 密码：user123
- 角色：普通用户
- 邮箱：test@shamgp.com

### 4.2 商品分类

1. 数码产品 (digital)
2. 服装鞋帽 (clothing)
3. 食品饮料 (food)

### 4.3 商品数据

| 商品名称 | 分类 | 价格 | 库存 | 状态 |
|---------|------|------|------|------|
| iPhone 15 Pro Max | 数码产品 | 9999.00 | 100 | 上架 |
| MacBook Pro 14" | 数码产品 | 14999.00 | 50 | 上架 |
| 经典款运动鞋 | 服装鞋帽 | 599.00 | 200 | 上架 |
| 纯棉休闲T恤 | 服装鞋帽 | 129.00 | 300 | 上架 |
| 有机坚果礼盒 | 食品饮料 | 268.00 | 80 | 上架 |
| 进口咖啡豆 | 食品饮料 | 168.00 | 120 | 上架 |

### 4.4 购物车数据

测试用户的购物车包含：
- iPhone 15 Pro Max × 1
- 经典款运动鞋 × 2

### 4.5 订单数据

测试用户有一个已完成的订单：
- 订单号：ORD202503310001
- 商品：经典款运动鞋 × 2
- 总价：1199.00
- 状态：已完成

## 5. 重置数据库

如需重置数据库，删除数据库文件并重新运行初始化脚本：

```bash
# 删除 SQLite 数据库文件
del shop_db.db  # Windows
rm shop_db.db   # Linux/Mac

# 重新初始化
python scripts/init_db.py
python scripts/seed_data.py
```

## 6. 验证数据库

可以使用 SQLite 工具直接查看数据库：

```bash
# 使用 sqlite3 命令行工具
sqlite3 shop_db.db

# 查询用户表
SELECT * FROM users;

# 查询商品表
SELECT * FROM products;

# 退出
.quit
```

或者使用 DB Browser for SQLite 等图形化工具打开 `shop_db.db` 文件。

## 7. 常见问题

### Q: 初始化时报错 "No module named 'xxx'"
A: 确保已激活虚拟环境并安装了所有依赖：`pip install -r requirements.txt`

### Q: 数据库文件在哪里？
A: SQLite 数据库文件位于 `backend/shop_db.db`

### Q: 如何切换到 PostgreSQL？
A: 修改 `.env` 文件中的 `DB_TYPE` 为 `postgresql`，并配置相应的连接信息

### Q: 种子数据可以修改吗？
A: 可以，编辑 `backend/scripts/seed_data.py` 文件来自定义测试数据
