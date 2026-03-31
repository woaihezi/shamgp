<template>
  <div class="product-detail-page">
    <Header />
    <main class="main-content">
      <div class="container">
        <div v-if="product" class="product-detail card">
          <div class="product-gallery">
            <img :src="product.image || 'https://via.placeholder.com/500x500?text=商品图片'" :alt="product.name" class="main-image">
          </div>
          <div class="product-info">
            <h1 class="product-title">{{ product.name }}</h1>
            <div class="product-price-section">
              <span class="price">¥{{ product.price.toFixed(2) }}</span>
              <span class="stock">库存: {{ product.stock }}件</span>
            </div>
            <div class="product-description">
              <h3>商品描述</h3>
              <p>{{ product.description || '暂无描述' }}</p>
            </div>
            <div class="product-actions">
              <div class="quantity-selector">
                <label>数量:</label>
                <button @click="quantity--" :disabled="quantity <= 1">-</button>
                <input type="number" v-model.number="quantity" min="1" :max="product.stock">
                <button @click="quantity++" :disabled="quantity >= product.stock">+</button>
              </div>
              <button class="btn btn-primary btn-large" @click="handleAddToCart">
                加入购物车
              </button>
              <button class="btn btn-default btn-large" @click="handleBuyNow">
                立即购买
              </button>
            </div>
          </div>
        </div>
        <div v-else class="loading">
          <p>加载中...</p>
        </div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { useCartStore } from '@/stores/cart'
import type { Product } from '@/api/product'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const product = ref<Product | null>(null)
const quantity = ref(1)

onMounted(() => {
  loadProduct()
})

function loadProduct() {
  const productId = Number(route.params.id)
  const mockProducts: Product[] = [
    {
      id: 1,
      name: 'iPhone 15 Pro Max',
      description: '苹果最新旗舰手机，钛金属设计，A17 Pro芯片，支持USB 3.2传输速度，Pro级摄像头系统，全天候显示的超视网膜XDR显示屏',
      price: 9999,
      stock: 100,
      categoryId: 1,
      image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=iPhone%2015%20Pro%20Max%20smartphone&image_size=square_hd',
      status: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    },
    {
      id: 2,
      name: 'MacBook Pro 14英寸',
      description: 'M3 Pro芯片，18小时续航，Liquid Retina XDR显示屏，专业级性能，适合创作者和开发者',
      price: 14999,
      stock: 50,
      categoryId: 2,
      image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=MacBook%20Pro%20laptop&image_size=square_hd',
      status: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    },
    {
      id: 3,
      name: 'AirPods Pro 2',
      description: '主动降噪，自适应通透模式，空间音频，个性化音量，对话感知，查找功能',
      price: 1899,
      stock: 200,
      categoryId: 3,
      image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=AirPods%20Pro%20wireless%20earbuds&image_size=square_hd',
      status: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  ]
  product.value = mockProducts.find(p => p.id === productId) || mockProducts[0]
}

function handleAddToCart() {
  if (product.value) {
    cartStore.addItem({
      id: product.value.id,
      name: product.value.name,
      price: product.value.price,
      image: product.value.image
    }, quantity.value)
    alert('已加入购物车')
  }
}

function handleBuyNow() {
  if (product.value) {
    cartStore.addItem({
      id: product.value.id,
      name: product.value.name,
      price: product.value.price,
      image: product.value.image
    }, quantity.value)
    router.push('/checkout')
  }
}
</script>

<style scoped>
.product-detail-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 40px 0;
}

.product-detail {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  padding: 40px;
}

.product-gallery {
  text-align: center;
}

.main-image {
  width: 100%;
  max-width: 500px;
  height: 500px;
  object-fit: cover;
  border-radius: 8px;
}

.product-title {
  font-size: 28px;
  color: #333;
  margin-bottom: 20px;
}

.product-price-section {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.product-price-section .price {
  font-size: 32px;
  font-weight: bold;
}

.product-price-section .stock {
  color: #666;
  font-size: 14px;
}

.product-description {
  margin-bottom: 30px;
}

.product-description h3 {
  font-size: 16px;
  color: #333;
  margin-bottom: 12px;
}

.product-description p {
  color: #666;
  line-height: 1.8;
}

.product-actions {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.quantity-selector {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quantity-selector label {
  color: #666;
}

.quantity-selector button {
  width: 36px;
  height: 36px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.3s;
}

.quantity-selector button:hover:not(:disabled) {
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.quantity-selector button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-selector input {
  width: 60px;
  height: 36px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.btn-large {
  padding: 14px 40px;
  font-size: 16px;
}

.loading {
  text-align: center;
  padding: 80px 0;
  color: #999;
}
</style>
