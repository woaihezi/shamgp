# 常见问题 FAQ

本文档收集了 ShamGP 商城项目开发和使用过程中的常见问题及解决方案。

---

## 一、安装和环境问题

### Q1: Python 版本不兼容怎么办？

**A:** 项目要求 Python 3.10 或更高版本。

**检查版本：**
```bash
python --version
```

**解决方案：**
- Windows: 从 [python.org](https://www.python.org/) 下载最新版本
- Linux/Mac: 使用 pyenv 或 conda 管理多个 Python 版本
- 使用 Python 3.10+ 的虚拟环境

---

### Q2: Node.js 版本不兼容怎么办？

**A:** 项目要求 Node.js 18.0 或更高版本。

**检查版本：**
```bash
node --version
```

**解决方案：**
- Windows/Mac: 从 [nodejs.org](https://nodejs.org/) 下载最新 LTS 版本
- Linux: 使用 nvm (Node Version Manager)
  ```bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
  nvm install 18
  nvm use 18
  ```

---

### Q3: pip install 失败怎么办？

**A:** 可能的原因和解决方案：

**1. 网络问题**
```bash
# 使用清华镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用阿里镜像源
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

**2. 权限问题（Linux/Mac）**
```bash
# 使用 --user 参数
pip install --user -r requirements.txt

# 或使用 sudo（不推荐）
sudo pip install -r requirements.txt
```

**3. 升级 pip**
```bash
pip install --upgrade pip
```

---

### Q4: npm install 失败怎么办？

**A:** 可能的原因和解决方案：

**1. 网络问题**
```bash
# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com
npm install

# 或临时使用镜像
npm install --registry=https://registry.npmmirror.com
```

**2. 清理缓存重新安装**
```bash
# 删除 node_modules 和 lock 文件
rm -rf node_modules package-lock.json
# Windows
rmdir /s /q node_modules
del package-lock.json

# 重新安装
npm install
```

**3. 使用 cnpm 或 yarn**
```bash
# 使用 cnpm
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install

# 或使用 yarn
npm install -g yarn
yarn install
```

---

## 二、后端问题

### Q5: 后端启动失败，提示 "No module named 'app'"

**A:** 确保在正确的目录下运行命令。

**正确的启动方式：**
```bash
cd backend
# 激活虚拟环境
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 方式1: 使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 方式2: 使用启动脚本（Windows）
python run_server.ps1
```

---

### Q6: 数据库连接失败怎么办？

**A:** 根据使用的数据库类型检查：

**SQLite（默认）:**
```bash
# 确保数据库文件存在
cd backend
ls -la shop_db.db  # Linux/Mac
dir shop_db.db     # Windows

# 如果不存在，重新初始化
python scripts/init_db.py
python scripts/seed_data.py
```

**MySQL/PostgreSQL:**
1. 检查数据库服务是否启动
2. 检查 `.env` 文件中的数据库配置
3. 确认用户名和密码正确
4. 确认数据库已创建

**测试连接（MySQL）:**
```bash
mysql -u your_user -p -h localhost shop_db
```

---

### Q7: 提示 "Secret key must be set"

**A:** 确保 `.env` 文件存在并配置了 `SECRET_KEY`。

```bash
cd backend
# 检查 .env 文件是否存在
ls -la .env  # Linux/Mac
dir .env     # Windows

# 如果不存在，从示例复制
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# 编辑 .env，设置 SECRET_KEY
SECRET_KEY=your-secret-key-here-change-in-production
```

---

### Q8: CORS 跨域问题

**A:** 后端已经配置了 CORS，允许所有来源。如果仍有问题：

**检查后端配置：**
`backend/app/main.py` 中已有：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**前端检查：**
确保 `vite.config.ts` 中的 proxy 配置正确。

---

## 三、前端问题

### Q9: 前端启动失败，提示 "port already in use"

**A:** 修改端口或关闭占用端口的程序。

**查找占用端口的程序：**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <进程ID> /F

# Linux/Mac
lsof -i :3000
kill -9 <进程ID>
```

**或修改前端端口：**

编辑 `vite.config.ts`:
```typescript
export default defineConfig({
  server: {
    port: 3002,  // 修改为其他端口
  }
})
```

或使用命令行参数：
```bash
npm run dev -- --port 3002
```

---

### Q10: 前端无法连接后端 API

**A:** 检查以下几点：

**1. 确保后端已启动**
```bash
# 测试后端
curl http://localhost:8000/health
```

**2. 检查 Vite proxy 配置**

编辑 `frontend-admin/vite.config.ts` 或 `frontend-shop/vite.config.ts`:
```typescript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path
      }
    }
  }
})
```

**3. 检查浏览器控制台**
- 打开 F12 开发者工具
- 查看 Network 标签页
- 确认请求的 URL 是否正确

---

### Q11: 前端页面空白或报错

**A:** 常见原因和解决方案：

**1. 清除浏览器缓存**
- 按 Ctrl+Shift+R (Windows/Linux) 或 Cmd+Shift+R (Mac) 强制刷新

**2. 检查控制台错误**
- 打开 F12 开发者工具
- 查看 Console 标签页的错误信息

**3. 重新构建依赖**
```bash
rm -rf node_modules package-lock.json
npm install
```

**4. 检查路由配置**
确认 `src/router/index.ts` 中的路由配置正确。

---

## 四、数据库问题

### Q12: 如何重置数据库？

**A:** 删除数据库文件并重新初始化：

**SQLite:**
```bash
cd backend
# 删除数据库文件
del shop_db.db  # Windows
rm shop_db.db   # Linux/Mac

# 重新初始化
python scripts/init_db.py
python scripts/seed_data.py
```

**MySQL:**
```sql
DROP DATABASE shop_db;
CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

然后重新运行初始化脚本。

---

### Q13: 如何修改测试数据？

**A:** 编辑种子数据脚本：

```bash
cd backend
# 编辑种子数据脚本
notepad scripts/seed_data.py  # Windows
nano scripts/seed_data.py     # Linux/Mac
```

修改后重新运行：
```bash
python scripts/seed_data.py
```

---

### Q14: 数据库表不存在怎么办？

**A:** 运行初始化脚本创建表：

```bash
cd backend
python scripts/init_db.py
```

如果仍有问题，检查：
1. `backend/app/models/__init__.py` 是否导出了所有模型
2. `backend/scripts/init_db.py` 是否正确导入了所有模型

---

## 五、认证和权限问题

### Q15: 登录失败怎么办？

**A:** 检查以下几点：

**1. 确认账号密码正确**
- 管理员: admin / admin123
- 测试用户: testuser / user123

**2. 检查用户是否存在**
```bash
cd backend
sqlite3 shop_db.db
SELECT id, username, status FROM users;
.quit
```

**3. 重置用户密码**
```python
# 在 Python 中
from app.core.security import get_password_hash
print(get_password_hash("new_password"))
```

然后更新数据库中的密码哈希。

---

### Q16: Token 过期怎么办？

**A:** Token 默认 7 天过期。重新登录获取新 Token。

**延长 Token 有效期：**
编辑 `.env` 文件：
```env
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7天，单位分钟
```

---

### Q17: 提示 "Not authenticated"

**A:** 确保请求中包含正确的 Authorization header：

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**检查前端：**
确认 `src/utils/request.ts` 或 `src/api/request.ts` 中正确设置了请求拦截器。

---

## 六、开发和调试问题

### Q18: 如何查看后端日志？

**A:** 根据启动方式不同：

**使用 uvicorn 直接启动：**
日志会直接输出到终端。

**使用 Systemd 管理（生产环境）：**
```bash
sudo journalctl -u shamgp-backend -f
```

**查看应用日志：**
```bash
tail -f /var/log/shamgp/error.log
tail -f /var/log/shamgp/access.log
```

---

### Q19: 如何调试 Python 代码？

**A:** 使用 print 语句或调试器：

**1. 使用 print（简单）**
```python
print("Debug info:", variable)
```

**2. 使用 pdb 调试器**
```python
import pdb
pdb.set_trace()  # 在这行断点
```

**3. 使用 VS Code 调试**
创建 `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "jinja": true,
      "justMyCode": true
    }
  ]
}
```

---

### Q20: 如何调试前端代码？

**A:** 使用浏览器开发者工具：

**1. 打开开发者工具**
- Windows/Linux: F12 或 Ctrl+Shift+I
- Mac: Cmd+Option+I

**2. 使用 debugger 语句**
在代码中添加：
```typescript
debugger;  // 执行到这里会断点
```

**3. 使用 VS Code 调试**
创建 `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch Chrome against localhost",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend-admin/src"
    }
  ]
}
```

---

## 七、性能问题

### Q21: 后端响应慢怎么办？

**A:** 可能的优化方案：

**1. 数据库优化**
- 添加适当的索引
- 优化查询语句
- 使用查询缓存

**2. 使用 Redis 缓存**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_products():
    # ...
```

