# 任务报告：营销与运营配置模块

**任务编号**: Task-06  
**任务名称**: 营销与运营配置模块  
**完成日期**: 2026-03-31  
**任务状态**: 已完成

---

## 一、任务概述

### 1.1 任务目标
为电商系统提供基础营销能力和首页运营位管理，包括优惠券管理、轮播图管理、广告位/推荐位管理、首页楼层配置等功能。

### 1.2 验收标准
1. ✅ 后台可配置优惠券
2. ✅ 后台可配置轮播图与推荐位
3. ✅ 商城首页可读取轮播与推荐商品
4. ✅ 优惠券模型能与订单流程衔接

---

## 二、实现内容

### 2.1 数据库设计

**文件路径**: `sql/06-marketing-ops.sql`

#### 创建的数据库表：

| 表名 | 说明 | 主要字段 |
|------|------|----------|
| `coupons` | 优惠券表 | id, name, type, discount_value, min_amount, total_count, used_count, per_limit, valid_start_time, valid_end_time, status, description |
| `coupon_receive_records` | 用户优惠券领取记录表 | id, user_id, coupon_id, status, order_id, used_time, received_time, expire_time |
| `banners` | 首页轮播图表 | id, title, image_url, link_url, sort, status, platform, description |
| `ad_spaces` | 广告位表 | id, name, code, width, height, description, status |
| `ads` | 广告表 | id, ad_space_id, title, image_url, link_url, sort, status, start_time, end_time, click_count, description |
| `floors` | 首页楼层表 | id, name, code, title, subtitle, sort, status, style |
| `floor_products` | 楼层商品关联表 | id, floor_id, product_id, sort, created_at |

### 2.2 后端实现

#### 2.2.1 数据模型层 (Models)

**文件路径**:
- `backend/app/models/base.py` - 基础模型
- `backend/app/models/coupon.py` - 优惠券模型
- `backend/app/models/banner.py` - 轮播图模型
- `backend/app/models/recommend.py` - 推荐位/广告/楼层模型

**核心模型类**:
- `Coupon` - 优惠券
- `CouponReceiveRecord` - 优惠券领取记录
- `Banner` - 轮播图
- `AdSpace` - 广告位
- `Ad` - 广告
- `Floor` - 楼层
- `FloorProduct` - 楼层商品关联

#### 2.2.2 数据验证层 (Schemas)

**文件路径**:
- `backend/app/schemas/common.py` - 通用Schema
- `backend/app/schemas/coupon.py` - 优惠券Schema
- `backend/app/schemas/banner.py` - 轮播图Schema
- `backend/app/schemas/recommend.py` - 推荐位Schema

#### 2.2.3 业务逻辑层 (Services)

**文件路径**:
- `backend/app/services/base.py` - 基础Service
- `backend/app/services/coupon_service.py` - 优惠券服务
- `backend/app/services/banner_service.py` - 轮播图服务
- `backend/app/services/recommend_service.py` - 推荐位服务

**核心服务功能**:
1. **CouponService**:
   - 优惠券CRUD操作
   - 获取可领取优惠券列表
   - 分页查询

2. **CouponReceiveRecordService**:
   - 用户领取优惠券
   - 用户优惠券查询
   - 使用优惠券
   - 计算折扣金额

3. **BannerService**:
   - 轮播图CRUD操作
   - 获取启用的轮播图

4. **AdSpaceService / AdService**:
   - 广告位和广告CRUD
   - 获取启用的广告

5. **FloorService / FloorProductService**:
   - 楼层和楼层商品CRUD
   - 获取启用的楼层

#### 2.2.4 API路由层 (API Routers)

**文件路径**:
- `backend/app/api/v1/admin/coupons.py` - 后台优惠券管理API
- `backend/app/api/v1/admin/banners.py` - 后台轮播图/广告/楼层管理API
- `backend/app/api/v1/shop/home.py` - 商城首页API
- `backend/app/api/v1/shop/coupons.py` - 商城优惠券API

