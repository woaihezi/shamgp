import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login, logout as apiLogout, getUserInfo, UserInfo } from '@/api/auth'

export const useAdminStore = defineStore('admin', () => {
  const token = ref<string | null>(null)
  const user = ref<UserInfo | null>(null)

  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('access_token', newToken)
  }

  function logout() {
    apiLogout().finally(() => {
      token.value = null
      user.value = null
      localStorage.removeItem('access_token')
    })
  }

  function initFromStorage() {
    token.value = localStorage.getItem('access_token')
  }

  async function fetchUserInfo() {
    const res = await getUserInfo()
    user.value = res.data
    return res.data
  }

  return { token, user, setToken, logout, initFromStorage, fetchUserInfo }
})