**3. 使用异步 I/O**
确保使用异步 SQLAlchemy 和异步端点。

---

### Q22: 前端加载慢怎么办？

**A:** 优化方案：

**1. 启用 Gzip 压缩**
在 Nginx 配置中添加：
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

**2. 使用 CDN**
将静态资源上传到 CDN。

**3. 代码分割和懒加载**
```typescript
const Home = () => import('./views/Home.vue')
```

**4. 图片优化**
- 使用 WebP 格式
- 图片懒加载
- 使用适当的尺寸

---

## 八、部署问题

### Q23: 生产环境和开发环境有什么区别？

**A:** 主要区别：

| 项目 | 开发环境 | 生产环境 |
|------|---------|---------|
| 数据库 | SQLite | MySQL/PostgreSQL |
| 调试 | 启用 | 禁用 |
| 日志 | 详细 | 精简 |
| 错误显示 | 显示详情 | 隐藏详情 |
| HTTPS | 可选 | 必需 |
| 性能优化 | 不优化 | 优化 |

---

### Q24: 如何备份数据？

**A:** 定期备份数据库：

**MySQL 备份：**
```bash
mysqldump -u user -p shop_db | gzip > backup_$(date +%Y%m%d).sql.gz
```

**恢复：**
```bash
gunzip < backup_20240101.sql.gz | mysql -u user -p shop_db
```

