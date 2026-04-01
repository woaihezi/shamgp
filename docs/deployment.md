# 部署指南

本文档介绍如何将 ShamGP 商城项目部署到生产环境。

---

## 一、生产环境准备

### 1.1 服务器要求

**最低配置：**
- CPU: 2 核
- 内存: 4 GB
- 硬盘: 40 GB
- 操作系统: Ubuntu 20.04+ / CentOS 8+ / Windows Server 2019+

**推荐配置：**
- CPU: 4 核+
- 内存: 8 GB+
- 硬盘: 100 GB+ SSD
- 操作系统: Ubuntu 22.04 LTS

### 1.2 软件要求

- **Node.js**: 18.0+
- **Python**: 3.10+
- **数据库**: MySQL 8.0+ 或 PostgreSQL 13+
- **Web 服务器**: Nginx 1.18+
- **进程管理**: PM2 (Node.js) / Supervisor (Python)
- **SSL 证书**: Let's Encrypt (免费) 或商业证书

---

## 二、数据库部署

### 2.1 MySQL 部署

#### 2.1.1 安装 MySQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server -y
sudo mysql_secure_installation
```

**CentOS/RHEL:**
```bash
sudo yum install mysql-server -y
sudo systemctl start mysqld
sudo mysql_secure_installation
```

#### 2.1.2 创建数据库和用户

```sql
-- 登录 MySQL
sudo mysql -u root -p

-- 创建数据库
CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER 'shop_user'@'localhost' IDENTIFIED BY 'your_strong_password';

-- 授权
GRANT ALL PRIVILEGES ON shop_db.* TO 'shop_user'@'localhost';

-- 刷新权限
FLUSH PRIVILEGES;

-- 退出
EXIT;
```

#### 2.1.3 优化 MySQL 配置

编辑 `/etc/mysql/mysql.conf.d/mysqld.cnf`:

```ini
[mysqld]
# 字符集
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# 连接设置
max_connections = 200

# 缓存设置
innodb_buffer_pool_size = 2G
innodb_log_file_size = 256M

# 慢查询日志
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow-query.log
long_query_time = 2
```

重启 MySQL:
```bash
sudo systemctl restart mysql
```

### 2.2 PostgreSQL 部署（可选）

#### 2.2.1 安装 PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```

#### 2.2.2 创建数据库和用户

```bash
# 切换到 postgres 用户
sudo -u postgres psql

-- 创建数据库
CREATE DATABASE shop_db;

-- 创建用户
CREATE USER shop_user WITH PASSWORD 'your_strong_password';

-- 授权
GRANT ALL PRIVILEGES ON DATABASE shop_db TO shop_user;

-- 退出
\q
```

---

## 三、后端部署

### 3.1 上传代码

```bash
# 在服务器上
cd /var/www
git clone <repository-url> shamgp
cd shamgp
```

### 3.2 配置环境变量

复制 `.env.example` 为 `.env`:

```bash
cd backend
cp .env.example .env
```

编辑 `.env`:

```env
# 数据库配置
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=shop_user
DB_PASSWORD=your_strong_password
DB_NAME=shop_db

# JWT 密钥（生产环境必须修改！）
SECRET_KEY=your-production-secret-key-change-this-in-production

# 访问令牌过期时间（分钟）
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# 后端配置
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# 项目名称
PROJECT_NAME=ShamGP E-commerce
```

### 3.3 创建 Python 虚拟环境

```bash
cd /var/www/shamgp/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3.4 初始化数据库

```bash
# 激活虚拟环境
source venv/bin/activate

# 创建表
python scripts/init_db.py

# 插入初始数据
python scripts/seed_data.py
```

### 3.5 使用 Gunicorn 部署

安装 Gunicorn:
```bash
pip install gunicorn uvloop httptools
```

创建 Gunicorn 配置文件 `gunicorn_config.py`:

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 10000
max_requests_jitter = 1000
timeout = 30
keepalive = 2
preload_app = True
accesslog = "/var/log/shamgp/access.log"
errorlog = "/var/log/shamgp/error.log"
loglevel = "info"
```

创建日志目录:
```bash
sudo mkdir -p /var/log/shamgp
sudo chown www-data:www-data /var/log/shamgp
```

### 3.6 使用 Systemd 管理进程

创建 Systemd 服务文件 `/etc/systemd/system/shamgp-backend.service`:

```ini
[Unit]
Description=ShamGP Backend Service
After=network.target mysql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/shamgp/backend
Environment="PATH=/var/www/shamgp/backend/venv/bin"
ExecStart=/var/www/shamgp/backend/venv/bin/gunicorn app.main:app -c gunicorn_config.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
sudo systemctl daemon-reload
sudo systemctl enable shamgp-backend
sudo systemctl start shamgp-backend
sudo systemctl status shamgp-backend
```

---

## 四、前端部署

### 4.1 构建管理后台

```bash
cd /var/www/shamgp/frontend-admin
npm install
npm run build
```

构建产物在 `dist/` 目录。

### 4.2 构建前端商城

```bash
cd /var/www/shamgp/frontend-shop
npm install
npm run build
```

构建产物在 `dist/` 目录。

### 4.3 使用 PM2 管理（可选）

如果使用 SSR 或需要开发环境热重载，可以使用 PM2:

```bash
npm install -g pm2
```

创建 `ecosystem.config.js`:

