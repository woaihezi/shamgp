<template>
  <component :is="item.children && item.children.length > 0 ? 'el-sub-menu' : 'el-menu-item'" :index="resolvePath">
    <template #title>
      <el-icon v-if="item.icon">
        <component :is="item.icon" />
      </el-icon>
      <span>{{ item.name }}</span>
    </template>
    <template v-if="item.children && item.children.length > 0">
      <MenuItem
        v-for="child in item.children.filter(c => c.type !== 'button')"
        :key="child.id"
        :item="child"
        :base-path="resolvePath"
      />
    </template>
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { MenuTree } from '@/api'

interface Props {
  item: MenuTree
  basePath: string
}

const props = defineProps<Props>()

const resolvePath = computed(() => {
  if (!props.basePath) {
    return props.item.path || ''
  }
  return props.basePath.endsWith('/') ? `${props.basePath}${props.item.path?.slice(1)}` : `${props.basePath}${props.item.path}`
})
</script>

<style scoped>
</style>
