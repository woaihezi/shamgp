import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
  id?: number
  username: string
  email?: string
  phone?: string
  avatar?: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string>('')

  const isLoggedIn = computed(() => !!token.value)

  function setUser(userData: User) {
    user.value = userData
  }

  function setToken(newToken: string) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  function logout() {
    user.value = null
    token.value = ''
    localStorage.removeItem('token')
  }

  function initFromStorage() {
    const savedToken = localStorage.getItem('token')
    if (savedToken) {
      token.value = savedToken
    }
  }

  return {
    user,
    token,
    isLoggedIn,
    setUser,
    setToken,
    logout,
    initFromStorage
  }
})
