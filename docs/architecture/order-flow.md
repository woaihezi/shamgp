# 下单与库存扣减流程

本文档描述 ShamGP 商城从浏览商品到完成订单的完整业务流程，基于 `backend/app/services/` 真实代码生成。

---

## 一、整体流程图

```
┌─────────────────────────┐
│  1. 浏览商品 → 商品详情   │
│  （写入浏览历史）         │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  2. 选择 SKU → 加入购物车 │
│  POST /api/v1/carts/items│
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  3. 购物车 → 结算页      │
│  GET /api/v1/carts/items │
│  （获取购物车商品列表）   │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  4. 选择收货地址         │
│  /api/v1/orders/addresses│
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  5. 选择优惠券（可选）    │
│  GET /api/v1/coupons/my  │
│  结算金额 = 商品-优惠+运费 │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  6. 提交订单             │
│  POST /api/v1/orders    │
│  （冻结库存/创建订单/扣减）│
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  7. 订单状态流转         │
│  待支付→已支付→已发货    │
│  →已完成/已取消         │
└─────────────────────────┘
```

---

## 二、详细步骤说明

### 步骤1：浏览商品

**前端**: `ProductDetail.vue` 加载时调用
**后端**: 无需专门接口（静默写入浏览历史）

浏览历史通过 `POST /api/v1/products/browse` 写入 `browse_histories` 表。

### 步骤2：加入购物车

**接口**: `POST /api/v1/carts/items`

**请求**:
```json
{
  "product_id": 1,
  "sku_id": 5,
  "quantity": 2
}
```

**后端逻辑** (`cart_service.py`):
1. 校验 SKU 是否存在
2. 校验库存是否充足
3. 检查购物车是否已有该 SKU
   - 有：更新数量
   - 无：新增记录
4. 返回购物车摘要

**数据库变更**: `cart_items` 表 INSERT/UPDATE

### 步骤3：购物车列表

**接口**: `GET /api/v1/carts/items`

**响应**:
```json
{
  "code": 200,
  "data": {
    "items": [...],
    "total": 3,
    "total_price": "299.00"
  }
}
```

### 步骤4：提交订单（核心）

**接口**: `POST /api/v1/orders`

**请求**:
```json
{
  "address_id": 1,
  "cart_item_ids": [1, 2, 3],
  "coupon_id": null
}
```

**后端逻辑** (`order_service.py` → `create_order`):

```
FOR each cart_item in cart_item_ids:
    1. 获取 SKU 信息（价格/库存）
    2. 校验库存（stock >= quantity）
    3. 冻结库存：stock -= quantity（乐观锁）
    4. 写入 inventory_records（类型=order_deduct）

CREATE order:
    1. 生成订单号（时间戳+随机数）
    2. 计算总金额（商品小计 + 运费 - 优惠）
    3. 状态 = pending_payment
    4. 写入 orders 表
    5. 写入 order_items 表

POST 订单创建:
    → 写入 order_status_logs（状态：pending_payment）

CLEAR cart_items:
    → DELETE FROM cart_items WHERE id IN (...)
```

**并发保护**: 
- 使用 `SELECT ... FOR UPDATE` 行锁（MySQL）
- 或应用层乐观锁（version 字段）
- 当前 SQLite 实现为普通 UPDATE，有超卖风险（生产环境需加固）

### 步骤5：支付（未实现）

**状态**: ❌ 未实现

当前 `pay_amount` 字段存在，但无实际支付接口。订单创建后直接进入 `paid` 状态。

### 步骤6：订单状态流转

**流转规则**:

| 操作 | 原状态 | 新状态 | 触发者 |
|------|--------|--------|--------|
| 支付成功 | pending_payment | paid | 支付回调 |
| 发货 | paid | shipped | 管理员 |
| 确认收货 | shipped | completed | 用户 |
| 取消 | pending_payment | canceled | 用户/系统 |
| 退款 | paid/shipped | refunded | 管理员 |

**日志记录**: 每次状态变更写入 `order_status_logs` 表。

**后端实现** (`order_service.py` → `update_order_status`):
```python
async def update_order_status(db, order_id, new_status, operator_type, operator_id=None, remark=None):
    # 获取当前状态
    # 校验流转是否合法
    # 更新订单状态
    # 写入 order_status_logs
```

---

## 三、库存扣减逻辑

### 当前实现（SQLite）

```python
# 伪代码
sku = await db.execute(select(ProductSku).where(ProductSku.id == sku_id))
if sku.stock < quantity:
    raise ValueError("库存不足")
sku.stock -= quantity
await db.commit()

# 记录库存变动
record = InventoryRecord(
    sku_id=sku_id,
    order_id=order_id,
    change_type="order_deduct",
    quantity_change=-quantity,
    before_stock=old_stock,
    after_stock=new_stock,
    reason=f"订单扣减"
)
```

### 生产环境加固建议

1. **悲观锁**: `SELECT ... FOR UPDATE` 锁定行
2. **乐观锁**: `UPDATE skus SET stock = stock - ? WHERE id = ? AND stock >= ?`
3. **库存预占**: 下单时冻结库存（stock_freeze），支付后真正扣减，超时释放
4. **消息队列**: 库存扣减通过 MQ 异步处理，避免并发冲突

---

## 四、关键文件位置

| 文件 | 作用 |
|------|------|
| `app/services/cart_service.py` | 购物车逻辑 |
| `app/services/order_service.py` | 订单创建/状态变更 |
| `app/services/inventory_service.py` | 库存管理 |
| `app/models/order.py` | 订单模型 |
| `app/models/inventory_record.py` | 库存变动记录 |
| `app/models/order_status_log.py` | 订单状态日志 |
| `app/api/v1/orders.py` | 订单API |
| `app/api/v1/cart.py` | 购物车API |

---

*本文档基于 `backend/app/services/` 真实代码生成