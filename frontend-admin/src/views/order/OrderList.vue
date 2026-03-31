<template>
  <div class="order-list">
    <h2>订单管理</h2>
    
    <div class="filter-bar">
      <el-select v-model="currentStatus" placeholder="订单状态" clearable @change="loadOrders" style="width: 200px;">
        <el-option label="全部" value="" />
        <el-option label="待付款" value="pending_payment" />
        <el-option label="待发货" value="paid" />
        <el-option label="待收货" value="shipped" />
        <el-option label="已完成" value="completed" />
        <el-option label="已取消" value="canceled" />
        <el-option label="退款中" value="refunding" />
        <el-option label="已退款" value="refunded" />
      </el-select>
      <el-button type="primary" @click="loadOrders">刷新</el-button>
    </div>
    
    <div v-loading="loading" class="table-container">
      <el-table :data="orders" style="width: 100%">
        <el-table-column prop="order_no" label="订单号" width="200" />
        <el-table-column label="商品信息" min-width="200">
          <template #default="{ row }">
            <div v-for="item in row.items" :key="item.id" class="order-item-info">
              {{ item.product_name }} x {{ item.quantity }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="consignee_name" label="收货人" width="120" />
        <el-table-column prop="consignee_phone" label="电话" width="130" />
        <el-table-column label="金额" width="120">
          <template #default="{ row }">
            <span class="amount">¥{{ row.pay_amount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="下单时间" width="180">
          <template #default="{ row }">
            {{ new Date(row.created_at).toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewDetail(row)">
              详情
            </el-button>
            <template v-if="row.status === 'paid'">
              <el-button type="success" link size="small" @click="shipOrder(row)">
                发货
              </el-button>
            </template>
            <template v-else-if="row.status === 'shipped'">
              <el-button type="primary" link size="small" @click="completeOrder(row)">
                完成
              </el-button>
            </template>
          </template>
        </el-table-column>
      </el-table>
      
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadOrders"
        @current-change="loadOrders"
        style="margin-top: 20px; justify-content: flex-end;"
      />
    </div>
    
    <el-dialog v-model="showDetail" title="订单详情" width="800px">
      <div v-if="currentOrder" class="order-detail">
        <div class="detail-section">
          <h4>订单信息</h4>
          <div class="detail-row">
            <span class="label">订单号:</span>
            <span>{{ currentOrder.order_no }}</span>
          </div>
          <div class="detail-row">
            <span class="label">状态:</span>
            <el-tag :type="getStatusType(currentOrder.status)">
              {{ getStatusText(currentOrder.status) }}
            </el-tag>
          </div>
          <div class="detail-row">
            <span class="label">下单时间:</span>
            <span>{{ new Date(currentOrder.created_at).toLocaleString() }}</span>
          </div>
        </div>
        
        <div class="detail-section">
          <h4>收货信息</h4>
          <div class="detail-row">
            <span class="label">收货人:</span>
            <span>{{ currentOrder.consignee_name }} {{ currentOrder.consignee_phone }}</span>
          </div>
          <div class="detail-row">
            <span class="label">地址:</span>
            <span>{{ currentOrder.consignee_address }}</span>
          </div>
        </div>
        
        <div class="detail-section">
          <h4>商品清单</h4>
          <el-table :data="currentOrder.items" style="width: 100%">
            <el-table-column prop="product_name" label="商品名称" />
            <el-table-column prop="price" label="单价" width="100">
              <template #default="{ row }">¥{{ row.price.toFixed(2) }}</template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="80" />
            <el-table-column prop="total_amount" label="小计" width="100">
              <template #default="{ row }">¥{{ row.total_amount.toFixed(2) }}</template>
            </el-table-column>
          </el-table>
        </div>
        
        <div class="detail-section">
          <h4>金额明细</h4>
          <div class="detail-row">
            <span class="label">商品总额:</span>
            <span>¥{{ currentOrder.total_amount.toFixed(2) }}</span>
          </div>
          <div class="detail-row">
            <span class="label">运费:</span>
            <span>¥{{ currentOrder.freight_amount.toFixed(2) }}</span>
          </div>
          <div class="detail-row total">
            <span class="label">实付金额:</span>
            <span class="amount">¥{{ currentOrder.pay_amount.toFixed(2) }}</span>
          </div>
        </div>
        
        <div v-if="currentOrder.remark" class="detail-section">
          <h4>订单备注</h4>
          <p>{{ currentOrder.remark }}</p>
        </div>
      </div>
      
      <template #footer>
        <div v-if="currentOrder">
          <template v-if="currentOrder.status === 'paid'">
            <el-button type="primary" @click="shipOrder(currentOrder)">发货</el-button>
          </template>
          <template v-else-if="currentOrder.status === 'shipped'">
            <el-button type="primary" @click="completeOrder(currentOrder)">完成订单</el-button>
          </template>
          <el-button @click="showDetail = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { orderApi, type Order } from '@/api/order'

const loading = ref(false)
const orders = ref<Order[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const currentStatus = ref('')
const showDetail = ref(false)
const currentOrder = ref<Order | null>(null)

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'pending_payment': '待付款',
    'paid': '待发货',
    'shipped': '待收货',
    'completed': '已完成',
    'canceled': '已取消',
    'refunding': '退款中',
    'refunded': '已退款'
  }
  return statusMap[status] || status
}

const getStatusType = (status: string) => {
  const typeMap: Record<string, any> = {
    'pending_payment': 'warning',
    'paid': 'primary',
    'shipped': 'info',
    'completed': 'success',
    'canceled': 'info',
    'refunding': 'warning',
    'refunded': 'danger'
  }
  return typeMap[status] || ''
}

const loadOrders = async () => {
  try {
    loading.value = true
    const res = await orderApi.getOrders({
      status: currentStatus.value || undefined,
      page: page.value,
      page_size: pageSize.value
    })
    if (res.code === 200) {
      orders.value = res.data
      total.value = res.total
    }
  } catch (error) {
    ElMessage.error('加载订单列表失败')
  } finally {
    loading.value = false
  }
}

const viewDetail = (order: Order) => {
  currentOrder.value = order
  showDetail.value = true
}

const shipOrder = async (order: Order) => {
  try {
    await ElMessageBox.confirm('确认发货？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const res = await orderApi.updateOrderStatus(order.id, 'shipped')
    if (res.code === 200) {
      ElMessage.success('发货成功')
      if (currentOrder.value?.id === order.id) {
        currentOrder.value = res.data
      }
      await loadOrders()
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

const completeOrder = async (order: Order) => {
  try {
    await ElMessageBox.confirm('确认完成订单？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const res = await orderApi.updateOrderStatus(order.id, 'completed')
    if (res.code === 200) {
      ElMessage.success('订单已完成')
      if (currentOrder.value?.id === order.id) {
        currentOrder.value = res.data
      }
      await loadOrders()
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.order-list {
  padding: 20px;
}
h2 {
  margin-bottom: 20px;
}
.filter-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 12px;
  align-items: center;
}
.table-container {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}
.order-item-info {
  padding: 4px 0;
}
.amount {
  color: #f56c6c;
  font-weight: 600;
}
.order-detail {
  max-height: 600px;
  overflow-y: auto;
}
.detail-section {
  margin-bottom: 24px;
}
.detail-section h4 {
  margin-bottom: 16px;
  font-size: 16px;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}
.detail-row {
  display: flex;
  margin-bottom: 12px;
}
.detail-row .label {
  width: 100px;
  color: #666;
}
.detail-row.total {
  padding-top: 12px;
  border-top: 1px solid #eee;
  font-size: 16px;
  font-weight: 600;
}
.detail-row.total .amount {
  color: #f56c6c;
  font-size: 18px;
}
</style>
