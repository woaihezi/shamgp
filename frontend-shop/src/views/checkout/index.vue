<template>
  <div class="checkout-page">
    <Header />
    <main class="main-content">
      <div class="container">
        <h1 class="page-title">确认订单</h1>
        
        <div v-if="cartItems.length > 0" class="checkout-content">
          <div class="checkout-left">
            <div class="address-section card">
              <h3>收货地址</h3>
              <div class="address-form">
                <div class="form-group">
                  <label>收货人</label>
                  <input v-model="form.name" type="text" placeholder="请输入收货人姓名">
                </div>
                <div class="form-group">
                  <label>手机号</label>
                  <input v-model="form.phone" type="text" placeholder="请输入手机号">
                </div>
                <div class="form-group full">
                  <label>详细地址</label>
                  <textarea v-model="form.address" placeholder="请输入详细地址"></textarea>
                </div>
              </div>
            </div>

            <div class="order-items-section card">
              <h3>商品清单</h3>
              <div class="order-items">
                <div v-for="item in cartItems" :key="item.id" class="order-item">
                  <img :src="item.image || 'https://via.placeholder.com/80x80?text=商品'" :alt="item.name" class="item-image">
                  <div class="item-info">
                    <h4 class="item-name">{{ item.name }}</h4>
                    <p class="item-price price">¥{{ item.price.toFixed(2) }}</p>
                  </div>
                  <span class="item-quantity">x{{ item.quantity }}</span>
                  <span class="item-subtotal price">¥{{ (item.price * item.quantity).toFixed(2) }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="checkout-right">
            <div class="order-summary card">
              <h3>订单摘要</h3>
              <div class="summary-row">
                <span>商品总额</span>
                <span>¥{{ totalPrice.toFixed(2) }}</span>
              </div>
              <div class="summary-row">
                <span>运费</span>
                <span>¥0.00</span>
              </div>
              <div class="summary-row total">
                <span>应付总额</span>
                <span class="price">¥{{ totalPrice.toFixed(2) }}</span>
              </div>
              <button class="btn btn-primary btn-large" @click="handleSubmitOrder" style="width: 100%; margin-top: 20px;">
                提交订单
              </button>
              <router-link to="/cart" class="btn btn-default" style="width: 100%; text-align: center; margin-top: 12px;">
                返回购物车
              </router-link>
            </div>
          </div>
        </div>

        <div v-else class="empty-checkout">
          <p>购物车是空的，请先添加商品</p>
          <router-link to="/products" class="btn btn-primary">去购物</router-link>
        </div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { useCartStore } from '@/stores/cart'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const cartStore = useCartStore()
const userStore = useUserStore()

const cartItems = computed(() => cartStore.items)
const totalPrice = computed(() => cartStore.totalPrice)

const form = ref({
  name: '',
  phone: '',
  address: ''
})

function handleSubmitOrder() {
  if (!userStore.isLoggedIn) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  if (!form.value.name || !form.value.phone || !form.value.address) {
    alert('请填写完整的收货信息')
    return
  }

  alert('订单提交成功！')
  cartStore.clearCart()
  router.push('/orders')
}
</script>

<style scoped>
.checkout-page {
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

.checkout-content {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 30px;
  align-items: start;
}

.checkout-left {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.address-section,
.order-items-section {
  padding: 24px;
}

.address-section h3,
.order-items-section h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
}

.address-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: 14px;
  color: #666;
}

.form-group input,
.form-group textarea {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #ff6b6b;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.order-item {
  display: grid;
  grid-template-columns: 80px 1fr auto auto;
  gap: 16px;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
}

.item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
}

.item-name {
  font-size: 14px;
  color: #333;
  margin-bottom: 4px;
}

.item-price {
  font-size: 14px;
}

.item-quantity {
  color: #666;
  font-size: 14px;
}

.item-subtotal {
  font-size: 16px;
  font-weight: bold;
}

.checkout-right {
  position: sticky;
  top: 80px;
}

.order-summary {
  padding: 24px;
}

.order-summary h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  color: #666;
}

.summary-row.total {
  border-top: 1px solid #eee;
  padding-top: 16px;
  margin-top: 12px;
  font-size: 18px;
  color: #333;
}

.summary-row.total .price {
  font-size: 24px;
}

.btn-large {
  padding: 14px 20px;
  font-size: 16px;
}

.empty-checkout {
  text-align: center;
  padding: 80px 0;
}

.empty-checkout p {
  color: #999;
  font-size: 16px;
  margin-bottom: 24px;
}
</style>
