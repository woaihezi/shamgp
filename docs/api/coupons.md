# 优惠券接口

本文档描述 ShamGP 商城优惠券相关的所有 API 接口，基于真实代码生成。

> **代码位置**: `backend/app/api/v1/coupons.py`  
> **路由前缀**: `/api/v1/coupons`

---

## 优惠券类型

| type 值 | 类型 | 说明 |
|---------|------|------|
| 1 | 满减券 | 满 X 减 Y（`满减金额` = Y，`门槛金额` = X） |
| 2 | 折扣券 | 直接打折（`折扣` = 折扣率，如 0.9 表示 9 折） |
| 3 | 无门槛券 | 无使用门槛（可直接抵扣） |

---

## 获取可领取的优惠券

获取当前可领取的优惠券列表（面向 C 端用户展示）。

**请求**: `GET /api/v1/coupons/available`

**认证**: 否（公开接口）

### 响应示例

```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "name": "新人满100减20",
      "code": "NEWBIE100",
      "type": 1,
      "满减金额": 20.00,
      "折扣": null,
      "门槛金额": 100.00,
      "total_count": 1000,
      "remain_count": 856,
      "per_user_limit": 1,
      "start_time": "2026-01-01T00:00:00",
      "end_time": "2026-12-31T23:59:59",
      "description": "仅限新人首次下单使用"
    },
    {
      "id": 2,
      "name": "9折折扣券",
      "code": "DISCOUNT10",
      "type": 2,
      "满减金额": 0,
      "折扣": 0.9,
      "门槛金额": 200.00,
      "total_count": 500,
      "remain_count": 320,
      "per_user_limit": 2,
      "start_time": null,
      "end_time": null,
      "description": "满200元可用9折"
    }
  ]
}
```

### 查询条件

返回满足以下**全部条件**的优惠券：

1. `status = 1`（已启用）
2. `remain_count > 0`（还有剩余库存）
3. `start_time IS NULL OR start_time <= NOW()`（已开始）
4. `end_time IS NULL OR end_time >= NOW()`（未过期）

### 对应后端代码

- **路由**: `backend/app/api/v1/coupons.py` — `GET /available`

---

## 领取优惠券

当前登录用户领取指定优惠券。

**请求**: `POST /api/v1/coupons/receive/{coupon_id}`

**认证**: 必须登录（JWT）

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| coupon_id | integer | 是 | 优惠券 ID |

### 响应示例（200 — 领取成功）

```json
{
  "code": 200,
  "message": "领取成功",
  "data": {
    "id": 15
  }
}
```

### 响应示例（400 — 优惠券不可用）

```json
{
  "code": 400,
  "message": "已领完"
}
```

或

```json
{
  "code": 400,
  "message": "您已领取过该优惠券（限领2张）"
}
```

或

```json
{
  "code": 400,
  "message": "优惠券已结束"
}
```

### 业务逻辑

1. **时间校验**：`start_time <= NOW() <= end_time`
2. **库存校验**：`remain_count > 0`，领取成功后 `-1`
3. **限领校验**：统计该用户已领取的该券数量 `>= per_user_limit` 则拒绝
4. **写入 UserCoupon**：创建用户-优惠券关联记录，`status = 0`（未使用）

### 对应后端代码

- **路由**: `backend/app/api/v1/coupons.py` — `POST /receive/{coupon_id}`

---

## 获取我的优惠券

获取当前用户已领取的全部优惠券。

**请求**: `GET /api/v1/coupons/my`

**认证**: 必须登录（JWT）

### 响应示例

```json
{
  "code": 200,
  "data": [
    {
      "id": 15,
      "coupon_id": 1,
      "name": "新人满100减20",
      "code": "NEWBIE100",
      "type": 1,
      "满减金额": 20.00,
      "折扣": null,
      "门槛金额": 100.00,
      "status": 0,
      "start_time": "2026-01-01T00:00:00",
      "end_time": "2026-12-31T23:59:59"
    }
  ]
}
```

### status 字段含义

| 值 | 说明 |
|----|------|
| 0 | 未使用 |
| 1 | 已使用 |
| 2 | 已过期 |

### 对应后端代码

- **路由**: `backend/app/api/v1/coupons.py` — `GET /my`

---

## 使用优惠券（结算时调用）

在用户提交订单结算时，将优惠券标记为已使用，并绑定到订单。

**请求**: `POST /api/v1/coupons/use`

**认证**: 必须登录（JWT）

### 请求体

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| coupon_id | integer | 是 | 用户优惠券记录 ID（`user_coupons.id`，不是 `coupon_id`） |
| order_id | integer | 是 | 关联的订单 ID |

### 响应示例（200）

```json
{
  "code": 200,
  "message": "优惠券已使用"
}
```

### 响应示例（400 — 优惠券不可用）

```json
{
  "code": 400,
  "message": "优惠券不可用"
}
```

### 业务逻辑

1. 验证 `user_coupon.id = coupon_id` 且属于当前用户且 `status = 0`（未使用）
2. 更新 `status = 1`（已使用）
3. 记录 `used_at = NOW()`
4. 记录 `order_id = order_id`（关联到订单）

### 实际结算流程

> **注意**：优惠券的实际金额扣减逻辑（满减/折扣计算）在当前代码中**尚未集成到订单创建流程**。`/use` 接口仅负责标记使用状态，订单金额计算时暂未自动应用优惠券优惠。实际扣减需在 `OrderService.create_order()` 中补充。

### 对应后端代码

- **路由**: `backend/app/api/v1/coupons.py` — `POST /use`

---

## 优惠券数据模型

### Coupon（优惠券规则表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigInteger | 主键，自增 |
| name | String(100) | 优惠券名称 |
| code | String(50) | 优惠券码（唯一） |
| type | SmallInteger | 类型：1满减 2折扣 3无门槛 |
| 满减金额 | Numeric(10,2) | 满减金额（满 X 减 Y 中的 Y） |
| 折扣 | Numeric(5,2) | 折扣率，如 0.9 表示 9 折 |
| 门槛金额 | Numeric(10,2) | 使用门槛（满 X 可用） |
| total_count | Integer | 发放总量，0 表示不限量 |
| remain_count | Integer | 剩余数量 |
| per_user_limit | Integer | 每人限领数量，默认 1 |
| start_time | DateTime | 开始时间（可空，表示立即生效） |
| end_time | DateTime | 结束时间（可空，表示永久有效） |
| status | SmallInteger | 状态：0禁用 1启用 |
| description | Text | 优惠券描述 |

### UserCoupon（用户-优惠券关联表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigInteger | 主键，自增 |
| user_id | Integer | 用户 ID（外键 → users） |
| coupon_id | BigInteger | 优惠券 ID（外键 → coupons） |
| status | SmallInteger | 状态：0未使用 1已使用 2已过期 |
| used_at | DateTime | 使用时间 |
| order_id | Integer | 关联订单 ID（订单创建后回填） |

### 关联关系

```
Coupon
└── user_coupons → UserCoupon[]（一对多）

User
└── user_coupons → UserCoupon[]（一对多）

UserCoupon
├── coupon → Coupon（多对一）
└── user → User（多对一）
```
