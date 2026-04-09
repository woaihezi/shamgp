<template>
  <div class="page-container">
    <h2>订单管理</h2>
    
    <!-- 搜索和筛选 -->
    <el-card class="mb-4">
      <el-form :inline="true" :model="searchForm" class="mb-4">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.order_no" placeholder="请输入订单号" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="选择状态">
            <el-option label="全部" value="" />
            <el-option label="待付款" value="pending_payment" />
            <el-option label="已付款" value="paid" />
            <el-option label="已发货" value="shipped" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadOrders">查询</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 订单列表 -->
    <el-card>
      <template #header>
        <div class="card-header">
          <span>订单列表</span>
          <span class="text-gray">共 {{ total }} 条记录</span>
        </div>
      </template>
      
      <el-table :data="orders" v-loading="loading" style="width: 100%">
        <el-table-column prop="order_no" label="订单号" width="200" />
        <el-table-column prop="user_id" label="用户" width="120">
          <template #default="{ row }">用户 #{{ row.user_id }}</template>
        </el-table-column>
        <el-table-column label="金额" width="120">
          <template #default="{ row }">¥{{ row.pay_amount?.toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewOrder(row.id)">查看详情</el-button>
            <el-button type="success" size="small" @click="updateStatus(row)" v-if="canUpdateStatus(row.status)">更新状态</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 订单详情弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      title="订单详情"
      width="800px"
      destroy-on-close
    >
      <div v-if="orderDetail" class="order-detail">
        <!-- 基本信息 -->
        <el-card class="mb-4">
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
              <el-tag :type="getStatusType(orderDetail.status)">{{ getStatusText(orderDetail.status) }}</el-tag>
            </div>
          </template>
          <el-descriptions :column="2">
            <el-descriptions-item label="订单号">{{ orderDetail.order_no }}</el-descriptions-item>
            <el-descriptions-item label="下单时间">{{ formatTime(orderDetail.created_at) }}</el-descriptions-item>
            <el-descriptions-item label="用户ID">{{ orderDetail.user_id }}</el-descriptions-item>
            <el-descriptions-item label="支付状态">{{ getPayStatusText(orderDetail.pay_status) }}</el-descriptions-item>
            <el-descriptions-item label="总金额" colspan="2">¥{{ orderDetail.total_amount?.toFixed(2) }}</el-descriptions-item>
            <el-descriptions-item label="实付金额" colspan="2">¥{{ orderDetail.pay_amount?.toFixed(2) }}</el-descriptions-item>
            <el-descriptions-item label="优惠金额" colspan="2">¥{{ orderDetail.discount_amount?.toFixed(2) }}</el-descriptions-item>
            <el-descriptions-item label="运费" colspan="2">¥{{ orderDetail.freight_amount?.toFixed(2) }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 收货信息 -->
        <el-card class="mb-4">
          <template #header>
            <span>收货信息</span>
          </template>
          <el-descriptions :column="1">
            <el-descriptions-item label="收货人">{{ orderDetail.consignee_name }}</el-descriptions-item>
            <el-descriptions-item label="联系电话">{{ orderDetail.consignee_phone }}</el-descriptions-item>
            <el-descriptions-item label="收货地址">{{ orderDetail.consignee_address }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 商品信息 -->
        <el-card class="mb-4">
          <template #header>
            <span>商品信息</span>
          </template>
          <el-table :data="orderDetail.items" style="width: 100%">
            <el-table-column prop="product_name" label="商品名称" min-width="200" />
            <el-table-column prop="price" label="单价" width="100">
              <template #default="{ row }">¥{{ row.price?.toFixed(2) }}</template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="80" />
            <el-table-column label="小计" width="120">
              <template #default="{ row }">¥{{ row.total_amount?.toFixed(2) }}</template>
            </el-table-column>
          </el-table>
        </el-card>

        <!-- 状态变更日志 -->
        <el-card>
          <template #header>
            <span>状态变更日志</span>
          </template>
          <el-table :data="orderDetail.status_logs" style="width: 100%">
            <el-table-column label="时间" width="180">
              <template #default="{ row }">
                {{ formatTime(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getOperatorType(row.operator_type)">{{ getOperatorTypeText(row.operator_type) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="状态变更" min-width="200">
              <template #default="{ row }">
                <span v-if="row.old_status">{{ getStatusText(row.old_status) }}</span>
                <span v-else>无</span>
                <span class="text-gray mx-2">→</span>
                <span class="text-primary">{{ getStatusText(row.new_status) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作人" width="120">
              <template #default="{ row }">
                {{ row.operator_id ? `用户 #${row.operator_id}` : '系统' }}
              </template>
            </el-table-column>
            <el-table-column label="备注" min-width="200">
              <template #default="{ row }">
                {{ row.remark || '-' }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
      <div v-else class="text-center py-8">
        <el-icon class="text-gray-400" :size="48"><Loading /></el-icon>
        <p class="text-gray-400 mt-2">加载中...</p>
      </div>
    </el-dialog>

    <!-- 状态更新弹窗 -->
    <el-dialog
      v-model="statusDialogVisible"
      title="更新订单状态"
      width="400px"
    >
      <el-form :model="statusForm" label-width="80px">
        <el-form-item label="当前状态">
          <el-tag :type="getStatusType(currentOrder?.status)">{{ getStatusText(currentOrder?.status) }}</el-tag>
        </el-form-item>
        <el-form-item label="新状态" required>
          <el-select v-model="statusForm.status" placeholder="选择新状态">
            <el-option
              v-for="option in statusOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="statusForm.remark" type="textarea" rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="statusDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmStatusUpdate">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import request from '@/api/request'

// 搜索表单
const searchForm = ref({
  order_no: '',
  status: ''
})

// 分页
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 订单数据
const orders = ref<any[]>([])
const loading = ref(false)

// 订单详情
const dialogVisible = ref(false)
const orderDetail = ref<any>(null)

// 状态更新
const statusDialogVisible = ref(false)
const currentOrder = ref<any>(null)
const statusForm = ref({
  status: '',
  remark: ''
})

// 状态选项
const statusOptions = ref([
  { label: '待付款', value: 'pending_payment' },
  { label: '已付款', value: 'paid' },
  { label: '已发货', value: 'shipped' },
  { label: '已完成', value: 'completed' },
  { label: '已取消', value: 'cancelled' }
])

// 格式化时间
const formatTime = (time: string) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

// 获取状态文本
const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending_payment: '待付款',
    paid: '已付款',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消',
    refunding: '退款中',
    refunded: '已退款'
  }
  return map[status] || status
}

// 获取状态类型
const getStatusType = (status: string) => {
  const map: Record<string, any> = {
    pending_payment: 'warning',
    paid: 'success',
    shipped: 'info',
    completed: 'success',
    cancelled: 'info',
    refunding: 'warning',
    refunded: 'info'
  }
  return map[status] || ''
}

// 获取支付状态文本
const getPayStatusText = (status: number) => {
  const map: Record<number, string> = {
    0: '未支付',
    1: '已支付',
    2: '已退款'
  }
  return map[status] || '未知'
}

// 获取操作类型文本
const getOperatorTypeText = (type: string) => {
  const map: Record<string, string> = {
    system: '系统',
    user: '用户',
    admin: '管理员'
  }
  return map[type] || type
}

// 获取操作类型标签
const getOperatorType = (type: string) => {
  const map: Record<string, string> = {
    system: 'info',
    user: 'warning',
    admin: 'success'
  }
  return map[type] || ''
}

// 判断是否可以更新状态
const canUpdateStatus = (status: string) => {
  const updatableStatuses = ['pending_payment', 'paid', 'shipped']
  return updatableStatuses.includes(status)
}

// 加载订单列表
const loadOrders = async () => {
  try {
    loading.value = true
    const res: any = await request.get('/orders/admin/', {
      params: {
        page: page.value,
        page_size: pageSize.value,
        status: searchForm.value.status,
        order_no: searchForm.value.order_no
      }
    })
    
    if (res.code === 200) {
      orders.value = res.data?.list || []
      total.value = res.data?.total || 0
    }
  } catch (err) {
    console.error('Failed to load orders:', err)
    ElMessage.error('加载订单失败')
  } finally {
    loading.value = false
  }
}

// 重置表单
const resetForm = () => {
  searchForm.value = {
    order_no: '',
    status: ''
  }
  loadOrders()
}

// 查看订单详情
const viewOrder = async (orderId: number) => {
  try {
    const res: any = await request.get(`/orders/admin/${orderId}`)
    if (res.code === 200) {
      orderDetail.value = res.data
      dialogVisible.value = true
    }
  } catch (err) {
    console.error('Failed to load order detail:', err)
    ElMessage.error('加载订单详情失败')
  }
}

// 打开状态更新弹窗
const updateStatus = (order: any) => {
  currentOrder.value = order
  statusForm.value = {
    status: '',
    remark: ''
  }
  statusDialogVisible.value = true
}

// 确认状态更新
const confirmStatusUpdate = async () => {
  if (!currentOrder.value || !statusForm.value.status) {
    ElMessage.warning('请选择新状态')
    return
  }
  
  try {
    const res: any = await request.put(`/orders/admin/${currentOrder.value.id}/status`, {
      status: statusForm.value.status
    })
    
    if (res.code === 200) {
      ElMessage.success('状态更新成功')
      statusDialogVisible.value = false
      loadOrders()
      // 如果当前打开了详情弹窗，刷新详情
      if (dialogVisible.value && orderDetail.value && orderDetail.value.id === currentOrder.value.id) {
        viewOrder(currentOrder.value.id)
      }
    }
  } catch (err) {
    console.error('Failed to update status:', err)
    ElMessage.error('状态更新失败')
  }
}

// 分页处理
const handleSizeChange = (size: number) => {
  pageSize.value = size
  loadOrders()
}

const handleCurrentChange = (current: number) => {
  page.value = current
  loadOrders()
}

// 初始加载
onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.page-container {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.order-detail {
  max-height: 70vh;
  overflow-y: auto;
}

.text-gray {
  color: #909399;
}

.text-primary {
  color: #409eff;
}

.text-gray-400 {
  color: #c0c4cc;
}

.mx-2 {
  margin: 0 8px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
