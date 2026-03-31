# 模块划分规划

## 1. 模块总览

系统分为三大模块群：

1. **通用管理模块群** - 可复用于任何后台系统的基础模块
2. **电商业务模块群** - 电商特有的业务模块
3. **扩展预留模块群** - 为未来功能预留的模块

## 2. 通用管理模块群

### 2.1 用户认证模块 (Auth Module)

**职责**:
- 用户注册、登录、登出
- JWT Token 生成与验证
- 密码加密与验证
- Token 刷新机制

**文件范围**:
- 后端: `backend/app/api/v1/shop/auth.py`, `backend/app/core/security.py`
- 前端商城: `frontend-shop/src/api/auth.ts`, `frontend-shop/src/views/Login/`
- 前端后台: `frontend-admin/src/api/auth.ts`, `frontend-admin/src/views/login/`

**依赖**: 无 (基础模块)

### 2.2 用户管理模块 (User Module)

**职责**:
- 用户 CRUD 操作
- 用户状态管理（启用/禁用）
- 用户信息查询与统计
- 用户角色分配

**文件范围**:
- 后端: `backend/app/api/v1/admin/users.py`, `backend/app/models/user.py`, `backend/app/schemas/user.py`, `backend/app/services/user_service.py`
- 前端后台: `frontend-admin/src/api/user.ts`, `frontend-admin/src/views/system/user/`

**依赖**: 角色模块

### 2.3 角色权限模块 (RBAC Module)

**职责**:
- 角色 CRUD
- 权限定义与管理
- 角色-权限关联
- 用户-角色关联
- 权限验证中间件

**文件范围**:
- 后端: `backend/app/api/v1/admin/roles.py`, `backend/app/api/v1/admin/permissions.py`, `backend/app/models/role.py`, `backend/app/models/permission.py`
- 前端后台: `frontend-admin/src/api/role.ts`, `frontend-admin/src/views/system/role/`

**依赖**: 无

### 2.4 菜单管理模块 (Menu Module)

**职责**:
- 菜单树结构管理
- 菜单-角色关联
- 动态菜单生成
- 菜单图标与路由配置

**文件范围**:
- 后端: `backend/app/api/v1/admin/menus.py`, `backend/app/models/menu.py`
- 前端后台: `frontend-admin/src/api/menu.ts`, `frontend-admin/src/views/system/menu/`

**依赖**: 角色模块

### 2.5 操作日志模块 (Log Module)

**职责**:
- 用户操作日志记录
- 登录日志记录
- 异常日志记录
- 日志查询与统计
- 日志归档

**文件范围**:
- 后端: `backend/app/api/v1/admin/logs.py`, `backend/app/models/log.py`, `backend/app/utils/logger.py`
- 前端后台: `frontend-admin/src/api/log.ts`, `frontend-admin/src/views/system/log/`

**依赖**: 无

### 2.6 系统配置模块 (Config Module)

**职责**:
- 系统参数配置
- 配置分组管理
- 配置热更新
- 配置版本管理

**文件范围**:
- 后端: `backend/app/api/v1/admin/configs.py`, `backend/app/models/config.py`
- 前端后台: `frontend-admin/src/api/config.ts`, `frontend-admin/src/views/system/config/`

**依赖**: 无

### 2.7 文件管理模块 (File Module)

**职责**:
- 文件上传（支持本地/OSS/MinIO）
- 文件下载
- 文件删除
- 文件分类管理
- 文件预览

**文件范围**:
- 后端: `backend/app/api/v1/admin/files.py`, `backend/app/models/file.py`, `backend/app/utils/file_util.py`
- 前端后台: `frontend-admin/src/api/file.ts`, `frontend-admin/src/components/Upload/`

**依赖**: 无

## 3. 电商业务模块群

### 3.1 商品分类模块 (Category Module)

**职责**:
- 分类树结构管理
- 分类属性配置
- 分类排序
- 分类状态管理

**文件范围**:
- 后端: `backend/app/api/v1/admin/categories.py`, `backend/app/models/category.py`
- 前端后台: `frontend-admin/src/api/category.ts`, `frontend-admin/src/views/product/category/`
- 前端商城: `frontend-shop/src/api/category.ts`

**依赖**: 无

### 3.2 商品管理模块 (Product Module)

**职责**:
- 商品 CRUD
- 商品 SKU 管理
- 商品库存管理
- 商品上下架
- 商品搜索与筛选
- 商品评价管理

**文件范围**:
- 后端: `backend/app/api/v1/admin/products.py`, `backend/app/api/v1/shop/products.py`, `backend/app/models/product.py`, `backend/app/services/product_service.py`
- 前端后台: `frontend-admin/src/api/product.ts`, `frontend-admin/src/views/product/`
- 前端商城: `frontend-shop/src/api/product.ts`, `frontend-shop/src/views/Product/`

**依赖**: 分类模块, 文件模块

### 3.3 购物车模块 (Cart Module)

**职责**:
- 购物车添加商品
- 购物车商品数量修改
- 购物车商品删除
- 购物车清空
- 购物车商品选中状态

**文件范围**:
- 后端: `backend/app/api/v1/shop/cart.py`, `backend/app/models/cart.py`
- 前端商城: `frontend-shop/src/api/cart.ts`, `frontend-shop/src/views/Cart/`, `frontend-shop/src/stores/modules/cart.ts`

