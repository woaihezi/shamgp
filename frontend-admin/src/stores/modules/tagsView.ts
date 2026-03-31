import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { RouteLocationNormalized } from 'vue-router'

export interface TagView extends Partial<RouteLocationNormalized> {
  title?: string
}

export const useTagsViewStore = defineStore('tagsView', () => {
  const visitedViews = ref<TagView[]>([])
  const cachedViews = ref<string[]>([])

  const addView = (view: TagView) => {
    addVisitedView(view)
    addCachedView(view)
  }

  const addVisitedView = (view: TagView) => {
    if (visitedViews.value.some(v => v.path === view.path)) return
    visitedViews.value.push({
      path: view.path,
      name: view.name,
      meta: view.meta,
      query: view.query,
      params: view.params,
      fullPath: view.fullPath,
      title: view.meta?.title || 'no-name'
    })
  }

  const addCachedView = (view: TagView) => {
    if (typeof view.name !== 'string') return
    if (cachedViews.value.includes(view.name)) return
    if (!view.meta?.noCache) {
      cachedViews.value.push(view.name)
    }
  }

  const delView = (view: TagView) => {
    return new Promise(resolve => {
      delVisitedView(view)
      delCachedView(view)
      resolve({
        visitedViews: [...visitedViews.value],
        cachedViews: [...cachedViews.value]
      })
    })
  }

  const delVisitedView = (view: TagView) => {
    const index = visitedViews.value.findIndex(v => v.path === view.path)
    if (index > -1) {
      visitedViews.value.splice(index, 1)
    }
  }

  const delCachedView = (view: TagView) => {
    if (typeof view.name !== 'string') return
    const index = cachedViews.value.indexOf(view.name)
    if (index > -1) {
      cachedViews.value.splice(index, 1)
    }
  }

  const delOthersViews = (view: TagView) => {
    delOthersVisitedViews(view)
    delOthersCachedViews(view)
  }

  const delOthersVisitedViews = (view: TagView) => {
    visitedViews.value = visitedViews.value.filter(v => {
      return v.meta?.affix || v.path === view.path
    })
  }

  const delOthersCachedViews = (view: TagView) => {
    if (typeof view.name !== 'string') return
    cachedViews.value = cachedViews.value.filter(v => {
      return v !== view.name
    })
  }

  const delAllViews = () => {
    return new Promise(resolve => {
      visitedViews.value = visitedViews.value.filter(v => v.meta?.affix)
      cachedViews.value = []
      resolve({
        visitedViews: [...visitedViews.value],
        cachedViews: [...cachedViews.value]
      })
    })
  }

  return {
    visitedViews,
    cachedViews,
    addView,
    addVisitedView,
    addCachedView,
    delView,
    delVisitedView,
    delCachedView,
    delOthersViews,
    delOthersVisitedViews,
    delOthersCachedViews,
    delAllViews
  }
})
