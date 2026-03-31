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
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="code" label="券码" width="140" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.type === 'fixed'" type="success">满减</el-tag>
            <el-tag v-else-if="row.type === 'discount'" type="warning">折扣</el-tag>
            <el-tag v-else>{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="优惠值" width="100">
          <template #default="{ row }">
            {{ row.type === 'discount' ? (row.discount_value * 100).toFixed(0) + '%' : '¥' + row.discount_value }}
          </template>
        </el-table-column>
        <el-table-column label="最低消费" width="100">
          <template #default="{ row }">¥{{ row.min_order_amount }}</template>
        </el-table-column>
        <el-table-column prop="total_count" label="总量" width="80" />
        <el-table-column prop="used_count" label="已用" width="80" />
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="截止日期" width="160">
          <template #default="{ row }">{{ row.end_date?.substring(0, 16) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
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
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        @size-change="loadCoupons"
        @current-change="loadCoupons"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>

    <!-- 新增/编辑 Dialog -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" destroy-on-close>
      <el-form :model="form" :rules="rules" label-width="120px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="例如：新人满减券" />
        </el-form-item>
        <el-form-item label="券码" prop="code">
          <el-input v-model="form.code" placeholder="例如：NEWUSER2026" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择类型">
            <el-option label="满减（固定金额）" value="fixed" />
            <el-option label="折扣（比例）" value="discount" />
          </el-select>
        </el-form-item>
        <el-form-item label="优惠值" prop="discount_value">
          <el-input-number v-model="form.discount_value" :min="0" :precision="2" />
          <span style="margin-left: 8px; color: #999; font-size: 12px">
            {{ form.type === 'discount' ? '填写 0.1 表示 9折' : '填写优惠金额，如 20' }}
          </span>
        </el-form-item>
        <el-form-item label="最低消费" prop="min_order_amount">
          <el-input-number v-model="form.min_order_amount" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="最高优惠" prop="max_discount_amount">
          <el-input-number v-model="form.max_discount_amount" :min="0" :precision="2" placeholder="不填则无上限" />
        </el-form-item>
        <el-form-item label="发放总量" prop="total_count">
          <el-input-number v-model="form.total_count" :min="0" />
        </el-form-item>
        <el-form-item label="每人限领" prop="per_user_limit">
          <el-input-number v-model="form.per_user_limit" :min="1" />
        </el-form-item>
        <el-form-item label="开始时间" prop="start_date">
          <el-date-picker
            v-model="form.start_date"
            type="datetime"
            placeholder="选择开始时间"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_date">
          <el-date-picker
            v-model="form.end_date"
            type="datetime"
            placeholder="选择结束时间"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio value="active">启用</el-radio>
            <el-radio value="inactive">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { couponApi, type Coupon } from '@/api/marketing'

const loading = ref(false)
const tableData = ref<Coupon[]>([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const currentId = ref<number | null>(null)
const submitting = ref(false)

const defaultForm = () => ({
  name: '',
  code: '',
  type: 'fixed',
  discount_value: 0,
  min_order_amount: 0,
  max_discount_amount: null as number | null,
  total_count: 0,
  per_user_limit: 1,
  start_date: '',
  end_date: '',
  status: 'active',
  is_public: true,
})

const form = reactive(defaultForm())

const rules = {
  name: [{ required: true, message: '请输入优惠券名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入券码', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  discount_value: [{ required: true, message: '请输入优惠值', trigger: 'blur' }],
  total_count: [{ required: true, message: '请输入发放总量', trigger: 'blur' }],
  start_date: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
  end_date: [{ required: true, message: '请选择结束时间', trigger: 'change' }],
}

const loadCoupons = async () => {
  loading.value = true
  try {
    const res: any = await couponApi.getCoupons({ page: page.value, page_size: pageSize.value })
    if (res.code === 200) {
      tableData.value = res.data.items || []
      total.value = res.data.total || 0
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增优惠券'
  isEdit.value = false
  currentId.value = null
  const d = defaultForm()
  d.code = 'CP' + Date.now().toString(36).toUpperCase() + Math.random().toString(36).substring(2, 6).toUpperCase()
  Object.assign(form, d)
  dialogVisible.value = true
}

const handleEdit = (row: Coupon) => {
  dialogTitle.value = '编辑优惠券'
  isEdit.value = true
  currentId.value = row.id
  Object.assign(form, {
    name: row.name,
    code: row.code,
    type: row.type,
    discount_value: row.discount_value,
    min_order_amount: row.min_order_amount,
    max_discount_amount: row.max_discount_amount || null,
    total_count: row.total_count,
    per_user_limit: row.per_user_limit,
    start_date: row.start_date?.substring(0, 19) || '',
    end_date: row.end_date?.substring(0, 19) || '',
    status: row.status,
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    const data: any = { ...form }
    if (isEdit.value && currentId.value) {
      delete data.code  // 编辑时不改券码
      await couponApi.updateCoupon(currentId.value, data)
    } else {
      await couponApi.createCoupon(data)
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
    await loadCoupons()
  } catch (e: any) {
    ElMessage.error('保存失败: ' + (e?.message || '未知错误'))
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (id: number) => {
  try {
    await couponApi.deleteCoupon(id)
    ElMessage.success('删除成功')
    await loadCoupons()
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => { loadCoupons() })
</script>

<style scoped>
.coupon-container { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
