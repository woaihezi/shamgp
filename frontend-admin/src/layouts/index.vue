<template>
  <div class="app-wrapper">
    <div v-if="device === 'mobile'" class="drawer-bg" @click="closeSidebar"></div>
    <Sidebar class="sidebar-container" />
    <div class="main-container">
      <div class="fixed-header">
        <Header />
        <TagsView />
      </div>
      <app-main />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'
import TagsView from './components/TagsView.vue'
import AppMain from './components/AppMain.vue'
import { useAppStore } from '@/stores'
import { useTagsViewStore } from '@/stores'

const appStore = useAppStore()
const tagsViewStore = useTagsViewStore()
const route = useRoute()

const device = computed(() => appStore.device)

const closeSidebar = () => {
  appStore.closeSidebar(true)
}

const isMobile = () => {
  const rect = document.body.getBoundingClientRect()
  return rect.width - 1 < 992
}

const resizeHandler = () => {
  if (!document.hidden) {
    const mobile = isMobile()
    if (mobile) {
      appStore.toggleDevice('mobile')
      appStore.closeSidebar(true)
    } else {
      appStore.toggleDevice('desktop')
      appStore.sidebar.opened = true
    }
  }
}

onMounted(() => {
  tagsViewStore.addView(route)
  const mobile = isMobile()
  if (mobile) {
    appStore.toggleDevice('mobile')
    appStore.closeSidebar(true)
  }
  window.addEventListener('resize', resizeHandler)
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeHandler)
})
</script>

<style lang="scss" scoped>
.app-wrapper {
  position: relative;
  height: 100%;
  width: 100%;
}

.drawer-bg {
  background: #000;
  opacity: 0.3;
  width: 100%;
  top: 0;
  height: 100%;
  position: absolute;
  z-index: 999;
}

.sidebar-container {
  transition: width 0.28s;
  width: 210px !important;
  background-color: #304156;
  height: 100%;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 1001;
  overflow: hidden;
}

.main-container {
  min-height: 100%;
  transition: margin-left 0.28s;
  margin-left: 210px;
  position: relative;
}

.fixed-header {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 9;
  width: calc(100% - 210px);
  transition: width 0.28s;
}
</style>
