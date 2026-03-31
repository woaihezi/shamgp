import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login, getUserInfo, logout as apiLogout, UserInfo, LoginParams } from '@/api'
import { setToken, removeToken, getToken } from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(getToken())
  const userInfo = ref<UserInfo | null>(null)

  async function doLogin(data: LoginParams) {
    const res = await login(data)
    const accessToken = res.data.access_token
    token.value = accessToken
    setToken(accessToken)
    return accessToken
  }

  async function getInfo() {
    const res = await getUserInfo()
    userInfo.value = res.data
    return res.data
  }

  async function doLogout() {
    await apiLogout()
    token.value = null
    userInfo.value = null
    removeToken()
  }

  function resetToken() {
    token.value = null
    userInfo.value = null
    removeToken()
  }

  return {
    token,
    userInfo,
    doLogin,
    getInfo,
    doLogout,
    resetToken
  }
})
