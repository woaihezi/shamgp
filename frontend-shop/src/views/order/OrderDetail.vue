<template>
  <div class="order-detail" v-if="order">
    <div class="header">
      <router-link to="/order/list" class="back-btn">← 返回订单列表</router-link>
      <h2>订单详情</h2>
    </div>

    <div class="order-status-bar" :class="order.status">
      <span class="status-text">{{ getStatusText(order.status) }}</span>
      <span class="status-tip">{{ getStatusTip(order.status) }}</span>
    </div>

    <div class="section">
      <h3>订单信息</h3>
      <div class="info-row"><span class="label">订单号</span><span class="value">{{ order.order_no }}</span></div>
      <div class="info-row"><span class="label">下单时间</span><span class="value">{{ new Date(order.created_at).toLocaleString() }}</span></div>
      <div v-if="order.pay_time" class="info-row"><span class="label">支付时间</span><span class="value">{{ new Date(order.pay_time).toLocaleString() }}</span></div>
      <div v-if="order.delivery_time" class="info-row"><span class="label">发货时间</span><span class="value">{{ new Date(order.delivery_time).toLocaleString() }}</span></div>
      <div v-if="order.receive_time" class="info-row"><span class="label">收货时间</span><span class="value">{{ new Date(order.receive_time).toLocaleString() }}</span></div>
    </div>

    <div class="section">
      <h3>收货信息</h3>
      <div class="address">
        <div class="address-info">
          <span class="name">{{ order.consignee_name }}</span>
          <span class="phone">{{ order.consignee_phone }}</span>
        </div>
        <div class="address-detail">{{ order.consignee_address }}</div>
      </div>
    </div>

    <div class="section">
      <h3>商品清单</h3>
      <div class="items">
        <div v-for="item in order.items" :key="item.id" class="item">
          <div class="item-name">{{ item.product_name }}</div>
          <div class="item-spec" v-if="item.sku_specs">{{ item.sku_specs }}</div>
          <div class="item-price">¥{{ item.price.toFixed(2) }}</div>
          <div class="item-quantity">x {{ item.quantity }}</div>
          <div class="item-total">¥{{ item.total_amount.toFixed(2) }}</div>
        </div>
      </div>
    </div>

    <div class="section">
      <h3>金额明细</h3>
      <div class="amount-row"><span>商品总额</span><span>¥{{ order.total_amount.toFixed(2) }}</span></div>
      <div class="amount-row" v-if="order.discount_amount > 0"><span>优惠金额</span><span class="discount">-¥{{ order.discount_amount.toFixed(2) }}</span></div>
      <div class="amount-row"><span>运费</span><span>¥{{ order.freight_amount.toFixed(2) }}</span></div>
      <div class="amount-row total"><span>实付金额</span><span class="total-amount">¥{{ order.pay_amount.toFixed(2) }}</span></div>
    </div>

    <div class="section" v-if="order.remark">
      <h3>订单备注</h3>
      <p class="remark">{{ order.remark }}</p>
    </div>

    <div class="actions">
      <!-- 待付款 -->
      <button v-if="order.status === 'pending_payment'" @click="openPay" class="btn btn-primary">
        去支付
      </button>
      <button v-if="order.status === 'pending_payment'" @click="cancelOrder" class="btn btn-outline">
        取消订单
      </button>

      <!-- 已付款 -->
      <span v-if="order.status === 'paid'" class="status-hint">等待商家发货</span>

      <!-- 已发货 -->
      <button v-if="order.status === 'shipped'" @click="confirmReceive" class="btn btn-primary">
        确认收货
      </button>

      <!-- 已完成 -->
      <button v-if="order.status === 'completed'" @click="reOrder" class="btn btn-outline">
        再次购买
      </button>

      <!-- 已完成/已发货 -->
      <button v-if="['paid','shipped','completed'].includes(order.status)" @click="showRefund = true" class="btn btn-outline">
        申请退款
      </button>
    </div>

    <!-- 退款 Modal -->
    <div v-if="showRefund" class="modal-overlay" @click="showRefund = false">
      <div class="modal" @click.stop>
        <h3>申请退款</h3>
        <p class="refund-tip">退款将原路返回，预计1-3个工作日到账</p>
        <select v-model="refundType" class="select">
          <option value="refund">仅退款（未收到货）</option>
          <option value="return">退货退款（已收到货）</option>
        </select>
        <textarea v-model="refundReason" placeholder="请填写退款原因" class="textarea"></textarea>
        <div class="modal-actions">
          <button @click="showRefund = false" class="btn btn-outline">取消</button>
          <button @click="submitRefund" class="btn btn-primary" :disabled="!refundReason">提交退款</button>
        </div>
      </div>
    </div>

    <!-- 支付 Modal -->
    <div v-if="pay.show" class="modal-overlay" @click.self="pay.show = false">
      <div class="modal">
        <h3>订单支付</h3>
        <div class="pay-info">
          <div class="pay-row"><span>订单号</span><span>{{ pay.order_no }}</span></div>
          <div class="pay-row"><span>支付金额</span><span class="pay-amount">¥{{ pay.pay_amount?.toFixed(2) }}</span></div>
          <div class="pay-row">
            <span>支付方式</span>
            <div class="channels">
              <label :class="{ selected: pay.channel === 'mock_wechat' }">
                <input type="radio" v-model="pay.channel" value="mock_wechat"> 微信支付
              </label>
              <label :class="{ selected: pay.channel === 'mock_alipay' }">
                <input type="radio" v-model="pay.channel" value="mock_alipay"> 支付宝
              </label>
            </div>
          </div>
        </div>
        <div class="qrcode-area">
          <img v-if="pay.qrcode" :src="pay.qrcode" alt="支付二维码" class="qrcode">
          <div v-if="pay.loading" class="loading-text">二维码生成中...</div>
          <div v-if="pay.paid" class="paid-text">✅ 支付成功！</div>
        </div>
        <div class="pay-tip">
          <span v-if="!pay.paid">请使用 {{ pay.channel === 'mock_wechat' ? '微信' : '支付宝' }} 扫码支付</span>
        </div>
        <div class="modal-actions">
          <button v-if="!pay.paid" @click="doPay" class="btn btn-primary">✅ 模拟支付成功</button>
          <button v-if="pay.paid" @click="pay.show = false; loadOrder()" class="btn btn-primary">完成</button>
          <button @click="pay.show = false" class="btn btn-outline">取消</button>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="loading" class="loading">加载中...</div>
  <div v-else class="loading">订单不存在</div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { orderApi, type Order } from '@/api/order'
