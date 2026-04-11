<template>
  <div class="page-container">
    <h2>订单管理</h2>
    <el-card>
      <!-- 搜索栏 -->
      <el-form :inline="true" class="search-form">
        <el-form-item label="订单状态">
          <el-select v-model="queryParams.status" placeholder="全部" clearable @change="handleSearch">
            <el-option label="待付款" value="pending_payment" />
            <el-option label="已付款" value="paid" />
            <el-option label="已发货" value="shipped" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="canceled" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 订单表格 -->
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="order_no" label="订单号" width="200" />
        <el-table-column prop="user_id" label="用户ID" width="100" />
        <el-table-column label="金额" width="120">
          <template #default="{ row }">
            <span class="amount">¥{{ Number(row.pay_amount || row.total_amount || 0).toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="收货人" width="120">
          <template #default="{ row }">
            {{ row.consignee_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="下单时间" min-width="180">
          <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="handleView(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="queryParams.page"
        v-model:page-size="queryParams.pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        @size-change="loadData"
        @current-change="loadData"
        style="margin-top: 16px; justify-content: flex-end;"
      />
    </el-card>

    <!-- 订单详情弹窗 -->
    <el-dialog v-model="detailVisible" title="订单详情" width="700px">
      <div v-if="detail" class="order-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ detail.order_no }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(detail.status)" size="small">{{ getStatusText(detail.status) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="用户ID">{{ detail.user_id }}</el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ formatTime(detail.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="收货人">{{ detail.consignee_name }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ detail.consignee_phone }}</el-descriptions-item>
          <el-descriptions-item label="收货地址" :span="2">{{ detail.consignee_address }}</el-descriptions-item>
          <el-descriptions-item label="订单金额">¥{{ Number(detail.total_amount || 0).toFixed(2) }}</el-descriptions-item>
          <el-descriptions-item label="实付金额">¥{{ Number(detail.pay_amount || 0).toFixed(2) }}</el-descriptions-item>
        </el-descriptions>
        <el-divider content-position="left">商品明细</el-divider>
        <div v-if="detail.items?.length" class="order-items">
          <div v-for="item in detail.items" :key="item.id" class="order-item">
            <span>{{ item.product_name }} × {{ item.quantity }}</span>
            <span>¥{{ Number(item.price || 0).toFixed(2) }}</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const tableData = ref<any[]>([])
const loading = ref(false)
const total = ref(0)
const detail = ref<any>(null)
const detailVisible = ref(false)

const queryParams = reactive({
  page: 1,
  pageSize: 20,
  status: '' as string | undefined,
})

const statusMap: Record<string, string> = {
  pending_payment: '待付款',
  paid: '已付款',
  shipped: '已发货',
  completed: '已完成',
  canceled: '已取消',
}

const statusTypeMap: Record<string, string> = {
  pending_payment: 'warning',
  paid: 'success',
  shipped: 'info',
  completed: 'success',
  canceled: 'info',
}

const getStatusText = (status: string) => statusMap[status] || status
const getStatusType = (status: string) => statusTypeMap[status] || ''

const formatTime = (time: string) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

const loadData = async () => {
  loading.value = true
  try {
    const params: any = {
      page: queryParams.page,
      page_size: queryParams.pageSize,
    }
    if (queryParams.status) {
      params.status = queryParams.status
    }
    const res: any = await fetch('/api/v1/orders/admin/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token') || ''}`,
        'Content-Type': 'application/json',
      },
    })
    const json = await res.json()
    if (json.code === 200 && json.data) {
      tableData.value = json.data.items || json.data || []
      total.value = json.data.total || 0
    }
  } catch {
    ElMessage.error('加载订单列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  queryParams.page = 1
  loadData()
}

const handleReset = () => {
  queryParams.status = undefined
  queryParams.page = 1
  loadData()
}

const handleView = async (row: any) => {
  try {
    const res = await fetch(`/api/v1/orders/admin/${row.id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token') || ''}`,
        'Content-Type': 'application/json',
      },
    })
    const json = await res.json()
    if (json.code === 200) {
      detail.value = json.data
      detailVisible.value = true
    }
  } catch {
    ElMessage.error('加载订单详情失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.search-form { margin-bottom: 16px; }
.amount { color: #f56c6c; font-weight: 600; }
.order-detail { padding: 0 8px; }
.order-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}
.order-item:last-child { border-bottom: none; }
</style>
