# API 接口规范

## 1. 总体规范

### 1.1 API 版本管理
- 所有 API 路径以 `/api/v1/` 开头
- 后续版本递增：`/api/v2/`、`/api/v3/`
- 版本号仅在不兼容变更时升级

### 1.2 RESTful 设计原则
- 使用标准 HTTP 方法：GET、POST、PUT、PATCH、DELETE
- 资源使用名词复数形式
- 使用路径参数和查询参数
- 使用 HTTP 状态码表示响应状态

### 1.3 路径规范

#### 后台管理 API
```
/api/v1/admin/{resource}
```

#### 商城 API
```
/api/v1/shop/{resource}
```

#### 示例路径
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/admin/users | 获取用户列表 |
| GET | /api/v1/admin/users/{id} | 获取用户详情 |
| POST | /api/v1/admin/users | 创建用户 |
| PUT | /api/v1/admin/users/{id} | 更新用户 |
| DELETE | /api/v1/admin/users/{id} | 删除用户 |
| PATCH | /api/v1/admin/users/{id}/status | 更新用户状态 |

---

## 2. 统一响应格式

### 2.1 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": 1699999999999
}
```

### 2.2 分页响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "total_pages": 5
  },
  "timestamp": 1699999999999
}
```

### 2.3 错误响应

```json
{
  "code": 400,
  "message": "参数错误",
  "errors": [
    {
      "field": "username",
      "message": "用户名不能为空"
    }
  ],
  "timestamp": 1699999999999
}
```

### 2.4 状态码规范

| HTTP 状态码 | code | 说明 |
|-------------|------|------|
| 200 | 200 | 成功 |
| 400 | 400 | 请求参数错误 |
| 401 | 401 | 未登录/Token 过期 |
| 403 | 403 | 无权限 |
| 404 | 404 | 资源不存在 |
| 409 | 409 | 资源冲突 |
| 422 | 422 | 数据验证失败 |
| 500 | 500 | 服务器内部错误 |

---

## 3. 请求参数规范

### 3.1 分页参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|-------|------|------|--------|------|
| page | int | 否 | 1 | 页码 |
| page_size | int | 否 | 20 | 每页数量，最大 100 |
| order_by | string | 否 | created_at | 排序字段 |
| order_dir | string | 否 | desc | 排序方向：asc, desc |

### 3.2 搜索参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|-------|------|------|--------|------|
| keyword | string | 否 | | 关键词搜索 |
| status | int | 否 | | 状态筛选 |
| start_date | string | 否 | | 开始日期 (YYYY-MM-DD) |
| end_date | string | 否 | | 结束日期 (YYYY-MM-DD) |

### 3.3 日期时间格式
- 请求格式：`YYYY-MM-DD HH:mm:ss` 或 `YYYY-MM-DD`
- 响应格式：ISO 8601，如 `2023-11-11T11:11:11Z`

---

## 4. 认证与授权

### 4.1 JWT 认证
- 使用 Bearer Token 方式
- Token 放在 Header 中：`Authorization: Bearer {token}`

### 4.2 Token 刷新
- Access Token 有效期：2 小时
- Refresh Token 有效期：7 天
- 刷新接口：`POST /api/v1/shop/auth/refresh`

### 4.3 权限控制
- 基于角色的权限控制 (RBAC)
- 权限码格式：`模块:操作`，如 `user:create`、`product:update`

---

## 5. 核心 API 接口定义

### 5.1 认证模块

#### 用户登录
```
POST /api/v1/shop/auth/login
Content-Type: application/json

Request:
{
  "username": "string",
  "password": "string"
}

Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "access_token": "string",
    "refresh_token": "string",
    "token_type": "bearer",
    "expires_in": 7200,
    "user": {
      "id": 1,
      "username": "string",
      "nickname": "string",
      "avatar": "string"
    }
  }
}
```

#### 刷新 Token
```
POST /api/v1/shop/auth/refresh
Content-Type: application/json

Request:
{
  "refresh_token": "string"
}

Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "access_token": "string",
    "expires_in": 7200
  }
}
```

---

### 5.2 用户管理模块

#### 获取用户列表
```
GET /api/v1/admin/users?page=1&page_size=20&keyword=xxx&status=1

Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "username": "string",
        "email": "string",
        "phone": "string",
        "nickname": "string",
        "avatar": "string",
        "status": 1,
        "created_at": "2023-11-11T11:11:11Z"
      }
    ],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "total_pages": 5
  }
}
```

