<template>
  <div class="home-page">
    <Header />
    <main class="main-content">
      <div class="container">
        <section class="banner-section">
          <div class="banner">
            <h1>欢迎来到商城</h1>
            <p>品质购物，从这里开始</p>
          </div>
        </section>

        <section class="section">
          <div class="section-header">
            <h2>热门商品</h2>
            <router-link to="/products" class="more-link">查看更多 &rarr;</router-link>
          </div>
          <div class="product-grid">
            <ProductCard v-for="product in hotProducts" :key="product.id" :product="product" />
          </div>
        </section>

        <section class="section">
          <div class="section-header">
            <h2>新品推荐</h2>
          </div>
          <div class="product-grid">
            <ProductCard v-for="product in newProducts" :key="product.id" :product="product" />
          </div>
        </section>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import ProductCard from '@/components/ProductCard.vue'
import type { Product } from '@/api/product'

const hotProducts = ref<Product[]>([])
const newProducts = ref<Product[]>([])

onMounted(() => {
  loadMockProducts()
})

function loadMockProducts() {
  const mockProducts: Product[] = [
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
    }
  ]
  hotProducts.value = mockProducts.slice(0, 4)
  newProducts.value = mockProducts.slice(2, 6)
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 20px 0;
}

.banner-section {
  margin-bottom: 40px;
}

.banner {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
  color: white;
  padding: 80px 40px;
  border-radius: 12px;
  text-align: center;
}

.banner h1 {
  font-size: 36px;
  margin-bottom: 12px;
}

.banner p {
  font-size: 18px;
  opacity: 0.9;
}

.section {
  margin-bottom: 50px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h2 {
  font-size: 24px;
  color: #333;
}

.more-link {
  color: #ff6b6b;
  font-size: 14px;
  transition: color 0.3s;
}

.more-link:hover {
  color: #ee5a5a;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}
</style>
