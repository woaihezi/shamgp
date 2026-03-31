<template>
  <div class="banner-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>轮播图管理</span>
          <el-button type="primary" @click="handleAdd">新增轮播图</el-button>
        </div>
      </template>

      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="image_url" label="图片" width="200">
          <template #default="{ row }">
            <el-image
              :src="row.image_url"
              style="width: 100px; height: 60px"
              fit="cover"
              :preview-src-list="[row.image_url]"
            />
          </template>
        </el-table-column>
        <el-table-column prop="sort" label="排序" width="80" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      destroy-on-close
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="图片URL" prop="image_url">
          <el-input v-model="form.image_url" placeholder="请输入图片URL" />
        </el-form-item>
        <el-form-item label="跳转链接" prop="link_url">
          <el-input v-model="form.link_url" placeholder="请输入跳转链接" />
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="form.sort" :min="0" />
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { bannerApi, type Banner, type BannerCreate, type BannerUpdate } from '@/api/marketing'

const loading = ref(false)
const tableData = ref<Banner[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref()
const isEdit = ref(false)
const currentId = ref<number | null>(null)

const form = reactive<Partial<BannerCreate & BannerUpdate>>({
  title: '',
  image_url: '',
  link_url: '',
  sort: 0,
  status: 1,
  platform: 1,
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  image_url: [{ required: true, message: '请输入图片URL', trigger: 'blur' }],
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await bannerApi.getBanners({ page: 1, page_size: 100 })
    tableData.value = res.data.items
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增轮播图'
  isEdit.value = false
  currentId.value = null
  Object.assign(form, {
    title: '',
    image_url: '',
    link_url: '',
    sort: 0,
    status: 1,
    platform: 1,
  })
  dialogVisible.value = true
}

const handleEdit = (row: Banner) => {
  dialogTitle.value = '编辑轮播图'
  isEdit.value = true
  currentId.value = row.id
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await bannerApi.deleteBanner(id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
    }
  }
}

const handleSubmit = async () => {
  await formRef.value.validate()
  try {
    if (isEdit.value && currentId.value) {
      await bannerApi.updateBanner(currentId.value, form as BannerUpdate)
      ElMessage.success('更新成功')
    } else {
      await bannerApi.createBanner(form as BannerCreate)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.banner-container {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
