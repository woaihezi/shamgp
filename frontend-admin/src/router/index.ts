import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import AdminLayout from "@/layouts/AdminLayout.vue";

const routes: RouteRecordRaw[] = [
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/login/index.vue"),
    meta: { hidden: true },
  },
  {
    path: "/",
    component: AdminLayout,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: () => import("@/views/dashboard/index.vue"),
        meta: { title: "Dashboard" },
      },
      {
        path: "products",
        name: "Products",
        component: () => import("@/views/products/index.vue"),
        meta: { title: "商品管理" },
      },
      {
        path: "orders",
        name: "Orders",
        component: () => import("@/views/orders/index.vue"),
        meta: { title: "订单管理" },
      },
      {
        path: "users",
        name: "Users",
        component: () => import("@/views/users/index.vue"),
        meta: { title: "用户管理" },
      },
      {
        path: "permissions",
        name: "Permissions",
        component: () => import("@/views/permissions/index.vue"),
        meta: { title: "权限管理" },
      },
      {
        path: "marketing",
        name: "Marketing",
        meta: { title: "营销管理" },
        children: [
          {
            path: "banners",
            name: "Banners",
            component: () => import("@/views/marketing/Banner.vue"),
            meta: { title: "轮播图管理" },
          },
          {
            path: "coupons",
            name: "Coupons",
            component: () => import("@/views/marketing/Coupon.vue"),
            meta: { title: "优惠券管理" },
          },
        ],
      },
      {
        path: "logs",
        name: "Logs",
        meta: { title: "系统日志" },
        children: [
          {
            path: "operation",
            name: "OperationLogs",
            component: () => import("@/views/logs/OperationLog.vue"),
            meta: { title: "操作日志" },
          },
          {
            path: "login",
            name: "LoginLogs",
            component: () => import("@/views/logs/LoginLog.vue"),
            meta: { title: "登录日志" },
          },
        ],
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Route guard: protect routes except /login
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('access_token')

  if (to.path === '/login') {
    if (token) {
      next('/')
    } else {
      next()
    }
  } else {
    if (token) {
      next()
    } else {
      next('/login')
    }
  }
})

export default router;
