<template>
  <div class="orders-page">
    <Header />
    <main class="main-content">
      <div class="container">
        <h1 class="page-title">我的订单</h1>
        
        <div class="order-tabs">
          <button 
            v-for="tab in orderTabs" 
            :key="tab.value"
            :class="['tab-btn', { active: activeTab === tab.value }]"
            @click="activeTab = tab.value; loadOrders()"
          >
            {{ tab.label }}
          </button>
        </div>

        <div v-if="loading" class="loading-state">
          <p>加载中...</p>
        </div>
        
        <div v-else-if="orders.length > 0" class="orders-list">
          <div v-for="order in orders" :key="order.id" class="order-card card">
            <div class="order-header">
              <div class="order-info">
                <span class="order-no">订单号: {{ order.order_no }}</span>
                <span class="order-time">{{ formatDate(order.created_at) }}</span>
              </div>
              <span class="order-status" :class="getStatusClass(order.status)">
                {{ getStatusText(order.status) }}
              </span>
            </div>
            <div class="order-items">
              <div v-for="item in order.items" :key="item.id" class="order-item">
                <div class="item-info">
                  <h4 class="item-name">{{ item.product_name }}</h4>
                  <span class="item-price">¥{{ item.price.toFixed(2) }} x {{ item.quantity }}</span>
                </div>
              </div>
            </div>
            <div class="order-footer">
              <span class="order-total">
                共 {{ order.items?.length || 0 }} 件商品，合计: 
                <span class="price">¥{{ order.total_amount.toFixed(2) }}</span>
              </span>
              <div class="order-actions">
                <button v-if="order.status === 'pending'" class="btn btn-default" @click="cancelOrder(order.id)">
                  取消订单
                </button>
                <button v-if="order.status === 'paid'" class="btn btn-primary">
                  查看物流
                </button>
                <button v-if="order.status === 'shipped'" class="btn btn-primary">
                  确认收货
                </button>
              </div>
            </div>
          </div>

          <div class="pagination" v-if="total > pageSize">
            <button class="btn" @click="changePage(page - 1)" :disabled="page === 1">上一页</button>
            <span>{{ page }} / {{ Math.ceil(total / pageSize) }}</span>
            <button class="btn" @click="changePage(page + 1)" :disabled="page >= Math.ceil(total / pageSize)">下一页</button>
          </div>
        </div>
        
        <div v-else class="empty-orders">
          <div class="empty-icon">📦</div>
          <p>暂无订单</p>
          <router-link to="/products" class="btn btn-primary">去购物</router-link>
        </div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { orderApi } from '@/api/order'
import type { Order } from '@/api/order'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const orders = ref<Order[]>([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const activeTab = ref('all')

const orderTabs = [
  { label: '全部', value: 'all' },
  { label: '待支付', value: 'pending' },
  { label: '已支付', value: 'paid' },
  { label: '已发货', value: 'shipped' },
  { label: '已完成', value: 'completed' }
]

onMounted(() => {
  if (userStore.isLoggedIn) {
    loadOrders()
  }
})

async function loadOrders() {
  loading.value = true
  try {
    const status = activeTab.value === 'all' ? undefined : activeTab.value
    const res: any = await orderApi.getOrders({
      status,
      page: page.value,
      page_size: pageSize.value
    })
    if (res.code === 200) {
      orders.value = res.data || []
      total.value = res.total || 0
    }
  } catch (e) {
    console.error('加载订单失败', e)
  } finally {
    loading.value = false
  }
}

function formatDate(dateString: string) {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

function getStatusText(status: string) {
  const statusMap: Record<string, string> = {
    'pending': '待支付',
    'paid': '已支付',
    'shipped': '已发货',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return statusMap[status] || '未知'
}

function getStatusClass(status: string) {
  const classMap: Record<string, string> = {
    'pending': 'pending',
    'paid': 'paid',
    'shipped': 'shipped',
    'completed': 'completed',
    'cancelled': 'cancelled'
  }
  return classMap[status] || ''
}

async function cancelOrder(orderId: number) {
  if (confirm('确定要取消该订单吗？')) {
    try {
      await orderApi.cancelOrder(orderId, '用户主动取消')
      loadOrders()
    } catch (e) {
      console.error('取消订单失败', e)
    }
  }
}

function changePage(newPage: number) {
  if (newPage < 1 || newPage > Math.ceil(total.value / pageSize.value)) {
    return
  }
  page.value = newPage
  loadOrders()
}
</script>

<style scoped>
.orders-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 40px 0;
}

.page-title {
  font-size: 28px;
  color: #333;
  margin-bottom: 30px;
}

.order-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  border-bottom: 1px solid #eee;
}

.tab-btn {
  padding: 12px 24px;
  border: none;
  background: none;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.tab-btn:hover {
  color: #ff6b6b;
}

.tab-btn.active {
  color: #ff6b6b;
  border-bottom-color: #ff6b6b;
}

.loading-state {
  text-align: center;
  padding: 80px 0;
  color: #666;
  font-size: 16px;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-card {
  padding: 24px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
  margin-bottom: 16px;
}

.order-info {
  display: flex;
  gap: 20px;
}

.order-no {
  font-size: 14px;
  color: #666;
}

.order-time {
  font-size: 14px;
  color: #999;
}

.order-status {
  font-size: 14px;
  font-weight: 500;
  padding: 4px 12px;
  border-radius: 4px;
}

.order-status.pending {
  background: #fff3cd;
  color: #856404;
}

.order-status.paid {
  background: #d1ecf1;
  color: #0c5460;
}

.order-status.shipped {
  background: #cce5ff;
  color: #004085;
}

.order-status.completed {
  background: #d4edda;
  color: #155724;
}

.order-status.cancelled {
  background: #f8d7da;
  color: #721c24;
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.order-item {
  padding: 12px;
  background: #f9f9f9;
  border-radius: 4px;
}

.item-name {
  font-size: 14px;
  color: #333;
  margin-bottom: 4px;
}

.item-price {
  font-size: 13px;
  color: #666;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid #eee;
}

.order-total {
  font-size: 14px;
  color: #666;
}

.order-total .price {
  font-size: 18px;
  font-weight: bold;
}

.order-actions {
  display: flex;
  gap: 12px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 40px;
  gap: 16px;
}

.pagination .btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination .btn:hover:not(:disabled) {
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.pagination .btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination span {
  font-size: 14px;
  color: #666;
}

.empty-orders {
  text-align: center;
  padding: 80px 0;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.empty-orders p {
  color: #999;
  font-size: 16px;
  margin-bottom: 24px;
}
</style>
