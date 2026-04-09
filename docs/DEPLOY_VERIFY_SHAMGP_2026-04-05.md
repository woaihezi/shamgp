# shamgp 部署验证报告（2026-04-05）

## 部署前检查清单
1. 必填环境变量（真实值）：
- `SECRET_KEY`：至少 32 位随机字符串，例如 `SHAMGP_SECRET_32PLUS_RANDOM_STRING_2026`
- `CORS_ORIGINS`：逗号分隔白名单，例如 `http://localhost:3000,http://localhost:3001`
- `CORS_ALLOW_CREDENTIALS`：`true` 或 `false`（若跨域携带 Cookie/认证头通常设 `true`）
2. 本机必须满足：
- Docker Desktop 已启动（若走容器验证）
- Python 运行环境可用（若走本地验证）
- 8000 端口可用

## 本轮验证结果
1. 配置安全校验（临时环境变量实例化 `Settings`）：通过
2. Dockerfile 构建验证：失败（Docker 引擎未连接）
3. 8000 端口探测：未运行（`False`）

## 当前完成度
- 安全配置收敛（CORS/JWT）：已完成
- 本地部署前配置可控性：已达到
- 容器部署执行：被 Docker 引擎状态阻塞

## 最小启动命令
```powershell
# 方式 A：本地直接启动（推荐先做）
cd C:\Users\Make\Desktop\shamgp\backend
$env:SECRET_KEY="<YOUR_32_PLUS_RANDOM_SECRET_KEY>"
$env:CORS_ORIGINS="http://localhost:3000,http://localhost:3001"
$env:CORS_ALLOW_CREDENTIALS="true"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 方式 B：容器构建（需 Docker 引擎在线）
cd C:\Users\Make\Desktop\shamgp
docker build -f Dockerfile -t shamgp-backend:latest .
```

## smoke test 命令
```powershell
curl.exe -s -o NUL -w "HEALTH HTTP=%{http_code} TIME=%{time_total}`n" http://127.0.0.1:8000/health
curl.exe -s -o NUL -w "DOCS HTTP=%{http_code} TIME=%{time_total}`n" http://127.0.0.1:8000/docs
```

## 成功标准
1. 应用可在 8000 正常启动
2. `/health` 返回 `200`
3. CORS 生效为白名单，不再出现 `allow_origins=["*"]`
4. `SECRET_KEY` 校验通过（无弱密钥报错）

## 失败排查顺序
1. 检查 `SECRET_KEY` 长度与占位值问题
2. 检查 `CORS_ORIGINS` 是否为空或包含 `*`
3. 检查 `CORS_ALLOW_CREDENTIALS` 值是否合法
4. 检查 8000 端口占用与启动日志
5. 若走容器路径，确认 Docker Desktop 在线

## 仍需手工补的变量
- `SECRET_KEY`
- `CORS_ORIGINS`
- `CORS_ALLOW_CREDENTIALS`
