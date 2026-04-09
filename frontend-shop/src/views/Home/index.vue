<template>
  <div class="home-page">
    <Header />
    <main class="main-content">
      <div class="container">
        <!-- 轮播图 -->
        <section class="banner-section" v-if="banners.length > 0">
          <div class="banner-slider">
            <div class="banner-item" v-for="banner in banners" :key="banner.id">
              <a :href="banner.link_url" target="_blank">
                <img :src="banner.image_url" :alt="banner.title" class="banner-image" />
              </a>
            </div>
          </div>
        </section>

        <!-- 楼层商品 -->
        <section v-for="floor in floors" :key="floor.id" class="section">
          <div class="section-header">
            <h2>{{ floor.name }}</h2>
            <router-link to="/products" class="more-link">查看更多 &rarr;</router-link>
          </div>
          <div class="product-grid">
            <div v-for="product in floor.products" :key="product.product_id" class="product-card">
              <router-link :to="`/product/${product.product_id}`" class="product-link">
                <div class="product-image">
                  <img :src="product.cover_image" :alt="product.name" />
                </div>
                <div class="product-info">
                  <h3 class="product-name">{{ product.name }}</h3>
                  <div class="product-price">
                    <span class="price">¥{{ product.price.toFixed(2) }}</span>
                    <span v-if="product.original_price" class="original-price">¥{{ product.original_price.toFixed(2) }}</span>
                  </div>
                </div>
              </router-link>
            </div>
          </div>
        </section>

        <!-- 热门商品 -->
        <section class="section" v-if="hotProducts.length > 0">
          <div class="section-header">
            <h2>热门商品</h2>
            <router-link to="/products" class="more-link">查看更多 &rarr;</router-link>
          </div>
          <div class="product-grid">
            <ProductCard v-for="product in hotProducts" :key="product.id" :product="product" />
          </div>
        </section>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <p>加载中...</p>
        </div>
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
import { homeApi } from '@/api/home'
import { shopProductApi } from '@/api/product'
import type { Banner, Floor } from '@/api/home'
import type { ProductSpu } from '@/api/product'

const loading = ref(true)
const banners = ref<Banner[]>([])
const floors = ref<Floor[]>([])
const hotProducts = ref<ProductSpu[]>([])

onMounted(() => {
  loadHomeData()
})

async function loadHomeData() {
  loading.value = true
  try {
    // 加载首页配置（轮播图和楼层）
    const homeRes = await homeApi.getHomeConfig()
    if (homeRes.code === 200) {
      banners.value = homeRes.data?.banners || []
      floors.value = homeRes.data?.floors || []
    }

    // 加载热门商品
    const productRes = await shopProductApi.getProducts({ page: 1, pageSize: 8 })
    if (productRes.code === 200) {
      hotProducts.value = productRes.data?.items || []
    }
  } catch (error) {
    console.error('加载首页数据失败', error)
  } finally {
    loading.value = false
  }
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

.banner-slider {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  height: 400px;
}

.banner-item {
  position: relative;
  width: 100%;
  height: 100%;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
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

.product-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.product-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
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
  padding: 16px;
}

.product-name {
  font-size: 16px;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.product-price {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price {
  font-size: 18px;
  font-weight: bold;
  color: #ff6b6b;
}

.original-price {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
}

.loading-state {
  text-align: center;
  padding: 80px 0;
  color: #666;
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .banner-slider {
    height: 250px;
  }
  
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 16px;
  }
  
  .product-image {
    height: 120px;
  }
  
  .product-info {
    padding: 12px;
  }
  
  .product-name {
    font-size: 14px;
  }
  
  .price {
    font-size: 16px;
  }
}
</style>
