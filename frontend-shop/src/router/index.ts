import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/products',
    name: 'ProductList',
    component: () => import('@/views/ProductList/index.vue')
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: () => import('@/views/ProductDetail/index.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login/index.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register/index.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile/index.vue')
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('@/views/cart/CartList.vue')
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: () => import('@/views/checkout/Checkout.vue')
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('@/views/order/OrderList.vue')
  },
  {
    path: '/order/list',
    name: 'OrderList',
    component: () => import('@/views/order/OrderList.vue')
  },
  {
    path: '/orders/:id',
    name: 'OrderDetail',
    component: () => import('@/views/order/OrderDetail.vue')
  },
  {
    path: '/order/detail/:id',
    name: 'OrderDetailLegacy',
    component: () => import('@/views/order/OrderDetail.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('access_token')
  
  const requiresAuth = to.meta.requiresAuth
  if (requiresAuth && !token) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    next('/')
  } else {
    next()
  }
})

export default router
