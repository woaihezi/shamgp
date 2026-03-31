<template>
  <div class="checkout">
    <h2>确认订单</h2>
    
    <div v-if="loading" class="loading">加载中...</div>
    
    <div v-else>
      <div class="section">
        <h3>收货地址</h3>
        <div v-if="addresses.length > 0" class="address-list">
          <div 
            v-for="addr in addresses" 
            :key="addr.id"
            class="address-item"
            :class="{ selected: selectedAddressId === addr.id }"
            @click="selectedAddressId = addr.id"
          >
            <div class="address-info">
              <span class="name">{{ addr.consignee_name }}</span>
              <span class="phone">{{ addr.consignee_phone }}</span>
            </div>
            <div class="address-detail">
              {{ addr.province }}{{ addr.city }}{{ addr.district }}{{ addr.detail_address }}
            </div>
            <div v-if="addr.is_default" class="default-tag">默认</div>
          </div>
        </div>
        <div v-else class="empty">
          <p>暂无收货地址</p>
        </div>
      </div>
      
      <div class="section">
        <h3>商品清单</h3>
        <div v-if="cartSummary && cartSummary.selected_items.length > 0" class="order-items">
          <div v-for="item in cartSummary.selected_items" :key="item.id" class="order-item">
            <div class="item-name">{{ item.product_name || `商品 #${item.product_id}` }}</div>
            <div class="item-price">¥{{ (item.product_price || 0).toFixed(2) }}</div>
            <div class="item-quantity">x {{ item.quantity }}</div>
            <div class="item-total">¥{{ ((item.product_price || 0) * item.quantity).toFixed(2) }}</div>
          </div>
        </div>
      </div>
      
      <div class="section">
        <h3>订单备注</h3>
        <textarea
          v-model="remark"
          placeholder="选填，可以告诉卖家您的特殊需求"
          class="remark-input"
        ></textarea>
      </div>

      <!-- 优惠券选择 -->
      <div class="section coupon-section" v-if="myCoupons.length > 0">
        <h3>使用优惠券</h3>
        <div class="coupon-select">
          <el-select
            v-model="selectedCouponId"
            placeholder="选择优惠券（暂不选择）"
            clearable
            @change="calcDiscount"
            style="width: 100%"
          >
            <el-option
              v-for="c in myCoupons"
              :key="c.id"
              :label="`${c.name}（满${c.门槛金额}减${c.满减金额}）`"
              :value="c.id"
            />
          </el-select>
        </div>
        <div class="discount-info" v-if="discountAmount > 0">
          已享优惠：-¥{{ discountAmount.toFixed(2) }}
        </div>
      </div>
      
      <div class="summary">
        <div class="summary-row">
          <span>商品总额</span>
          <span>¥{{ (cartSummary?.total_amount || 0).toFixed(2) }}</span>
        </div>
        <div class="summary-row">
          <span>运费</span>
          <span class="freight-note">{{ freight === 0 ? '满99包邮' : `¥${freight.toFixed(2)}` }}</span>
        </div>
        <div class="summary-row total">
          <span>应付总额</span>
          <span class="total-amount">¥{{ totalAmount.toFixed(2) }}</span>
        </div>
      </div>
      
      <div class="actions">
        <router-link to="/cart" class="btn btn-outline">返回购物车</router-link>
        <button @click="submitOrder" class="btn btn-primary" :disabled="submitting || !selectedAddressId">
          {{ submitting ? '提交中...' : '提交订单' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { cartApi, type CartSummary } from '@/api/cart'
import { orderApi, type Address } from '@/api/order'
import { couponApi } from '@/api/coupon'

const router = useRouter()
const loading = ref(true)
const submitting = ref(false)
const cartSummary = ref<CartSummary | null>(null)
const addresses = ref<Address[]>([])
const selectedAddressId = ref<number | null>(null)
const remark = ref('')

// 优惠券相关
const myCoupons = ref<any[]>([])
const selectedCouponId = ref<number | null>(null)
const discountAmount = ref(0)

const loadMyCoupons = async () => {
  try {
    const res = await couponApi.getMyCoupons()
    myCoupons.value = (res.data || []).filter((c: any) => c.status === 0)
  } catch (e) {
    // 静默失败
  }
}

// 计算优惠金额
const calcDiscount = () => {
  if (!selectedCouponId.value) {
    discountAmount.value = 0
    return
  }
  const coupon = myCoupons.value.find((c: any) => c.id === selectedCouponId.value)
  if (!coupon) return

  const subtotal = cartSummary.value?.total_amount || 0

  if (coupon.type === 1) {
    // 满减
    if (subtotal >= coupon.门槛金额) {
      discountAmount.value = Math.min(Number(coupon.满减金额), subtotal)
    } else {
      discountAmount.value = 0
      ElMessage.warning(`订单金额需满${coupon.门槛金额}元才可使用此券`)
    }
  } else if (coupon.type === 2) {
    // 折扣
    discountAmount.value = subtotal * (1 - Number(coupon.折扣))
  } else if (coupon.type === 3) {
    // 无门槛
    discountAmount.value = Number(coupon.满减金额)
  }
}

watch(selectedCouponId, () => {
  calcDiscount()
})

// 运费计算（满99包邮，否则10元）
const freight = computed(() => {
  const subtotal = cartSummary.value?.total_amount || 0
  if (subtotal >= 99) return 0
  return 10
})

// 应付总额（纳入优惠+运费）
const totalAmount = computed(() => {
  const subtotal = cartSummary.value?.total_amount || 0
  return subtotal - discountAmount.value + freight.value
})

const loadData = async () => {
  try {
    loading.value = true
    const [cartRes, addrRes] = await Promise.all([
      cartApi.getSummary(),
      orderApi.getAddresses()
    ])
    
    if (cartRes.code === 200) {
      cartSummary.value = cartRes.data
    }
    if (addrRes.code === 200) {
      addresses.value = addrRes.data
      const defaultAddr = addrRes.data.find(a => a.is_default)
      selectedAddressId.value = defaultAddr?.id || addrRes.data[0]?.id || null
    }
  } catch (error) {
    console.error('Failed to load data:', error)
  } finally {
    loading.value = false
  }
}

const submitOrder = async () => {
  if (!selectedAddressId.value || !cartSummary.value) return

  try {
    submitting.value = true
    const res = await orderApi.createOrder({
      address_id: selectedAddressId.value,
      cart_item_ids: cartSummary.value.selected_items.map(i => i.id),
      remark: remark.value,
      coupon_id: selectedCouponId.value,
    })

    if (res.code === 200) {
      // 如果用了优惠券，标记已使用
      if (selectedCouponId.value && res.data?.id) {
        try {
          await couponApi.useCoupon(selectedCouponId.value, res.data.id)
        } catch {}
      }
      ElMessage.success('订单创建成功')
      router.push(`/order/detail/${res.data.id}`)
    }
  } catch (error: any) {
    ElMessage.error(error?.message || '提交订单失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadData()
  loadMyCoupons()
})
</script>

<style scoped>
.checkout {
  padding: 20px 0;
  max-width: 800px;
}
h2 {
  margin-bottom: 24px;
}
.loading {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}
.section {
  margin-bottom: 24px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #eee;
}
.section h3 {
  margin-bottom: 16px;
  font-size: 16px;
}
.address-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.address-item {
  padding: 16px;
  border: 2px solid #eee;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
}
.address-item:hover {
  border-color: #ddd;
}
.address-item.selected {
  border-color: #ff6600;
  background: #fff9f5;
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
.default-tag {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 2px 8px;
  background: #ff6600;
  color: #fff;
  font-size: 12px;
  border-radius: 4px;
}
.empty {
  text-align: center;
  color: #999;
  padding: 20px;
}
.order-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.order-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 4px;
}
.order-item .item-name {
  flex: 1;
}
.order-item .item-price {
  color: #666;
  min-width: 100px;
}
.order-item .item-quantity {
  color: #666;
  min-width: 60px;
  text-align: center;
}
.order-item .item-total {
  color: #ff6600;
  font-weight: 600;
  min-width: 100px;
  text-align: right;
}
.remark-input {
  width: 100%;
  min-height: 80px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  resize: vertical;
}
.summary {
  padding: 20px;
  background: #fff9f5;
  border-radius: 8px;
  margin-bottom: 24px;
}
.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  color: #666;
}
.summary-row.total {
  padding-top: 12px;
  border-top: 1px solid #ffddd2;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}
.total-amount {
  color: #ff6600;
  font-size: 24px;
}
.freight-note {
  color: #999;
  font-size: 13px;
}
.coupon-section {
  .coupon-select {
    margin-bottom: 8px;
  }
  .discount-info {
    color: #ff6600;
    font-size: 14px;
    font-weight: 500;
  }
}
.actions {
  display: flex;
  justify-content: space-between;
  gap: 16px;
}
.btn {
  padding: 12px 32px;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-size: 16px;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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
