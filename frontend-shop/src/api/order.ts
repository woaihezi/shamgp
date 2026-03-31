import request from './request'

export interface Address {
  id: number
  user_id: number
  consignee_name: string
  consignee_phone: string
  province: string
  city: string
  district: string
  detail_address: string
  zip_code?: string
  is_default: boolean
  created_at: string
  updated_at: string
}

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

export interface CreateOrderParams {
  address_id: number
  cart_item_ids: number[]
  remark?: string
}

export interface Refund {
  id: number
  order_id: number
  order_item_id?: number
  refund_no: string
  user_id: number
  refund_amount: number
  refund_reason: string
  refund_type: string
  status: string
  audit_time?: string
  audit_user_id?: number
  audit_remark?: string
  refund_time?: string
  created_at: string
  updated_at: string
}

export const orderApi = {
  getAddresses: () => request.get<{ code: number; data: Address[] }>('/orders/addresses'),
  getDefaultAddress: () => request.get<{ code: number; data: Address }>('/orders/addresses/default'),
  createAddress: (data: Omit<Address, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => 
    request.post<{ code: number; data: Address }>('/orders/addresses', data),
  updateAddress: (id: number, data: Partial<Omit<Address, 'id' | 'user_id' | 'created_at' | 'updated_at'>>) => 
    request.put<{ code: number; data: Address }>(`/orders/addresses/${id}`, data),
  deleteAddress: (id: number) => request.delete<{ code: number }>(`/orders/addresses/${id}`),
  
  createOrder: (data: CreateOrderParams) => request.post<{ code: number; data: Order }>('/orders/', data),
  getOrders: (params?: { status?: string; page?: number; page_size?: number }) => 
    request.get<{ code: number; data: Order[]; total: number }>('/orders/', { params }),
  getOrder: (id: number) => request.get<{ code: number; data: Order }>(`/orders/${id}`),
  cancelOrder: (id: number, cancel_reason: string) => 
    request.post<{ code: number; data: Order }>(`/orders/${id}/cancel`, null, { params: { cancel_reason } }),
  updateOrderStatus: (id: number, status: string) => 
    request.put<{ code: number; data: Order }>(`/orders/${id}/status`, { status }),
  
  getRefunds: (params?: { order_id?: number }) => 
    request.get<{ code: number; data: Refund[] }>('/orders/refunds', { params }),
  getRefund: (id: number) => request.get<{ code: number; data: Refund }>(`/orders/refunds/${id}`),
  createRefund: (data: Omit<Refund, 'id' | 'refund_no' | 'user_id' | 'created_at' | 'updated_at' | 'status' | 'audit_time' | 'audit_user_id' | 'audit_remark' | 'refund_time'>) => 
    request.post<{ code: number; data: Refund }>('/orders/refunds', data)
}
