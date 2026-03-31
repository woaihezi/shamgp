# Completed Work - 2026-03-31

## Task Summary
Built admin Dashboard and Order Management pages for Vue3 admin frontend.

## Files Created/Modified

### 1. `src/api/request.ts` — Updated
- Added JWT request interceptor that reads `Bearer ${token}` from `localStorage.getItem('token')` and injects into `Authorization` header on every request.

### 2. `src/views/dashboard/index.vue` — Replaced
- 4 stat cards (今日订单数, 本月销售额, 用户总数, 待处理订单) using `<el-card>` + `<el-statistic>`
- Each card has a colored icon badge (orders/sales/users/pending)
- Recent orders table: columns 订单号/用户/金额/状态/时间, top 5 rows
- Status tags: 待付款=warning, 已付款=success, 已发货=info
- Tries `/admin/stats` + `/orders/admin/` API first; falls back to mock data on failure
- "查看全部" button navigates to `/orders`

### 3. `src/views/orders/index.vue` — Created (new file)
- New `views/orders/` directory created
- `<el-radio-button>` status filter tabs: 全部/待付款/已付款/已发货/已完成/已取消
- Table: 订单号/用户ID/商品数/总金额/状态(标签)/支付方式/下单时间/操作
- Action buttons:
  - 已付款 → "发货" → PUT `/orders/admin/{id}/status` with `{status: "shipped"}`
  - 已发货 → "确认收货" → PUT with `{status: "completed"}`
- `<el-pagination>` with page sizes 10/20/50
- Error handling with `loadFailed` alert and ElMessage errors

### 4. `src/router/index.ts` — Updated
- Added `/orders` route pointing to `views/orders/index.vue` under Layout
- Route name: `Orders`, path: `/orders/index`

## API Endpoints Used
- `GET /api/v1/orders/admin/` — paginated order list (params: page, page_size, status)
- `PUT /api/v1/orders/admin/{id}/status` — update order status
- `GET /api/v1/admin/stats` — dashboard statistics

## Notes
- Token is read from `localStorage.getItem('token')` (set by login page)
- All API calls handle errors gracefully and fall back to mock data or error messages
- Chinese labels throughout; Element Plus `<el-tag>` types match status semantics
