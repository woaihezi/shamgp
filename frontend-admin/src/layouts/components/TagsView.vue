<template>
  <div class="tags-view-container">
    <scroll-pane ref="scrollPaneRef" class="tags-view-wrapper">
      <router-link
        v-for="tag in visitedViews"
        :key="tag.path"
        :class="isActive(tag) ? 'active' : ''"
        :to="{ path: tag.path, query: tag.query, params: tag.params }"
        class="tags-view-item"
        @click.middle="!isAffix(tag) ? closeSelectedTag(tag) : ''"
      >
        {{ tag.title }}
        <span v-if="!isAffix(tag)" class="el-icon-close" @click.prevent.stop="closeSelectedTag(tag)">
          <svg viewBox="0 0 1024 1024" width="14" height="14">
            <path d="M512 64a448 448 0 1 0 448 448A448 448 0 0 0 512 64zm165.44 617.344-45.248 45.248L512 557.248l-120.192 169.344-45.248-45.248L466.752 512l-120.192-120.192 45.248-45.248L512 466.752l120.192-120.192 45.248 45.248L557.248 512z" />
          </svg>
        </span>
      </router-link>
    </scroll-pane>
    <div class="tags-view-right-menu">
      <el-dropdown trigger="click" @command="handleTagsViewContextMenu">
        <div class="tags-view-contextmenu-icon">
          <el-icon><ArrowDown /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="refresh">刷新</el-dropdown-item>
            <el-dropdown-item command="close">关闭当前</el-dropdown-item>
            <el-dropdown-item command="closeOthers">关闭其他</el-dropdown-item>
            <el-dropdown-item command="closeAll">关闭所有</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter, type RouteLocationNormalized } from 'vue-router'
import { ArrowDown } from '@element-plus/icons-vue'
import ScrollPane from './ScrollPane.vue'
import { useTagsViewStore, type TagView } from '@/stores'

const route = useRoute()
const router = useRouter()
const tagsViewStore = useTagsViewStore()
const scrollPaneRef = ref()

const visitedViews = computed(() => tagsViewStore.visitedViews)

const isActive = (route: TagView) => {
  return route.path === route.path
}

const isAffix = (tag: TagView) => {
  return tag.meta?.affix
}

const closeSelectedTag = (view: TagView) => {
  tagsViewStore.delView(view).then(({ visitedViews }) => {
    if (isActive(route)) {
      toLastView(visitedViews as TagView[])
    }
  })
}

const toLastView = (visitedViews: TagView[]) => {
  const latestView = visitedViews.slice(-1)[0]
  if (latestView) {
    router.push(latestView.fullPath || '/dashboard')
  } else {
    router.push('/dashboard')
  }
}

const refreshSelectedTag = (view: RouteLocationNormalized) => {
  tagsViewStore.delCachedView(view)
  const { fullPath } = view
  router.replace('/redirect' + fullPath)
}

const closeOthersTags = () => {
  tagsViewStore.delOthersViews(route)
}

const closeAllTags = () => {
  tagsViewStore.delAllViews().then(({ visitedViews }) => {
    toLastView(visitedViews as TagView[])
  })
}

const handleTagsViewContextMenu = (command: string) => {
  switch (command) {
    case 'refresh':
      refreshSelectedTag(route)
      break
    case 'close':
      closeSelectedTag(route)
      break
    case 'closeOthers':
      closeOthersTags()
      break
    case 'closeAll':
      closeAllTags()
      break
  }
}
</script>

<style lang="scss" scoped>
.tags-view-container {
  height: 34px;
  width: 100%;
  background: #fff;
  border-bottom: 1px solid #d8dce5;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.12);
  display: flex;
}

.tags-view-wrapper {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
}

.tags-view-item {
  display: inline-block;
  position: relative;
  cursor: pointer;
  height: 26px;
  line-height: 26px;
  border: 1px solid #d8dce5;
  color: #495060;
  background: #fff;
  padding: 0 8px;
  font-size: 12px;
  margin-left: 5px;
  margin-top: 4px;
  text-decoration: none;

  &:first-of-type {
    margin-left: 15px;
  }

  &:hover {
    color: #409eff;
  }

  &.active {
    background-color: #409eff;
    color: #fff;
    border-color: #409eff;

    &::before {
      content: '';
      background: #fff;
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      position: relative;
      margin-right: 4px;
    }
  }
}

.tags-view-right-menu {
  display: flex;
  align-items: center;
  padding-right: 10px;
  border-left: 1px solid #d8dce5;
}

.tags-view-contextmenu-icon {
  cursor: pointer;
  padding: 0 5px;
  height: 100%;
  display: flex;
  align-items: center;
}
</style>
