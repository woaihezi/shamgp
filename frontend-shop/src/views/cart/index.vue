<template>
  <div class="cart-page">
    <Header />
    <main class="main-content">
      <div class="container">
        <h1 class="page-title">购物车</h1>
        
        <div v-if="cartItems.length > 0" class="cart-content">
          <div class="cart-list">
            <div v-for="item in cartItems" :key="item.id" class="cart-item card">
              <img :src="item.image || 'https://via.placeholder.com/100x100?text=商品'" :alt="item.name" class="item-image">
              <div class="item-info">
                <h3 class="item-name">{{ item.name }}</h3>
                <p class="item-price price">¥{{ item.price.toFixed(2) }}</p>
              </div>
              <div class="item-quantity">
                <button @click="updateQuantity(item.productId, item.quantity - 1)" :disabled="item.quantity <= 1">-</button>
                <span>{{ item.quantity }}</span>
                <button @click="updateQuantity(item.productId, item.quantity + 1)">+</button>
              </div>
              <div class="item-subtotal">
                <span class="price">¥{{ (item.price * item.quantity).toFixed(2) }}</span>
              </div>
              <button class="btn-remove" @click="removeItem(item.productId)">删除</button>
            </div>
          </div>
          
          <div class="cart-summary card">
            <h3>订单摘要</h3>
            <div class="summary-row">
              <span>商品总数:</span>
              <span>{{ totalCount }} 件</span>
            </div>
            <div class="summary-row">
              <span>商品总额:</span>
              <span class="price">¥{{ totalPrice.toFixed(2) }}</span>
            </div>
            <div class="summary-row total">
              <span>总计:</span>
              <span class="price">¥{{ totalPrice.toFixed(2) }}</span>
            </div>
            <div class="cart-actions">
              <button class="btn btn-default" @click="clearCart">清空购物车</button>
              <button class="btn btn-primary" @click="goToCheckout">去结算</button>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-cart">
          <div class="empty-icon">🛒</div>
          <p>购物车是空的</p>
          <router-link to="/products" class="btn btn-primary">去购物</router-link>
        </div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const cartStore = useCartStore()

const cartItems = computed(() => cartStore.items)
const totalPrice = computed(() => cartStore.totalPrice)
const totalCount = computed(() => cartStore.totalCount)

function updateQuantity(productId: number, quantity: number) {
  cartStore.updateQuantity(productId, quantity)
}

function removeItem(productId: number) {
  cartStore.removeItem(productId)
}

function clearCart() {
  if (confirm('确定要清空购物车吗？')) {
    cartStore.clearCart()
  }
}

function goToCheckout() {
  router.push('/checkout')
}
</script>

<style scoped>
.cart-page {
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

.cart-content {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 30px;
  align-items: start;
}

.cart-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cart-item {
  display: grid;
  grid-template-columns: 100px 1fr auto auto auto;
  gap: 20px;
  padding: 20px;
  align-items: center;
}

.item-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
}

.item-info {
  flex: 1;
}

.item-name {
  font-size: 16px;
  color: #333;
  margin-bottom: 8px;
}

.item-price {
  font-size: 18px;
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-quantity button {
  width: 32px;
  height: 32px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s;
}

.item-quantity button:hover:not(:disabled) {
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.item-quantity button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.item-quantity span {
  min-width: 40px;
  text-align: center;
  font-size: 16px;
}

.item-subtotal {
  font-size: 18px;
  min-width: 100px;
  text-align: right;
}

.btn-remove {
  padding: 8px 16px;
  border: none;
  background: none;
  color: #999;
  cursor: pointer;
  font-size: 14px;
  transition: color 0.3s;
}

.btn-remove:hover {
  color: #ff6b6b;
}

.cart-summary {
  padding: 24px;
  position: sticky;
  top: 80px;
}

.cart-summary h3 {
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

.cart-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 24px;
}

.empty-cart {
  text-align: center;
  padding: 80px 0;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.empty-cart p {
  color: #999;
  font-size: 16px;
  margin-bottom: 24px;
}
</style>
