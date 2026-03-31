<template>
  <div v-if="!item.meta?.hidden">
    <template v-if="hasOneShowingChild(item.children) && !onlyOneChild.meta?.alwaysShow">
      <el-menu-item :index="resolvePath(onlyOneChild.path)" @click="handleClick(onlyOneChild)">
        <el-icon v-if="onlyOneChild.meta?.icon"><component :is="getIcon(onlyOneChild.meta.icon)" /></el-icon>
        <template #title>{{ onlyOneChild.meta?.title }}</template>
      </el-menu-item>
    </template>
    <el-sub-menu v-else :index="resolvePath(item.path)">
      <template #title>
        <el-icon v-if="item.meta?.icon"><component :is="getIcon(item.meta.icon)" /></el-icon>
        <span>{{ item.meta?.title }}</span>
      </template>
      <sidebar-item
        v-for="child in item.children"
        :key="child.path"
        :item="child"
        :base-path="resolvePath(child.path)"
      />
    </el-sub-menu>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, type RouteRecordRaw } from 'vue-router'
import path from 'path-browserify'

const props = defineProps<{
  item: RouteRecordRaw
  basePath: string
}>()

const router = useRouter()

const onlyOneChild = ref<RouteRecordRaw>()

const hasOneShowingChild = (children: RouteRecordRaw[] | undefined): boolean => {
  if (!children || children.length === 0) return false
  const showingChildren = children.filter(child => !child.meta?.hidden)
  if (showingChildren.length === 1) {
    onlyOneChild.value = showingChildren[0]
    return true
  }
  return false
}

const resolvePath = (routePath: string) => {
  if (routePath.startsWith('/')) return routePath
  return path.resolve(props.basePath, routePath)
}

const getIcon = (icon: string | undefined): string => {
  if (!icon) return ''
  const iconMap: Record<string, string> = {
    dashboard: 'DataAnalysis',
    setting: 'Setting',
    table: 'Grid',
    form: 'Document'
  }
  return iconMap[icon] || 'Monitor'
}

const handleClick = (item: RouteRecordRaw) => {
  router.push(resolvePath(item.path))
}
</script>
