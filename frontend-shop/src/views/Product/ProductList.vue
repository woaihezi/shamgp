<template>
  <div class="product-list">
    <div class="container">
      <div class="products">
        <!-- 搜索栏 -->
        <div class="search-bar">
          <el-input
            v-model="queryParams.keyword"
            placeholder="搜索商品"
            clearable
            style="width: 300px"
            @keyup.enter="handleSearch"
          >
            <template #append>
              <el-button :icon="Search" @click="handleSearch" />
            </template>
          </el-input>
        </div>

        <!-- 分类筛选器 + 排序 -->
        <div class="filter-row">
          <div class="filter-bar">
            <span
              :class="{ active: !selectedCategory }"
              @click="selectCategory(null)"
            >全部</span>
            <span
              v-for="cat in categories"
              :key="cat.id"
              :class="{ active: selectedCategory === cat.id }"
              @click="selectCategory(cat.id)"
            >
              {{ cat.name }}
            </span>
          </div>
          <div class="sort-bar">
            <el-select v-model="sortBy" @change="handleSortChange" style="width: 160px">
              <el-option label="综合" value="default" />
              <el-option label="价格从低到高" value="price_asc" />
              <el-option label="价格从高到低" value="price_desc" />
              <el-option label="销量优先" value="sales" />
            </el-select>
          </div>
        </div>

        <!-- 商品列表 -->
        <div class="product-grid">
          <div
            v-for="product in products"
            :key="product.id"
            class="product-card"
            @click="goToDetail(product.id!)"
          >
            <div class="product-image">
              <img
                :src="product.cover_image || product.mainImage || 'https://via.placeholder.com/300x300'"
                :alt="product.name"
              />
              <span v-if="product.is_hot" class="tag hot">热卖</span>
              <span v-if="product.is_new" class="tag new">新品</span>
            </div>
            <div class="product-info">
              <h3 class="product-name">{{ product.name }}</h3>
              <p class="product-subtitle">{{ product.subtitle }}</p>
              <div class="product-price">
                <span class="price">¥{{ (product.minPrice || product.price || 0).toFixed(2) }}</span>
                <span
                  v-if="product.maxPrice && product.maxPrice !== product.minPrice"
                  class="price-range"
                >
                  - ¥{{ product.maxPrice?.toFixed(2) }}
                </span>
                <span v-if="product.original_price" class="original-price">
                  ¥{{ product.original_price.toFixed(2) }}
                </span>
              </div>
              <div class="product-meta">
                <span>销量: {{ product.sales || product.salesCount || 0 }}</span>
                <span v-if="product.views || product.viewCount">
                  浏览: {{ product.views || product.viewCount }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="products.length === 0 && !loading" class="empty-state">
          <p>暂无商品</p>
        </div>

        <!-- 分页 -->
        <div class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            :total="total"
            :page-size="pageSize"
            layout="prev, pager, next"
            @current-change="loadProducts"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { shopProductApi, ProductSpu, Category } from '@/api/product'

const router = useRouter()

const loading = ref(false)

// 查询参数
const queryParams = ref({
  keyword: ''
})

// 分页
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 分类
const selectedCategory = ref<number | null>(null)
const categories = ref<Category[]>([])

// 排序
const sortBy = ref('default')

// 商品列表
const products = ref<ProductSpu[]>([])

// 加载分类
const loadCategories = async () => {
  try {
    const res = await shopProductApi.getCategories()
    if (res.data) {
      // 递归扁平化分类（包含子分类）
      const flatten = (cats: Category[]): Category[] => {
        let result: Category[] = []
        cats.forEach(cat => {
          result.push(cat)
          if (cat.children?.length) {
            result = result.concat(flatten(cat.children))
          }
        })
        return result
      }
      categories.value = flatten(res.data)
    }
  } catch (error) {
    console.error('加载分类失败', error)
  }
}

// 加载商品列表
const loadProducts = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      pageSize: pageSize.value,
      keyword: queryParams.value.keyword || undefined
    }
    if (selectedCategory.value) {
      params.categoryId = selectedCategory.value
    }
    // 排序参数
    if (sortBy.value === 'price_asc') {
      params.sort = 'price'
      params.order = 'asc'
    } else if (sortBy.value === 'price_desc') {
      params.sort = 'price'
      params.order = 'desc'
    } else if (sortBy.value === 'sales') {
      params.sort = 'sales'
      params.order = 'desc'
    }

    const res = await shopProductApi.getProducts(params)
    if (res.data) {
      products.value = res.data.items || []
      total.value = res.data.total || 0
    }
  } catch (error) {
    ElMessage.error('加载商品失败')
  } finally {
    loading.value = false
  }
}

// 选择分类
const selectCategory = (categoryId: number | null) => {
  selectedCategory.value = categoryId
  currentPage.value = 1
  loadProducts()
}

// 排序变化
const handleSortChange = () => {
  currentPage.value = 1
  loadProducts()
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  loadProducts()
}

// 跳转详情
const goToDetail = (id: number) => {
  router.push(`/product/${id}`)
}

onMounted(() => {
  loadCategories()
  loadProducts()
})
</script>

<style scoped>
.product-list {
  padding: 20px 0;
  background: #f5f5f5;
  min-height: calc(100vh - 100px);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.products {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}

.search-bar {
  margin-bottom: 16px;
  display: flex;
  justify-content: flex-end;
}

.filter-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 16px;
}

.filter-bar {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  flex: 1;
}

.filter-bar span {
  cursor: pointer;
  padding: 6px 16px;
  border-radius: 16px;
  background: #f5f5f5;
  font-size: 14px;
  transition: all 0.2s;
  white-space: nowrap;
}

.filter-bar span.active {
  background: #ff4400;
  color: #fff;
}

.filter-bar span:hover:not(.active) {
  background: #ffddcc;
}

.sort-bar {
  flex-shrink: 0;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 30px;
}

.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  background: #fff;
}

.product-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}

.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  position: relative;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-image .tag {
  position: absolute;
  top: 8px;
  left: 8px;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: #fff;
}

.product-image .tag.hot {
  background: #e74c3c;
}

.product-image .tag.new {
  background: #2ecc71;
}

.product-info {
  padding: 12px;
}

.product-name {
  font-size: 14px;
  color: #333;
  margin: 0 0 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-subtitle {
  font-size: 12px;
  color: #999;
  margin: 0 0 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  margin-bottom: 8px;
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.price {
  font-size: 18px;
  color: #e74c3c;
  font-weight: bold;
}

.price-range {
  font-size: 13px;
  color: #e74c3c;
}

.original-price {
  font-size: 12px;
  color: #999;
  text-decoration: line-through;
}

.product-meta {
  font-size: 12px;
  color: #999;
  display: flex;
  justify-content: space-between;
}

.empty-state {
  text-align: center;
  padding: 60px 0;
  color: #999;
  font-size: 14px;
}

.pagination {
  display: flex;
  justify-content: center;
}
</style>
