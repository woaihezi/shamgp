<template>
  <div class="coupon-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>优惠券管理</span>
          <el-button type="primary" @click="handleAdd">新增优惠券</el-button>
        </div>
      </template>

      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="优惠券名称" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.type === 1" type="success">满减券</el-tag>
            <el-tag v-else-if="row.type === 2" type="warning">折扣券</el-tag>
            <el-tag v-else>无门槛券</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="discount_value" label="优惠值" width="100" />
        <el-table-column prop="min_amount" label="最低使用金额" width="120" />
        <el-table-column prop="total_count" label="发放总量" width="100" />
        <el-table-column prop="used_count" label="已使用" width="80" />
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

      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      destroy-on-close
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="优惠券名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入优惠券名称" />
        </el-form-item>
        <el-form-item label="优惠券类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择类型">
            <el-option label="满减券" :value="1" />
            <el-option label="折扣券" :value="2" />
            <el-option label="无门槛券" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="优惠值" prop="discount_value">
          <el-input-number v-model="form.discount_value" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="最低使用金额" prop="min_amount">
          <el-input-number v-model="form.min_amount" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="发放总量" prop="total_count">
          <el-input-number v-model="form.total_count" :min="0" />
        </el-form-item>
        <el-form-item label="每人限领" prop="per_limit">
          <el-input-number v-model="form.per_limit" :min="1" />
        </el-form-item>
        <el-form-item label="有效期开始" prop="valid_start_time">
          <el-date-picker
            v-model="form.valid_start_time"
            type="datetime"
            placeholder="选择日期时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="有效期结束" prop="valid_end_time">
          <el-date-picker
            v-model="form.valid_end_time"
            type="datetime"
            placeholder="选择日期时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio :value="1">启用</el-radio>
            <el-radio :value="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
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
import { couponApi, type Coupon, type CouponCreate, type CouponUpdate } from '@/api/marketing'

const loading = ref(false)
const tableData = ref<Coupon[]>([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref()
const isEdit = ref(false)
const currentId = ref<number | null>(null)

const form = reactive<Partial<CouponCreate & CouponUpdate>>({
  name: '',
  type: 1,
  discount_value: 0,
  min_amount: 0,
  total_count: 0,
  per_limit: 1,
  valid_start_time: '',
  valid_end_time: '',
  status: 1,
  description: '',
})

const rules = {
  name: [{ required: true, message: '请输入优惠券名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  discount_value: [{ required: true, message: '请输入优惠值', trigger: 'blur' }],
  total_count: [{ required: true, message: '请输入发放总量', trigger: 'blur' }],
  valid_start_time: [{ required: true, message: '请选择有效期开始', trigger: 'change' }],
  valid_end_time: [{ required: true, message: '请选择有效期结束', trigger: 'change' }],
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await couponApi.getCoupons({
      page: page.value,
      page_size: pageSize.value,
    })
    tableData.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增优惠券'
  isEdit.value = false
  currentId.value = null
  Object.assign(form, {
    name: '',
    type: 1,
    discount_value: 0,
    min_amount: 0,
    total_count: 0,
    per_limit: 1,
    valid_start_time: '',
    valid_end_time: '',
    status: 1,
    description: '',
  })
  dialogVisible.value = true
}

const handleEdit = (row: Coupon) => {
  dialogTitle.value = '编辑优惠券'
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
    await couponApi.deleteCoupon(id)
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
      await couponApi.updateCoupon(currentId.value, form as CouponUpdate)
      ElMessage.success('更新成功')
    } else {
      await couponApi.createCoupon(form as CouponCreate)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error(error)
  }
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchData()
}

const handleCurrentChange = (val: number) => {
  page.value = val
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.coupon-container {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