**Admin API 端点**:

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/admin/coupons` | 获取优惠券列表 |
| GET | `/api/v1/admin/coupons/{id}` | 获取优惠券详情 |
| POST | `/api/v1/admin/coupons` | 创建优惠券 |
| PUT | `/api/v1/admin/coupons/{id}` | 更新优惠券 |
| DELETE | `/api/v1/admin/coupons/{id}` | 删除优惠券 |
| GET | `/api/v1/admin/banners` | 获取轮播图列表 |
| POST | `/api/v1/admin/banners` | 创建轮播图 |
| PUT | `/api/v1/admin/banners/{id}` | 更新轮播图 |
| DELETE | `/api/v1/admin/banners/{id}` | 删除轮播图 |
| GET | `/api/v1/admin/ad-spaces` | 获取广告位列表 |
| POST | `/api/v1/admin/ad-spaces` | 创建广告位 |
| PUT | `/api/v1/admin/ad-spaces/{id}` | 更新广告位 |
| DELETE | `/api/v1/admin/ad-spaces/{id}` | 删除广告位 |
| GET | `/api/v1/admin/ads` | 获取广告列表 |
| POST | `/api/v1/admin/ads` | 创建广告 |
| PUT | `/api/v1/admin/ads/{id}` | 更新广告 |
| DELETE | `/api/v1/admin/ads/{id}` | 删除广告 |
| GET | `/api/v1/admin/floors` | 获取楼层列表 |
| POST | `/api/v1/admin/floors` | 创建楼层 |
| PUT | `/api/v1/admin/floors/{id}` | 更新楼层 |
| DELETE | `/api/v1/admin/floors/{id}` | 删除楼层 |

**Shop API 端点**:

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/shop/home/banners` | 获取首页轮播图 |
| GET | `/api/v1/shop/home/coupons/available` | 获取可领取优惠券 |
| GET | `/api/v1/shop/home/floors` | 获取首页楼层 |
| GET | `/api/v1/shop/home/config` | 获取首页完整配置 |
| GET | `/api/v1/shop/coupons/available` | 获取可领取优惠券 |
| POST | `/api/v1/shop/coupons/receive` | 领取优惠券 |
| GET | `/api/v1/shop/coupons/my` | 获取我的优惠券 |
| POST | `/api/v1/shop/coupons/use/{id}` | 使用优惠券 |
| GET | `/api/v1/shop/coupons/calculate-discount/{id}` | 计算折扣金额 |

### 2.3 前端实现

#### 2.3.1 后台管理前端 (frontend-admin)

**文件路径**:
- `frontend-admin/src/api/marketing.ts` - 营销模块API
- `frontend-admin/src/api/request.ts` - 请求封装
- `frontend-admin/src/views/marketing/Coupon.vue` - 优惠券管理页面
- `frontend-admin/src/views/marketing/Banner.vue` - 轮播图管理页面

**主要功能**:
1. **优惠券管理页面**:
   - 优惠券列表展示
   - 新增/编辑/删除优惠券
   - 支持满减券、折扣券、无门槛券
   - 配置有效期、使用门槛、领取限制

2. **轮播图管理页面**:
   - 轮播图列表展示
   - 新增/编辑/删除轮播图
   - 配置图片、跳转链接、排序、状态

#### 2.3.2 商城前台 (frontend-shop)

**文件路径**:
- `frontend-shop/src/api/home.ts` - 首页API
- `frontend-shop/src/api/request.ts` - 请求封装
- `frontend-shop/src/views/home/Home.vue` - 商城首页

**主要功能**:
1. **首页展示**:
   - 轮播图展示
   - 可领取优惠券展示
   - 楼层商品展示（简化版）
   - 优惠券领取功能

---

## 三、优惠券与订单流程衔接

### 3.1 优惠券模型设计

优惠券系统提供了与订单流程衔接的基础字段和接口：

1. **优惠券基础字段**:
   - `type`: 优惠券类型（满减/折扣/无门槛）
   - `discount_value`: 优惠值
   - `min_amount`: 最低使用金额
   - `valid_start_time` / `valid_end_time`: 有效期

2. **用户优惠券记录字段**:
   - `status`: 优惠券状态（未使用/已使用/已过期）
   - `order_id`: 关联的订单ID
   - `used_time`: 使用时间

3. **订单集成接口**:
   - `calculate_discount()`: 计算折扣金额
   - `use_coupon()`: 使用优惠券并关联订单

### 3.2 订单流程集成建议

在订单创建流程中集成优惠券的步骤：

1. **订单确认页**:
   - 调用 `/api/v1/shop/coupons/my?status=1` 获取用户可用优惠券
   - 选择优惠券后调用 `calculate_discount()` 计算优惠金额

2. **订单创建**:
   - 验证优惠券有效性
   - 扣减优惠券（调用 `use_coupon()`）
   - 将优惠券ID和折扣金额保存到订单

3. **订单取消**:
   - 恢复优惠券状态为未使用
   - 清除订单关联

---

