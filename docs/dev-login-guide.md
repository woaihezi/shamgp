# 登录和用户认证指南

## 1. 概述

本指南介绍如何登录管理后台，以及用户认证的相关流程。

## 2. 账号信息

### 2.1 管理员账号

**账号：**
- 用户名：`admin`
- 密码：`admin123`
- 角色：系统管理员

**权限：**
- 访问管理后台所有页面
- 管理商品、订单、用户等
- 系统设置

### 2.2 测试用户账号

**账号：**
- 用户名：`testuser`
- 密码：`user123`
- 角色：普通用户

**用途：**
- 测试商城端功能
- 测试购物车和订单流程

## 3. 登录管理后台

### 3.1 启动服务

首先确保后端和前端服务都已启动：

**启动后端：**
```bash
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**启动前端管理后台：**
```bash
cd frontend-admin
npm install
npm run dev
```

### 3.2 访问登录页

在浏览器中打开：http://localhost:3000

如果未登录，会自动跳转到登录页：http://localhost:3000/login

### 3.3 登录步骤

1. 在登录页输入用户名和密码：
   - 用户名：`admin`
   - 密码：`admin123`

2. 点击"登录"按钮或按回车键

3. 登录成功后会自动跳转到管理后台首页

### 3.4 登录成功后

登录成功后：
- Token 会保存到 localStorage
- 自动获取用户信息
- 跳转到首页或之前尝试访问的页面
- 右上角显示用户昵称和头像

## 4. 认证流程详解

### 4.1 登录流程

```
用户输入账号密码
    ↓
前端调用 POST /api/v1/auth/login
    ↓
后端验证账号密码
    ↓
后端生成 JWT Token
    ↓
前端保存 Token 到 localStorage
    ↓
前端调用 GET /api/v1/auth/userinfo
    ↓
获取用户信息和权限
    ↓
登录完成，跳转到首页
```

### 4.2 Token 使用

登录成功后，前端会在每个 API 请求的 Header 中携带 Token：

```
Authorization: Bearer <access_token>
```

### 4.3 Token 有效期

默认配置：
- Token 有效期：7 天（60 * 24 * 7 分钟）
- 可在 `.env` 文件中修改 `ACCESS_TOKEN_EXPIRE_MINUTES` 配置

### 4.4 登出流程

1. 点击用户菜单中的"退出登录"
2. 前端调用 POST /api/v1/auth/logout
3. 清除 localStorage 中的 Token
4. 清除用户状态
5. 跳转到登录页

## 5. API 接口说明

### 5.1 登录接口

**接口：** `POST /api/v1/auth/login`

**请求体：**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

### 5.2 获取用户信息

**接口：** `GET /api/v1/auth/userinfo`

**请求头：**
```
Authorization: Bearer <access_token>
```

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "admin",
    "nickname": "系统管理员",
    "avatar": "",
    "email": "admin@shamgp.com",
    "phone": "13800138000",
    "roles": ["admin"],
    "permissions": []
  }
}
```

### 5.3 获取菜单树

**接口：** `GET /api/v1/auth/menu-tree`

**说明：** 获取当前用户有权限访问的菜单树

### 5.4 获取路由

**接口：** `GET /api/v1/auth/routers`

**说明：** 获取当前用户有权限访问的路由配置

### 5.5 登出

**接口：** `POST /api/v1/auth/logout`

## 6. 路由守卫

前端实现了路由守卫，自动处理登录状态：

### 6.1 未登录用户

- 访问 `/login` → 允许
- 访问其他页面 → 自动跳转到 `/login?redirect=<原路径>`

### 6.2 已登录用户

- 访问 `/login` → 自动跳转到 `/`
- 访问需要权限的页面 → 检查用户信息，如未获取则自动获取
- 如果 Token 失效 → 清除状态，跳转到登录页

## 7. 常见问题

### Q: 登录失败怎么办？
A: 
1. 确认后端服务已启动（http://localhost:8000）
2. 确认数据库已初始化并包含种子数据
3. 检查用户名和密码是否正确（admin/admin123）
4. 查看浏览器控制台的错误信息

### Q: 登录后刷新页面又要重新登录？
A: 
1. 检查 localStorage 中是否有 token
2. 确认 Token 未过期
3. 查看浏览器控制台是否有获取用户信息失败的错误

### Q: Token 存在但请求返回 401？
A: 
1. 确认 Token 格式正确（Bearer + 空格 + token）
2. 确认 Token 未过期
3. 尝试重新登录

### Q: 如何修改默认账号密码？
A: 
1. 修改 `backend/scripts/seed_data.py` 中的密码
2. 重新运行种子数据脚本
3. 或者直接在数据库中更新用户密码（需要使用 bcrypt 加密）

### Q: 菜单怎么配置？
A: 
- 当前最小闭环使用静态菜单（在路由配置中定义）
- 动态菜单功能尚未完全实现，需要在数据库中配置 menu 表
