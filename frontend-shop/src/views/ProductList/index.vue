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
          <ProductCard v-for="product in products" :key="product.id" :product="product" />
        </div>

        <div v-if="loading" class="loading-state">
          <p>加载中...</p>
        </div>

        <div v-else-if="products.length === 0" class="empty-state">
          <p>暂无商品</p>
        </div>

        <div class="pagination" v-if="total > pageSize">
          <button class="btn" @click="changePage(page - 1)" :disabled="page === 1">上一页</button>
          <span>{{ page }} / {{ Math.ceil(total / pageSize) }}</span>
          <button class="btn" @click="changePage(page + 1)" :disabled="page >= Math.ceil(total / pageSize)">下一页</button>
        </div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import ProductCard from '@/components/ProductCard.vue'
import { shopProductApi } from '@/api/product'
import type { ProductSpu } from '@/api/product'

const route = useRoute()
const router = useRouter()
const keyword = ref('')
const products = ref<ProductSpu[]>([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const pageSize = ref(24)

onMounted(() => {
  // 从路由参数中获取搜索关键词和分类ID
  if (route.query.keyword) {
    keyword.value = route.query.keyword as string
  }
  loadProducts()
})

async function loadProducts() {
  loading.value = true
  try {
    const categoryId = route.query.categoryId ? Number(route.query.categoryId) : undefined
    const res: any = await shopProductApi.getProducts({
      page: page.value,
      pageSize: pageSize.value,
      categoryId,
      keyword: keyword.value
    })
    if (res.code === 200) {
      products.value = res.data?.items || []
      total.value = res.data?.total || 0
    }
  } catch (e) {
    console.error('加载商品失败', e)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  page.value = 1
  // 更新路由参数
  router.push({
    path: '/products',
    query: {
      ...route.query,
      keyword: keyword.value,
      page: '1'
    }
  })
  loadProducts()
}

function changePage(newPage: number) {
  if (newPage < 1 || newPage > Math.ceil(total.value / pageSize.value)) {
    return
  }
  page.value = newPage
  // 更新路由参数
  router.push({
    path: '/products',
    query: {
      ...route.query,
      page: newPage.toString()
    }
  })
  loadProducts()
}

// 监听路由变化，重新加载商品
watch(
  () => route.query,
  () => {
    if (route.query.page) {
      page.value = Number(route.query.page)
    } else {
      page.value = 1
    }
    if (route.query.keyword) {
      keyword.value = route.query.keyword as string
    }
    loadProducts()
  },
  { deep: true }
)
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

.loading-state {
  text-align: center;
  padding: 80px 0;
  color: #666;
  font-size: 16px;
}

.empty-state {
  text-align: center;
  padding: 80px 0;
  color: #999;
  font-size: 16px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 40px;
  gap: 16px;
}

.pagination .btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination .btn:hover:not(:disabled) {
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.pagination .btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination span {
  font-size: 14px;
  color: #666;
}
</style>
