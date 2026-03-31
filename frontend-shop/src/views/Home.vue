<template>
  <div class="home">
    <h2>欢迎来到 Shamgp 商城</h2>
    <div class="actions">
      <router-link to="/cart" class="btn">查看购物车</router-link>
      <router-link to="/order/list" class="btn">查看订单</router-link>
    </div>
    <div class="info">
      <p>测试账号: testuser</p>
      <p>测试地址已预置，请直接前往购物车和订单页面测试功能</p>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.home {
  text-align: center;
  padding: 60px 20px;
}
h2 {
  font-size: 32px;
  color: #333;
  margin-bottom: 40px;
}
.actions {
  margin-bottom: 40px;
}
.btn {
  display: inline-block;
  padding: 12px 32px;
  background: #ff6600;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
  margin: 0 10px;
  font-size: 16px;
}
.btn:hover {
  background: #e55a00;
}
.info {
  color: #666;
  line-height: 1.8;
}
</style>
