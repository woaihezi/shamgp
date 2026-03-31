<template>
  <div class="product-card card">
    <router-link :to="`/product/${product.id}`" class="product-link">
      <div class="product-image">
        <img :src="product.image || 'https://via.placeholder.com/300x300?text=商品图片'" :alt="product.name">
      </div>
      <div class="product-info">
        <h3 class="product-name">{{ product.name }}</h3>
        <p class="product-desc">{{ product.description }}</p>
        <div class="product-price">
          <span class="price">¥{{ product.price.toFixed(2) }}</span>
          <span class="stock">库存: {{ product.stock }}</span>
        </div>
      </div>
    </router-link>
    <div class="product-actions">
      <button class="btn btn-primary" @click="handleAddToCart">加入购物车</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useCartStore } from '@/stores/cart'
import type { Product } from '@/api/product'

interface Props {
  product: Product
}

defineProps<Props>()

const cartStore = useCartStore()

function handleAddToCart() {
  cartStore.addItem({
    id: props.product.id,
    name: props.product.name,
    price: props.product.price,
    image: props.product.image
  })
}
</script>

<style scoped>
.product-card {
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.product-link {
  display: block;
}

.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f5f5f5;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.product-info {
  padding: 15px;
}

.product-name {
  font-size: 16px;
  margin-bottom: 8px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-desc {
  font-size: 13px;
  color: #666;
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-price .price {
  font-size: 18px;
  font-weight: bold;
}

.product-price .stock {
  font-size: 13px;
  color: #999;
}

.product-actions {
  padding: 0 15px 15px;
}

.product-actions .btn {
  width: 100%;
}
</style>
