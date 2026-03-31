import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getRouters, getMenuTree, RouterItem, MenuTree } from '@/api'
import { RouteRecordRaw } from 'vue-router'

const modules = import.meta.glob('@/views/**/*.vue')

export const usePermissionStore = defineStore('permission', () => {
  const routes = ref<RouteRecordRaw[]>([])
  const menuTree = ref<MenuTree[]>([])
  const addRoutes = ref<RouteRecordRaw[]>([])

  function filterAsyncRoutes(routers: RouterItem[]): RouteRecordRaw[] {
    const res: RouteRecordRaw[] = []
    routers.forEach((route) => {
      const tmp: any = {
        path: route.path,
        name: route.name,
        redirect: route.redirect,
        meta: route.meta ? {
          title: route.meta.title,
          icon: route.meta.icon,
          permission: route.meta.permission,
          isKeepAlive: route.meta.is_keep_alive,
          isIframe: route.meta.is_iframe,
          isVisible: route.meta.is_visible
        } : undefined
      }

      if (route.component) {
        const componentPath = route.component.startsWith('/') 
          ? route.component.slice(1) 
          : route.component
        tmp.component = modules[`/src/views/${componentPath}.vue`]
      }

      if (route.children && route.children.length > 0) {
        tmp.children = filterAsyncRoutes(route.children)
      }

      res.push(tmp)
    })
    return res
  }

  async function generateRoutes() {
    const [routersRes, menuRes] = await Promise.all([getRouters(), getMenuTree()])
    const accessedRoutes = filterAsyncRoutes(routersRes.data)
    addRoutes.value = accessedRoutes
    routes.value = accessedRoutes
    menuTree.value = menuRes.data
    return accessedRoutes
  }

  return {
    routes,
    menuTree,
    addRoutes,
    generateRoutes
  }
})
