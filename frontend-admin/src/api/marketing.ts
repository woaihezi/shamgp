import request from './request'

const BASE_URL = '/api/v1/admin'

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

export interface CouponCreate {
  name: string
  type: number
  discount_value: number
  min_amount: number
  total_count: number
  per_limit: number
  valid_start_time: string
  valid_end_time: string
  status: number
  description?: string
}

export interface CouponUpdate {
  name?: string
  type?: number
  discount_value?: number
  min_amount?: number
  total_count?: number
  per_limit?: number
  valid_start_time?: string
  valid_end_time?: string
  status?: number
  description?: string
}

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

export interface BannerCreate {
  title: string
  image_url: string
  link_url?: string
  sort: number
  status: number
  platform: number
  description?: string
}

export interface BannerUpdate {
  title?: string
  image_url?: string
  link_url?: string
  sort?: number
  status?: number
  platform?: number
  description?: string
}

export interface AdSpace {
  id: number
  name: string
  code: string
  width?: number
  height?: number
  description?: string
  status: number
  created_at: string
  updated_at: string
}

export interface Ad {
  id: number
  ad_space_id: number
  title: string
  image_url: string
  link_url?: string
  sort: number
  status: number
  start_time?: string
  end_time?: string
  click_count: number
  description?: string
  created_at: string
  updated_at: string
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

export const couponApi = {
  getCoupons: (params: { page?: number; page_size?: number; status?: number }) => {
    return request.get<ApiResponse<PageResult<Coupon>>>(`${BASE_URL}/coupons`, { params })
  },
  getCoupon: (id: number) => {
    return request.get<ApiResponse<Coupon>>(`${BASE_URL}/coupons/${id}`)
  },
  createCoupon: (data: CouponCreate) => {
    return request.post<ApiResponse<Coupon>>(`${BASE_URL}/coupons`, data)
  },
  updateCoupon: (id: number, data: CouponUpdate) => {
    return request.put<ApiResponse<Coupon>>(`${BASE_URL}/coupons/${id}`, data)
  },
  deleteCoupon: (id: number) => {
    return request.delete<ApiResponse<any>>(`${BASE_URL}/coupons/${id}`)
  },
}

export const bannerApi = {
  getBanners: (params: { page?: number; page_size?: number; status?: number; platform?: number }) => {
    return request.get<ApiResponse<PageResult<Banner>>>(`${BASE_URL}/banners`, { params })
  },
  getBanner: (id: number) => {
    return request.get<ApiResponse<Banner>>(`${BASE_URL}/banners/${id}`)
  },
  createBanner: (data: BannerCreate) => {
    return request.post<ApiResponse<Banner>>(`${BASE_URL}/banners`, data)
  },
  updateBanner: (id: number, data: BannerUpdate) => {
    return request.put<ApiResponse<Banner>>(`${BASE_URL}/banners/${id}`, data)
  },
  deleteBanner: (id: number) => {
    return request.delete<ApiResponse<any>>(`${BASE_URL}/banners/${id}`)
  },
}

export const adSpaceApi = {
  getAdSpaces: (params: { page?: number; page_size?: number; status?: number }) => {
    return request.get<ApiResponse<PageResult<AdSpace>>>(`${BASE_URL}/ad-spaces`, { params })
  },
  getAdSpace: (id: number) => {
    return request.get<ApiResponse<AdSpace>>(`${BASE_URL}/ad-spaces/${id}`)
  },
  createAdSpace: (data: Partial<AdSpace>) => {
    return request.post<ApiResponse<AdSpace>>(`${BASE_URL}/ad-spaces`, data)
  },
  updateAdSpace: (id: number, data: Partial<AdSpace>) => {
    return request.put<ApiResponse<AdSpace>>(`${BASE_URL}/ad-spaces/${id}`, data)
  },
  deleteAdSpace: (id: number) => {
    return request.delete<ApiResponse<any>>(`${BASE_URL}/ad-spaces/${id}`)
  },
}

export const adApi = {
  getAds: (params: { page?: number; page_size?: number; ad_space_id?: number; status?: number }) => {
    return request.get<ApiResponse<PageResult<Ad>>>(`${BASE_URL}/ads`, { params })
  },
  getAd: (id: number) => {
    return request.get<ApiResponse<Ad>>(`${BASE_URL}/ads/${id}`)
  },
  createAd: (data: Partial<Ad>) => {
    return request.post<ApiResponse<Ad>>(`${BASE_URL}/ads`, data)
  },
  updateAd: (id: number, data: Partial<Ad>) => {
    return request.put<ApiResponse<Ad>>(`${BASE_URL}/ads/${id}`, data)
  },
  deleteAd: (id: number) => {
    return request.delete<ApiResponse<any>>(`${BASE_URL}/ads/${id}`)
  },
}

export const floorApi = {
  getFloors: (params: { page?: number; page_size?: number; status?: number }) => {
    return request.get<ApiResponse<PageResult<Floor>>>(`${BASE_URL}/floors`, { params })
  },
  getFloor: (id: number) => {
    return request.get<ApiResponse<Floor>>(`${BASE_URL}/floors/${id}`)
  },
  createFloor: (data: Partial<Floor>) => {
    return request.post<ApiResponse<Floor>>(`${BASE_URL}/floors`, data)
  },
  updateFloor: (id: number, data: Partial<Floor>) => {
    return request.put<ApiResponse<Floor>>(`${BASE_URL}/floors/${id}`, data)
  },
  deleteFloor: (id: number) => {
    return request.delete<ApiResponse<any>>(`${BASE_URL}/floors/${id}`)
  },
}
