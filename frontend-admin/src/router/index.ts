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
