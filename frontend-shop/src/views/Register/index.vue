<template>
  <div class="auth-page">
    <div class="auth-card card">
      <h1>注册</h1>
      <p class="subtitle">创建新账号后即可下单与查看订单</p>

      <form class="auth-form" @submit.prevent="handleRegister">
        <label class="field">
          <span>用户名</span>
          <input v-model.trim="form.username" type="text" placeholder="至少 3 个字符" required />
        </label>

        <label class="field">
          <span>邮箱</span>
          <input v-model.trim="form.email" type="email" placeholder="可选" />
        </label>

        <label class="field">
          <span>手机号</span>
          <input v-model.trim="form.phone" type="tel" placeholder="可选" />
        </label>

        <label class="field">
          <span>密码</span>
          <input v-model="form.password" type="password" placeholder="至少 6 位" required />
        </label>

        <label class="field">
          <span>确认密码</span>
          <input v-model="form.confirmPassword" type="password" placeholder="再次输入密码" required />
        </label>

        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

        <button class="btn btn-primary submit-btn" type="submit" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>

      <p class="footer-text">
        已有账号？
        <router-link to="/login">去登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { register as registerApi } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const errorMsg = ref('')
const form = reactive({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: ''
})

function validate() {
  if (form.username.length < 3) {
    errorMsg.value = '用户名至少 3 个字符'
    return false
  }
  if (form.password.length < 6) {
    errorMsg.value = '密码至少 6 位'
    return false
  }
  if (form.password !== form.confirmPassword) {
    errorMsg.value = '两次输入的密码不一致'
    return false
  }
  return true
}

async function handleRegister() {
  errorMsg.value = ''
  if (!validate()) return
  loading.value = true

  try {
    const res = await registerApi({
      username: form.username,
      password: form.password,
      email: form.email || undefined,
      phone: form.phone || undefined
    }) as any

    const token = res?.data?.access_token
    if (!token) throw new Error('注册成功但未返回 token')

    userStore.setToken(token)
    userStore.setUser({
      username: form.username,
      email: form.email || undefined,
      phone: form.phone || undefined
    })
    router.replace('/')
  } catch (error: any) {
    errorMsg.value = error?.response?.data?.detail || error?.message || '注册失败，请稍后重试'
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
