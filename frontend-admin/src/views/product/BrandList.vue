<template>
  <div class="brand-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>品牌管理</span>
          <el-button type="primary" @click="handleAdd">新增品牌</el-button>
        </div>
      </template>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="Logo" width="100">
          <template #default="{ row }">
            <el-image
              v-if="row.logo"
              :src="row.logo"
              style="width: 60px; height: 60px"
              fit="cover"
            />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="品牌名称" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="sort" label="排序" width="100" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="品牌名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入品牌名称" />
        </el-form-item>
        <el-form-item label="Logo" prop="logo">
          <el-input v-model="form.logo" placeholder="请输入Logo URL" />
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="form.sort" :min="0" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入品牌描述"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio :value="1">启用</el-radio>
            <el-radio :value="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance, FormRules } from 'element-plus'
import { brandApi, Brand } from '@/api/product'

const tableData = ref<Brand[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('新增品牌')
const formRef = ref<FormInstance>()
const isEdit = ref(false)

const form = reactive<Brand>({
  name: '',
  logo: '',
  sort: 0,
  description: '',
  status: 1
})

const rules = reactive<FormRules<Brand>>({
  name: [{ required: true, message: '请输入品牌名称', trigger: 'blur' }]
})

const loadData = async () => {
  try {
    const res = await brandApi.getList()
    if (res.data) {
      tableData.value = res.data
    }
  } catch (error) {
    ElMessage.error('加载数据失败')
  }
}

const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增品牌'
  Object.assign(form, {
    name: '',
    logo: '',
    sort: 0,
    description: '',
    status: 1
  })
  dialogVisible.value = true
}

const handleEdit = (row: Brand) => {
  isEdit.value = true
  dialogTitle.value = '编辑品牌'
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleDelete = async (row: Brand) => {
  try {
    await ElMessageBox.confirm('确定要删除该品牌吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await brandApi.delete(row.id!)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          await brandApi.update(form.id!, form)
          ElMessage.success('更新成功')
        } else {
          await brandApi.create(form)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadData()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }
  })
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.brand-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
