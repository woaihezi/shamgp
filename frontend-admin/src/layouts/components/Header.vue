<template>
  <div class="navbar">
    <div class="hamburger-container" @click="toggleSidebar">
      <svg class="hamburger" :class="{ 'is-active': sidebar.opened }" viewBox="0 0 1024 1024" width="64" height="64">
        <path d="M408 448h208c17.673 0 32-14.327 32-32s-14.327-32-32-32H408c-17.673 0-32 14.327-32 32s14.327 32 32 32z m0 192h208c17.673 0 32-14.327 32-32s-14.327-32-32-32H408c-17.673 0-32 14.327-32 32s14.327 32 32 32z m0-384h208c17.673 0 32-14.327 32-32s-14.327-32-32-32H408c-17.673 0-32 14.327-32 32s14.327 32 32 32z" />
      </svg>
    </div>
    <div class="right-menu">
      <el-dropdown class="avatar-container" trigger="click">
        <div class="avatar-wrapper">
          <el-avatar :size="40" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
          <span class="username">{{ userStore.name }}</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>个人中心</el-dropdown-item>
            <el-dropdown-item divided>退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore, useUserStore } from '@/stores'

const appStore = useAppStore()
const userStore = useUserStore()

const sidebar = computed(() => appStore.sidebar)

const toggleSidebar = () => {
  appStore.toggleSidebar()
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.hamburger-container {
  line-height: 46px;
  height: 100%;
  float: left;
  cursor: pointer;
  transition: background 0.3s;
  padding: 0 15px;
  display: flex;
  align-items: center;

  &:hover {
    background: rgba(0, 0, 0, 0.025);
  }
}

.hamburger {
  display: inline-block;
  vertical-align: middle;
  width: 20px;
  height: 20px;
  fill: currentColor;

  &.is-active {
    transform: rotate(180deg);
  }
}

.right-menu {
  float: right;
  height: 100%;
  line-height: 50px;
  display: flex;
  align-items: center;
}

.avatar-container {
  margin-right: 20px;
  cursor: pointer;

  .avatar-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .username {
    font-size: 14px;
    color: #606266;
  }
}
</style>
