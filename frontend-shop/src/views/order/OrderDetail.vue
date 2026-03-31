<template>
  <div class="order-detail" v-if="order">
    <div class="header">
      <router-link to="/order/list" class="back-btn"
        >← 返回订单列表</router-link
      >
      <h2>订单详情</h2>
    </div>

    <div class="section">
      <h3>订单信息</h3>
      <div class="info-row">
        <span class="label">订单号:</span>
        <span class="value">{{ order.order_no }}</span>
      </div>
      <div class="info-row">
        <span class="label">订单状态:</span>
        <span class="value status">{{ getStatusText(order.status) }}</span>
      </div>
      <div class="info-row">
        <span class="label">下单时间:</span>
        <span class="value">{{
          new Date(order.created_at).toLocaleString()
        }}</span>
      </div>
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
          <div class="item-spec" v-if="item.sku_specs">
            {{ item.sku_specs }}
          </div>
          <div class="item-price">¥{{ item.price.toFixed(2) }}</div>
          <div class="item-quantity">x {{ item.quantity }}</div>
          <div class="item-total">¥{{ item.total_amount.toFixed(2) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>
    </div>
    
    <div class="section">
      <h3>金额明细</h3>
      <div class="amount-row">
        <span>商品总额</span>
        <span>¥{{ order.total_amount.toFixed(2) }}</span>
      </div>
      <div class="amount-row" v-if="order.discount_amount > 0">
        <span>优惠金额</span>
        <span class="discount">-¥{{ order.discount_amount.toFixed(2) }}</span>
      </div>
      <div class="amount-row">
        <span>运费</span>
        <span>¥{{ order.freight_amount.toFixed(2) }}</span>
      </div>
      <div class="amount-row total">
        <span>实付金额</span>
        <span class="total-amount">¥{{ order.pay_amount.toFixed(2) }}</span>
      </div>
    </div>
    
    <div class="section" v-if="order.remark">
      <h3>订单备注</h3>
      <p class="remark">{{ order.remark }}</p>
    </div>
    
    <div class="actions">
      <button 
        v-if="order.status === 'pending_payment'" 
        @click="simulatePay"
        class="btn btn-primary"
      >
        模拟支付
      </button>
      <button 
        v-if="order.status === 'pending_payment'" 
        @click="cancelOrder"
        class="btn btn-outline"
      >
        取消订单
      </button>
      <button 
        v-if="order.status === 'shipped'" 
        @click="confirmReceive"
        class="btn btn-primary"
      >
        确认收货
      </button>
      <button 
        v-if="['paid', 'shipped', 'completed'].includes(order.status)" 
        @click="showRefund = true"
        class="btn btn-outline"
      >
        申请退款
      </button>
    </div>
    
    <div v-if="showRefund" class="modal-overlay" @click="showRefund = false">
      <div class="modal" @click.stop>
        <h3>申请退款</h3>
        <select v-model="refundType" class="select">
          <option value="refund">仅退款</option>
          <option value="return">退货退款</option>
        </select>
        <textarea 
          v-model="refundReason" 
          placeholder="请填写退款原因"
          class="textarea"
        ></textarea>
        <div class="modal-actions">
          <button @click="showRefund = false" class="btn btn-outline">取消</button>
          <button @click="submitRefund" class="btn btn-primary" :disabled="!refundReason">提交</button>
        </div>
      </div>
    </div>
  </div>
  
  <div v-else-if="loading" class="loading">加载中...</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { orderApi, type Order } from '@/api/order'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const order = ref<Order | null>(null)
const showRefund = ref(false)
const refundType = ref('refund')
const refundReason = ref('')

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

const loadOrder = async () => {
  const id = Number(route.params.id)
  if (!id) return
  
  try {
    loading.value = true
    const res = await orderApi.getOrder(id)
    if (res.code === 200) {
      order.value = res.data
    }
  } catch (error) {
    console.error('Failed to load order:', error)
  } finally {
    loading.value = false
  }
}

const simulatePay = async () => {
  if (!order.value) return
  
  try {
    const res = await orderApi.updateOrderStatus(order.value.id, 'paid')
    if (res.code === 200) {
      order.value = res.data
    }
  } catch (error) {
    console.error('Failed to pay:', error)
  }
}

const cancelOrder = async () => {
  if (!order.value || !confirm('确定要取消订单吗？')) return
  
  try {
    const res = await orderApi.cancelOrder(order.value.id, '用户取消')
    if (res.code === 200) {
      order.value = res.data
    }
  } catch (error) {
    console.error('Failed to cancel order:', error)
  }
}

const confirmReceive = async () => {
  if (!order.value || !confirm('确认已收到商品？')) return
  
  try {
    const res = await orderApi.updateOrderStatus(order.value.id, 'completed')
    if (res.code === 200) {
      order.value = res.data
    }
  } catch (error) {
    console.error('Failed to confirm receive:', error)
  }
}

const submitRefund = async () => {
  if (!order.value || !refundReason.value) return
  
  try {
    await orderApi.createRefund({
      order_id: order.value.id,
      refund_reason: refundReason.value,
      refund_type: refundType.value
    })
    showRefund.value = false
    refundReason.value = ''
    await loadOrder()
  } catch (error) {
    console.error('Failed to submit refund:', error)
  }
}

onMounted(() => {
  loadOrder()
})
</script>

<style scoped>
.order-detail {
  padding: 20px 0;
  max-width: 800px;
}
.header {
  margin-bottom: 24px;
}
.back-btn {
  display: inline-block;
  margin-bottom: 12px;
  color: #666;
  text-decoration: none;
}
.back-btn:hover {
  color: #ff6600;
}
h2 {
  margin: 0;
}
.loading {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}
.section {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 16px;
}
.section h3 {
  margin-bottom: 16px;
  font-size: 16px;
  color: #333;
}
.info-row {
  display: flex;
  margin-bottom: 12px;
}
.label {
  color: #666;
  min-width: 100px;
}
.value {
  color: #333;
}
.value.status {
  color: #ff6600;
  font-weight: 600;
}
.address {
  line-height: 1.8;
}
.address-info {
  margin-bottom: 8px;
}
.name {
  font-weight: 600;
  margin-right: 16px;
}
.phone {
  color: #666;
}
.address-detail {
  color: #666;
}
.items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 4px;
}
.item-name {
  flex: 1;
}
.item-spec {
  color: #999;
  font-size: 13px;
  margin-right: 16px;
}
.item-price {
  color: #666;
  min-width: 100px;
}
.item-quantity {
  color: #666;
  min-width: 60px;
  text-align: center;
}
.item-total {
  color: #ff6600;
  font-weight: 600;
  min-width: 100px;
  text-align: right;
}
.amount-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  color: #666;
}
.amount-row.total {
  padding-top: 12px;
  border-top: 1px solid #eee;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}
.discount {
  color: #52c41a;
}
.total-amount {
  color: #ff6600;
  font-size: 24px;
}
.remark {
  color: #666;
  margin: 0;
}
.actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}
.btn {
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
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
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  width: 400px;
  max-width: 90%;
}
.modal h3 {
  margin-top: 0;
  margin-bottom: 16px;
}
.select, .textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 12px;
  font-size: 14px;
}
.textarea {
  min-height: 100px;
  resize: vertical;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}
</style>
