<template>
  <div class="product-list-page">
    <Header />
    <main class="main-content">
      <div class="container">
        <div class="page-header">
          <h1 class="page-title">商品列表</h1>
          <div class="filter-bar">
            <input 
              v-model="keyword" 
              type="text" 
              placeholder="搜索商品..." 
              class="search-input"
              @keyup.enter="handleSearch"
            />
            <button class="btn btn-primary" @click="handleSearch">搜索</button>
          </div>
        </div>

        <div class="product-grid">
          <ProductCard v-for="product in filteredProducts" :key="product.id" :product="product" />
        </div>

        <div v-if="filteredProducts.length === 0" class="empty-state">
          <p>暂无商品</p>
        </div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import ProductCard from '@/components/ProductCard.vue'
import { shopProductApi } from '@/api/product'
import type { ProductSpu } from '@/api/product'

const route = useRoute()
const keyword = ref('')
const products = ref<ProductSpu[]>([])
const loading = ref(false)

// 当前行为：前端过滤（非服务端分页）
// 后续可优化为服务端分页 + 搜索
const filteredProducts = computed(() => {
  let result = [...products.value]
  
  if (route.query.categoryId) {
    const categoryId = Number(route.query.categoryId)
    result = result.filter(p => (p as any).category_id === categoryId || (p as any).categoryId === categoryId)
  }
  
  if (keyword.value) {
    const kw = keyword.value.toLowerCase()
    result = result.filter(p => 
      p.name.toLowerCase().includes(kw) || 
      ((p as any).description && (p as any).description.toLowerCase().includes(kw))
    )
  }
  
  return result
})

onMounted(() => {
  loadProducts()
})

async function loadProducts() {
  try {
    loading.value = true
    const categoryId = route.query.categoryId ? Number(route.query.categoryId) : undefined
    const res: any = await shopProductApi.getProducts({ 
      page: 1, 
      pageSize: 50,
      categoryId: categoryId,
      keyword: keyword.value || undefined
    })
    if (res.code === 200) {
      products.value = res.data?.items || res.data || []
    }
  } catch (e) {
    console.error('加载商品失败', e)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  loadProducts()
}
</script>

<style scoped>
.product-list-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 40px 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 20px;
}

.page-title {
  font-size: 28px;
  color: #333;
}

.filter-bar {
  display: flex;
  gap: 12px;
}

.search-input {
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  width: 300px;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #ff6b6b;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

.empty-state {
  text-align: center;
  padding: 80px 0;
  color: #999;
  font-size: 16px;
}
</style>
