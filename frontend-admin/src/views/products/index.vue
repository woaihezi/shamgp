<template>
  <div class="products-page">
    <el-card>
      <!-- 页头 -->
      <template #header>
        <div class="card-header">
          <span class="title">商品管理</span>
          <el-button type="primary" @click="openDialog()">新增商品</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <el-form :inline="true" class="search-form">
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.keyword"
            placeholder="商品名称 / 品牌 / 分类"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="名称" min-width="160" />
        <el-table-column prop="brand" label="品牌" min-width="120" />
        <el-table-column prop="category" label="分类" min-width="100" />
        <el-table-column prop="price" label="价格（元）" width="110">
          <template #default="{ row }">
            {{ row.price != null ? `¥${row.price.toFixed(2)}` : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="90" />
        <el-table-column prop="sales" label="销量" width="90" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'" size="small">
              {{ row.status === 1 ? '上架' : '下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="openDialog(row)">编辑</el-button>
            <el-button
              size="small"
              :type="row.status === 1 ? 'warning' : 'success'"
              link
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
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadData"
          @current-change="loadData"
        />
      </div>
    </el-card>

    <!-- 新增 / 编辑弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'add' ? '新增商品' : '编辑商品'"
      width="600px"
      @closed="resetForm"
    >
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入商品名称" />
        </el-form-item>
        <el-form-item label="副标题" prop="subtitle">
          <el-input v-model="formData.subtitle" placeholder="请输入副标题" />
        </el-form-item>
        <el-form-item label="品牌" prop="brandId">
          <el-input-number v-model="formData.brandId" :min="1" placeholder="品牌ID" style="width: 100%" />
        </el-form-item>
        <el-form-item label="分类" prop="categoryId">
          <el-input-number v-model="formData.categoryId" :min="1" placeholder="分类ID" style="width: 100%" />
        </el-form-item>
        <el-form-item label="价格（元）" prop="price">
          <el-input-number v-model="formData.price" :min="0" :precision="2" placeholder="现价" style="width: 100%" />
        </el-form-item>
        <el-form-item label="原价（元）" prop="originalPrice">
          <el-input-number v-model="formData.originalPrice" :min="0" :precision="2" placeholder="原价（选填）" style="width: 100%" />
        </el-form-item>
        <el-form-item label="库存" prop="stock">
          <el-input-number v-model="formData.stock" :min="0" placeholder="库存数量" style="width: 100%" />
        </el-form-item>
        <el-form-item label="商品描述" prop="description">
          <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入商品描述" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio :value="1">上架</el-radio>
            <el-radio :value="0">下架</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { getProducts, createProduct, updateProduct } from '@/api/product'

// 搜索表单
const searchForm = reactive({
  keyword: ''
})

// 表格数据
const tableData = ref<any[]>([])
const loading = ref(false)

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 弹窗
const dialogVisible = ref(false)
const dialogMode = ref<'add' | 'edit'>('add')
const submitLoading = ref(false)
const formRef = ref<FormInstance>()
const editingId = ref<number | null>(null)

const formData = reactive({
  name: '',
  subtitle: '',
  brandId: undefined as number | undefined,
  categoryId: undefined as number | undefined,
  price: undefined as number | undefined,
  originalPrice: undefined as number | undefined,
  stock: undefined as number | undefined,
  description: '',
  status: 1
})

const formRules: FormRules = {
  name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  stock: [{ required: true, message: '请输入库存', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      keyword: searchForm.keyword || undefined
    }
    const res: any = await getProducts(params)
    tableData.value = res.items ?? res.data ?? res.list ?? []
    pagination.total = res.total ?? 0
  } catch {
    ElMessage.error('加载商品列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  loadData()
}

// 重置
const handleReset = () => {
  searchForm.keyword = ''
  pagination.page = 1
  loadData()
}

// 打开弹窗
const openDialog = (row?: any) => {
  if (row) {
    dialogMode.value = 'edit'
    editingId.value = row.id
    Object.assign(formData, {
      name: row.name ?? '',
      subtitle: row.subtitle ?? '',
      brandId: row.brandId ?? undefined,
      categoryId: row.categoryId ?? undefined,
      price: row.price ?? undefined,
      originalPrice: row.originalPrice ?? undefined,
      stock: row.stock ?? undefined,
      description: row.description ?? '',
      status: row.status ?? 1
    })
  } else {
    dialogMode.value = 'add'
    editingId.value = null
    resetForm()
  }
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  formRef.value?.resetFields()
  Object.assign(formData, {
    name: '',
    subtitle: '',
    brandId: undefined,
    categoryId: undefined,
    price: undefined,
    originalPrice: undefined,
    stock: undefined,
    description: '',
    status: 1
  })
}

// 提交
const handleSubmit = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
  } catch {
    return
  }
  submitLoading.value = true
  try {
    if (dialogMode.value === 'add') {
      await createProduct(formData)
      ElMessage.success('新增成功')
    } else {
      await updateProduct(editingId.value!, formData)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    loadData()
  } catch {
    ElMessage.error(dialogMode.value === 'add' ? '新增失败' : '更新失败')
  } finally {
    submitLoading.value = false
  }
}

// 切换上下架
const toggleStatus = async (row: any) => {
  const newStatus = row.status === 1 ? 0 : 1
  try {
    await updateProduct(row.id, { status: newStatus })
    ElMessage.success(newStatus === 1 ? '上架成功' : '下架成功')
    loadData()
  } catch {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.products-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

.search-form {
  margin-bottom: 16px;
}

.pagination-wrap {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
