<template>
  <div class="orders-page">
    <Header />
    <main class="main-content">
      <div class="container">
        <h1 class="page-title">我的订单</h1>
        
        <div v-if="orders.length > 0" class="orders-list">
          <div v-for="order in orders" :key="order.id" class="order-card card">
            <div class="order-header">
              <div class="order-info">
                <span class="order-no">订单号: {{ order.orderNo }}</span>
                <span class="order-time">{{ formatDate(order.createdAt) }}</span>
              </div>
              <span class="order-status" :class="getStatusClass(order.status)">
                {{ getStatusText(order.status) }}
              </span>
            </div>
            <div class="order-items">
              <div v-for="item in order.items" :key="item.id" class="order-item">
                <div class="item-info">
                  <h4 class="item-name">{{ item.productName }}</h4>
                  <span class="item-price">¥{{ item.price.toFixed(2) }} x {{ item.quantity }}</span>
                </div>
              </div>
            </div>
            <div class="order-footer">
              <span class="order-total">
                共 {{ order.items?.length || 0 }} 件商品，合计: 
                <span class="price">¥{{ order.totalAmount.toFixed(2) }}</span>
              </span>
              <div class="order-actions">
                <button v-if="order.status === 0" class="btn btn-default" @click="cancelOrder(order.id)">
                  取消订单
                </button>
                <button v-if="order.status === 1" class="btn btn-primary">
                  查看物流
                </button>
              </div>
            </div>
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
import type { Order, OrderItem } from '@/api/order'

const orders = ref<Order[]>([])

onMounted(() => {
  loadMockOrders()
})

function loadMockOrders() {
  const mockOrderItems: OrderItem[] = [
    {
      id: 1,
      orderId: 1,
      productId: 1,
      productName: 'iPhone 15 Pro Max',
      price: 9999,
      quantity: 1,
      createdAt: new Date().toISOString()
    },
    {
      id: 2,
      orderId: 1,
      productId: 3,
      productName: 'AirPods Pro 2',
      price: 1899,
      quantity: 2,
      createdAt: new Date().toISOString()
    }
  ]

  orders.value = [
    {
      id: 1,
      orderNo: 'SH202401010001',
      userId: 1,
      totalAmount: 13797,
      status: 1,
      createdAt: new Date(Date.now() - 86400000).toISOString(),
      updatedAt: new Date(Date.now() - 86400000).toISOString(),
      items: mockOrderItems
    },
    {
      id: 2,
      orderNo: 'SH202401020002',
      userId: 1,
      totalAmount: 14999,
      status: 0,
      createdAt: new Date(Date.now() - 172800000).toISOString(),
      updatedAt: new Date(Date.now() - 172800000).toISOString(),
      items: [
        {
          id: 3,
          orderId: 2,
          productId: 2,
          productName: 'MacBook Pro 14英寸',
          price: 14999,
          quantity: 1,
          createdAt: new Date(Date.now() - 172800000).toISOString()
        }
      ]
    }
  ]
}

function formatDate(dateString: string) {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

function getStatusText(status: number) {
  const statusMap: Record<number, string> = {
    0: '待支付',
    1: '已支付',
    2: '已发货',
    3: '已完成',
    4: '已取消'
  }
  return statusMap[status] || '未知'
}

function getStatusClass(status: number) {
  const classMap: Record<number, string> = {
    0: 'pending',
    1: 'paid',
    2: 'shipped',
    3: 'completed',
    4: 'cancelled'
  }
  return classMap[status] || ''
}

function cancelOrder(orderId: number) {
  if (confirm('确定要取消该订单吗？')) {
    const order = orders.value.find(o => o.id === orderId)
    if (order) {
      order.status = 4
    }
  }
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
