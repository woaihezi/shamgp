<template>
  <div class="order-list">
    <h2>我的订单</h2>
    
    <div class="filter-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.value"
        class="tab"
        :class="{ active: currentStatus === tab.value }"
        @click="currentStatus = tab.value; loadOrders()"
      >
        {{ tab.label }}
      </button>
    </div>
    
    <div v-if="loading" class="loading">加载中...</div>
    
    <div v-else-if="orders.length === 0" class="empty">
      <p>暂无订单</p>
    </div>
    
    <div v-else class="orders">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-header">
          <span class="order-no">订单号: {{ order.order_no }}</span>
          <span class="order-status">{{ getStatusText(order.status) }}</span>
        </div>
        
        <div class="order-items">
          <div v-for="item in order.items" :key="item.id" class="order-item">
            <div class="item-name">{{ item.product_name }}</div>
            <div class="item-price">¥{{ item.price.toFixed(2) }}</div>
            <div class="item-quantity">x {{ item.quantity }}</div>
          </div>
        </div>
        
        <div class="order-footer">
          <div class="order-time">{{ new Date(order.created_at).toLocaleString() }}</div>
          <div class="order-amount">
            共 {{ order.items.reduce((sum, item) => sum + item.quantity, 0) }} 件商品，
            合计: <span class="amount">¥{{ order.pay_amount.toFixed(2) }}</span>
          </div>
          <div class="order-actions">
            <router-link :to="`/order/detail/${order.id}`" class="btn btn-small">查看详情</router-link>
            <button 
              v-if="order.status === 'pending_payment'" 
              @click="simulatePay(order)"
              class="btn btn-primary btn-small"
            >
              模拟支付
            </button>
            <button 
              v-if="order.status === 'pending_payment'" 
              @click="cancelOrder(order)"
              class="btn btn-outline btn-small"
            >
              取消订单
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { orderApi, type Order } from '@/api/order'

const tabs = [
  { label: '全部', value: '' },
  { label: '待付款', value: 'pending_payment' },
  { label: '待发货', value: 'paid' },
  { label: '待收货', value: 'shipped' },
  { label: '已完成', value: 'completed' },
  { label: '已取消', value: 'canceled' }
]

const loading = ref(true)
const currentStatus = ref('')
const orders = ref<Order[]>([])

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

const loadOrders = async () => {
  try {
    loading.value = true
    const res = await orderApi.getOrders({ status: currentStatus.value || undefined })
    if (res.code === 200) {
      orders.value = res.data
    }
  } catch (error) {
    console.error('Failed to load orders:', error)
  } finally {
    loading.value = false
  }
}

const simulatePay = async (order: Order) => {
  try {
    await orderApi.updateOrderStatus(order.id, 'paid')
    await loadOrders()
  } catch (error) {
    console.error('Failed to pay:', error)
  }
}

const cancelOrder = async (order: Order) => {
  if (!confirm('确定要取消订单吗？')) return
  
  try {
    await orderApi.cancelOrder(order.id, '用户取消')
    await loadOrders()
  } catch (error) {
    console.error('Failed to cancel order:', error)
  }
}

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.order-list {
  padding: 20px 0;
}
h2 {
  margin-bottom: 24px;
}
.filter-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 12px;
}
.tab {
  padding: 8px 20px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 14px;
  border-radius: 4px;
}
.tab:hover {
  background: #f5f5f5;
}
.tab.active {
  background: #ff6600;
  color: #fff;
}
.loading, .empty {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}
.orders {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.order-card {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}
.order-header {
  display: flex;
  justify-content: space-between;
  padding: 16px;
  background: #f9f9f9;
  border-bottom: 1px solid #eee;
}
.order-no {
  color: #666;
}
.order-status {
  color: #ff6600;
  font-weight: 600;
}
.order-items {
  padding: 16px;
}
.order-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
}
.order-item .item-name {
  flex: 1;
}
.order-item .item-price {
  color: #666;
  margin-right: 16px;
}
.order-item .item-quantity {
  color: #666;
}
.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-top: 1px solid #eee;
  flex-wrap: wrap;
  gap: 12px;
}
.order-time {
  color: #999;
  font-size: 13px;
}
.order-amount {
  color: #666;
}
.amount {
  color: #ff6600;
  font-size: 18px;
  font-weight: 600;
}
.order-actions {
  display: flex;
  gap: 8px;
}
.btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-size: 14px;
}
.btn-small {
  padding: 6px 12px;
  font-size: 13px;
}
.btn-outline {
  border: 1px solid #ddd;
  background: #fff;
  color: #333;
}
.btn-primary {
  border: none;
  background: #ff6600;
  color: #fff;
}
</style>
