<template>
  <div class="dashboard-container">
    <!-- 统计卡片 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon orders-icon">
            <el-icon :size="28"><ShoppingCart /></el-icon>
          </div>
          <el-statistic title="今日订单数" :value="stats.today_orders" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon sales-icon">
            <el-icon :size="28"><Money /></el-icon>
          </div>
          <el-statistic title="今日销售额" prefix="¥" :value="stats.today_sales" :precision="2" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon users-icon">
            <el-icon :size="28"><User /></el-icon>
          </div>
          <el-statistic title="用户总数" :value="stats.total_users" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon pending-icon">
            <el-icon :size="28"><Clock /></el-icon>
          </div>
          <el-statistic title="在售商品" :value="stats.on_sale_products" />
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
            <el-table-column prop="id" label="用户" width="120">
              <template #default="{ row }">用户 #{{ row.id }}</template>
            </el-table-column>
            <el-table-column label="金额" width="120">
              <template #default="{ row }">
                <span class="amount">¥{{ row.total_amount?.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="时间" min-width="180">
              <template #default="{ row }">
                {{ formatTime(row.created_at || new Date().toISOString()) }}
              </template>
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
  total_users: 0,
  today_users: 0,
  total_orders: 0,
  today_orders: 0,
  total_products: 0,
  on_sale_products: 0,
  total_sales: 0,
  today_sales: 0
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
    cancelled: '已取消'
  }
  return map[status] || status
}

const getStatusType = (status: string) => {
  const map: Record<string, any> = {
    pending_payment: 'warning',
    paid: 'success',
    shipped: 'info',
    completed: 'success',
    cancelled: 'info'
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
    const res: any = await request.get('/dashboard/stats')

    if (res.code === 200 && res.data) {
      stats.value = res.data
    }
  } catch (err) {
    console.error('Failed to load stats:', err)
    loadFailed.value = true
  }
}

// 获取最近订单
const loadRecentOrders = async () => {
  try {
    tableLoading.value = true
    const res: any = await request.get('/dashboard/order-stats')

    if (res.code === 200 && res.data && res.data.recent_orders) {
      recentOrders.value = res.data.recent_orders
    }
  } catch (err) {
    console.error('Failed to load recent orders:', err)
    loadFailed.value = true
  } finally {
    tableLoading.value = false
  }
}

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