import request from '@/api/request'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const order = ref<Order | null>(null)
const showRefund = ref(false)
const refundType = ref('refund')
const refundReason = ref('')

const pay = reactive({
  show: false, order_no: '', pay_amount: 0, channel: 'mock_wechat',
  qrcode: '', loading: false, paid: false, tradeNo: ''
})

const getStatusText = (s: string) => {
  const m: Record<string, string> = {
    pending_payment: '待付款', paid: '待发货', shipped: '待收货',
    completed: '已完成', canceled: '已取消', refunding: '退款中', refunded: '已退款'
  }
  return m[s] || s
}

const getStatusTip = (s: string) => {
  const m: Record<string, string> = {
    pending_payment: '请尽快完成支付，订单30分钟后自动取消',
    paid: '商家正在准备商品，请耐心等待',
    shipped: '商品已发货，请注意查收',
    completed: '交易已完成，感谢您的购买',
    canceled: '订单已取消',
    refunding: '退款申请已提交，等待审核',
    refunded: '退款已原路返回'
  }
  return m[s] || ''
}

const loadOrder = async () => {
  const id = Number(route.params.id)
  if (!id) return
  try {
    loading.value = true
    const res = await orderApi.getOrder(id)
    if (res.code === 200) order.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openPay = async () => {
  if (!order.value) return
  pay.order_no = order.value.order_no
  pay.pay_amount = order.value.pay_amount
  pay.show = true
  pay.loading = true
  pay.paid = false
  pay.qrcode = ''
  try {
    const res: any = await request.post(
      `/payments/pay?order_id=${order.value.id}&pay_channel=${pay.channel}`
    )
    if (res.code === 200) {
      pay.qrcode = res.data.qrcode_url
      pay.tradeNo = res.data.trade_no
    }
  } catch (e: any) {
    alert('创建支付失败: ' + (e?.message || ''))
    pay.show = false
  } finally {
    pay.loading = false
  }
}

const doPay = async () => {
  try {
    const res: any = await request.get(
      `/payments/gateway?trade_no=${pay.tradeNo}&order_no=${pay.order_no}&amount=${pay.pay_amount}&channel=${pay.channel}&action=pay`
    )
    if (res.code === 200 && res.data.status === 'success') {
      pay.paid = true
      await loadOrder()
    } else {
      alert('支付失败')
    }
  } catch (e: any) {
    alert('支付失败: ' + (e?.message || ''))
  }
}

const cancelOrder = async () => {
  if (!order.value || !confirm('确定要取消订单吗？')) return
  try {
    const res = await orderApi.cancelOrder(order.value.id, '用户取消')
    if (res.code === 200) order.value = res.data
  } catch (e) { console.error(e) }
}

const confirmReceive = async () => {
  if (!order.value || !confirm('确认已收到商品？')) return
  try {
    const res = await orderApi.updateOrderStatus(order.value.id, 'completed')
    if (res.code === 200) order.value = res.data
  } catch (e) { console.error(e) }
}

const submitRefund = async () => {
  if (!order.value || !refundReason.value) return
  try {
    await orderApi.createRefund({ order_id: order.value.id, refund_reason: refundReason.value, refund_type: refundType.value })
    showRefund.value = false
    refundReason.value = ''
    await loadOrder()
  } catch (e) { console.error(e) }
}

const reOrder = async () => {
  if (!order.value) return
  try {
    for (const item of order.value.items) {
      await request.post('/carts/items', { product_id: item.product_id, quantity: item.quantity })
    }
    alert('商品已加入购物车')
    router.push('/cart')
  } catch (e) { console.error(e) }
}

onMounted(() => { loadOrder() })
</script>

<style scoped>
.order-detail { padding: 20px 0; max-width: 800px; }
.header { margin-bottom: 16px; }
.back-btn { display: inline-block; margin-bottom: 12px; color: #666; text-decoration: none; font-size: 14px; }
.back-btn:hover { color: #ff6600; }
h2 { margin: 0; }
.loading { text-align: center; padding: 60px 20px; color: #666; }

.order-status-bar {
  padding: 16px 20px; border-radius: 8px; margin-bottom: 16px;
  background: linear-gradient(135deg, #ff6600, #ff8533); color: white;
}
.order-status-bar.paid { background: linear-gradient(135deg, #1890ff, #69c0ff); }
.order-status-bar.shipped { background: linear-gradient(135deg, #52c41a, #95de64); }
.order-status-bar.completed { background: linear-gradient(135deg, #52c41a, #b7eb8f); }
.order-status-bar.canceled { background: #999; }
.order-status-bar.refunding { background: linear-gradient(135deg, #faad14, #ffe58f); color: #333; }
.status-text { font-size: 18px; font-weight: bold; display: block; margin-bottom: 4px; }
.status-tip { font-size: 13px; opacity: 0.85; }

.section { background: #fff; border: 1px solid #eee; border-radius: 8px; padding: 20px; margin-bottom: 16px; }
.section h3 { margin: 0 0 16px; font-size: 16px; }
.info-row { display: flex; margin-bottom: 10px; }
.label { color: #999; min-width: 90px; }
.value { color: #333; }

.address { line-height: 1.8; }
.address-info { margin-bottom: 8px; }
.name { font-weight: 600; margin-right: 16px; }
.phone { color: #666; }
.address-detail { color: #666; }

.items { display: flex; flex-direction: column; gap: 10px; }
.item { display: flex; align-items: center; padding: 12px; background: #fafafa; border-radius: 4px; }
.item-name { flex: 1; }
.item-spec { color: #999; font-size: 13px; margin-right: 16px; }
.item-price { color: #666; min-width: 90px; }
.item-quantity { color: #666; min-width: 60px; text-align: center; }
.item-total { color: #ff6600; font-weight: 600; min-width: 90px; text-align: right; }

.amount-row { display: flex; justify-content: space-between; margin-bottom: 10px; color: #666; }
.amount-row.total { margin-top: 12px; padding-top: 12px; border-top: 1px solid #eee; color: #333; font-size: 16px; font-weight: 600; }
.discount { color: #52c41a; }
.total-amount { color: #ff6600; font-size: 22px; }

.remark { color: #666; margin: 0; }

.actions { display: flex; gap: 12px; margin-top: 24px; flex-wrap: wrap; }
.status-hint { color: #52c41a; font-size: 14px; align-self: center; }
.btn { padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 14px; }
.btn-outline { border: 1px solid #ddd; background: #fff; color: #333; }
.btn-primary { border: none; background: #ff6600; color: #fff; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: #fff; border-radius: 12px; padding: 28px; width: 400px; max-width: 90vw; }
.modal h3 { text-align: center; margin: 0 0 20px; }
.refund-tip { color: #999; font-size: 13px; margin-bottom: 16px; }
.select, .textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; margin-bottom: 12px; font-size: 14px; }
.textarea { min-height: 90px; resize: vertical; }
.modal-actions { display: flex; gap: 10px; justify-content: center; margin-top: 16px; }

.pay-info { margin-bottom: 20px; }
.pay-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f0f0f0; align-items: center; }
.pay-row:last-child { border-bottom: none; }
.pay-amount { color: #ff6600; font-size: 20px; font-weight: bold; }
.channels { display: flex; gap: 10px; }
.channels label { padding: 6px 14px; border: 2px solid #eee; border-radius: 6px; cursor: pointer; font-size: 13px; display: flex; align-items: center; gap: 4px; }
.channels label.selected { border-color: #52c41a; color: #52c41a; }
.qrcode-area { text-align: center; padding: 20px; background: #fafafa; border-radius: 8px; margin-bottom: 16px; min-height: 220px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.qrcode { width: 200px; height: 200px; }
.loading-text { color: #999; padding: 80px 0; }
.paid-text { color: #52c41a; font-size: 18px; font-weight: bold; padding: 60px 0; }
.pay-tip { text-align: center; color: #666; font-size: 14px; margin-bottom: 8px; }
</style>
