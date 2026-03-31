# 优惠券与结算流程

本文档描述 ShamGP 商城优惠券从发放到核销的完整流程，基于 `backend/app/models/coupon.py` 和 `backend/app/api/v1/coupons.py` 真实代码生成。

---

## 一、优惠券类型

| type值 | 类型 | 说明 | 计算方式 |
|--------|------|------|---------|
| 1 | 满减券 | 满X减Y | 满足门槛时直接减`满减金额` |
| 2 | 折扣券 | X折 | 满足门槛时价格 × `折扣` |
| 3 | 无门槛券 | 直减/包邮 | 不限门槛，直接减`满减金额` |

---

## 二、优惠券全生命周期

```
┌─────────────────────────────────────────┐
│  1. 管理员创建优惠券（后台）             │
│  coupons 表 INSERT                      │
└──────────────────┬──────────────────────┘
                   ↓
┌──────────────────▼──────────────────────┐
│  2. 用户领取优惠券                       │
│  POST /api/v1/coupons/receive/{id}     │
│  coupons.remain_count -= 1             │
│  user_coupons INSERT（status=0）        │
└──────────────────┬──────────────────────┘
                   ↓
┌──────────────────▼──────────────────────┐
│  3. 用户查看我的优惠券                   │
│  GET /api/v1/coupons/my                │
│  → 返回 user_coupons JOIN coupons       │
└──────────────────┬──────────────────────┘
                   ↓
┌──────────────────▼──────────────────────┐
│  4. 结算页选择优惠券                      │
│  前端根据门槛判断是否可叠加              │
│  实时计算优惠金额                        │
└──────────────────┬──────────────────────┘
                   ↓
┌──────────────────▼──────────────────────┐
│  5. 提交订单时使用优惠券                  │
│  POST /api/v1/orders（传入coupon_id）   │
│  优惠金额写入 order.discount_amount     │
│  user_coupons.status → 1（已使用）      │
│  user_coupons.order_id → 订单ID         │
└─────────────────────────────────────────┘
```

---

## 三、优惠券领取 API

### 获取可领取优惠券

**接口**: `GET /api/v1/coupons/available`

**后端逻辑**:
```python
条件：
- coupons.status == 1（已启用）
- coupons.remain_count > 0（还有库存）
- (coupons.start_time IS NULL OR <= 当前时间)
- (coupons.end_time IS NULL OR >= 当前时间)
排序：按门槛金额升序
```

### 领取优惠券

**接口**: `POST /api/v1/coupons/receive/{coupon_id}`

**后端逻辑**:
```
1. 校验优惠券是否存在
2. 校验时间（未开始/已结束）
3. 校验库存（remain_count > 0）
4. 校验用户限领（已有数量 < per_user_limit）
5. 执行：
   coupons.remain_count -= 1
   user_coupons INSERT（status=0）
```

**领取失败场景**:
| 错误 | code | 说明 |
|------|------|------|
| 优惠券不存在 | 404 | 已删除或ID错误 |
| 尚未开始 | 400 | `start_time > now` |
| 已结束 | 400 | `end_time < now` |
| 已领完 | 400 | `remain_count <= 0` |
| 超过限领 | 400 | `已有数量 >= per_user_limit` |

---

## 四、结算页优惠计算

### 前端计算规则

```typescript
function calcDiscount(subtotal: number, coupon: Coupon): number {
  if (coupon.type === 1) {
    // 满减：满门槛金额才可用
    if (subtotal >= coupon.门槛金额) {
      return Math.min(Number(coupon.满减金额), subtotal)
    }
  } else if (coupon.type === 2) {
    // 折扣：门槛为0或满足门槛
    if (coupon.门槛金额 === 0 || subtotal >= coupon.门槛金额) {
      return subtotal * (1 - Number(coupon.折扣))
    }
  } else if (coupon.type === 3) {
    // 无门槛直减
    return Number(coupon.满减金额)
  }
  return 0
}
```

### 应付金额计算

```
应付金额 = 商品总额 - 优惠金额 + 运费
```

---

## 五、优惠券使用 API

### 使用优惠券

**接口**: `POST /api/v1/coupons/use`

**请求**:
```json
{
  "coupon_id": 1,
  "order_id": 123
}
```

**后端逻辑**:
```python
1. 查找 user_coupons（id + user_id + status=0）
2. 校验是否可用
3. 更新：
   user_coupons.status = 1（已使用）
   user_coupons.used_at = NOW()
   user_coupons.order_id = order_id
```

---

## 六、数据表结构

### coupons（优惠券主表）

```sql
CREATE TABLE coupons (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100),           -- 名称
  code VARCHAR(50) UNIQUE,      -- 券码
  type SMALLINT,                -- 1满减 2折扣 3无门槛
  满减金额 DECIMAL(10,2),       -- 满减金额
  折扣 DECIMAL(5,2),            -- 折扣率
  门槛金额 DECIMAL(10,2),       -- 使用门槛
  total_count INTEGER,          -- 总量（0不限）
  remain_count INTEGER,         -- 剩余
  per_user_limit INTEGER,       -- 每人限领
  start_time DATETIME,
  end_time DATETIME,
  status SMALLINT,              -- 0禁用 1启用
  description TEXT
);
```

### user_coupons（用户优惠券表）

```sql
CREATE TABLE user_coupons (
  id INTEGER PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  coupon_id INTEGER REFERENCES coupons(id),
  status SMALLINT,             -- 0未使用 1已使用 2已过期
  used_at DATETIME,
  order_id INTEGER             -- 使用后关联订单
);
```

---

## 七、种子数据（当前）

| ID | 名称 | 码 | 类型 | 满减/折扣 | 门槛 | 剩余 |
|----|------|-----|------|-----------|------|------|
| 1 | 新人专享满减券 | NEWBIE01 | 满减 | ¥20 | ¥99 | 100 |
| 2 | 限时满减券 | LIMIT99 | 满减 | ¥30 | ¥199 | 50 |
| 3 | 无门槛立减券 | FREESHIP | 无门槛 | ¥10 | ¥0 | 200 |
| 4 | 节日大促满减 | FEST30 | 满减 | ¥50 | ¥299 | 30 |
| 5 | VIP专属折扣 | VIP10 | 折扣 | 9折 | ¥0 | 999 |

---

## 八、运费规则（当前状态）

**状态**: ⚠️ 固定 ¥0（未实现真实运费计算）

结算页目前显示"运费到付"，未按地区/重量计算。后续需新增 `shipping_rules` 表支持。

---

*本文档基于 `backend/app/models/coupon.py` 和 `backend/app/api/v1/coupons.py` 真实代码生成