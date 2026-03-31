<template>
  <div class="dashboard-container">
    <!-- 统计卡片 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon orders-icon">
            <el-icon :size="28"><ShoppingCart /></el-icon>
          </div>
          <el-statistic title="今日订单数" :value="stats.todayOrders" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon sales-icon">
            <el-icon :size="28"><Money /></el-icon>
          </div>
          <el-statistic title="本月销售额" prefix="¥" :value="stats.monthSales" :precision="2" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon users-icon">
            <el-icon :size="28"><User /></el-icon>
          </div>
          <el-statistic title="用户总数" :value="stats.totalUsers" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon pending-icon">
            <el-icon :size="28"><Clock /></el-icon>
          </div>
          <el-statistic title="待处理订单" :value="stats.pendingOrders" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 加载失败提示 -->
    <el-alert v-if="loadFailed" title="加载失败，请刷新重试" type="error" show-icon style="margin: 20px 0;" />

    <!-- 最近订单 -->
    <el-row :gutter="20" style="margin-top: 24px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近订单</span>
              <el-button type="primary" link @click="$router.push('/orders')">查看全部</el-button>
            </div>
          </template>
          <el-table :data="recentOrders" v-loading="tableLoading" style="width: 100%">
            <el-table-column prop="order_no" label="订单号" width="200" />
            <el-table-column prop="user_id" label="用户" width="120">
              <template #default="{ row }">用户 #{{ row.user_id }}</template>
            </el-table-column>
            <el-table-column label="金额" width="120">
              <template #default="{ row }">
                <span class="amount">¥{{ row.pay_amount?.toFixed(2) || row.total_amount?.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="时间" min-width="180">
              <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ShoppingCart, Money, User, Clock } from '@element-plus/icons-vue'
import request from '@/api/request'

// 统计数据
const stats = ref({
  todayOrders: 128,
  monthSales: 45230,
  totalUsers: 1203,
  pendingOrders: 23
})

// 最近订单
const recentOrders = ref<any[]>([])
const tableLoading = ref(false)
const loadFailed = ref(false)

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending_payment: '待付款',
    paid: '已付款',
    shipped: '已发货',
    completed: '已完成',
    canceled: '已取消'
  }
  return map[status] || status
}

const getStatusType = (status: string) => {
  const map: Record<string, any> = {
    pending_payment: 'warning',
    paid: 'success',
    shipped: 'info',
    completed: 'success',
    canceled: 'info'
  }
  return map[status] || ''
}

const formatTime = (time: string) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

// 获取统计数据
const loadStats = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return

    const res: any = await request.get('/admin/stats', {
      headers: { Authorization: `Bearer ${token}` }
    })

    if (res.code === 200 && res.data) {
      stats.value = res.data
    }
  } catch {
    // API 不可用时使用 mock 数据（已设置默认值）
    loadFailed.value = true
  }
}

// 获取最近订单
const loadRecentOrders = async () => {
  try {
    tableLoading.value = true
    const token = localStorage.getItem('token')
    if (!token) return

    const res: any = await request.get('/orders/admin/', {
      headers: { Authorization: `Bearer ${token}` },
      params: { page: 1, page_size: 5 }
    })

    if (res.code === 200) {
      recentOrders.value = Array.isArray(res.data) ? res.data : (res.data?.list || [])
    }
  } catch {
    // API 不可用时使用 mock 数据
    recentOrders.value = getMockRecentOrders()
  } finally {
    tableLoading.value = false
  }
}

const getMockRecentOrders = () => [
  { order_no: 'ORD20260331001', user_id: 1001, pay_amount: 299.00, status: 'paid', created_at: new Date(Date.now() - 1000 * 60 * 5).toISOString() },
  { order_no: 'ORD20260331002', user_id: 1002, pay_amount: 1280.50, status: 'shipped', created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString() },
  { order_no: 'ORD20260331003', user_id: 1003, pay_amount: 59.00, status: 'pending_payment', created_at: new Date(Date.now() - 1000 * 60 * 60).toISOString() },
  { order_no: 'ORD20260331004', user_id: 1004, pay_amount: 899.00, status: 'completed', created_at: new Date(Date.now() - 1000 * 60 * 90).toISOString() },
  { order_no: 'ORD20260331005', user_id: 1005, pay_amount: 450.00, status: 'paid', created_at: new Date(Date.now() - 1000 * 60 * 120).toISOString() }
]

onMounted(() => {
  loadStats()
  loadRecentOrders()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.stat-card {
  text-align: center;
  position: relative;
}

.stat-icon {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.orders-icon { background: #409eff; }
.sales-icon { background: #67c23a; }
.users-icon { background: #e6a23c; }
.pending-icon { background: #f56c6c; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.amount {
  color: #f56c6c;
  font-weight: 600;
}
</style>
