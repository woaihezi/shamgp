import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref('')
  const name = ref('Admin')
  const avatar = ref('')

  const setToken = (newToken: string) => {
    token.value = newToken
  }

  const setName = (newName: string) => {
    name.value = newName
  }

  const setAvatar = (newAvatar: string) => {
    avatar.value = newAvatar
  }

  const resetUser = () => {
    token.value = ''
    name.value = 'Admin'
    avatar.value = ''
  }

  return {
    token,
    name,
    avatar,
    setToken,
    setName,
    setAvatar,
    resetUser
  }
})
