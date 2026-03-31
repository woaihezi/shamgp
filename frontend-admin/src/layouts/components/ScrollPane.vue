<template>
  <div class="scroll-container" ref="scrollContainer" @wheel.prevent="handleScroll">
    <div class="scroll-wrapper" ref="scrollWrapper" :style="{ left: `${left}px` }">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

const scrollContainer = ref<HTMLElement>()
const scrollWrapper = ref<HTMLElement>()
const left = ref(0)
const rightBtn = ref<HTMLElement>()

const handleScroll = (e: WheelEvent) => {
  const eventDelta = e.wheelDelta || -e.deltaY * 40
  const $scrollWrapper = scrollWrapper.value
  const $scrollContainer = scrollContainer.value
  if ($scrollWrapper && $scrollContainer) {
    const scrollWrapperWidth = $scrollWrapper.offsetWidth
    const currentOffset = left.value
    const containerWidth = $scrollContainer.offsetWidth
    const delta = eventDelta < 0 ? -100 : 100
    let newLeft = currentOffset + delta
    if (newLeft > 0) {
      newLeft = 0
    }
    if (containerWidth - newLeft > scrollWrapperWidth) {
      newLeft = containerWidth - scrollWrapperWidth
    }
    left.value = newLeft
  }
}
</script>

<style lang="scss" scoped>
.scroll-container {
  white-space: nowrap;
  position: relative;
  overflow: hidden;
  width: 100%;

  .scroll-wrapper {
    position: absolute;
  }
}
</style>
