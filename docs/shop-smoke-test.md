# 商城冒烟测试报告

> 测试时间：2026-03-31 16:20
> 后端：`http://localhost:8000`
> 状态：✅ 核心链路通过

---

## 测试命令与结果

### 1. 用户注册
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser2","password":"test123456","email":"test2@test.com"}'
```
**结果：`200`**
```json
{"code":200,"message":"success","data":{"access_token":"eyJhbGc..."}}
```

---

### 2. 用户登录
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser2","password":"test123456"}'
```
**结果：`200`**
```json
{"code":200,"message":"success","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}}
```

---

### 3. 商品列表
```bash
curl http://127.0.0.1:8000/api/v1/products \
  -H "Authorization: Bearer <token>"
```
**结果：`200`**
```json
{"code":200,"message":"success","data":{"items":[...],"total":6,"page":1,"page_size":20}}
```

---

### 4. 商品详情
```bash
curl http://127.0.0.1:8000/api/v1/products/1 \
  -H "Authorization: Bearer <token>"
```
**结果：`200`**
```json
{"code":200,"message":"success","data":{"id":1,"name":"iPhone 15 Pro Max","price":9999.00,...}}
```

---

### 5. 加入购物车
```bash
curl -X POST http://127.0.0.1:8000/api/v1/carts/items \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"product_id":1,"quantity":2}'
```
**结果：`200`**
```json
{"code":200,"message":"success","data":{"id":3,"product_id":1,"quantity":2,...}}
```

---

### 6. 购物车摘要
```bash
curl http://127.0.0.1:8000/api/v1/carts/summary \
  -H "Authorization: Bearer <token>"
```
**结果：`200`**
```json
{"code":200,"message":"success","data":{"total_amount":39996.00,"total_items":2,"items":[...]}}
```

---

## 联调状态

| 流程步骤 | 状态 |
|---------|------|
| 注册 → 登录 | ✅ 通过 |
| 商品列表 | ✅ 通过 |
| 商品详情 | ✅ 通过 |
| 加入购物车 | ✅ 通过 |
| 购物车查询 | ✅ 通过 |
| 创建订单（需地址） | ⚠️ 待实现 |
| 订单支付 | ⚠️ 待实现 |

---

## 已知问题

1. 创建订单需要 `address_id`，目前数据库中有地址但前端未对接
2. 优惠券下单核销需要 `coupon_code` 参数，前后端尚未联调
3. 商品分类、首页横幅、推荐楼层等 Shop 端尚未对接
