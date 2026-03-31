<template>
  <div class="home">
    <section class="hero">
      <div class="container hero-content">
        <h1>ShamGP 商城</h1>
        <p>精选商品，快速下单，覆盖日常数码与生活好物。</p>
        <router-link class="btn btn-primary" to="/products">立即选购</router-link>
      </div>
    </section>

    <section class="container block">
      <div class="block-header">
        <h2>热门商品</h2>
        <router-link to="/products">查看全部</router-link>
      </div>

      <div v-if="loading" class="placeholder">商品加载中...</div>
      <div v-else-if="products.length === 0" class="placeholder">暂无商品</div>
      <div v-else class="product-grid">
        <div v-for="item in products" :key="item.id" class="product-card" @click="goToDetail(item.id)">
          <img :src="item.cover_image || placeholder" :alt="item.name" />
          <div class="info">
            <h3>{{ item.name }}</h3>
            <p>{{ item.brief || item.description || '暂无描述' }}</p>
            <div class="price-row">
              <span class="price">¥{{ Number(item.price || 0).toFixed(2) }}</span>
              <span v-if="item.original_price" class="original">¥{{ Number(item.original_price).toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { shopProductApi } from '@/api/product'

interface HomeProduct {
  id: number
  name: string
  brief?: string
  description?: string
  cover_image?: string
  price?: number
  original_price?: number
}

const router = useRouter()
const loading = ref(true)
const products = ref<HomeProduct[]>([])
const placeholder = 'https://via.placeholder.com/480x480?text=ShamGP'

function normalizeList(payload: any): HomeProduct[] {
  if (Array.isArray(payload)) return payload
  if (Array.isArray(payload?.items)) return payload.items
  if (Array.isArray(payload?.data)) return payload.data
  if (Array.isArray(payload?.data?.items)) return payload.data.items
  return []
}

async function loadProducts() {
  loading.value = true
  try {
    const res = await shopProductApi.getProducts({ page: 1, pageSize: 8 }) as any
    products.value = normalizeList(res?.data).slice(0, 8)
  } catch {
    products.value = []
  } finally {
    loading.value = false
  }
}

function goToDetail(id?: number) {
  if (!id) return
  router.push(`/product/${id}`)
}

onMounted(loadProducts)
</script>

<style scoped>
.home {
  min-height: 100%;
  background: #f7f8fa;
  padding-bottom: 32px;
}

.hero {
  background: linear-gradient(135deg, #ff5a3c, #ff8d2c);
  color: #fff;
}

.hero-content {
  padding: 64px 20px;
}

.hero h1 {
  margin: 0 0 10px;
  font-size: 40px;
}

.hero p {
  margin: 0 0 20px;
  max-width: 560px;
  opacity: 0.95;
}

.block {
  margin-top: 24px;
}

.block-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.block-header h2 {
  margin: 0;
  font-size: 22px;
}

.block-header a {
  color: #ff5a3c;
}

.placeholder {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  color: #666;
}

.product-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
}

.product-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.product-card img {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  background: #f1f1f1;
}

.info {
  padding: 12px;
}

.info h3 {
  margin: 0 0 8px;
  font-size: 16px;
}

.info p {
  margin: 0 0 10px;
  color: #666;
  font-size: 13px;
  line-height: 1.4;
  min-height: 36px;
}

.price-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.original {
  color: #999;
  text-decoration: line-through;
  font-size: 12px;
}
</style>