**自动化备份：**
使用 cron 定时任务（Linux）或任务计划程序（Windows）。

---

### Q25: 如何升级项目版本？

**A:** 升级步骤：

```bash
# 1. 备份数据
# 2. 拉取最新代码
git pull origin main

# 3. 更新依赖
cd backend
pip install -r requirements.txt
cd ../frontend-admin
npm install
cd ../frontend-shop
npm install

# 4. 运行数据库迁移
cd ../backend
alembic upgrade head  # 如果使用 Alembic

# 5. 重启服务
sudo systemctl restart shamgp-backend
```

---

## 九、其他问题

### Q26: 项目可以商用吗？

**A:** 查看项目的 LICENSE 文件。本项目使用 MIT 许可证，可以自由使用、修改和商用。

---

### Q27: 如何贡献代码？

**A:** 贡献流程：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

### Q28: 在哪里寻求帮助？

**A:** 获取帮助的渠道：

1. 查看本文档的 FAQ
2. 查看项目的 Issue 列表
3. 在 GitHub 上提交 Issue
4. 联系项目维护者

---

### Q29: 有没有视频教程？

**A:** 目前没有官方视频教程，但可以参考：
- FastAPI 官方文档
- Vue 3 官方文档
- 项目的 README 和文档目录

---

### Q30: 如何自定义主题和样式？

**A:** 根据项目不同：

**管理后台（Element Plus）:**
编辑 `frontend-admin/src/styles/index.scss`，覆盖 Element Plus 的 CSS 变量。

**前端商城:**
编辑 `frontend-shop/src/styles/index.css`，自定义样式。

---

*文档更新时间: 2026-04-01*
