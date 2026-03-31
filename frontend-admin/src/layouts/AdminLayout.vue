<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <div class="sidebar" :class="{ 'is-collapse': isCollapse, 'is-mobile': isMobile }">
      <div class="sidebar-header">
        <div class="logo">
          <svg width="28" height="28" viewBox="0 0 40 40" fill="none">
            <rect width="40" height="40" rx="8" fill="#4a9eff"/>
            <path d="M12 20L18 26L28 14" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span v-if="!isCollapse" class="logo-text">SHAMGP</span>
        </div>
      </div>

      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :collapse-transition="false"
        background-color="#1a1a2e"
        text-color="rgba(255,255,255,0.65)"
        active-text-color="#ffffff"
        class="sidebar-menu"
        @select="handleMenuSelect"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <template #title>Dashboard</template>
        </el-menu-item>
        <el-menu-item index="/products">
          <el-icon><Goods /></el-icon>
          <template #title>商品管理</template>
        </el-menu-item>
        <el-menu-item index="/orders">
          <el-icon><List /></el-icon>
          <template #title>订单管理</template>
        </el-menu-item>
        <el-menu-item index="/users">
          <el-icon><User /></el-icon>
          <template #title>用户管理</template>
        </el-menu-item>
        <el-menu-item index="/permissions">
          <el-icon><Lock /></el-icon>
          <template #title>权限管理</template>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- Mobile overlay -->
    <div v-if="isMobile && !isCollapse" class="sidebar-overlay" @click="toggleSidebar" />

    <!-- Main -->
    <div class="main-wrapper" :class="{ 'is-collapse': isCollapse, 'is-mobile': isMobile }">
      <!-- Header -->
      <div class="header-bar">
        <div class="header-left">
          <el-icon class="collapse-btn" @click="toggleSidebar">
            <Expand v-if="isCollapse" />
            <Fold v-else />
          </el-icon>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentMenuName">{{ currentMenuName }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="32" bg-color="#4a9eff">
                {{ adminStore.user?.username?.[0]?.toUpperCase() || 'A' }}
              </el-avatar>
              <span class="username">{{ adminStore.user?.username || '管理员' }}</span>
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <!-- Content -->
      <div class="content-area">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Odometer, Goods, List, User, Lock, Fold, Expand, ArrowDown } from '@element-plus/icons-vue'
import { useAdminStore } from '@/stores/admin'

const router = useRouter()
const route = useRoute()
const adminStore = useAdminStore()

const isCollapse = ref(false)
const isMobile = ref(false)
const currentMenuName = ref('')

const menuNameMap: Record<string, string> = {
  '/dashboard': 'Dashboard',
  '/products': '商品管理',
  '/orders': '订单管理',
  '/users': '用户管理',
  '/permissions': '权限管理'
}

const activeMenu = computed(() => '/' + route.path.split('/').filter(Boolean)[0])

function checkMobile() {
  isMobile.value = window.innerWidth < 768
  if (isMobile.value) isCollapse.value = true
}

function toggleSidebar() {
  isCollapse.value = !isCollapse.value
}

function handleMenuSelect(index: string) {
  if (index.startsWith('/')) {
    router.push(index)
    currentMenuName.value = menuNameMap[index] || ''
  }
}

async function handleCommand(command: string) {
  if (command === 'logout') {
    adminStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }
}

onMounted(() => {
  adminStore.initFromStorage()
  if (adminStore.token) {
    adminStore.fetchUserInfo().catch(() => {})
  }
  checkMobile()
  window.addEventListener('resize', checkMobile)
  currentMenuName.value = menuNameMap[activeMenu.value] || ''
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* Sidebar */
.sidebar {
  width: 210px;
  background: #1a1a2e;
  height: 100vh;
  display: flex;
  flex-direction: column;
  transition: width 0.28s;
  flex-shrink: 0;
  position: relative;
  z-index: 100;
}

.sidebar.is-collapse {
  width: 64px;
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  overflow: hidden;
}

.logo-text {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 1px;
  white-space: nowrap;
}

.sidebar-menu {
  border-right: none;
  flex: 1;
  overflow-y: auto;
}

:deep(.el-menu-item) {
  height: 52px;
  line-height: 52px;
}

:deep(.el-menu-item:hover) {
  background: rgba(255,255,255,0.06) !important;
}

:deep(.el-menu-item.is-active) {
  background: rgba(74, 158, 255, 0.15) !important;
  color: #4a9eff !important;
}

:deep(.el-menu-item.is-active::before) {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: #4a9eff;
  border-radius: 0 2px 2px 0;
}

/* Mobile overlay */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 99;
}

/* Main wrapper */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  transition: margin-left 0.28s;
  background: #f0f2f5;
}

.main-wrapper.is-mobile {
  margin-left: 0;
}

/* Header */
.header-bar {
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  font-size: 20px;
  cursor: pointer;
  color: #666;
  transition: color 0.2s;
}

.collapse-btn:hover {
  color: #4a9eff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}

.user-info:hover {
  background: #f5f5f5;
}

.username {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

/* Content */
.content-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: -210px;
  }

  .sidebar:not(.is-collapse) {
    left: 0;
  }

  .sidebar.is-mobile {
    left: -210px;
  }

  .sidebar.is-mobile:not(.is-collapse) {
    left: 0;
  }

  .username {
    display: none;
  }
}
</style>
