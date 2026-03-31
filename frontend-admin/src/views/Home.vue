<template>
  <div class="home">
    <h2>欢迎来到 Shamgp 后台管理系统</h2>
    <div class="actions">
      <router-link to="/order" class="btn">订单管理</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.home {
  padding: 40px;
  text-align: center;
}
h2 {
  margin-bottom: 32px;
}
.btn {
  display: inline-block;
  padding: 12px 32px;
  background: #409eff;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
  font-size: 16px;
}
.btn:hover {
  background: #66b1ff;
}
</style>
