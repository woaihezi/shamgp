import request from './request'

export interface Coupon {
  id: number
  name: string
  code: string
  type: string
  discount_value: number
  min_order_amount: number
  max_discount_amount?: number
  start_date: string
  end_date: string
  status: string
  total_count: number
  used_count: number
  per_user_limit: number
  is_public: boolean
  created_at: string
  updated_at: string
}

export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

// 优惠券 API — 后端实际路径: /api/v1/coupons/
export const couponApi = {
  getCoupons: (params?: { page?: number; page_size?: number }) =>
    request.get<ApiResponse<PageResult<Coupon>>>('/coupons', { params }),

  getCoupon: (id: number) =>
    request.get<ApiResponse<Coupon>>(`/coupons/${id}`),

  createCoupon: (data: Partial<Coupon>) =>
    request.post<ApiResponse<{ id: number }>>('/coupons', data),

  updateCoupon: (id: number, data: Partial<Coupon>) =>
    request.put<ApiResponse<any>>(`/coupons/${id}`, data),

  deleteCoupon: (id: number) =>
    request.delete<ApiResponse<any>>(`/coupons/${id}`),

  verifyCoupon: (code: string, order_amount: number) =>
    request.get<ApiResponse<{ valid: boolean; discount?: number; reason?: string }>>(
      `/coupons/verify?code=${code}&order_amount=${order_amount}`
    ),
}

// Banner API
export interface Banner {
  id: number
  title: string
  image_url: string
  link_url?: string
  sort: number
  status: number
  platform: number
  description?: string
}

export const bannerApi = {
  getBanners: (params?: { page?: number; page_size?: number; platform?: number }) =>
    request.get<ApiResponse<PageResult<Banner>>>('/banners', { params }),
  
  createBanner: (data: Partial<Banner>) =>
    request.post<ApiResponse<{ id: number }>>('/banners', data),
  
  updateBanner: (id: number, data: Partial<Banner>) =>
    request.put<ApiResponse<any>>(`/banners/${id}`, data),
  
  deleteBanner: (id: number) =>
    request.delete<ApiResponse<any>>(`/banners/${id}`),
}
