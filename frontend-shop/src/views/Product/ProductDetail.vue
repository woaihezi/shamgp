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
        <!-- 图片画廊 -->
        <div class="image-gallery">
          <!-- 缩略图列表 -->
          <div class="thumb-list">
            <div
              v-for="(img, idx) in imageList"
              :key="idx"
              :class="['thumb', { active: idx === currentIndex }]"
              @click="activeImage = img; currentIndex = idx"
            >
              <img :src="img" />
            </div>
          </div>
          <!-- 主图 -->
          <div class="main-image">
            <img :src="activeImage" />
            <!-- 左右切换箭头 -->
            <span class="arrow left" @click="prevImage" v-if="currentIndex > 0">‹</span>
            <span class="arrow right" @click="nextImage" v-if="currentIndex < imageList.length - 1">›</span>
            <!-- 图片计数 -->
            <div class="image-counter" v-if="imageList.length > 1">{{ currentIndex + 1 }} / {{ imageList.length }}</div>
          </div>
        </div>

        <div class="product-info">
          <h1 class="product-title">{{ product.name }}</h1>
          <p class="product-subtitle">{{ product.subtitle }}</p>

          <!-- 价格区间 -->
          <div class="price-section" v-if="!selectedSku">
            <span class="price-label">价格</span>
            <div class="price-wrap">
              <span class="current-price">¥{{ minPrice }}</span>
              <span v-if="maxPrice && maxPrice !== minPrice" class="price-range">
                - ¥{{ maxPrice }}
              </span>
              <span v-if="originalPrice" class="original-price">¥{{ originalPrice }}</span>
            </div>
          </div>

          <!-- SKU 价格（选中规格后显示） -->
          <div class="price-section" v-else>
            <span class="price-label">价格</span>
            <div class="price-wrap">
              <span class="current-price">¥{{ selectedSku.price }}</span>
              <span v-if="selectedSku.originalPrice" class="original-price">¥{{ selectedSku.originalPrice }}</span>
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

          <!-- SKU 选择器（按规格维度展开） -->
          <div class="sku-selector" v-if="Object.keys(specOptions).length > 0">
            <div v-for="(values, specName) in specOptions" :key="specName" class="spec-row">
              <span class="spec-name">{{ specName }}：</span>
              <div class="spec-values">
                <button
                  v-for="val in values"
                  :key="val"
                  :class="['spec-btn', { active: selectedSpecs[specName] === val, disabled: !isSpecAvailable(specName, val) }]"
                  @click="selectSpec(specName, val)"
                >
                  {{ val }}
                </button>
              </div>
            </div>
            <div class="sku-info" v-if="selectedSku">
              <span>已选：{{ selectedSku.name || (selectedSku as any).sku_name }}</span>
              <span class="sku-price">¥{{ selectedSku.price }}</span>
            </div>
          </div>

          <!-- 旧版 SKU 列表（当没有 specs JSON 时降级显示） -->
          <div class="sku-section" v-else-if="skus.length">
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

          <!-- 库存 -->
          <div class="stock-section">
            <div class="stock-label">库存</div>
            <div class="stock-value">
              {{ displayStock }} {{ product.unit || '件' }}
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
            <el-button size="large" @click="toggleFavorite" :type="isFavorited ? 'danger' : 'default'">
              {{ isFavorited ? '已收藏' : '收藏' }}
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { shopProductApi, ProductSpu, ProductSku, ProductImage } from '@/api/product'
import { cartApi } from '@/api/cart'

const route = useRoute()
const router = useRouter()

const product = ref<ProductSpu | null>(null)
const skus = ref<ProductSku[]>([])
const carouselImages = ref<ProductImage[]>([])
const selectedSku = ref<ProductSku | null>(null)
const activeImageIndex = ref(0)
const activeTab = ref('detail')
const quantity = ref(1)
const isFavorited = ref(false)

// ─────────────────────────────────────
// 图片画廊
// ─────────────────────────────────────
const imageList = computed(() => {
  if (!product.value) return []
  // 优先用 images JSON 字段，否则用 cover_image / mainImage
  const cover = product.value.cover_image || product.value.mainImage || ''
  let extra: string[] = []
  if (product.value.images) {
    try {
      extra = JSON.parse(product.value.images as unknown as string)
    } catch {
      extra = []
    }
  }
  return [cover, ...extra].filter(Boolean)
})

