import request from './request'

export interface CartItem {
  id: number
  user_id: number
  product_id: number
  sku_id?: number
  quantity: number
  selected: boolean
  product_name?: string
  product_image?: string
  product_price?: number
  created_at: string
  updated_at: string
}

export interface CartSummary {
  total_items: number
  total_quantity: number
  total_amount: number
  selected_items: CartItem[]
}

export interface AddCartItemParams {
  product_id: number
  sku_id?: number
  quantity: number
}

export interface UpdateCartItemParams {
  quantity?: number
  selected?: boolean
}

export const cartApi = {
  getSummary: () => request.get<{ code: number; data: CartSummary }>('/carts/summary'),
  getItems: () => request.get<{ code: number; data: CartItem[] }>('/carts/items'),
  addItem: (data: AddCartItemParams) => request.post<{ code: number; data: CartItem }>('/carts/items', data),
  updateItem: (id: number, data: UpdateCartItemParams) => request.put<{ code: number; data: CartItem }>(`/carts/items/${id}`, data),
  removeItem: (id: number) => request.delete<{ code: number }>(`/carts/items/${id}`),
  clearCart: () => request.delete<{ code: number }>('/carts/clear')
}
