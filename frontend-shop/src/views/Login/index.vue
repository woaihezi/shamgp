<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card card">
        <h1 class="login-title">登录</h1>
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="form.username" type="text" placeholder="请输入用户名" required>
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="form.password" type="password" placeholder="请输入密码" required>
          </div>
          <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
          <button type="submit" class="btn btn-primary btn-large" :disabled="loading">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>
        <div class="login-footer">
          <span>还没有账号？</span>
          <router-link to="/register">立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { login as loginApi } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const errorMsg = ref('')
const form = ref({
  username: '',
  password: ''
})

async function handleLogin() {
  loading.value = true
  errorMsg.value = ''

  try {
    const res = await loginApi(form.value) as any
    const token = res.data?.access_token
    if (!token) throw new Error('No token returned')

    userStore.setToken(token)
    userStore.setUser({ id: 1, username: form.value.username })
    router.push('/')
  } catch (error: any) {
    errorMsg.value = error?.message || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}
.login-container {
  width: 100%;
  max-width: 420px;
}
.login-card {
  padding: 40px;
}
.login-title {
  text-align: center;
  font-size: 28px;
  color: #333;
  margin-bottom: 32px;
}
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.form-group label {
  font-size: 14px;
  color: #666;
}
.form-group input {
  padding: 14px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
  outline: none;
  transition: border-color 0.3s;
}
.form-group input:focus {
  border-color: #ff6b6b;
}
.error-msg {
  color: #e74c3c;
  font-size: 13px;
  padding: 8px 12px;
  background: #fdf0ef;
  border-radius: 6px;
}
.btn-large {
  padding: 14px;
  font-size: 16px;
  margin-top: 12px;
}
.btn-large:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.login-footer {
  text-align: center;
  margin-top: 24px;
  color: #666;
  font-size: 14px;
}
.login-footer a {
  color: #ff6b6b;
  font-weight: 500;
  margin-left: 4px;
}
</style>
