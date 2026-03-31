<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card card">
        <h1 class="register-title">注册</h1>
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="form.username" type="text" placeholder="请输入用户名" required>
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="form.email" type="email" placeholder="请输入邮箱">
          </div>
          <div class="form-group">
            <label>手机号</label>
            <input v-model="form.phone" type="tel" placeholder="请输入手机号">
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="form.password" type="password" placeholder="请输入密码" required>
          </div>
          <div class="form-group">
            <label>确认密码</label>
            <input v-model="form.confirmPassword" type="password" placeholder="请再次输入密码" required>
          </div>
          <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
          <button type="submit" class="btn btn-primary btn-large" :disabled="loading">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </form>
        <div class="register-footer">
          <span>已有账号？</span>
          <router-link to="/login">立即登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { register as registerApi } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const errorMsg = ref('')
const form = ref({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: ''
})

async function handleRegister() {
  if (form.value.password !== form.value.confirmPassword) {
    errorMsg.value = '两次输入的密码不一致'
    return
  }
  
  if (!form.value.username || form.value.username.length < 3) {
    errorMsg.value = '用户名至少3个字符'
    return
  }
  
  if (!form.value.password || form.value.password.length < 6) {
    errorMsg.value = '密码至少6个字符'
    return
  }

  loading.value = true
  errorMsg.value = ''
  
  try {
    const res = await registerApi({
      username: form.value.username,
      email: form.value.email || undefined,
      phone: form.value.phone || undefined,
      password: form.value.password
    }) as any
    const token = res.data?.access_token
    if (!token) throw new Error('No token returned')

    userStore.setToken(token)
    userStore.setUser({ 
      id: 1, 
      username: form.value.username,
      email: form.value.email,
      phone: form.value.phone
    })
    router.push('/')
  } catch (error: any) {
    errorMsg.value = error?.message || '注册失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.register-container {
  width: 100%;
  max-width: 420px;
}

.register-card {
  padding: 40px;
}

.register-title {
  text-align: center;
  font-size: 28px;
  color: #333;
  margin-bottom: 32px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
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

.register-footer {
  text-align: center;
  margin-top: 24px;
  color: #666;
  font-size: 14px;
}

.register-footer a {
  color: #ff6b6b;
  font-weight: 500;
  margin-left: 4px;
}

.register-footer a:hover {
  text-decoration: underline;
}
</style>
