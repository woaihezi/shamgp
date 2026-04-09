# shamgp P0 修复报告（2026-04-05）

## 1. 修改文件清单
- `backend/app/core/config.py`
- `backend/app/main.py`
- `.env.example`
- `README.md`
- `Dockerfile`（新增）

## 2. 修改原因
- CORS P0 修复：
1. 移除 `allow_origins=["*"]`。
2. 改为从环境变量 `CORS_ORIGINS` 读取白名单。
3. 增加校验：`CORS_ORIGINS` 不能为空且禁止 `*`。
4. `allow_credentials` 改为读取 `CORS_ALLOW_CREDENTIALS`，避免配置不一致。
- JWT P0 修复：
1. `SECRET_KEY` 改为必须由环境变量提供（不再使用代码内弱默认值）。
2. 增加弱密钥与长度校验（至少 32 位）。
- 部署可用性：
1. 新增后端可运行 Dockerfile。
- 文档示例：
1. `.env.example` 增加开发/生产 CORS 示例和 SECRET_KEY 强密钥说明。

## 3. 风险说明
- 启动行为变更：未设置强 `SECRET_KEY` 或 CORS 配置非法（含 `*`）时会启动失败，这是预期的安全阻断。
- 若现网仍依赖通配符跨域，需要先补齐真实来源白名单再发布。

## 4. 验证命令
```powershell
python -m py_compile backend/app/core/config.py backend/app/main.py

# 镜像构建（在项目根目录）
docker build -f Dockerfile -t shamgp-backend:latest .

# 本地运行前建议先设置：
# SECRET_KEY, CORS_ORIGINS, CORS_ALLOW_CREDENTIALS
```

## 5. 未完成项
- 需手工设置真实环境变量：
1. `SECRET_KEY`（至少 32 位随机字符串）
2. `CORS_ORIGINS`（真实前端域名白名单）
3. `CORS_ALLOW_CREDENTIALS`（按是否携带 Cookie/认证头设置 true/false）
