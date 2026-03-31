<template>
  <footer class="footer">
    <div class="container content">
      <div>
        <h3>ShamGP 商城</h3>
        <p>为你提供稳定、简洁的购物体验。</p>
      </div>
      <div class="meta">
        <span>帮助中心</span>
        <span>配送说明</span>
        <span>售后服务</span>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
</script>

<style scoped>
.footer {
  background: #1f2937;
  color: #d1d5db;
  margin-top: 32px;
}

.content {
  min-height: 88px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-top: 12px;
  padding-bottom: 12px;
}

h3 {
  margin: 0 0 6px;
  color: #fff;
  font-size: 16px;
}

p {
  margin: 0;
  font-size: 13px;
}

.meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
}

@media (max-width: 900px) {
  .content {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
