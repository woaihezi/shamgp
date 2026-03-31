<template>
  <div class="sidebar-wrapper">
    <div class="logo-container">
      <h1 class="sidebar-title">管理后台</h1>
    </div>
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu
        :default-active="activeMenu"
        :collapse="!sidebar.opened"
        :background-color="variables.menuBg"
        :text-color="variables.menuText"
        :unique-opened="false"
        :active-text-color="variables.menuActiveText"
        :collapse-transition="false"
        mode="vertical"
      >
        <sidebar-item
          v-for="route in routes"
          :key="route.path"
          :item="route"
          :base-path="route.path"
        />
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import SidebarItem from './SidebarItem.vue'
import { useAppStore } from '@/stores'

const appStore = useAppStore()
const route = useRoute()
const router = useRouter()

const variables = {
  menuBg: '#304156',
  menuText: '#bfcbd9',
  menuActiveText: '#409EFF'
}

const routes = computed(() => {
  const mainRoute = router.options.routes.find(r => r.path === '/')
  return mainRoute?.children || []
})

const activeMenu = computed(() => {
  return route.path
})

const sidebar = computed(() => appStore.sidebar)
</script>

<style lang="scss" scoped>
.sidebar-wrapper {
  height: 100%;
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
}

.logo-container {
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2b2f3a;
}

.sidebar-title {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  margin: 0;
}

.scrollbar-wrapper {
  overflow-x: hidden !important;
}

.el-menu {
  border: none;
  height: 100%;
  width: 100% !important;
}
</style>