```javascript
module.exports = {
  apps: [
    {
      name: 'shamgp-admin',
      script: 'npm',
      args: 'run preview',
      cwd: '/var/www/shamgp/frontend-admin',
      env: {
        NODE_ENV: 'production',
        PORT: 3000
      }
    },
    {
      name: 'shamgp-shop',
      script: 'npm',
      args: 'run preview',
      cwd: '/var/www/shamgp/frontend-shop',
      env: {
        NODE_ENV: 'production',
        PORT: 3001
      }
    }
  ]
}
```

启动:
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

---

## 五、Nginx 配置

### 5.1 安装 Nginx

```bash
sudo apt install nginx -y
```

### 5.2 配置反向代理

创建 Nginx 配置文件 `/etc/nginx/sites-available/shamgp`:

```nginx
upstream backend {
    server 127.0.0.1:8000;
}

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS 配置
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL 证书配置
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 日志
    access_log /var/log/nginx/shamgp-access.log;
    error_log /var/log/nginx/shamgp-error.log;

    # 前端商城
    location / {
        root /var/www/shamgp/frontend-shop/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 管理后台
    location /admin {
        alias /var/www/shamgp/frontend-admin/dist;
        index index.html;
        try_files $uri $uri/ /admin/index.html;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 静态文件缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        root /var/www/shamgp;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### 5.3 启用配置

```bash
# 创建符号链接
sudo ln -s /etc/nginx/sites-available/shamgp /etc/nginx/sites-enabled/

# 删除默认配置
sudo rm /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

---

## 六、SSL 证书配置

### 6.1 使用 Let's Encrypt 免费证书

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

Certbot 会自动配置 Nginx 的 SSL 设置。

---

## 七、防火墙配置

### 7.1 UFW (Ubuntu)

```bash
# 允许 SSH
sudo ufw allow 22/tcp

# 允许 HTTP 和 HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable
sudo ufw status
```

### 7.2 firewalld (CentOS)

```bash
# 允许 HTTP 和 HTTPS
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## 八、备份策略

### 8.1 数据库备份

创建备份脚本 `/var/www/shamgp/scripts/backup-db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/shamgp"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="shop_db"
DB_USER="shop_user"
DB_PASS="your_strong_password"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/shop_db_$DATE.sql.gz

# 保留最近 30 天的备份
find $BACKUP_DIR -name "shop_db_*.sql.gz" -mtime +30 -delete
```

添加执行权限:
```bash
chmod +x /var/www/shamgp/scripts/backup-db.sh
```

添加到 crontab:
```bash
sudo crontab -e
```

添加以下行（每天凌晨 2 点备份）:
```
0 2 * * * /var/www/shamgp/scripts/backup-db.sh
```

### 8.2 代码备份

```bash
# 使用 Git 版本控制
cd /var/www/shamgp
git add .
git commit -m "Backup $(date)"
git push origin main
```

---

## 九、监控和日志

### 9.1 日志查看

```bash
# 后端日志
sudo tail -f /var/log/shamgp/error.log
sudo tail -f /var/log/shamgp/access.log

# Nginx 日志
sudo tail -f /var/log/nginx/shamgp-access.log
sudo tail -f /var/log/nginx/shamgp-error.log

# Systemd 日志
sudo journalctl -u shamgp-backend -f
```

### 9.2 进程监控

```bash
# 后端服务状态
sudo systemctl status shamgp-backend

# PM2 状态（如果使用）
pm2 status

# Nginx 状态
sudo systemctl status nginx
```

---

## 十、性能优化

### 10.1 数据库优化

- 定期分析表: `ANALYZE TABLE;`
- 定期优化表: `OPTIMIZE TABLE;`
- 添加适当的索引
- 使用查询缓存

### 10.2 前端优化

- 启用 Gzip 压缩
- 使用 CDN 加速静态资源
- 图片懒加载
- 代码分割和按需加载

### 10.3 后端优化

- 使用 Redis 缓存
- 数据库连接池
- 异步任务处理（Celery）
- CDN 加速

---

## 十一、安全建议

1. **定期更新**: 保持系统和依赖包更新
2. **防火墙**: 只开放必要的端口
3. **SSH 安全**: 使用密钥认证，禁用密码登录
4. **数据库安全**: 限制远程访问，使用强密码
5. **文件权限**: 设置正确的文件权限
6. **定期备份**: 确保备份可用并定期测试
7. **HTTPS**: 强制使用 HTTPS
8. **监控**: 实时监控异常访问

---

## 十二、故障排查

### 12.1 后端服务无法启动

```bash
# 检查服务状态
sudo systemctl status shamgp-backend

# 查看日志
sudo journalctl -u shamgp-backend -n 50

# 检查端口占用
sudo netstat -tlnp | grep 8000
```

### 12.2 数据库连接失败

```bash
# 检查数据库状态
sudo systemctl status mysql

# 测试连接
mysql -u shop_user -p -h localhost shop_db

# 检查防火墙
sudo ufw status
```

### 12.3 Nginx 502 Bad Gateway

```bash
# 检查后端服务是否运行
sudo systemctl status shamgp-backend

# 检查 Nginx 配置
sudo nginx -t

# 查看 Nginx 错误日志
sudo tail -f /var/log/nginx/shamgp-error.log
```

---

*文档更新时间: 2026-04-01*
