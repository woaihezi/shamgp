import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const sidebar = ref({
    opened: true,
    withoutAnimation: false
  })
  const device = ref('desktop')
  const size = ref('default')

  const toggleSidebar = () => {
    sidebar.value.opened = !sidebar.value.opened
    sidebar.value.withoutAnimation = false
  }

  const closeSidebar = (withoutAnimation: boolean) => {
    sidebar.value.opened = false
    sidebar.value.withoutAnimation = withoutAnimation
  }

  const toggleDevice = (newDevice: string) => {
    device.value = newDevice
  }

  const setSize = (newSize: string) => {
    size.value = newSize
  }

  return {
    sidebar,
    device,
    size,
    toggleSidebar,
    closeSidebar,
    toggleDevice,
    setSize
  }
})
