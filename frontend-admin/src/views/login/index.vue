<template>
  <div class="login-page">
    <div class="login-left">
      <div class="brand">
        <div class="brand-logo">
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
            <rect width="40" height="40" rx="8" fill="#4a9eff"/>
            <path d="M12 20L18 26L28 14" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <span class="brand-name">SHAMGP</span>
      </div>
      <div class="left-content">
        <h1>高效管理<br/>轻松运营</h1>
        <p>专业的电商后台管理系统，助力企业数字化转型</p>
      </div>
    </div>

    <div class="login-right">
      <div class="login-card">
        <div class="login-card-header">
          <h2>管理员登录</h2>
          <p>欢迎回来，请输入您的账号信息</p>
        </div>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-position="top"
          @submit.prevent="handleLogin"
        >
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              size="large"
              :prefix-icon="User"
              clearable
            />
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              :prefix-icon="Lock"
              show-password
              clearable
            />
          </el-form-item>

          <el-form-item v-if="errorMsg">
            <div class="error-tip">
              <el-icon><CircleCloseFilled /></el-icon>
              <span>{{ errorMsg }}</span>
            </div>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="login-btn"
              native-type="submit"
            >
              {{ loading ? '登录中...' : '登 录' }}
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { User, Lock, CircleCloseFilled } from '@element-plus/icons-vue'
import { login } from '@/api/auth'
import { useAdminStore } from '@/stores/admin'

const router = useRouter()
const adminStore = useAdminStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const errorMsg = ref('')

const form = reactive({
  username: '',
  password: ''
})

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

async function handleLogin() {
  if (!formRef.value) return
  errorMsg.value = ''

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      const res: any = await login(form)
      const token = res.data?.access_token
      if (!token) {
        errorMsg.value = '登录失败：未获取到令牌'
        return
      }
      adminStore.setToken(token)
      ElMessage.success('登录成功')
      router.push('/')
    } catch (err: any) {
      errorMsg.value = err?.response?.data?.message || err?.message || '登录失败，请检查用户名和密码'
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-page {
  display: flex;
  min-height: 100vh;
  background: #0f0f1a;
}

/* Left panel */
.login-left {
  width: 45%;
  background: #1a1a2e;
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.login-left::before {
  content: '';
  position: absolute;
  top: -200px;
  left: -200px;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(74, 158, 255, 0.08) 0%, transparent 70%);
  pointer-events: none;
}

.login-left::after {
  content: '';
  position: absolute;
  bottom: -150px;
  right: -100px;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(123, 97, 255, 0.06) 0%, transparent 70%);
  pointer-events: none;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1;
}

.brand-name {
  font-size: 22px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 2px;
}

.left-content {
  z-index: 1;
}

.left-content h1 {
  font-size: 42px;
  font-weight: 700;
  color: #fff;
  line-height: 1.3;
  margin: 0 0 20px;
}

.left-content p {
  font-size: 15px;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.8;
  margin: 0;
}

/* Right panel */
.login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: #ffffff;
}

.login-card {
  width: 100%;
  max-width: 420px;
}

.login-card-header {
  margin-bottom: 36px;
}

.login-card-header h2 {
  font-size: 26px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0 0 8px;
}

.login-card-header p {
  font-size: 14px;
  color: #8c8c8c;
  margin: 0;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #333;
}

:deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #e8e8e8 inset;
  transition: box-shadow 0.2s;
}

:deep(.el-input__wrapper:hover),
:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #4a9eff inset;
}

.error-tip {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #f56c6c;
  font-size: 13px;
  background: #fef0f0;
  padding: 8px 12px;
  border-radius: 6px;
  width: 100%;
}

.login-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
  font-weight: 600;
  background: #1a1a2e;
  border: none;
  border-radius: 8px;
  transition: background 0.2s;
}

.login-btn:hover {
  background: #2a2a4e !important;
}

@media (max-width: 768px) {
  .login-left {
    display: none;
  }
  .login-right {
    width: 100%;
  }
}
</style>
