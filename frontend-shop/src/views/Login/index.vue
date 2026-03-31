<template>
  <div class="auth-page">
    <div class="auth-card card">
      <h1>登录</h1>
      <p class="subtitle">使用账号密码登录商城</p>

      <form class="auth-form" @submit.prevent="handleLogin">
        <label class="field">
          <span>用户名</span>
          <input v-model.trim="form.username" type="text" placeholder="请输入用户名" autocomplete="username" required />
        </label>

        <label class="field">
          <span>密码</span>
          <input v-model="form.password" type="password" placeholder="请输入密码" autocomplete="current-password" required />
        </label>

        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

        <button class="btn btn-primary submit-btn" type="submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <p class="footer-text">
        没有账号？
        <router-link to="/register">去注册</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getUserInfo, login as loginApi } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const errorMsg = ref('')
const form = reactive({
  username: '',
  password: ''
})

async function handleLogin() {
  loading.value = true
  errorMsg.value = ''

  try {
    const loginRes = await loginApi({ username: form.username, password: form.password }) as any
    const token = loginRes?.data?.access_token
    if (!token) throw new Error('登录成功但未返回 token')

    userStore.setToken(token)

    try {
      const userRes = await getUserInfo() as any
      userStore.setUser(userRes?.data || { username: form.username })
    } catch {
      userStore.setUser({ username: form.username })
    }

    router.replace('/')
  } catch (error: any) {
    errorMsg.value = error?.response?.data?.detail || error?.message || '登录失败，请检查账号或密码'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - 120px);
  display: grid;
  place-items: center;
  padding: 24px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  padding: 28px;
}

h1 {
  margin: 0;
  font-size: 28px;
  color: #222;
}

.subtitle {
  margin: 8px 0 20px;
  color: #666;
  font-size: 14px;
}

.auth-form {
  display: grid;
  gap: 14px;
}

.field {
  display: grid;
  gap: 8px;
}

.field span {
  font-size: 14px;
  color: #444;
}

.field input {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 12px;
  font-size: 15px;
  outline: none;
}

.field input:focus {
  border-color: #ff6b6b;
}

.error {
  margin: 0;
  font-size: 13px;
  color: #d93025;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  font-size: 15px;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.footer-text {
  margin: 14px 0 0;
  color: #666;
  text-align: center;
}

.footer-text a {
  color: #ff6b6b;
}
</style>
