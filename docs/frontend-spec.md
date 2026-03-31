# 前端开发规范

## 1. 项目结构规范

### 1.1 目录命名
- 目录名：小写字母 + 短横线（kebab-case），如 `user-manage`
- 组件目录：大写字母开头（PascalCase），如 `UserForm`
- 文件名：小写字母 + 短横线（kebab-case），如 `user-list.ts`

### 1.2 文件组织
```
src/
├── api/           # API 接口
│   ├── index.ts   # Axios 实例配置
│   ├── request.ts # 请求封装
│   └── user.ts    # 用户模块 API
├── assets/        # 静态资源
│   ├── images/
│   └── styles/
├── components/    # 公共组件
│   ├── common/    # 通用组件
│   └── business/  # 业务组件
├── layouts/       # 布局组件
├── router/        # 路由
├── stores/        # Pinia 状态管理
├── utils/         # 工具函数
├── views/         # 页面视图
└── types/         # TypeScript 类型定义
```

---

## 2. TypeScript 规范

### 2.1 类型定义
- 使用 `interface` 定义对象类型
- 使用 `type` 定义联合类型、交叉类型
- 类型文件放在 `src/types/` 目录

```typescript
// src/types/user.ts
export interface User {
  id: number
  username: string
  email?: string
  status: number
  created_at: string
}

export interface UserListParams {
  page?: number
  page_size?: number
  keyword?: string
  status?: number
}

export interface UserListResponse {
  list: User[]
  total: number
  page: number
  page_size: number
}
```

### 2.2 类型导出
- 使用具名导出，避免默认导出
- 类型文件统一导出所有类型

```typescript
// src/types/index.ts
export * from './user'
export * from './product'
export * from './api'
```

---

## 3. Vue 组件规范

### 3.1 组件命名
- 组件名：PascalCase，如 `UserForm.vue`
- 单文件组件必须有 `name` 属性

```vue
<template>
  <div class="user-form">
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: 'UserForm'
})
</script>

<style scoped lang="scss">
.user-form {
}
</style>
```

### 3.2 Props 定义
- 使用 `withDefaults` 定义默认值
- 必须添加类型注解

```vue
<script setup lang="ts">
interface Props {
  title: string
  visible?: boolean
  data?: User
}

const props = withDefaults(defineProps<Props>(), {
  visible: false
})
</script>
```

### 3.3 Emits 定义
- 使用 `defineEmits` 定义事件
- 必须添加类型注解

```vue
<script setup lang="ts">
interface Emits {
  (e: 'submit', data: User): void
  (e: 'cancel'): void
}

const emit = defineEmits<Emits>()

const handleSubmit = () => {
  emit('submit', userData.value)
}
</script>
```

### 3.4 组合式函数
- 文件名：`useXxx.ts`，如 `useUser.ts`
- 返回值使用对象解构

```typescript
// src/utils/useUser.ts
import { ref, computed } from 'vue'
import type { User } from '@/types'

export function useUser() {
  const user = ref<User | null>(null)
  const isLogin = computed(() => !!user.value)

  const setUser = (data: User) => {
    user.value = data
  }

  const logout = () => {
    user.value = null
  }

  return {
    user,
    isLogin,
    setUser,
    logout
  }
}
```

---

## 4. API 请求规范

### 4.1 Axios 实例配置

```typescript
// src/api/index.ts
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { getToken, removeToken } from '@/utils/auth'
import router from '@/router'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000
})

request.interceptors.request.use(
  config => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

request.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== 200) {
      ElMessage.error(res.message || '请求失败')
      if (res.code === 401) {
        removeToken()
        router.push('/login')
      }
      return Promise.reject(new Error(res.message))
    }
    return res
  },
  error => {
    ElMessage.error(error.message || '网络错误')
    return Promise.reject(error)
  }
)

export default request
```

### 4.2 API 模块定义

```typescript
// src/api/user.ts
import request from './index'
import type { User, UserListParams, UserListResponse } from '@/types'

export const userApi = {
  list(params: UserListParams) {
    return request.get<UserListResponse>('/admin/users', { params })
  },

  detail(id: number) {
    return request.get<User>(`/admin/users/${id}`)
  },

  create(data: Partial<User>) {
    return request.post('/admin/users', data)
  },

  update(id: number, data: Partial<User>) {
    return request.put(`/admin/users/${id}`, data)
  },

  delete(id: number) {
    return request.delete(`/admin/users/${id}`)
  }
}
```

---

## 5. Pinia 状态管理规范

### 5.1 Store 定义

```typescript
// src/stores/modules/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { userApi } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(getToken() || '')
  const userInfo = ref<User | null>(null)

  const isLogin = computed(() => !!token.value)

  const login = async (username: string, password: string) => {
    const res = await userApi.login({ username, password })
    token.value = res.data.access_token
    userInfo.value = res.data.user
    setToken(res.data.access_token)
  }

  const logout = () => {
    token.value = ''
    userInfo.value = null
    removeToken()
  }

  const fetchUserInfo = async () => {
    const res = await userApi.getCurrentUser()
    userInfo.value = res.data
  }

  return {
    token,
    userInfo,
    isLogin,
    login,
    logout,
    fetchUserInfo
  }
})
```

---

## 6. 路由规范

### 6.1 路由配置

```typescript
// src/router/index.ts
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layouts/index.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '仪表盘', icon: 'dashboard' }
      },
      {
        path: 'system',
        name: 'System',
        redirect: '/system/user',
        meta: { title: '系统管理', icon: 'setting' },
        children: [
          {
            path: 'user',
            name: 'UserManage',
            component: () => import('@/views/system/user/index.vue'),
            meta: { title: '用户管理', icon: 'user' }
          }
        ]
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLogin) {
    next('/login')
  } else {
    next()
  }
})

export default router
```

---

## 7. 样式规范

### 7.1 SCSS 规范
- 使用 scoped 样式
- BEM 命名规范：`block__element--modifier`

```scss
<style scoped lang="scss">
.user-list {
  &__header {
    margin-bottom: 16px;
  }

  &__table {
    &--striped {
      background: #f5f5f5;
    }
  }
}
</style>
```

### 7.2 变量定义

```scss
// src/assets/styles/variables.scss
$primary-color: #409eff;
$success-color: #67c23a;
$warning-color: #e6a23c;
$danger-color: #f56c6c;

$border-radius: 4px;
$box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
```

---

## 8. 前端商城特有规范

### 8.1 组件分类
- 基础组件：轮播、导航、底部
- 业务组件：商品卡片、购物车条目、订单卡片

### 8.2 性能优化
- 图片懒加载
- 路由懒加载
- 虚拟列表（长列表）
- 防抖节流

```typescript
// src/utils/lazy.ts
import { useIntersectionObserver } from '@vueuse/core'

export function useLazyLoad(target: Ref<HTMLElement | null>) {
  const { stop } = useIntersectionObserver(
    target,
    ([{ isIntersecting }]) => {
      if (isIntersecting) {
        stop()
      }
    }
  )
}
```

---

## 9. 代码提交规范

### 9.1 Commit Message 格式
```
<type>(<scope>): <subject>

<type>:
  feat: 新功能
  fix: 修复bug
  docs: 文档更新
  style: 代码格式
  refactor: 重构
  test: 测试相关
  chore: 构建/工具

示例:
feat(admin): 添加用户管理模块
fix(shop): 修复购物车数量计算错误
```
