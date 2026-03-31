<template>
  <div class="home">
    <!-- 顶部 Banner -->
    <div class="banner">
      <div class="banner-content">
        <h1>ShamGP 商城</h1>
        <p>精选商品，品质生活</p>
        <router-link to="/products" class="banner-btn">立即选购</router-link>
      </div>
    </div>

    <!-- 分类导航 -->
    <div class="categories">
      <div
        v-for="cat in categories.slice(0, 6)"
        :key="cat.id"
        class="category-item"
        @click="goToCategory(cat.id!)"
      >
        <div class="cat-icon">{{ cat.name?.charAt(0) || '📦' }}</div>
        <div class="cat-name">{{ cat.name }}</div>
      </div>
    </div>

    <!-- 热门商品 -->
    <div class="section">
      <div class="section-header">
        <h2>热门商品</h2>
        <router-link to="/products" class="more-link">查看更多 →</router-link>
      </div>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else class="product-grid">
        <div
          v-for="product in products"
          :key="product.id"
          class="product-card"
          @click="goToDetail(product.id!)"
        >
          <div class="product-image">
            <img
              :src="(product as any).cover_image || (product as any).mainImage || placeholder"
              :alt="product.name"
              @error="e => (e.target as HTMLImageElement).src = placeholder"
            >
            <span v-if="(product as any).is_hot" class="hot-tag">热卖</span>
            <span v-if="(product as any).is_new" class="new-tag">新品</span>
          </div>
          <div class="product-info">
            <div class="product-name">{{ product.name }}</div>
            <div class="product-price">
              <span class="price">¥{{ ((product as any).price || 0).toFixed(2) }}</span>
              <span v-if="(product as any).original_price" class="original-price">
                ¥{{ ((product as any).original_price || 0).toFixed(2) }}
              </span>
            </div>
            <div class="product-meta">
              <span>销量 {{ (product as any).sales || 0 }}</span>
              <span>{{ (product as any).views || 0 }} 人浏览</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部信息 -->
    <div class="home-footer">
      <p>© 2026 ShamGP 商城 · localhost:5173</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { shopProductApi } from '@/api/product'

const router = useRouter()
const loading = ref(true)
const products = ref<any[]>([])
const categories = ref<any[]>([])
const placeholder = 'https://via.placeholder.com/300x300?text=Product'

const loadData = async () => {
  try {
    loading.value = true
    // 并行加载分类和商品
    const [catRes, prodRes] = await Promise.all([
      shopProductApi.getCategories().catch(() => ({ data: [] })),
      shopProductApi.getProducts({ page: 1, pageSize: 8 }).catch(() => ({ data: { items: [] } }))
    ])

    if (catRes?.data) {
      const flatten = (cats: any[]): any[] => {
        let result: any[] = []
        cats.forEach((c: any) => {
          result.push(c)
          if (c.children?.length) result = result.concat(flatten(c.children))
        })
        return result
      }
      categories.value = flatten(Array.isArray(catRes.data) ? catRes.data : [])
    }

    if (prodRes?.data?.items) {
      products.value = prodRes.data.items
    }
  } catch (e) {
    console.error('Home data load error:', e)
  } finally {
    loading.value = false
  }
}

const goToCategory = (id: number) => {
  router.push(`/products?categoryId=${id}`)
}

const goToDetail = (id: number) => {
  router.push(`/product/${id}`)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: #f5f5f5;
}

.banner {
  background: linear-gradient(135deg, #ff6600, #ff8533);
  color: white;
  padding: 80px 20px;
  text-align: center;
}
.banner h1 {
  font-size: 48px;
  margin: 0 0 16px;
}
.banner p {
  font-size: 20px;
  margin: 0 0 32px;
  opacity: 0.9;
}
.banner-btn {
  display: inline-block;
  padding: 14px 40px;
  background: white;
  color: #ff6600;
  text-decoration: none;
  border-radius: 30px;
  font-weight: 600;
  font-size: 16px;
}
.categories {
  display: flex;
  justify-content: center;
  gap: 0;
  background: white;
  padding: 24px 0;
  overflow-x: auto;
}
.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 100px;
  padding: 12px 20px;
  cursor: pointer;
  border-radius: 12px;
  transition: background 0.2s;
}
.category-item:hover {
  background: #fff3e6;
}
.cat-icon {
  font-size: 32px;
  margin-bottom: 8px;
}
.cat-name {
  font-size: 13px;
  color: #666;
}
.section {
  max-width: 1200px;
  margin: 32px auto;
  padding: 0 20px;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.section-header h2 {
  font-size: 22px;
  color: #333;
  margin: 0;
}
.more-link {
  color: #ff6600;
  text-decoration: none;
  font-size: 14px;
}
.loading {
  text-align: center;
  padding: 60px;
  color: #999;
}
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}
.product-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}
.product-image {
  position: relative;
  height: 240px;
  overflow: hidden;
  background: #fafafa;
}
.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.hot-tag, .new-tag {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 12px;
  color: white;
}
.hot-tag { background: #e74c3c; }
.new-tag { background: #409eff; left: 70px; }
.product-info {
  padding: 14px;
}
.product-name {
  font-size: 15px;
  color: #333;
  margin-bottom: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.product-price {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 8px;
}
.price {
  font-size: 20px;
  color: #e74c3c;
  font-weight: bold;
}
.original-price {
  font-size: 13px;
  color: #999;
  text-decoration: line-through;
}
.product-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
}
.home-footer {
  text-align: center;
  padding: 40px 20px;
  color: #999;
  font-size: 13px;
}
</style>
