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
import type { Product } from '@/api/product'

const route = useRoute()
const keyword = ref('')
const products = ref<Product[]>([])

const filteredProducts = computed(() => {
  let result = [...products.value]
  
  if (route.query.categoryId) {
    const categoryId = Number(route.query.categoryId)
    result = result.filter(p => p.categoryId === categoryId)
  }
  
  if (keyword.value) {
    const kw = keyword.value.toLowerCase()
    result = result.filter(p => 
      p.name.toLowerCase().includes(kw) || 
      (p.description && p.description.toLowerCase().includes(kw))
    )
  }
  
  return result
})

onMounted(() => {
  loadMockProducts()
})

function loadMockProducts() {
  products.value = [
    {
      id: 1,
      name: 'iPhone 15 Pro Max',
      description: '苹果最新旗舰手机，钛金属设计，A17 Pro芯片',
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
      description: 'M3 Pro芯片，18小时续航，Liquid Retina XDR显示屏',
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
      description: '主动降噪，自适应通透模式，空间音频',
      price: 1899,
      stock: 200,
      categoryId: 3,
      image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=AirPods%20Pro%20wireless%20earbuds&image_size=square_hd',
      status: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    },
    {
      id: 4,
      name: 'iPad Pro 12.9英寸',
      description: 'M2芯片，Liquid Retina XDR显示屏，Apple Pencil支持',
      price: 8999,
      stock: 80,
      categoryId: 1,
      image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=iPad%20Pro%20tablet&image_size=square_hd',
      status: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    },
    {
      id: 5,
      name: 'Apple Watch Ultra 2',
      description: '钛金属表壳，S9芯片，双频GPS，100米防水',
      price: 6499,
      stock: 60,
      categoryId: 3,
      image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Apple%20Watch%20smartwatch&image_size=square_hd',
      status: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    },
    {
      id: 6,
      name: 'Magic Keyboard',
      description: '无线蓝牙键盘，背光按键，适配Mac和iPad',
      price: 999,
      stock: 150,
      categoryId: 2,
      image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=wireless%20keyboard&image_size=square_hd',
      status: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    },
    {
      id: 7,
      name: 'Sony WH-1000XM5 降噪耳机',
      description: '业界领先降噪，30小时续航，舒适佩戴',
      price: 2699,
      stock: 90,
      categoryId: 3,
      image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Sony%20noise%20cancelling%20headphones&image_size=square_hd',
      status: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    },
    {
      id: 8,
      name: 'Dell XPS 13 笔记本',
      description: '13.4英寸4K触控屏，Intel i7处理器，16GB内存',
      price: 10999,
      stock: 40,
      categoryId: 2,
      image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Dell%20XPS%20laptop&image_size=square_hd',
      status: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  ]
}

function handleSearch() {
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
