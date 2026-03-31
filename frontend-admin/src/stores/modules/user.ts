import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi, getUserInfo, logout as logoutApi, type LoginParams } from '@/api'
import { setToken as saveToken, removeToken, getToken } from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(getToken() || '')
  const name = ref('')
  const avatar = ref('')
  const roles = ref<string[]>([])
  const permissions = ref<string[]>([])

  const setTokenValue = (newToken: string) => {
    token.value = newToken
  }

  const setName = (newName: string) => {
    name.value = newName
  }

  const setAvatar = (newAvatar: string) => {
    avatar.value = newAvatar
  }

  const setRoles = (newRoles: string[]) => {
    roles.value = newRoles
  }

  const setPermissions = (newPermissions: string[]) => {
    permissions.value = newPermissions
  }

  const resetUser = () => {
    token.value = ''
    name.value = ''
    avatar.value = ''
    roles.value = []
    permissions.value = []
    removeToken()
  }

  async function doLogin(loginForm: LoginParams) {
    try {
      const res = await loginApi(loginForm)
      const accessToken = res.data.access_token || res.data.accessToken
      token.value = accessToken
      saveToken(accessToken)
      return res
    } catch (error) {
      throw error
    }
  }

  async function getInfo() {
    try {
      const res = await getUserInfo()
      const userInfo = res.data
      name.value = userInfo.nickname || userInfo.username
      avatar.value = userInfo.avatar || ''
      roles.value = userInfo.roles || []
      permissions.value = userInfo.permissions || []
      return res
    } catch (error) {
      throw error
    }
  }

  async function doLogout() {
    try {
      await logoutApi()
    } finally {
      resetUser()
    }
  }

  return {
    token,
    name,
    avatar,
    roles,
    permissions,
    setToken: setTokenValue,
    setName,
    setAvatar,
    setRoles,
    setPermissions,
    resetUser,
    doLogin,
    getInfo,
    doLogout
  }
})
