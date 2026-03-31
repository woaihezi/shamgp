import request from './request'

export interface CouponInfo {
  id: number
  name: string
  code: string
  type: number
  满减金额: number
  折扣: number | null
  门槛金额: number
  total_count: number
  remain_count: number
  per_user_limit: number
  start_time: string | null
  end_time: string | null
  description: string | null
}

export interface UserCoupon {
  id: number
  coupon_id: number
  name: string
  code: string
  type: number
  满减金额: number
  折扣: number | null
  门槛金额: number
  status: number
  start_time: string | null
  end_time: string | null
}

export const couponApi = {
  /** 获取当前可领取的优惠券 */
  getAvailable: () => request.get<any, { code: number; data: CouponInfo[] }>('/coupons/available'),

  /** 领取优惠券 */
  receive: (couponId: number) => request.post<any, { code: number; message: string; data: { id: number } }>(`/coupons/receive/${couponId}`),

  /** 获取我的优惠券 */
  getMyCoupons: () => request.get<any, { code: number; data: UserCoupon[] }>('/coupons/my'),

  /** 使用优惠券（结算时调用） */
  useCoupon: (couponId: number, orderId: number) =>
    request.post<any, { code: number; message: string }>('/coupons/use', { coupon_id: couponId, order_id: orderId }),
}
