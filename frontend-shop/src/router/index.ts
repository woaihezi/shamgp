import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
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
    path: '/order/list',
    name: 'OrderList',
    component: () => import('@/views/order/OrderList.vue')
  },
  {
    path: '/order/detail/:id',
    name: 'OrderDetail',
    component: () => import('@/views/order/OrderDetail.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