const activeImage = ref('')
const currentIndex = ref(0)

watch(imageList, (list) => {
  if (list.length > 0) {
    activeImage.value = list[0]
    currentIndex.value = 0
  }
}, { immediate: true })

const prevImage = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    activeImage.value = imageList.value[currentIndex.value]
  }
}

const nextImage = () => {
  if (currentIndex.value < imageList.value.length - 1) {
    currentIndex.value++
    activeImage.value = imageList.value[currentIndex.value]
  }
}

// ─────────────────────────────────────
// SKU 规格解析（按维度展开）
// ─────────────────────────────────────
const skuList = computed(() => {
  if (!product.value?.skus || (product.value.skus as unknown as ProductSku[]).length === 0) return []
  return product.value.skus as unknown as ProductSku[]
})

// 提取所有规格维度及选项，如 { 颜色: ['黑色', '白色'], 容量: ['128G', '256G'] }
const specOptions = computed(() => {
  const list = skuList.value
  if (!list || list.length === 0) return {}
  const options: Record<string, Set<string>> = {}
  for (const sku of list) {
    try {
      const s = JSON.parse((sku as any).specs || '{}')
      for (const key of Object.keys(s)) {
        if (!options[key]) options[key] = new Set<string>()
        if (s[key]) options[key].add(s[key])
      }
    } catch {
      // 跳过解析失败的 SKU
    }
  }
  const result: Record<string, string[]> = {}
  for (const key of Object.keys(options)) {
    result[key] = Array.from(options[key])
  }
  return result
})

// 当前选中的规格映射
const selectedSpecs = ref<Record<string, string>>({})

// 当前匹配到的完整 SKU
const selectedSkuBySpecs = computed(() => {
  const list = skuList.value
  if (!list || list.length === 0) return null
  if (Object.keys(selectedSpecs.value).length < Object.keys(specOptions.value).length) return null
  for (const sku of list) {
    try {
      const s = JSON.parse((sku as any).specs || '{}')
      let match = true
      for (const key of Object.keys(selectedSpecs.value)) {
        if (s[key] !== selectedSpecs.value[key]) { match = false; break }
      }
      if (match) return sku as ProductSku
    } catch {
      // 跳过
    }
  }
  return null
})

// 监听 spec 选择变化，同步 selectedSku
watch(selectedSkuBySpecs, (sku) => {
  if (sku) selectedSku.value = sku
})

const selectSpec = (specName: string, val: string) => {
  if (!isSpecAvailable(specName, val)) return
  selectedSpecs.value = { ...selectedSpecs.value, [specName]: val }
}

const isSpecAvailable = (specName: string, val: string): boolean => {
  const list = skuList.value
  const testSpecs = { ...selectedSpecs.value, [specName]: val }
  for (const sku of list) {
    try {
      const s = JSON.parse((sku as any).specs || '{}')
      let match = true
      for (const key of Object.keys(testSpecs)) {
        if (s[key] !== testSpecs[key]) { match = false; break }
      }
      if (match && (sku as any).stock > 0) return true
    } catch {
      // 跳过
    }
  }
  return false
}

// ─────────────────────────────────────
// 价格 / 库存显示
// ─────────────────────────────────────
const displayStock = computed(() => {
  if (selectedSku.value) {
    const inv = (selectedSku.value as any).inventory
    if (inv?.availableStock !== undefined) return inv.availableStock
    return (selectedSku.value as any).stock ?? 0
  }
  return product.value?.stock ?? 0
})

const minPrice = computed(() => {
  if (!skus.value.length) return (product.value?.price ?? 0).toFixed(2)
  return Math.min(...skus.value.map(s => s.price)).toFixed(2)
})

const maxPrice = computed(() => {
  if (!skus.value.length) return 0
  return Math.max(...skus.value.map(s => s.price)).toFixed(2)
})

const originalPrice = computed(() => {
  if (!skus.value.length) return null
  const prices = skus.value.map(s => (s as any).originalPrice).filter(p => p) as number[]
  if (!prices.length) return null
  return Math.max(...prices).toFixed(2)
})

