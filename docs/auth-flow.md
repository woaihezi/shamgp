# ShamGP 商城项目 - 认证流程

**更新时间**: 2026-04-01

---

## 一、认证方式

项目使用 **JWT (JSON Web Token)** 进行认证。

---

## 二、后端认证流程

### 1. 登录获取 Token

**接口**: `POST /api/v1/auth/login`

**请求体**:
```json
{
  "username": "testuser",
  "password": "user123"
}
```

**响应**:
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

### 2. 使用 Token 访问受保护接口

在请求头中添加 Authorization:
```
Authorization: Bearer <access_token>
```

### 3. 后端鉴权依赖

- `get_current_user`: 获取当前用户（可能未激活）
- `get_current_active_user`: 获取当前激活用户（常用）

### 4. Token 过期时间

默认: 7 天 (10080 分钟)

可通过环境变量 `ACCESS_TOKEN_EXPIRE_MINUTES` 配置

---

## 三、前端商城 (frontend-shop) 认证流程

### 1. Token 存储

- 存储位置: `localStorage`
- 键名: `access_token`

### 2. 请求拦截器

文件: `frontend-shop/src/utils/request.ts`

自动在请求头中添加 Authorization:
```typescript
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

### 3. 响应拦截器

自动处理 401 未认证状态，跳转登录页

### 4. 登录流程

1. 用户输入用户名密码
2. 调用 `POST /api/v1/auth/login`
3. 将返回的 `access_token` 存入 localStorage
4. 跳转首页或目标页面

### 5. 登出流程

1. 调用 `POST /api/v1/auth/logout`（可选）
2. 清除 localStorage 中的 `access_token`
3. 跳转登录页

---

## 四、管理后台 (frontend-admin) 认证流程

### 1. Token 存储

- 存储位置: `localStorage`
- 键名: `access_token`（统一使用，不再使用 'token'）

### 2. 请求拦截器

文件: `frontend-admin/src/api/request.ts`

自动在请求头中添加 Authorization

### 3. 路由守卫

文件: `frontend-admin/src/router/index.ts`

检查 `localStorage.getItem('access_token')`，未登录则跳转登录页

### 4. Store (Pinia)

文件: `frontend-admin/src/stores/modules/user.ts`

管理用户登录状态和 Token

---

## 五、受保护接口清单

### 需要登录鉴权的接口

- `/api/v1/auth/userinfo`
- `/api/v1/auth/logout`
- `/api/v1/carts/*`
- `/api/v1/orders/*`（除公开商品外）
- `/api/v1/dashboard/*`
- `/api/v1/inventory/*`
- `/api/v1/users/*`（部分）

---

## 六、注意事项

1. **统一 Token 键名**: 全项目只使用 `access_token`，不再使用 `token`
2. **Bearer 前缀**: 请求头格式必须是 `Bearer <token>`，注意空格
3. **Token 安全**: 生产环境必须使用 HTTPS
4. **Secret Key**: 生产环境必须修改 `SECRET_KEY` 环境变量
