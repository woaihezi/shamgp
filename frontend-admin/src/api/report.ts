
import request from '@/utils/request'

export interface DashboardStats {
  total_users: number
  today_users: number
  total_orders: number
  today_orders: number
  total_products: number
  on_sale_products: number
  total_sales: number
  today_sales: number
}

export interface SalesTrendItem {
  date: string
  amount: number
  order_count: number
}

export interface SalesTrendResponse {
  trend: SalesTrendItem[]
  total_amount: number
  total_orders: number
}

export interface UserGrowthItem {
  date: string
  count: number
  cumulative: number
}

export interface UserGrowthResponse {
  growth: UserGrowthItem[]
  total_users: number
}

export interface OrderStats {
  pending_payment: number
  paid: number
  shipped: number
  completed: number
  cancelled: number
}

export interface OrderStatsResponse {
  stats: OrderStats
  recent_orders: any[]
}

export interface ApiResponse&lt;T = any&gt; {
  code: number
  message: string
  data: T
}

export const getDashboardStats = () =&gt; {
  return request.get&lt;ApiResponse&lt;DashboardStats&gt;&gt;('/dashboard/stats')
}

export const getSalesTrend = (days: number = 7) =&gt; {
  return request.get&lt;ApiResponse&lt;SalesTrendResponse&gt;&gt;('/dashboard/sales-trend', {
    params: { days }
  })
}

export const getUserGrowth = (days: number = 7) =&gt; {
  return request.get&lt;ApiResponse&lt;UserGrowthResponse&gt;&gt;('/dashboard/user-growth', {
    params: { days }
  })
}

export const getOrderStats = () =&gt; {
  return request.get&lt;ApiResponse&lt;OrderStatsResponse&gt;&gt;('/dashboard/order-stats')
}
