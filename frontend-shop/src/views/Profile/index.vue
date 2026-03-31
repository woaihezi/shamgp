<template>
  <div class="profile-page">
    <Header />
    <main class="main-content">
      <div class="container">
        <h1 class="page-title">个人中心</h1>
        
        <div class="profile-content">
          <div class="profile-info card">
            <div class="profile-header">
              <div class="avatar">
                {{ user?.username?.charAt(0)?.toUpperCase() || 'U' }}
              </div>
              <div class="user-info">
                <h2 class="username">{{ user?.username || '未登录' }}</h2>
                <p class="user-email">{{ user?.email || '未设置邮箱' }}</p>
                <p class="user-phone">{{ user?.phone || '未设置手机号' }}</p>
              </div>
            </div>
          </div>

          <div class="profile-menu card">
            <h3>我的账户</h3>
            <div class="menu-list">
              <router-link to="/orders" class="menu-item">
                <span class="menu-icon">📦</span>
                <span>我的订单</span>
                <span class="menu-arrow">&rarr;</span>
              </router-link>
              <router-link to="/cart" class="menu-item">
                <span class="menu-icon">🛒</span>
                <span>购物车</span>
                <span class="menu-arrow">&rarr;</span>
              </router-link>
              <div class="menu-item">
                <span class="menu-icon">⚙️</span>
                <span>账户设置</span>
                <span class="menu-arrow">&rarr;</span>
              </div>
              <div class="menu-item">
                <span class="menu-icon">📍</span>
                <span>收货地址</span>
                <span class="menu-arrow">&rarr;</span>
              </div>
            </div>
          </div>

          <div class="profile-stats card">
            <h3>统计数据</h3>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">{{ orderCount }}</div>
                <div class="stat-label">订单数</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">¥{{ totalSpent.toFixed(2) }}</div>
                <div class="stat-label">累计消费</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ favoriteCount }}</div>
                <div class="stat-label">收藏商品</div>
              </div>
            </div>
          </div>

          <div class="profile-actions">
            <template v-if="isLoggedIn">
              <button class="btn btn-default" @click="handleLogout">退出登录</button>
            </template>
            <template v-else>
              <router-link to="/login" class="btn btn-primary">立即登录</router-link>
              <router-link to="/register" class="btn btn-default">注册账号</router-link>
            </template>
          </div>
        </div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const isLoggedIn = computed(() => userStore.isLoggedIn)
const user = computed(() => userStore.user)

const orderCount = ref(5)
const totalSpent = ref(28796)
const favoriteCount = ref(12)

function handleLogout() {
  userStore.logout()
  router.push('/')
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 40px 0;
}

.page-title {
  font-size: 28px;
  color: #333;
  margin-bottom: 30px;
}

.profile-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.profile-info,
.profile-menu,
.profile-stats {
  padding: 24px;
}

.profile-info {
  grid-column: 1 / -1;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
  color: white;
  font-size: 40px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.username {
  font-size: 24px;
  color: #333;
  margin-bottom: 8px;
}

.user-email,
.user-phone {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.profile-menu h3,
.profile-stats h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
}

.menu-list {
  display: flex;
  flex-direction: column;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #eee;
  transition: color 0.3s;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:hover {
  color: #ff6b6b;
}

.menu-icon {
  font-size: 20px;
  margin-right: 12px;
}

.menu-item span:nth-child(2) {
  flex: 1;
  font-size: 15px;
}

.menu-arrow {
  color: #ccc;
  font-size: 18px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #ff6b6b;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.profile-actions {
  grid-column: 1 / -1;
  display: flex;
  gap: 12px;
  justify-content: center;
}
</style>
