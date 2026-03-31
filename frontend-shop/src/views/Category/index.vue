<template>
  <div class="category-page">
    <Header />
    <main class="main-content">
      <div class="container">
        <h1 class="page-title">商品分类</h1>
        <div class="category-grid">
          <div v-for="category in categories" :key="category.id" class="category-item card" @click="goToProductList(category.id)">
            <div class="category-icon">{{ getCategoryIcon(category.name) }}</div>
            <h3 class="category-name">{{ category.name }}</h3>
            <p class="category-count">{{ category.children ? category.children.length + ' 个子分类' : '点击查看商品' }}</p>
          </div>
        </div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import type { Category } from '@/api/category'

const router = useRouter()
const categories = ref<Category[]>([])

onMounted(() => {
  loadMockCategories()
})

function loadMockCategories() {
  categories.value = [
    {
      id: 1,
      name: '手机数码',
      parentId: undefined,
      sort: 1,
      createdAt: new Date().toISOString(),
      children: [
        { id: 11, name: '手机', parentId: 1, sort: 1, createdAt: new Date().toISOString() },
        { id: 12, name: '平板', parentId: 1, sort: 2, createdAt: new Date().toISOString() },
        { id: 13, name: '智能手表', parentId: 1, sort: 3, createdAt: new Date().toISOString() }
      ]
    },
    {
      id: 2,
      name: '电脑办公',
      parentId: undefined,
      sort: 2,
      createdAt: new Date().toISOString(),
      children: [
        { id: 21, name: '笔记本', parentId: 2, sort: 1, createdAt: new Date().toISOString() },
        { id: 22, name: '台式机', parentId: 2, sort: 2, createdAt: new Date().toISOString() },
        { id: 23, name: '外设', parentId: 2, sort: 3, createdAt: new Date().toISOString() }
      ]
    },
    {
      id: 3,
      name: '家用电器',
      parentId: undefined,
      sort: 3,
      createdAt: new Date().toISOString(),
      children: [
        { id: 31, name: '电视', parentId: 3, sort: 1, createdAt: new Date().toISOString() },
        { id: 32, name: '空调', parentId: 3, sort: 2, createdAt: new Date().toISOString() },
        { id: 33, name: '冰箱', parentId: 3, sort: 3, createdAt: new Date().toISOString() }
      ]
    },
    {
      id: 4,
      name: '服饰鞋包',
      parentId: undefined,
      sort: 4,
      createdAt: new Date().toISOString(),
      children: [
        { id: 41, name: '男装', parentId: 4, sort: 1, createdAt: new Date().toISOString() },
        { id: 42, name: '女装', parentId: 4, sort: 2, createdAt: new Date().toISOString() },
        { id: 43, name: '鞋靴', parentId: 4, sort: 3, createdAt: new Date().toISOString() }
      ]
    },
    {
      id: 5,
      name: '美妆个护',
      parentId: undefined,
      sort: 5,
      createdAt: new Date().toISOString()
    },
    {
      id: 6,
      name: '食品生鲜',
      parentId: undefined,
      sort: 6,
      createdAt: new Date().toISOString()
    }
  ]
}

function goToProductList(categoryId?: number) {
  router.push({ path: '/products', query: { categoryId } })
}

function getCategoryIcon(name: string) {
  const icons: Record<string, string> = {
    '手机数码': '📱',
    '电脑办公': '💻',
    '家用电器': '📺',
    '服饰鞋包': '👕',
    '美妆个护': '💄',
    '食品生鲜': '🍎'
  }
  return icons[name] || '🛍️'
}
</script>

<style scoped>
.category-page {
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

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.category-item {
  padding: 40px 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.category-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.category-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.category-name {
  font-size: 20px;
  color: #333;
  margin-bottom: 8px;
}

.category-count {
  font-size: 14px;
  color: #999;
}
</style>
