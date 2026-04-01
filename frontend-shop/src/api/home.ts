import request from './request'

export interface Banner {
  id: number
  title: string
  image_url: string
  link_url?: string
  sort: number
  status: number
  platform: number
  description?: string
  created_at: string
  updated_at: string
}

export interface Coupon {
  id: number
  name: string
  type: number
  discount_value: number
  min_amount: number
  total_count: number
  used_count: number
  per_limit: number
  valid_start_time: string
  valid_end_time: string
  status: number
  description?: string
  created_at: string
  updated_at: string
}

export interface FloorProduct {
  product_id: number
  sort: number
  cover_image?: string
  price: number
  original_price?: number
  name: string
}

export interface Floor {
  id: number
  name: string
  code: string
  title?: string
  subtitle?: string
  sort: number
  status: number
  style: number
  products: FloorProduct[]
  created_at: string
  updated_at: string
}

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export const homeApi = {
  getBanners: (platform?: number) => {
    return request.get<ApiResponse<Banner[]>>('/shop/home/banners', { params: { platform } })
  },
  getAvailableCoupons: () => {
    return request.get<ApiResponse<Coupon[]>>('/shop/home/coupons/available')
  },
  getFloors: () => {
    return request.get<ApiResponse<any[]>>('/shop/home/floors')
  },
  getHomeConfig: (platform?: number) => {
    return request.get<ApiResponse<{ banners: Banner[]; floors: Floor[] }>>('/shop/home/config', { params: { platform } })
  },
}

export const couponApi = {
  getAvailableCoupons: () => {
    return request.get<ApiResponse<Coupon[]>>('/shop/coupons/available')
  },
  receiveCoupon: (couponId: number) => {
    return request.post<ApiResponse<any>>('/shop/coupons/receive', { coupon_id: couponId })
  },
  getMyCoupons: () => {
    return request.get<ApiResponse<Coupon[]>>('/shop/coupons/my')
  },
}
