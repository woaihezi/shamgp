<template>
  <header class="header">
    <div class="container bar">
      <router-link class="logo" to="/">ShamGP</router-link>

      <nav class="nav">
        <router-link to="/">首页</router-link>
        <router-link to="/products">商品</router-link>
        <router-link to="/cart">购物车</router-link>
        <router-link to="/orders">订单</router-link>
      </nav>

      <div class="actions">
        <template v-if="isLoggedIn">
          <router-link to="/profile">{{ displayName }}</router-link>
          <button class="logout" type="button" @click="handleLogout">退出</button>
        </template>
        <template v-else>
          <router-link to="/login">登录</router-link>
          <router-link to="/register">注册</router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const isLoggedIn = computed(() => userStore.isLoggedIn)
const displayName = computed(() => userStore.user?.nickname || userStore.user?.username || '用户')

function handleLogout() {
  userStore.logout()
  router.push('/login')
}

onMounted(() => {
  userStore.initFromStorage()
})
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  border-bottom: 1px solid #ececec;
}

.bar {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  color: #ff5a3c;
}

.nav {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav a {
  color: #333;
}

.nav a.router-link-active {
  color: #ff5a3c;
  font-weight: 600;
}

.actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

.actions a {
  color: #333;
}

.logout {
  border: none;
  background: transparent;
  cursor: pointer;
  color: #666;
  padding: 0;
}

@media (max-width: 900px) {
  .bar {
    flex-wrap: wrap;
    height: auto;
    padding: 10px 0;
  }

  .nav {
    width: 100%;
    order: 3;
    overflow-x: auto;
    padding-bottom: 4px;
  }
}
</style>