**依赖**: 商品模块, 用户模块

### 3.4 订单管理模块 (Order Module)

**职责**:
- 订单创建
- 订单支付
- 订单状态流转
- 订单退款
- 订单查询与统计
- 订单导出

**文件范围**:
- 后端: `backend/app/api/v1/admin/orders.py`, `backend/app/api/v1/shop/orders.py`, `backend/app/models/order.py`, `backend/app/services/order_service.py`
- 前端后台: `frontend-admin/src/api/order.ts`, `frontend-admin/src/views/order/`
- 前端商城: `frontend-shop/src/api/order.ts`, `frontend-shop/src/views/Order/`

**依赖**: 商品模块, 购物车模块, 用户模块, 支付模块

### 3.5 支付模块 (Payment Module)

**职责**:
- 支付渠道配置
- 支付订单创建
- 支付回调处理
- 支付状态查询
- 退款处理

**文件范围**:
- 后端: `backend/app/api/v1/shop/payments.py`, `backend/app/services/payment_service.py`
- 前端商城: `frontend-shop/src/api/payment.ts`

**依赖**: 订单模块

### 3.6 用户中心模块 (User Center Module)

**职责**:
- 用户信息编辑
- 收货地址管理
- 我的订单
- 我的收藏
- 账户安全

**文件范围**:
- 后端: `backend/app/api/v1/shop/users.py`
- 前端商城: `frontend-shop/src/views/User/`

**依赖**: 用户模块, 订单模块

### 3.7 数据统计模块 (Dashboard Module)

**职责**:
- 销售数据统计
- 订单数据统计
- 用户数据统计
- 商品数据统计
- 数据可视化图表

**文件范围**:
- 后端: `backend/app/api/v1/admin/dashboard.py`, `backend/app/services/dashboard_service.py`
- 前端后台: `frontend-admin/src/views/dashboard/`

**依赖**: 订单模块, 商品模块, 用户模块

## 4. 扩展预留模块群

### 4.1 AI 助手模块 (AI Assistant Module)

**预留位置**:
- 后端: `backend/app/api/v1/ai/`, `backend/app/services/ai/`
- 前端后台: `frontend-admin/src/views/ai/`

**功能规划**:
- 智能客服
- 商品推荐
- 智能问答
- 内容生成

### 4.2 Excel 导入导出模块 (Excel Module)

**预留位置**:
- 后端: `backend/app/utils/excel.py`
- 前端后台: `frontend-admin/src/components/Excel/`

**功能规划**:
- 批量数据导入
- 数据模板下载
- 数据导出（支持多种格式）
- 导入数据验证

### 4.3 可视化大屏模块 (Big Screen Module)

**预留位置**:
- 前端后台: `frontend-admin/src/views/dashboard/big-screen/`

**功能规划**:
- 实时数据展示
- 多维度数据可视化
- 自定义大屏布局
- 大屏模板管理

### 4.4 工作流模块 (Workflow Module)

**预留位置**:
- 后端: `backend/app/api/v1/workflow/`, `backend/app/services/workflow/`
- 前端后台: `frontend-admin/src/views/workflow/`

**功能规划**:
- 流程设计器
- 流程实例管理
- 任务管理
- 流程审批

### 4.5 CRM 模块 (CRM Module)

**预留位置**:
- 后端: `backend/app/api/v1/crm/`
- 前端后台: `frontend-admin/src/views/crm/`

**功能规划**:
- 客户管理
- 线索管理
- 商机管理
- 合同管理

### 4.6 OA 模块 (OA Module)

**预留位置**:
- 后端: `backend/app/api/v1/oa/`
- 前端后台: `frontend-admin/src/views/oa/`

**功能规划**:
- 考勤管理
- 请假审批
- 报销管理
- 会议管理

### 4.7 工单模块 (Ticket Module)

**预留位置**:
- 后端: `backend/app/api/v1/ticket/`
- 前端后台: `frontend-admin/src/views/ticket/`

**功能规划**:
- 工单创建
- 工单分配
- 工单处理
- 工单评价

## 5. 模块依赖关系图

```
┌─────────────────────────────────────────────────────────────┐
│                        扩展预留模块群                         │
│  [AI] [Excel] [大屏] [工作流] [CRM] [OA] [工单]            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        电商业务模块群                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ [数据统计] ───────────────────────────┐              │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ [用户中心] [支付] ───┐                                │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ [订单] ────────────────────┐                           │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ [购物车] [商品] ─────────┐                             │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ [分类] [文件]                                             │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        通用管理模块群                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ [用户管理] [菜单管理] [操作日志] [系统配置]             │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ [角色权限]                                               │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ [用户认证]                                               │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 6. 模块开发优先级

### Phase 1 - 核心基础设施 (必须最先完成)
1. 用户认证模块
2. 角色权限模块
3. 用户管理模块

### Phase 2 - 通用管理模块
1. 菜单管理模块
2. 操作日志模块
3. 系统配置模块
4. 文件管理模块

### Phase 3 - 电商核心业务
1. 商品分类模块
2. 商品管理模块
3. 购物车模块
4. 订单管理模块

### Phase 4 - 电商补充功能
1. 支付模块
2. 用户中心模块
3. 数据统计模块

### Phase 5 - 扩展功能
1. AI 助手模块
2. Excel 导入导出模块
3. 可视化大屏模块
4. 工作流模块
5. CRM / OA / 工单模块
