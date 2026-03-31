<template>
  <div class="product-detail" v-if="product">
    <div class="container">
      <div class="breadcrumb">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item v-if="product.category">
            {{ product.category.name }}
          </el-breadcrumb-item>
          <el-breadcrumb-item>{{ product.name }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>

      <div class="product-content">
        <div class="product-gallery">
          <div class="main-image">
            <el-image
              :src="product.mainImage || 'https://via.placeholder.com/500x500'"
              :preview-src-list="imageUrls"
              fit="cover"
            />
          </div>
          <div class="thumbnails" v-if="carouselImages.length">
            <div
              v-for="(img, index) in carouselImages"
              :key="img.id"
              class="thumbnail"
              :class="{ active: activeImageIndex === index }"
              @click="activeImageIndex = index"
            >
              <img :src="img.imageUrl" :alt="product.name" />
            </div>
          </div>
        </div>

        <div class="product-info">
          <h1 class="product-title">{{ product.name }}</h1>
          <p class="product-subtitle">{{ product.subtitle }}</p>

          <div class="price-section">
            <span class="price-label">价格</span>
            <div class="price-wrap">
              <span class="current-price">¥{{ minPrice }}</span>
              <span v-if="maxPrice && maxPrice !== minPrice" class="price-range">
                - ¥{{ maxPrice }}
              </span>
              <span v-if="originalPrice" class="original-price">¥{{ originalPrice }}</span>
            </div>
          </div>

          <div class="product-meta">
            <div class="meta-item">
              <span class="meta-label">销量</span>
              <span class="meta-value">{{ product.salesCount }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">浏览</span>
              <span class="meta-value">{{ product.viewCount }}</span>
            </div>
            <div class="meta-item" v-if="product.brand">
              <span class="meta-label">品牌</span>
              <span class="meta-value">{{ product.brand.name }}</span>
            </div>
          </div>

          <div class="sku-section" v-if="skus.length">
            <div class="sku-label">规格</div>
            <div class="sku-list">
              <div
                v-for="sku in skus"
                :key="sku.id"
                class="sku-item"
                :class="{ active: selectedSku?.id === sku.id }"
                @click="selectSku(sku)"
              >
                <img v-if="sku.image" :src="sku.image" :alt="sku.name" />
                <span>{{ sku.name }}</span>
              </div>
            </div>
          </div>

          <div class="stock-section" v-if="selectedSku?.inventory">
            <div class="stock-label">库存</div>
            <div class="stock-value">
              {{ selectedSku.inventory.availableStock }} {{ product.unit || '件' }}
            </div>
          </div>

          <div class="quantity-section">
            <div class="quantity-label">数量</div>
            <div class="quantity-wrap">
              <el-input-number v-model="quantity" :min="1" :max="maxStock" size="large" />
            </div>
          </div>

          <div class="action-buttons">
            <el-button type="primary" size="large" @click="addToCart">
              加入购物车
            </el-button>
            <el-button type="danger" size="large" @click="buyNow">
              立即购买
            </el-button>
          </div>
        </div>
      </div>

      <div class="product-description">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="商品详情" name="detail">
            <div class="detail-content" v-html="product.description || '暂无商品详情'"></div>
          </el-tab-pane>
          <el-tab-pane label="规格参数" name="specs">
            <div class="specs-content">
              <p>规格参数内容</p>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { shopProductApi, ProductSpu, ProductSku, ProductImage } from '@/api/product'

const route = useRoute()
const router = useRouter()

const product = ref<ProductSpu | null>(null)
const skus = ref<ProductSku[]>([])
const carouselImages = ref<ProductImage[]>([])
const selectedSku = ref<ProductSku | null>(null)
const activeImageIndex = ref(0)
const activeTab = ref('detail')
const quantity = ref(1)

const imageUrls = computed(() => {
  if (product.value?.mainImage) {
    return [product.value.mainImage, ...carouselImages.value.map(img => img.imageUrl)]
  }
  return carouselImages.value.map(img => img.imageUrl)
})

const minPrice = computed(() => {
  if (!skus.value.length) return 0
  return Math.min(...skus.value.map(s => s.price)).toFixed(2)
})

const maxPrice = computed(() => {
  if (!skus.value.length) return 0
  return Math.max(...skus.value.map(s => s.price)).toFixed(2)
})

const originalPrice = computed(() => {
  if (!skus.value.length) return null
  const prices = skus.value.map(s => s.originalPrice).filter(p => p) as number[]
  if (!prices.length) return null
  return Math.max(...prices).toFixed(2)
})

const maxStock = computed(() => {
  if (selectedSku.value?.inventory?.availableStock) {
    return selectedSku.value.inventory.availableStock
  }
  return 999
})

const loadProduct = async (id: number) => {
  try {
    const res = await shopProductApi.getProduct(id)
    if (res.data) {
      product.value = res.data
      skus.value = res.data.skus || []
      carouselImages.value = (res.data.images || []).filter(img => img.imageType === 0)
      
      if (skus.value.length) {
        selectedSku.value = skus.value[0]
      }
    }
  } catch (error) {
    ElMessage.error('加载商品详情失败')
  }
}

const selectSku = (sku: ProductSku) => {
  selectedSku.value = sku
}

const addToCart = () => {
  if (!selectedSku.value) {
    ElMessage.warning('请选择商品规格')
    return
  }
  ElMessage.success('已加入购物车')
}

const buyNow = () => {
  if (!selectedSku.value) {
    ElMessage.warning('请选择商品规格')
    return
  }
  ElMessage.success('立即购买')
}

onMounted(() => {
  const id = Number(route.params.id)
  if (id) {
    loadProduct(id)
  }
})
</script>

<style scoped>
.product-detail {
  padding: 20px 0;
  background: #f5f5f5;
  min-height: calc(100vh - 100px);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.breadcrumb {
  background: #fff;
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.product-content {
  display: flex;
  gap: 30px;
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.product-gallery {
  width: 500px;
  flex-shrink: 0;
}

.main-image {
  width: 100%;
  height: 500px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 15px;
}

.main-image :deep(.el-image) {
  width: 100%;
  height: 100%;
}

.thumbnails {
  display: flex;
  gap: 10px;
}

.thumbnail {
  width: 80px;
  height: 80px;
  border: 2px solid transparent;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.thumbnail:hover,
.thumbnail.active {
  border-color: #409eff;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  flex: 1;
}

.product-title {
  font-size: 24px;
  color: #333;
  margin: 0 0 10px;
}

.product-subtitle {
  font-size: 14px;
  color: #999;
  margin: 0 0 20px;
}

.price-section {
  background: #fff5f5;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.price-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
  display: block;
}

.price-wrap {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.current-price {
  font-size: 32px;
  color: #e74c3c;
  font-weight: bold;
}

.price-range {
  font-size: 24px;
  color: #e74c3c;
}

.original-price {
  font-size: 16px;
  color: #999;
  text-decoration: line-through;
}

.product-meta {
  display: flex;
  gap: 30px;
  margin-bottom: 20px;
  padding: 15px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.meta-item {
  display: flex;
  gap: 10px;
}

.meta-label {
  color: #999;
}

.meta-value {
  color: #333;
  font-weight: 500;
}

.sku-section,
.stock-section,
.quantity-section {
  margin-bottom: 20px;
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.sku-label,
.stock-label,
.quantity-label {
  color: #999;
  width: 60px;
  flex-shrink: 0;
}

.sku-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.sku-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.sku-item:hover,
.sku-item.active {
  border-color: #409eff;
  color: #409eff;
}

.sku-item img {
  width: 30px;
  height: 30px;
  border-radius: 4px;
  object-fit: cover;
}

.stock-value {
  color: #333;
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.action-buttons .el-button {
  padding: 15px 40px;
  font-size: 16px;
}

.product-description {
  background: #fff;
  border-radius: 8px;
}

.detail-content {
  padding: 20px;
  min-height: 400px;
}

.specs-content {
  padding: 20px;
  min-height: 400px;
}
</style>