#### 创建用户
```
POST /api/v1/admin/users
Content-Type: application/json

Request:
{
  "username": "string",
  "password": "string",
  "email": "string",
  "phone": "string",
  "nickname": "string",
  "role_ids": [1, 2]
}
```

---

### 5.3 商品管理模块

#### 获取商品列表
```
GET /api/v1/admin/products?page=1&page_size=20&category_id=1&status=1

Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "name": "string",
        "cover_image": "string",
        "price": 99.99,
        "original_price": 199.99,
        "stock": 100,
        "sales": 50,
        "status": 1,
        "created_at": "2023-11-11T11:11:11Z"
      }
    ],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
}
```

#### 商城商品列表
```
GET /api/v1/shop/products?page=1&page_size=20&category_id=1&keyword=xxx&sort=sales
```

---

### 5.4 订单管理模块

#### 创建订单
```
POST /api/v1/shop/orders
Content-Type: application/json

Request:
{
  "address_id": 1,
  "cart_item_ids": [1, 2, 3],
  "remark": "string"
}

Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "order_id": 1,
    "order_no": "ORDER202311110001",
    "total_amount": 299.97
  }
}
```

#### 获取订单详情
```
GET /api/v1/shop/orders/{id}

Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "order_no": "ORDER202311110001",
    "status": 0,
    "total_amount": 299.97,
    "pay_amount": 299.97,
    "consignee_name": "string",
    "consignee_phone": "string",
    "consignee_address": "string",
    "items": [
      {
        "id": 1,
        "product_name": "string",
        "product_image": "string",
        "price": 99.99,
        "quantity": 3,
        "total_amount": 299.97
      }
    ],
    "created_at": "2023-11-11T11:11:11Z"
  }
}
```

---

### 5.5 购物车模块

#### 获取购物车列表
```
GET /api/v1/shop/cart

Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "product_id": 1,
        "product_name": "string",
        "product_image": "string",
        "sku_specs": "string",
        "price": 99.99,
        "quantity": 2,
        "selected": true
      }
    ],
    "selected_total": 199.98
  }
}
```

#### 添加购物车
```
POST /api/v1/shop/cart
Content-Type: application/json

Request:
{
  "product_id": 1,
  "sku_id": 1,
  "quantity": 2
}
```

---

## 6. 文件上传

### 6.1 单文件上传
```
POST /api/v1/admin/files/upload
Content-Type: multipart/form-data

Request:
file: [binary]

Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "url": "https://example.com/uploads/xxx.jpg",
    "name": "xxx.jpg",
    "size": 102400
  }
}
```

### 6.2 多文件上传
```
POST /api/v1/admin/files/upload/batch
Content-Type: multipart/form-data

Request:
files: [binary1, binary2, ...]
```

---

## 7. 接口分层设计

### 7.1 后端分层

```
┌─────────────────────────────────┐
│   API Router Layer (routers)    │  路由层：处理请求参数
├─────────────────────────────────┤
│  Service Layer (services)        │  业务层：处理业务逻辑
├─────────────────────────────────┤
│  Repository Layer (models)       │  数据层：数据库操作
├─────────────────────────────────┤
│    Database (PostgreSQL)         │  数据库
└─────────────────────────────────┘
```

### 7.2 分层职责

#### Router 层
- 参数接收与验证
- 调用 Service 层
- 返回统一响应格式
- 不包含业务逻辑

#### Service 层
- 业务逻辑处理
- 事务控制
- 调用 Repository 层
- 跨表操作

#### Repository 层
- 单表 CRUD 操作
- 复杂查询
- 不包含业务逻辑

---

## 8. 错误码定义

### 8.1 通用错误码
| code | message | 说明 |
|------|---------|------|
| 200 | success | 成功 |
| 400 | 请求参数错误 | 参数验证失败 |
| 401 | 未登录或 Token 已过期 | 需要重新登录 |
| 403 | 无权限操作 | 权限不足 |
| 404 | 资源不存在 | 记录未找到 |
| 409 | 资源已存在 | 唯一键冲突 |
| 500 | 服务器内部错误 | 系统异常 |

### 8.2 业务错误码
| code | message | 说明 |
|------|---------|------|
| 1001 | 用户名或密码错误 | 登录失败 |
| 1002 | 用户已被禁用 | 账户状态异常 |
| 2001 | 商品库存不足 | 下单失败 |
| 2002 | 订单已支付 | 重复支付 |
| 2003 | 订单状态不允许此操作 | 状态流转错误 |
| 3001 | 购物车商品不存在 | 操作无效 |
