<template>
  <div class="product-page">
    <!-- 页头 -->
    <div class="page-header">
      <h2>商品管理</h2>
      <el-button type="primary" @click="openCreateDialog">新增商品</el-button>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索商品名称"
        style="width: 240px"
        clearable
        @keyup.enter="handleSearch"
      />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
      <el-button @click="resetSearch">重置</el-button>
    </div>

    <!-- 表格 -->
    <el-table :data="productList" v-loading="loading" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="商品名称" min-width="160" />
      <el-table-column prop="brand" label="品牌" width="120" />
      <el-table-column prop="category" label="分类" width="100" />
      <el-table-column prop="price" label="价格" width="100">
        <template #default="{ row }">
          ¥{{ row.price }}
        </template>
      </el-table-column>
      <el-table-column prop="stock" label="库存" width="80" />
      <el-table-column prop="sales" label="销量" width="80" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'info'" disable-transitions>
            {{ row.status === 1 ? '上架' : '下架' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
          <el-button
            size="small"
            :type="row.status === 1 ? 'warning' : 'success'"
            @click="toggleStatus(row)"
          >
            {{ row.status === 1 ? '下架' : '上架' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination-wrap">
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        @size-change="fetchProducts"
        @current-change="fetchProducts"
      />
    </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="resetForm"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入商品名称" />
        </el-form-item>
        <el-form-item label="副标题" prop="subtitle">
          <el-input v-model="form.subtitle" placeholder="请输入副标题" />
        </el-form-item>
        <el-form-item label="分类ID" prop="category_id">
          <el-input-number v-model="form.category_id" :min="1" />
        </el-form-item>
        <el-form-item label="品牌ID" prop="brand_id">
          <el-input-number v-model="form.brand_id" :min="1" />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="form.price" :min="0.01" :precision="2" />
        </el-form-item>
        <el-form-item label="原价" prop="original_price">
          <el-input-number v-model="form.original_price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="库存" prop="stock">
          <el-input-number v-model="form.stock" :min="0" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio :value="1">上架</el-radio>
            <el-radio :value="0">下架</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { productApi } from '@/api/product'

// 列表数据
const productList = ref([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const searchKeyword = ref('')

// 弹窗
const dialogVisible = ref(false)
const dialogTitle = computed(() => (editingId.value ? '编辑商品' : '新增商品'))
const editingId = ref(null)
const submitLoading = ref(false)
const formRef = ref(null)

// 表单
const defaultForm = () => ({
  name: '',
  subtitle: '',
  category_id: null,
  brand_id: null,
  price: null,
  original_price: null,
  description: '',
  stock: 0,
  status: 1,
})

const form = reactive(defaultForm())

const rules = {
  name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '价格必须大于0', trigger: 'blur' },
  ],
}

// 获取列表
async function fetchProducts() {
  loading.value = true
  try {
    const res = await productApi.getProducts({
      page,
      page_size: pageSize.value,
      keyword: searchKeyword.value || undefined,
    })
    productList.value = res.data || []
    total.value = res.total || 0
  } catch {
    ElMessage.error('获取商品列表失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  page.value = 1
  fetchProducts()
}

function resetSearch() {
  searchKeyword.value = ''
  page.value = 1
  fetchProducts()
}

// 打开新增
function openCreateDialog() {
  editingId.value = null
  Object.assign(form, defaultForm())
  dialogVisible.value = true
}

// 打开编辑
function openEditDialog(row) {
  editingId.value = row.id
  Object.assign(form, {
    name: row.name,
    subtitle: row.subtitle || '',
    category_id: row.category_id || null,
    brand_id: row.brand_id || null,
    price: row.price,
    original_price: row.original_price || null,
    description: row.description || '',
    stock: row.stock,
    status: row.status,
  })
  dialogVisible.value = true
}

// 提交表单
async function submitForm() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitLoading.value = true
  try {
    if (editingId.value) {
      await productApi.updateProduct(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      await productApi.createProduct(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchProducts()
  } catch {
    ElMessage.error(editingId.value ? '更新失败' : '创建失败')
  } finally {
    submitLoading.value = false
  }
}

// 重置表单
function resetForm() {
  formRef.value?.resetFields()
  Object.assign(form, defaultForm())
  editingId.value = null
}

// 上下架切换
async function toggleStatus(row) {
  const newStatus = row.status === 1 ? 0 : 1
  try {
    await productApi.updateProduct(row.id, { status: newStatus })
    ElMessage.success(newStatus === 1 ? '上架成功' : '下架成功')
    fetchProducts()
  } catch {
    ElMessage.error('操作失败')
  }
}

fetchProducts()
</script>

<style scoped>
.product-page {
  padding: 24px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}

.pagination-wrap {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
