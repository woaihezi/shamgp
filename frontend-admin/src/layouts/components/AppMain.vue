<template>
  <section class="app-main">
    <breadcrumb />
    <div class="page-container">
      <router-view v-slot="{ Component }">
        <keep-alive :include="cachedViews">
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Breadcrumb from '@/components/Breadcrumb/index.vue'
import { useTagsViewStore } from '@/stores'

const tagsViewStore = useTagsViewStore()

const cachedViews = computed(() => tagsViewStore.cachedViews)
</script>

<style lang="scss" scoped>
.app-main {
  min-height: calc(100vh - 84px);
  width: 100%;
  position: relative;
  overflow: hidden;
  padding-top: 84px;
  background: #f0f2f5;
}

.page-container {
  padding: 20px;
}
</style>
