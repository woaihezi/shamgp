# ShamGP 商城 — 改进计划

> 生成时间：2026-03-31（最新）
> 目标：把项目从"能跑但粗糙"推进到"可演示、可联动、视觉明显提升"

---

## 一、已完成项（2026-03-31 本轮）

### P0 数据接入 ✅
- 种子数据：15分类、95用户、133商品、218 SKU、399图片、6楼层
- 修复 `recommend.py` 未注册问题（floors/floor_products/ad_spaces/ads 建表）

### P0 数据库缺失能力补齐 ✅（7个）
1. ✅ 收藏表 `favorites` — 前后端完整
2. ✅ 浏览历史表 `browse_histories` — 前后端完整
3. ✅ 订单状态日志表 `order_status_logs` — 前后端完整
4. ✅ 商品图片表 `product_images` — 已存在并使用
5. ✅ 优惠券表 `coupons` + `user_coupons` — 完整（领券/用券/查询）
6. ✅ 楼层体系 `floors` + `floor_products` — 修复注册问题
7. ✅ SKU 真实库存扣减 — `deduct_stock_for_order` 乐观锁 + 订单集成

### P0 前端改版 ✅
1. ✅ ProductDetail — 图片画廊（多图+缩略图+箭头导航）
2. ✅ ProductDetail — SKU 选择器（规格联动+库存联动+价格联动）
3. ✅ ProductList — 真实数据 + 分类筛选 + 排序 + 分页 + 5列网格
4. ✅ Home.vue — 楼层真实商品数据渲染
5. ✅ Checkout — 优惠券选择（满减/折扣计算+优惠联动）
6. ✅ Checkout — 运费计算（满99包邮/10元运费）
7. ✅ ProductDetail — 收藏按钮（增/删）
8. ✅ ProductDetail — 浏览历史自动写入
9. ✅ ProductDetail — 加入购物车真实 API 调用

### P0 运费规则 ✅
- ✅ `shipping_rules` 表（4条规则：全国/包邮/一线城市/偏远地区）
- ✅ `shipping_service.py` 同步版本
- ✅ Checkout.vue 运费显示（满99包邮/10元运费联动）

### docs 文档 ✅（10个文件）
`docs/api/`:
- `products.md` ✅
- `cart.md` ✅
- `orders.md` ✅
- `coupons.md` ✅
- `favorites.md` ✅
- `browse-history.md` ✅

`docs/architecture/`:
- `system-structure.md` ✅
- `data-models.md` ✅
- `order-flow.md` ✅
- `coupon-flow.md` ✅

---

## 二、进行中项

（无）

---

## 三、待完成项

### P1
| 项 | 优先级 | 说明 |
|----|--------|------|
| task-02 / task-05 复核 | P1 | 报告异常简略，验证真实执行情况 |
| 后台订单状态变更日志查看 | P1 | 管理员可查看订单状态流转记录 |

### P2
| 项 | 优先级 | 说明 |
|----|--------|------|
| 移动端适配 | P2 | 响应式布局 |
| 搜索功能（全文搜索） | P2 | Elasticsearch 或 LIKE 改进 |
| 商品详情页多图轮播增强 | P2 | 当前图片画廊较基础 |

### P3
| 项 | 优先级 | 说明 |
|----|--------|------|
| 支付功能对接 | P3 | 支付宝/微信 |
| SKU 规格图真实图片 | P3 | 当前用 picsum 占位 |
| 物流跟踪接口 | P3 | 对接快递100等 |

---

## 四、技术架构

- 后端：FastAPI + SQLAlchemy 2.0（异步）+ SQLite
- 前端：Vue 3 + Vite + TypeScript + Pinia + Element Plus
- 数据库：SQLite（开发）
- 部署：Docker 骨架

---

## 五、数据库表清单（完整）

| 表名 | 用途 | 数据量 |
|------|------|--------|
| users | 用户 | 95 |
| product_categories | 分类 | 15 |
| product_spus | 商品SPU | 133 |
| product_skus | SKU | 218 |
| product_images | 图片 | 399 |
| brands | 品牌 | 0 |
| addresses | 地址 | 95 |
| orders | 订单 | 0 |
| order_items | 订单项 | 0 |
| cart_items | 购物车 | 0 |
| favorites | 收藏 | 0 |
| browse_histories | 浏览历史 | 0 |
| order_status_logs | 订单日志 | 0 |
| coupons | 优惠券 | 5 |
| user_coupons | 用户优惠券 | 0 |
| floors | 楼层 | 6 |
| floor_products | 楼层商品 | 48 |
| inventory_records | 库存变动 | 0 |
| refunds | 退款 | 0 |
| ad_spaces | 广告位 | 0 |
| ads | 广告 | 0 |
| shipping_rules | 运费规则 | 4 |

---

*本文档基于 2026-03-31 真实代码落地生成