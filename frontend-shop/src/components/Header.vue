<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <router-link to="/" class="logo">商城</router-link>
        <nav class="nav">
          <router-link to="/">首页</router-link>
          <router-link to="/category">分类</router-link>
          <router-link to="/products">商品</router-link>
        </nav>
        <div class="user-actions">
          <router-link to="/cart" class="cart-link">
            <span>购物车</span>
            <span v-if="cartCount > 0" class="cart-badge">{{ cartCount }}</span>
          </router-link>
          <template v-if="isLoggedIn">
            <router-link to="/orders">我的订单</router-link>
            <router-link to="/profile">个人中心</router-link>
            <a href="javascript:void(0)" @click="handleLogout">退出</a>
          </template>
          <template v-else>
            <router-link to="/login">登录</router-link>
            <router-link to="/register">注册</router-link>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const userStore = useUserStore()
const cartStore = useCartStore()

const isLoggedIn = computed(() => userStore.isLoggedIn)
const cartCount = computed(() => cartStore.totalCount)

function handleLogout() {
  userStore.logout()
  router.push('/')
}

onMounted(() => {
  userStore.initFromStorage()
  cartStore.loadFromStorage()
})
</script>

<style scoped>
.header {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #ff6b6b;
}

.nav {
  display: flex;
  gap: 30px;
}

.nav a {
  color: #333;
  transition: color 0.3s;
}

.nav a:hover,
.nav a.router-link-active {
  color: #ff6b6b;
}

.user-actions {
  display: flex;
  gap: 20px;
  align-items: center;
}

.user-actions a {
  color: #333;
  transition: color 0.3s;
}

.user-actions a:hover {
  color: #ff6b6b;
}

.cart-link {
  position: relative;
}

.cart-badge {
  position: absolute;
  top: -8px;
  right: -12px;
  background: #ff6b6b;
  color: white;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}
</style>
