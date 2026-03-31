<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>关于我们</h3>
          <p>品质商城，为您提供优质的购物体验</p>
        </div>
        <div class="footer-section">
          <h3>客户服务</h3>
          <ul>
            <li><a href="#">帮助中心</a></li>
            <li><a href="#">退换货政策</a></li>
            <li><a href="#">联系我们</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h3>购物指南</h3>
          <ul>
            <li><a href="#">购物流程</a></li>
            <li><a href="#">支付方式</a></li>
            <li><a href="#">配送说明</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2024 商城 版权所有</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
</script>

<style scoped>
.footer {
  background: #333;
  color: #fff;
  padding: 40px 0 20px;
  margin-top: 40px;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid #555;
}

.footer-section h3 {
  margin-bottom: 20px;
  font-size: 16px;
}

.footer-section p {
  color: #aaa;
  font-size: 14px;
  line-height: 1.6;
}

.footer-section ul {
  list-style: none;
}

.footer-section ul li {
  margin-bottom: 10px;
}

.footer-section ul li a {
  color: #aaa;
  font-size: 14px;
  transition: color 0.3s;
}

.footer-section ul li a:hover {
  color: #fff;
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  color: #aaa;
  font-size: 14px;
}
</style>
