# 浏览历史接口

本文档描述 ShamGP 商城浏览历史相关的所有 API 接口，基于真实代码生成。

> **代码位置**: `backend/app/api/v1/browse_history.py`  
> **路由前缀**: `/api/v1/browse-history`

---

## 记录浏览历史

记录或更新用户对某商品的浏览历史。同一用户对同一商品重复浏览时，**更新时间**而非创建新记录。

**请求**: `POST /api/v1/browse-history/browse`

**认证**: 必须登录（JWT）

### Query 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| product_id | integer | 是 | 商品 ID |

### 响应示例（200）

```json
{
  "code": 200,
  "message": "浏览记录已保存"
}
```

### 业务逻辑

1. 查询是否存在 `user_id + product_id` 相同的浏览记录
2. **如果已存在** → 用原生 SQL 更新 `browse_time = NOW()`（保留原记录）
3. **如果不存在** → 新建 `BrowseHistory` 记录

### 对应后端代码

- **路由**: `backend/app/api/v1/browse_history.py` — `POST /browse`

### 注意事项

- 当前接口**仅记录浏览**，无获取浏览历史列表的 API
- 未来可通过 `GET /browse-history` 扩展查询功能

---

## BrowseHistory 数据模型

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigInteger | 主键，自增 |
| user_id | Integer | 用户 ID（外键 → users） |
| product_id | Integer | 商品 ID（外键 → products） |
| browse_time | DateTime | 浏览时间（重复浏览时更新） |

### 索引

- `INDEX browse_histories(user_id)`
- `INDEX browse_histories(product_id)`

### 关联关系

```
User
└── browse_histories → BrowseHistory[]（一对多）

BrowseHistory
├── user → User（多对一）
└── product → Product（多对一）
```
