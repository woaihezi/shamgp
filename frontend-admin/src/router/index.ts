import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import Layout from "@/layouts/index.vue";

const routes: RouteRecordRaw[] = [
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/login/index.vue"),
    meta: { hidden: true },
  },
  {
    path: "/",
    component: Layout,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: () => import("@/views/dashboard/index.vue"),
        meta: { title: "首页", icon: "dashboard" },
      },
    ],
  },
  {
    path: "/product",
    component: Layout,
    redirect: "/product/list",
    meta: { title: "商品管理", icon: "product" },
    children: [
      {
        path: "list",
        name: "ProductList",
        component: () => import("@/views/product/ProductList.vue"),
        meta: { title: "商品列表" },
      },
      {
        path: "category",
        name: "CategoryList",
        component: () => import("@/views/product/CategoryList.vue"),
        meta: { title: "分类管理" },
      },
      {
        path: "brand",
        name: "BrandList",
        component: () => import("@/views/product/BrandList.vue"),
        meta: { title: "品牌管理" },
      },
    ],
  },
  {
    path: "/order",
    component: Layout,
    redirect: "/order/list",
    meta: { title: "订单管理", icon: "order" },
    children: [
      {
        path: "list",
        name: "OrderList",
        component: () => import("@/views/order/OrderList.vue"),
        meta: { title: "订单列表" },
      },
    ],
  },
  {
    path: "/marketing",
    component: Layout,
    redirect: "/marketing/banner",
    meta: { title: "营销运营", icon: "marketing" },
    children: [
      {
        path: "banner",
        name: "Banner",
        component: () => import("@/views/marketing/Banner.vue"),
        meta: { title: "Banner管理" },
      },
      {
        path: "coupon",
        name: "Coupon",
        component: () => import("@/views/marketing/Coupon.vue"),
        meta: { title: "优惠券管理" },
      },
    ],
  },
  {
    path: "/file",
    component: Layout,
    redirect: "/file/index",
    children: [
      {
        path: "index",
        name: "File",
        component: () => import("@/views/file/index.vue"),
        meta: { title: "文件管理", icon: "file" },
      },
    ],
  },
  {
    path: "/setting",
    component: Layout,
    redirect: "/setting/index",
    children: [
      {
        path: "index",
        name: "Setting",
        component: () => import("@/views/setting/index.vue"),
        meta: { title: "系统设置", icon: "setting" },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
