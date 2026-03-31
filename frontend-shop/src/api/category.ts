import request from '@/utils/request'

export interface Category {
  id: number
  name: string
  parentId?: number
  sort: number
  createdAt: string
  children?: Category[]
}

export function getCategoryList() {
  return request.get<Category[]>('/api/v1/categories')
}
