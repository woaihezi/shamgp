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
          <span class="order-status" :class="order.status">{{ getStatusText(order.status) }}</span>
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

            <!-- 待付款：显示去支付按钮 -->
            <button
              v-if="order.status === 'pending_payment'"
              @click="openPayModal(order)"
              class="btn btn-primary btn-small"
            >
              去支付
            </button>

            <!-- 已付款：显示去发货按钮（用户视角） -->
            <span v-if="order.status === 'paid'" class="status-hint">等待商家发货</span>

            <!-- 已发货：显示确认收货 -->
            <button
              v-if="order.status === 'shipped'"
              @click="confirmReceive(order)"
              class="btn btn-primary btn-small"
            >
              确认收货
            </button>

            <!-- 已完成：显示再次购买 -->
            <button
              v-if="order.status === 'completed'"
              @click="reOrder(order)"
              class="btn btn-outline btn-small"
            >
              再次购买
            </button>

            <!-- 待付款：取消订单 -->
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

    <!-- 支付 Modal -->
    <div v-if="payModal.show" class="modal-overlay" @click.self="payModal.show = false">
      <div class="modal">
        <h3>订单支付</h3>
        <div class="pay-info">
          <div class="pay-row">
            <span>订单号</span>
            <span>{{ payModal.order?.order_no }}</span>
          </div>
          <div class="pay-row">
            <span>支付金额</span>
            <span class="pay-amount">¥{{ payModal.order?.pay_amount?.toFixed(2) }}</span>
          </div>
          <div class="pay-row">
            <span>支付方式</span>
            <div class="channel-options">
              <label :class="{ selected: payModal.channel === 'mock_wechat' }">
                <input type="radio" v-model="payModal.channel" value="mock_wechat">
                微信支付
              </label>
              <label :class="{ selected: payModal.channel === 'mock_alipay' }">
                <input type="radio" v-model="payModal.channel" value="mock_alipay">
                支付宝
              </label>
            </div>
          </div>
        </div>

        <!-- 二维码 -->
        <div class="qrcode-area">
          <img v-if="payModal.qrcode" :src="payModal.qrcode" alt="支付二维码" class="qrcode">
          <div v-if="payModal.loading" class="qrcode-loading">生成中...</div>
        </div>

        <div class="pay-tip">
          <p v-if="!payModal.paid">请使用{{ payModal.channel === 'mock_wechat' ? '微信' : '支付宝' }}扫码支付</p>
          <p v-else class="paid-text">✅ 支付成功！</p>
        </div>

        <div class="modal-actions">
          <button v-if="!payModal.paid" @click="confirmPay" class="btn btn-primary">
            模拟支付成功（测试用）
          </button>
          <button v-if="payModal.paid" @click="payModal.show = false; loadOrders()" class="btn btn-primary">
            完成
          </button>
          <button @click="payModal.show = false" class="btn btn-outline">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { orderApi, type Order } from '@/api/order'
import request from '@/api/request'

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

const payModal = reactive({
  show: false,
  order: null as Order | null,
  channel: 'mock_wechat',
  qrcode: '',
  loading: false,
  paid: false,
  tradeNo: ''
})

const getStatusText = (status: string) => {
  const m: Record<string, string> = {
    pending_payment: '待付款', paid: '待发货', shipped: '待收货',
    completed: '已完成', canceled: '已取消', refunding: '退款中', refunded: '已退款'
  }
  return m[status] || status
}

const loadOrders = async () => {
  try {
    loading.value = true
    const res = await orderApi.getOrders({ status: currentStatus.value || undefined })
    if (res.code === 200) {
      orders.value = res.data || []
    }
  } catch (e) {
    console.error('Failed to load orders:', e)
  } finally {
    loading.value = false
  }
}

const openPayModal = async (order: Order) => {
  payModal.order = order
  payModal.show = true
  payModal.loading = true
  payModal.paid = false
  payModal.qrcode = ''
  payModal.channel = 'mock_wechat'

  try {
    const res: any = await request.post(`/payments/pay?order_id=${order.id}&pay_channel=${payModal.channel}`)
    if (res.code === 200) {
      payModal.qrcode = res.data.qrcode_url
      payModal.tradeNo = res.data.trade_no
    }
  } catch (e: any) {
    alert('创建支付失败: ' + (e?.message || '未知错误'))
    payModal.show = false
  } finally {
    payModal.loading = false
  }
}