## 四、文件清单

### 4.1 后端文件

| 文件路径 | 说明 |
|---------|------|
| `backend/app/models/base.py` | 基础模型类 |
| `backend/app/models/coupon.py` | 优惠券模型 |
| `backend/app/models/banner.py` | 轮播图模型 |
| `backend/app/models/recommend.py` | 推荐位/广告/楼层模型 |
| `backend/app/schemas/common.py` | 通用Schema |
| `backend/app/schemas/coupon.py` | 优惠券Schema |
| `backend/app/schemas/banner.py` | 轮播图Schema |
| `backend/app/schemas/recommend.py` | 推荐位Schema |
| `backend/app/services/base.py` | 基础Service |
| `backend/app/services/coupon_service.py` | 优惠券服务 |
| `backend/app/services/banner_service.py` | 轮播图服务 |
| `backend/app/services/recommend_service.py` | 推荐位服务 |
| `backend/app/api/v1/admin/coupons.py` | 后台优惠券API |
| `backend/app/api/v1/admin/banners.py` | 后台轮播图/广告/楼层API |
| `backend/app/api/v1/shop/home.py` | 商城首页API |
| `backend/app/api/v1/shop/coupons.py` | 商城优惠券API |
| `backend/app/core/config.py` | 配置文件 |
| `backend/app/core/database.py` | 数据库连接 |
| `backend/app/api/v1/api.py` | API路由聚合 |
| `backend/app/main.py` | FastAPI应用入口 |

### 4.2 前端文件

| 文件路径 | 说明 |
|---------|------|
| `frontend-admin/src/api/marketing.ts` | 营销模块API |
| `frontend-admin/src/api/request.ts` | 请求封装 |
| `frontend-admin/src/views/marketing/Coupon.vue` | 优惠券管理页面 |
| `frontend-admin/src/views/marketing/Banner.vue` | 轮播图管理页面 |
| `frontend-shop/src/api/home.ts` | 首页API |
| `frontend-shop/src/api/request.ts` | 请求封装 |
| `frontend-shop/src/views/home/Home.vue` | 商城首页 |

### 4.3 数据库文件

| 文件路径 | 说明 |
|---------|------|
| `sql/06-marketing-ops.sql` | 营销模块数据库表结构 |

### 4.4 文档文件

| 文件路径 | 说明 |
|---------|------|
| `docs/task-reports/task-06-marketing-ops.md` | 本任务报告 |

---

## 五、技术栈

### 5.1 后端技术栈
- **框架**: FastAPI 0.104.1
- **ORM**: SQLAlchemy 2.0.23 (异步)
- **数据验证**: Pydantic v2.5.2
- **数据库**: PostgreSQL (异步驱动: asyncpg)

### 5.2 前端技术栈
- **框架**: Vue 3.4 + TypeScript
- **UI组件库**: Element Plus
- **HTTP客户端**: Axios
- **构建工具**: Vite

---

## 六、使用说明

### 6.1 后端启动

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 Swagger 文档: http://localhost:8000/docs

### 6.2 前端启动

**后台管理前端**:
```bash
cd frontend-admin
npm install
npm run dev
```

**商城前台**:
```bash
cd frontend-shop
npm install
npm run dev
```

### 6.3 数据库初始化

执行 SQL 文件:
```bash
psql -U shamgp -d shamgp -f sql/06-marketing-ops.sql
```

---

## 七、后续优化建议

1. **优惠券高级功能**:
   - 优惠券指定商品分类
   - 优惠券叠加规则
   - 优惠券使用统计报表

2. **运营位增强**:
   - A/B测试支持
   - 定时上下架
   - 流量数据分析

3. **性能优化**:
   - Redis 缓存热门运营配置
   - 图片CDN加速
   - 接口响应优化

4. **权限控制**:
   - 营销模块权限细分
   - 操作日志记录
   - 数据权限隔离

---

## 八、总结

本次任务成功实现了电商系统的营销与运营配置模块，包括：

✅ 完整的数据库设计（7张核心表）  
✅ 后端CRUD接口（Admin + Shop）  
✅ 优惠券核心业务逻辑（领取、使用、折扣计算）  
✅ 轮播图、广告位、楼层等运营位管理  
✅ 后台管理页面（优惠券、轮播图）  
✅ 商城前台首页展示  
✅ 与订单流程的衔接设计  

所有功能均按照需求规格完成，代码结构清晰，易于维护和扩展。

---

**报告编写人**: AI Assistant  
**审核状态**: 待审核
