<template>
  <div class="cart">
    <h2>购物车</h2>
    
    <div v-if="loading" class="loading">加载中...</div>
    
    <div v-else-if="!cartSummary || cartSummary.total_items === 0" class="empty">
      <p>购物车是空的</p>
      <div class="demo-section">
        <h3>演示：添加测试商品到购物车</h3>
        <div class="demo-products">
          <button v-for="product in demoProducts" :key="product.id" @click="addDemoProduct(product)" class="btn btn-small">
            {{ product.name }} - ¥{{ product.price }}
          </button>
        </div>
      </div>
    </div>
    
    <div v-else>
      <div class="cart-items">
        <div v-for="item in cartSummary.selected_items" :key="item.id" class="cart-item">
          <div class="item-info">
            <input 
              type="checkbox" 
              :checked="item.selected" 
              @change="toggleItem(item)"
            />
            <div class="item-name">{{ item.product_name || `商品 #${item.product_id}` }}</div>
            <div class="item-price">¥{{ (item.product_price || 0).toFixed(2) }}</div>
            <div class="item-quantity">
              <button @click="updateQuantity(item, -1)" class="btn-quantity">-</button>
              <span>{{ item.quantity }}</span>
              <button @click="updateQuantity(item, 1)" class="btn-quantity">+</button>
            </div>
            <div class="item-total">¥{{ ((item.product_price || 0) * item.quantity).toFixed(2) }}</div>
            <button @click="removeItem(item)" class="btn-remove">删除</button>
          </div>
        </div>
      </div>
      
      <div class="cart-footer">
        <div class="cart-total">
          合计: <span class="total-amount">¥{{ cartSummary.total_amount.toFixed(2) }}</span>
        </div>
        <div class="cart-actions">
          <button @click="clearCart" class="btn btn-outline">清空购物车</button>
          <router-link to="/checkout" class="btn btn-primary">去结算</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { cartApi, type CartSummary, type CartItem } from '@/api/cart'

const loading = ref(true)
const cartSummary = ref<CartSummary | null>(null)

const demoProducts = [
  { id: 1, name: 'iPhone 15 Pro', price: 8999 },
  { id: 2, name: 'Samsung Galaxy S24', price: 6999 },
  { id: 3, name: 'MacBook Pro 14', price: 14999 },
  { id: 4, name: 'ThinkPad X1 Carbon', price: 9999 }
]

const loadCart = async () => {
  try {
    loading.value = true
    const res = await cartApi.getSummary()
    if (res.code === 200) {
      cartSummary.value = res.data
    }
  } catch (error) {
    console.error('Failed to load cart:', error)
  } finally {
    loading.value = false
  }
}

const addDemoProduct = async (product: any) => {
  try {
    await cartApi.addItem({
      product_id: product.id,
      quantity: 1
    })
    await loadCart()
  } catch (error) {
    console.error('Failed to add item:', error)
  }
}

const toggleItem = async (item: CartItem) => {
  try {
    await cartApi.updateItem(item.id, { selected: !item.selected })
    await loadCart()
  } catch (error) {
    console.error('Failed to toggle item:', error)
  }
}

const updateQuantity = async (item: CartItem, delta: number) => {
  const newQuantity = item.quantity + delta
  if (newQuantity < 1) return
  
  try {
    await cartApi.updateItem(item.id, { quantity: newQuantity })
    await loadCart()
  } catch (error) {
    console.error('Failed to update quantity:', error)
  }
}

const removeItem = async (item: CartItem) => {
  try {
    await cartApi.removeItem(item.id)
    await loadCart()
  } catch (error) {
    console.error('Failed to remove item:', error)
  }
}

const clearCart = async () => {
  if (!confirm('确定要清空购物车吗？')) return
  
  try {
    await cartApi.clearCart()
    await loadCart()
  } catch (error) {
    console.error('Failed to clear cart:', error)
  }
}

onMounted(() => {
  loadCart()
})
</script>

<style scoped>
.cart {
  padding: 20px 0;
}
h2 {
  margin-bottom: 24px;
}
.loading, .empty {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}
.demo-section {
  margin-top: 40px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}
.demo-section h3 {
  margin-bottom: 16px;
}
.demo-products {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}
.cart-items {
  margin-bottom: 24px;
}
.cart-item {
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 12px;
}
.item-info {
  display: flex;
  align-items: center;
  gap: 16px;
}
.item-name {
  flex: 1;
  font-weight: 500;
}
.item-price {
  color: #ff6600;
  min-width: 100px;
}
.item-quantity {
  display: flex;
  align-items: center;
  gap: 8px;
}
.btn-quantity {
  width: 28px;
  height: 28px;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 4px;
  cursor: pointer;
}
.btn-quantity:hover {
  background: #f5f5f5;
}
.item-total {
  color: #ff6600;
  font-weight: 600;
  min-width: 120px;
}
.btn-remove {
  padding: 6px 12px;
  border: none;
  background: #ff4d4f;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}
.cart-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
}
.cart-total {
  font-size: 18px;
}
.total-amount {
  color: #ff6600;
  font-size: 24px;
  font-weight: 600;
}
.cart-actions {
  display: flex;
  gap: 12px;
}
.btn {
  padding: 10px 24px;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-size: 14px;
}
.btn-small {
  padding: 8px 16px;
}
.btn-outline {
  border: 1px solid #ddd;
  background: #fff;
  color: #333;
}
.btn-primary {
  border: none;
  background: #ff6600;
  color: #fff;
}
.btn:hover {
  opacity: 0.9;
}
</style>
