<template>
  <div class="sidebar">
    <div class="logo-container">
      <h2 v-if="appStore.sidebar.opened" class="logo-text">SHAMGP</h2>
      <h2 v-else class="logo-text">S</h2>
    </div>
    <el-menu
      :default-active="activeMenu"
      :collapse="!appStore.sidebar.opened"
      :unique-opened="true"
      :router="true"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
    >
      <template v-for="route in permissionStore.menuTree" :key="route.id">
        <MenuItem
          v-if="route.type !== 'button'"
          :item="route"
          :base-path="''"
        />
      </template>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { usePermissionStore } from '@/stores/permission'
import MenuItem from './MenuItem.vue'

const route = useRoute()
const appStore = useAppStore()
const permissionStore = usePermissionStore()

const activeMenu = computed(() => route.path)
</script>

<style scoped>
.sidebar {
  height: 100%;
  overflow-y: auto;
}

.logo-container {
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #263445;
}

.logo-text {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.el-menu {
  border-right: none;
}
</style>
