<template>
  <div id="app">
    <header class="header">
      <div class="container">
        <h1 class="logo">Shamgp 商城</h1>
        <nav class="nav">
          <router-link to="/">首页</router-link>
          <router-link to="/cart">购物车</router-link>
          <router-link to="/order/list">我的订单</router-link>
        </nav>
      </div>
    </header>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 0;
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}
.logo {
  font-size: 24px;
  color: #ff6600;
  margin: 0;
}
.nav a {
  margin-left: 24px;
  text-decoration: none;
  color: #333;
  font-size: 16px;
}
.nav a:hover {
  color: #ff6600;
}
.nav a.router-link-active {
  color: #ff6600;
  font-weight: 600;
}
.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>
