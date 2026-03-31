<template>
  <div class="product-list">
    <div class="container">
      <div class="filters">
        <h3>商品分类</h3>
        <div class="category-list">
          <div
            v-for="cat in categories"
            :key="cat.id"
            class="category-item"
            :class="{ active: queryParams.categoryId === cat.id }"
            @click="selectCategory(cat.id)"
          >
            {{ cat.name }}
          </div>
        </div>

        <h3 style="margin-top: 20px">品牌筛选</h3>
        <div class="brand-list">
          <div
            v-for="brand in brands"
            :key="brand.id"
            class="brand-item"
            :class="{ active: queryParams.brandId === brand.id }"
            @click="selectBrand(brand.id)"
          >
            {{ brand.name }}
          </div>
        </div>
      </div>

      <div class="products">
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

        <div class="product-grid">
          <div
            v-for="product in products"
            :key="product.id"
            class="product-card"
            @click="goToDetail(product.id!)"
          >
            <div class="product-image">
              <img :src="product.mainImage || 'https://via.placeholder.com/300x300'" :alt="product.name" />
            </div>
            <div class="product-info">
              <h3 class="product-name">{{ product.name }}</h3>
              <p class="product-subtitle">{{ product.subtitle }}</p>
              <div class="product-price">
                <span class="price">¥{{ product.minPrice?.toFixed(2) }}</span>
                <span v-if="product.maxPrice && product.maxPrice !== product.minPrice" class="price-range">
                  - ¥{{ product.maxPrice?.toFixed(2) }}
                </span>
              </div>
              <div class="product-meta">
                <span>销量: {{ product.salesCount }}</span>
                <span>浏览: {{ product.viewCount }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="pagination">
          <el-pagination
            v-model:current-page="queryParams.page"
            v-model:page-size="queryParams.pageSize"
            :total="total"
            :page-sizes="[12, 24, 48]"
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
import { shopProductApi, ProductSpu, Category, Brand } from '@/api/product'

const router = useRouter()

const queryParams = ref({
  page: 1,
  pageSize: 12,
  keyword: '',
  categoryId: undefined as number | undefined,
  brandId: undefined as number | undefined
})

const products = ref<ProductSpu[]>([])
const categories = ref<Category[]>([])
const brands = ref<Brand[]>([])
const total = ref(0)

const loadCategories = async () => {
  try {
    const res = await shopProductApi.getCategories()
    if (res.data) {
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

const loadBrands = async () => {
  try {
    const res = await shopProductApi.getBrands()
    if (res.data) {
      brands.value = res.data
    }
  } catch (error) {
    console.error('加载品牌失败', error)
  }
}

const loadProducts = async () => {
  try {
    const res = await shopProductApi.getProducts(queryParams.value)
    if (res.data) {
      products.value = res.data.items
      total.value = res.data.total
    }
  } catch (error) {
    ElMessage.error('加载商品失败')
  }
}

const selectCategory = (categoryId: number | undefined) => {
  queryParams.value.categoryId = categoryId === queryParams.value.categoryId ? undefined : categoryId
  queryParams.value.page = 1
  loadProducts()
}

const selectBrand = (brandId: number | undefined) => {
  queryParams.value.brandId = brandId === queryParams.value.brandId ? undefined : brandId
  queryParams.value.page = 1
  loadProducts()
}

const handleSearch = () => {
  queryParams.value.page = 1
  loadProducts()
}

const goToDetail = (id: number) => {
  router.push(`/product/${id}`)
}

onMounted(() => {
  loadCategories()
  loadBrands()
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
  display: flex;
  gap: 20px;
}

.filters {
  width: 220px;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  flex-shrink: 0;
}

.filters h3 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #333;
}

.category-item,
.brand-item {
  padding: 8px 12px;
  margin-bottom: 8px;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s;
}

.category-item:hover,
.brand-item:hover {
  background: #f0f0f0;
}

.category-item.active,
.brand-item.active {
  background: #409eff;
  color: #fff;
}

.products {
  flex: 1;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.product-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}

.product-image {
  width: 100%;
  height: 220px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  padding: 15px;
}

.product-name {
  font-size: 14px;
  color: #333;
  margin: 0 0 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-subtitle {
  font-size: 12px;
  color: #999;
  margin: 0 0 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  margin-bottom: 10px;
}

.price {
  font-size: 20px;
  color: #e74c3c;
  font-weight: bold;
}

.price-range {
  font-size: 14px;
  color: #e74c3c;
}

.product-meta {
  font-size: 12px;
  color: #999;
  display: flex;
  justify-content: space-between;
}

.pagination {
  display: flex;
  justify-content: center;
}
</style>