const confirmPay = async () => {
  if (!payModal.order) return
  try {
    // 调用 mock 网关确认支付
    const res: any = await request.get(
      `/payments/gateway?trade_no=${payModal.tradeNo}&order_no=${payModal.order.order_no}&amount=${payModal.order.pay_amount}&channel=${payModal.channel}&action=pay`
    )
    if (res.code === 200 && res.data.status === 'success') {
      payModal.paid = true
      await loadOrders()
    } else {
      alert('支付失败')
    }
  } catch (e: any) {
    alert('支付失败: ' + (e?.message || ''))
  }
}

const confirmReceive = async (order: Order) => {
  if (!confirm('确认已收到商品？')) return
  try {
    await orderApi.updateOrderStatus(order.id, 'completed')
    await loadOrders()
  } catch (e) {
    console.error(e)
  }
}

const cancelOrder = async (order: Order) => {
  if (!confirm('确定要取消订单吗？')) return
  try {
    await orderApi.cancelOrder(order.id, '用户取消')
    await loadOrders()
  } catch (e) {
    console.error(e)
  }
}

const reOrder = async (order: Order) => {
  // 把已完成订单的商品重新加入购物车
  try {
    for (const item of order.items) {
      await request.post('/carts/items', { product_id: item.product_id, quantity: item.quantity })
    }
    alert('商品已加入购物车')
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => { loadOrders() })
</script>

<style scoped>
.order-list { padding: 20px 0; }
h2 { margin-bottom: 24px; }
.filter-tabs {
  display: flex; gap: 8px; margin-bottom: 24px;
  border-bottom: 2px solid #f0f0f0; padding-bottom: 12px;
}
.tab {
  padding: 8px 20px; border: none; background: none;
  cursor: pointer; font-size: 14px; border-radius: 4px;
}
.tab:hover { background: #f5f5f5; }
.tab.active { background: #ff6600; color: #fff; }
.loading, .empty { text-align: center; padding: 60px 20px; color: #666; }
.orders { display: flex; flex-direction: column; gap: 16px; }
.order-card { background: #fff; border: 1px solid #eee; border-radius: 8px; overflow: hidden; }
.order-header {
  display: flex; justify-content: space-between; padding: 16px;
  background: #f9f9f9; border-bottom: 1px solid #eee;
}
.order-status { color: #ff6600; font-weight: 600; }
.order-status.completed { color: #52c41a; }
.order-status.canceled { color: #999; }
.order-items { padding: 16px; }
.order-item { display: flex; align-items: center; padding: 8px 0; }
.order-item .item-name { flex: 1; }
.order-item .item-price { color: #666; margin-right: 16px; }
.order-item .item-quantity { color: #666; }
.order-footer {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px; border-top: 1px solid #eee; flex-wrap: wrap; gap: 12px;
}
.order-time { color: #999; font-size: 13px; }
.order-amount { color: #666; }
.amount { color: #ff6600; font-size: 18px; font-weight: 600; }
.order-actions { display: flex; gap: 8px; align-items: center; }
.status-hint { color: #52c41a; font-size: 13px; }
.btn {
  padding: 8px 16px; border-radius: 4px; cursor: pointer;
  text-decoration: none; font-size: 14px;
}
.btn-small { padding: 6px 12px; font-size: 13px; }
.btn-outline { border: 1px solid #ddd; background: #fff; color: #333; }
.btn-primary { border: none; background: #ff6600; color: #fff; }

/* Modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.modal {
  background: #fff; border-radius: 16px; padding: 32px; width: 400px; max-width: 90vw;
}
.modal h3 { text-align: center; margin-bottom: 24px; }
.pay-info { margin-bottom: 20px; }
.pay-row {
  display: flex; justify-content: space-between; padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}
.pay-row:last-child { border-bottom: none; }
.pay-amount { color: #ff6600; font-size: 20px; font-weight: bold; }
.channel-options { display: flex; gap: 12px; }
.channel-options label {
  padding: 6px 16px; border: 2px solid #eee; border-radius: 8px;
  cursor: pointer; font-size: 13px; display: flex; align-items: center; gap: 6px;
}
.channel-options label.selected { border-color: #52c41a; color: #52c41a; }
.qrcode-area {
  text-align: center; padding: 20px; background: #fafafa;
  border-radius: 8px; margin-bottom: 16px;
}
.qrcode { width: 200px; height: 200px; }
.qrcode-loading { padding: 80px; color: #999; }
.pay-tip { text-align: center; color: #666; font-size: 14px; margin-bottom: 24px; }
.paid-text { color: #52c41a; font-size: 16px; font-weight: bold; }
.modal-actions { display: flex; gap: 12px; justify-content: center; }
</style>
