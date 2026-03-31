<template>
  <div class="home-container">
    <div class="banner-section">
      <el-carousel height="400px" :interval="5000" arrow="always">
        <el-carousel-item v-for="banner in banners" :key="banner.id">
          <a v-if="banner.link_url" :href="banner.link_url" target="_blank">
            <img :src="banner.image_url" :alt="banner.title" class="banner-image" />
          </a>
          <img v-else :src="banner.image_url" :alt="banner.title" class="banner-image" />
        </el-carousel-item>
      </el-carousel>
    </div>

    <div class="coupon-section" v-if="coupons.length > 0">
      <h2 class="section-title">限时优惠券</h2>
      <div class="coupon-list">
        <div v-for="coupon in coupons" :key="coupon.id" class="coupon-item">
          <div class="coupon-left">
            <div class="coupon-value">
              <span class="symbol">¥</span>
              <span class="amount">{{ coupon.discount_value }}</span>
            </div>
            <div class="coupon-condition" v-if="coupon.min_amount > 0">
              满{{ coupon.min_amount }}元可用
            </div>
          </div>
          <div class="coupon-right">
            <div class="coupon-name">{{ coupon.name }}</div>
            <div class="coupon-time">
              {{ coupon.valid_start_time }} ~ {{ coupon.valid_end_time }}
            </div>
            <el-button type="primary" size="small" @click="handleReceiveCoupon(coupon.id)">
              立即领取
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <div class="floor-section" v-for="floor in floors" :key="floor.id">
      <h2 class="section-title">{{ floor.title || floor.name }}</h2>
      <p v-if="floor.subtitle" class="section-subtitle">{{ floor.subtitle }}</p>
      <div class="product-list">
        <div class="product-item" v-for="i in 4" :key="i">
          <div class="product-image">
            <img :src="`https://picsum.photos/200/200?random=${floor.id}${i}`" alt="商品图片" />
          </div>
          <div class="product-name">示例商品 {{ floor.id }}-{{ i }}</div>
          <div class="product-price">¥{{ (Math.random() * 100 + 10).toFixed(2) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { homeApi, couponApi, type Banner, type Coupon, type Floor } from '@/api/home'

const banners = ref<Banner[]>([])
const coupons = ref<Coupon[]>([])
const floors = ref<Floor[]>([])

const fetchHomeData = async () => {
  try {
    const [bannerRes, couponRes, floorRes] = await Promise.all([
      homeApi.getBanners(1),
      homeApi.getAvailableCoupons(),
      homeApi.getFloors(),
    ])
    banners.value = bannerRes.data
    coupons.value = couponRes.data
    floors.value = floorRes.data
  } catch (error) {
    console.error(error)
  }
}

const handleReceiveCoupon = async (couponId: number) => {
  try {
    await couponApi.receiveCoupon(couponId, 1)
    ElMessage.success('领取成功')
    fetchHomeData()
  } catch (error) {
    ElMessage.error('领取失败')
  }
}

onMounted(() => {
  fetchHomeData()
})
</script>

<style scoped lang="scss">
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.banner-section {
  margin-bottom: 40px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.section-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.section-subtitle {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
}

.coupon-section {
  margin-bottom: 40px;
}

.coupon-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.coupon-item {
  display: flex;
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.coupon-left {
  width: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  padding: 20px;
}

.coupon-value {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 8px;
}

.symbol {
  font-size: 18px;
}

.amount {
  font-size: 36px;
}

.coupon-condition {
  font-size: 12px;
  opacity: 0.9;
}

.coupon-right {
  flex: 1;
  padding: 20px;
  background: white;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.coupon-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.coupon-time {
  font-size: 12px;
  color: #999;
  margin-bottom: 12px;
}

.floor-section {
  margin-bottom: 40px;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.product-item {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  }
}

.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.product-name {
  padding: 12px 16px 8px;
  font-size: 14px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  padding: 0 16px 16px;
  font-size: 18px;
  font-weight: bold;
  color: #ff4d4f;
}
</style>
