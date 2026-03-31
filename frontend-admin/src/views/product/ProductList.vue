<template>
  <div class="product-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>商品列表</span>
          <el-button type="primary" @click="handleAdd">新增商品</el-button>
        </div>
      </template>
      
      <el-form :inline="true" :model="queryParams" class="search-form">
        <el-form-item label="关键词">
          <el-input v-model="queryParams.keyword" placeholder="商品名称" clearable />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="queryParams.categoryId" placeholder="请选择分类" clearable>
            <el-option
              v-for="cat in categories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="请选择状态" clearable>
            <el-option label="下架" :value="0" />
            <el-option label="上架" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="商品名称" />
        <el-table-column prop="category.name" label="分类" width="120" />
        <el-table-column prop="brand.name" label="品牌" width="120" />
        <el-table-column label="价格区间" width="150">
          <template #default="{ row }">
            {{ row.minPrice ? '¥' + row.minPrice : '-' }} - {{ row.maxPrice ? '¥' + row.maxPrice : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="salesCount" label="销量" width="100" />
        <el-table-column prop="viewCount" label="浏览量" width="100" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '上架' : '下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button
              v-if="row.status === 0"
              size="small"
              type="success"
              @click="handlePublish(row)"
            >
              上架
            </el-button>
            <el-button
              v-else
              size="small"
              type="warning"
              @click="handleUnpublish(row)"
            >
              下架
            </el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="queryParams.page"
        v-model:page-size="queryParams.pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSearch"
        @current-change="handleSearch"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { productApi, categoryApi, ProductSpu, Category } from '@/api/product'

const queryParams = ref({
  page: 1,
  pageSize: 20,
  keyword: '',
  categoryId: undefined as number | undefined,
  status: undefined as number | undefined
})

const tableData = ref<ProductSpu[]>([])
const total = ref(0)
const categories = ref<Category[]>([])

const loadData = async () => {
  try {
    const res = await productApi.getList(queryParams.value)
    if (res.data) {
      tableData.value = res.data.items
      total.value = res.data.total
    }
  } catch (error) {
    ElMessage.error('加载数据失败')
  }
}

const loadCategories = async () => {
  try {
    const res = await categoryApi.getTree()
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
    ElMessage.error('加载分类失败')
  }
}

const handleSearch = () => {
  queryParams.value.page = 1
  loadData()
}

const handleReset = () => {
  queryParams.value = {
    page: 1,
    pageSize: 20,
    keyword: '',
    categoryId: undefined,
    status: undefined
  }
  loadData()
}

const handleAdd = () => {
  ElMessage.info('新增商品功能')
}

const handleEdit = (row: ProductSpu) => {
  ElMessage.info('编辑商品: ' + row.name)
}

const handlePublish = async (row: ProductSpu) => {
  try {
    await ElMessageBox.confirm('确定要上架该商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await productApi.publish(row.id!)
    ElMessage.success('上架成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('上架失败')
    }
  }
}

const handleUnpublish = async (row: ProductSpu) => {
  try {
    await ElMessageBox.confirm('确定要下架该商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await productApi.unpublish(row.id!)
    ElMessage.success('下架成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('下架失败')
    }
  }
}

const handleDelete = async (row: ProductSpu) => {
  try {
    await ElMessageBox.confirm('确定要删除该商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await productApi.delete(row.id!)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadData()
  loadCategories()
})
</script>

<style scoped>
.product-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}
</style>
