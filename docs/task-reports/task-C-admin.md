# 任务线 C：管理后台 (frontend-admin)

## 任务概述
负责管理后台核心功能完善，包括商品、分类、订单管理。

## 完成状态

### 1. 完善商品管理 ✅

**文件**: `frontend-admin/src/views/products/index.vue`

实现功能:
- 商品列表展示
- 商品新增/编辑/删除
- 商品上架/下架
- 商品搜索和筛选
- 分页功能

### 2. 完善分类管理 ✅

**文件**: `frontend-admin/src/views/product/CategoryList.vue`

实现功能:
- 分类树形结构展示
- 分类新增/编辑/删除
- 分类排序
- 分类状态管理

### 3. 完善订单管理 ✅

**文件**: `frontend-admin/src/views/orders/index.vue`

实现功能:
- 订单列表展示
- 订单详情查看
- 订单状态更新
- 订单搜索和筛选
- 订单导出

### 4. 统一 access_token ✅

**实现**:
- 统一使用 `localStorage.access_token`
- 请求拦截器自动附加 Token
- 响应拦截器处理 401 跳转

### 5. 修正 dashboard 中 mock 与假路径 ✅

**文件**: `frontend-admin/src/views/dashboard/index.vue`

修改内容:
- 移除硬编码的 mock 数据
- 修正 API 路径到 `/api/v1/dashboard/*`
- 添加真实 API 调用
- 标记为 P2，暂不深挖报表功能

## 修改文件列表

```
frontend-admin/
├── src/
│   ├── views/
│   │   ├── products/
│   │   │   └── index.vue
│   │   ├── product/
│   │   │   └── CategoryList.vue
│   │   ├── orders/
│   │   │   └── index.vue
│   │   └── dashboard/
│   │       └── index.vue
│   ├── api/
│   │   ├── product.ts
│   │   ├── order.ts
│   │   └── dashboard.ts
│   ├── stores/
│   │   └── user.ts
│   └── router/
│       └── index.ts
```

## 可运行模块

✅ 登录/登出
✅ 商品管理
✅ 分类管理
✅ 订单管理
✅ 用户管理
✅ 权限管理

## 未完成模块

- 数据看板统计 (P2)
- 营销活动管理
- 库存管理

## 下一阶段建议

- 完善数据看板统计
- 添加营销活动管理
- 实现库存管理
- 优化 UI/UX 细节
