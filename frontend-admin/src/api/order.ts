import request from './request'

export interface OrderItem {
  id: number
  order_id: number
  product_id: number
  product_name: string
  product_image?: string
  sku_id?: number
  sku_specs?: string
  price: number
  quantity: number
  total_amount: number
  created_at: string
  updated_at: string
}

export interface Order {
  id: number
  order_no: string
  user_id: number
  total_amount: number
  pay_amount: number
  discount_amount: number
  freight_amount: number
  status: string
  pay_status: number
  pay_time?: string
  pay_type?: string
  consignee_name: string
  consignee_phone: string
  consignee_address: string
  remark?: string
  cancel_time?: string
  cancel_reason?: string
  delivery_time?: string
  receive_time?: string
  items: OrderItem[]
  created_at: string
  updated_at: string
}

export const orderApi = {
  getOrders: (params?: { status?: string; page?: number; page_size?: number }) => 
    request.get<{ code: number; data: Order[]; total: number }>('/orders/admin/', { params }),
  getOrder: (id: number) => 
    request.get<{ code: number; data: Order }>(`/orders/admin/${id}`),
  updateOrderStatus: (id: number, status: string) => 
    request.put<{ code: number; data: Order }>(`/orders/admin/${id}/status`, { status })
}