const maxStock = computed(() => {
  if (selectedSku.value) {
    const inv = (selectedSku.value as any).inventory
    if (inv?.availableStock) return inv.availableStock
    return (selectedSku.value as any).stock ?? 999
  }
  return 999
})

// ─────────────────────────────────────
// 收藏
// ─────────────────────────────────────
const toggleFavorite = async () => {
  try {
    if (isFavorited.value) {
      await shopProductApi.removeFavorite(product.value!.id!)
    } else {
      await shopProductApi.addFavorite(product.value!.id!)
    }
    isFavorited.value = !isFavorited.value
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// ─────────────────────────────────────
// 商品加载
// ─────────────────────────────────────
const loadProduct = async (id: number) => {
  try {
    const res = await shopProductApi.getProduct(id)
    if (res.data) {
      product.value = res.data
      skus.value = res.data.skus || []
      carouselImages.value = (res.data.images || []).filter((img: ProductImage) => img.imageType === 0)

      if (skus.value.length) {
        selectedSku.value = skus.value[0]
      }
    }
    if (product.value?.id) {
      try {
        await shopProductApi.addBrowseHistory(product.value.id)
      } catch (e) {
        // 静默失败
      }
    }
  } catch (error) {
    ElMessage.error('加载商品详情失败')
  }
}

const selectSku = (sku: ProductSku) => {
  selectedSku.value = sku
}

const addToCart = async () => {
  if (!selectedSku.value) {
    ElMessage.warning('请选择商品规格')
    return
  }
  try {
    await cartApi.addItem({
      product_id: product.value?.id!,
      sku_id: selectedSku.value.id,
      quantity: quantity.value
    })
    ElMessage.success('已加入购物车')
  } catch (error: any) {
    ElMessage.error(error?.message || '加入购物车失败')
  }
}

const buyNow = async () => {
  if (!selectedSku.value) {
    ElMessage.warning('请选择商品规格')
    return
  }
  try {
    await cartApi.addItem({
      product_id: product.value?.id!,
      sku_id: selectedSku.value.id,
      quantity: quantity.value
    })
    router.push('/checkout')
  } catch (error: any) {
    ElMessage.error(error?.message || '操作失败')
  }
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

/* ─────────────────────────────────────
   图片画廊
───────────────────────────────────── */
.image-gallery {
  display: flex;
  gap: 12px;
  width: 500px;
  flex-shrink: 0;
}

.thumb-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 68px;
  flex-shrink: 0;
}

.thumb {
  width: 60px;
  height: 60px;
  border: 2px solid transparent;
  cursor: pointer;
  border-radius: 4px;
  overflow: hidden;
  transition: border-color 0.2s;
}

.thumb.active {
  border-color: #ff4400;
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.main-image {
  position: relative;
  width: 400px;
  height: 400px;
  border-radius: 8px;
  overflow: hidden;
  background: #fafafa;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.main-image .arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 32px;
  cursor: pointer;
  background: rgba(0, 0, 0, 0.3);
  color: white;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  user-select: none;
  transition: background 0.2s;
}

.main-image .arrow:hover {
  background: rgba(0, 0, 0, 0.5);
}

.main-image .arrow.left {
  left: 8px;
}

.main-image .arrow.right {
  right: 8px;
}

.main-image .image-counter {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}

/* ─────────────────────────────────────
   商品信息
───────────────────────────────────── */
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

/* ─────────────────────────────────────
   SKU 选择器（规格维度展开）
───────────────────────────────────── */
.sku-selector {
  margin: 16px 0;
}

.spec-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.spec-name {
  width: 70px;
  font-size: 14px;
  color: #666;
  flex-shrink: 0;
}

.spec-values {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.spec-btn {
  padding: 4px 12px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 4px;
  font-size: 13px;
  transition: all 0.2s;
  color: #333;
}

.spec-btn.active {
  border-color: #ff4400;
  color: #ff4400;
  background: #fff5f2;
}

.spec-btn.disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.sku-info {
  margin-top: 8px;
  font-size: 14px;
  color: #333;
}

.sku-price {
  color: #ff4400;
  font-weight: bold;
  margin-left: 12px;
}

/* 旧版 SKU 列表降级 */
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

.quantity-section {
  margin-bottom: 20px;
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.quantity-label {
  color: #999;
  width: 60px;
  flex-shrink: 0;
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
