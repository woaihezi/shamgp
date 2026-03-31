<template>
  <div class="page-container">
    <div v-if="title" class="page-header">
      <h2 class="page-title">{{ title }}</h2>
      <div v-if="$slots.extra" class="page-extra">
        <slot name="extra"></slot>
      </div>
    </div>
    <div class="page-content">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title?: string
}>()
</script>

<style lang="scss" scoped>
.page-container {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.page-title {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.page-content {
  min-height: calc(100vh - 240px);
}
</style>
