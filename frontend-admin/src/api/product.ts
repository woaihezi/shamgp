import request from '@/utils/request'

export interface Category {
  id?: number
  name: string
  parentId?: number
  sort?: number
  icon?: string
  description?: string
  status?: number
  createdAt?: string
  updatedAt?: string
  children?: Category[]
}

export interface Brand {
  id?: number
  name: string
  logo?: string
  description?: string
  sort?: number
  status?: number
  createdAt?: string
  updatedAt?: string
}

export interface ProductImage {
  id?: number
  spuId: number
  imageUrl: string
  imageType?: number
  sort?: number
  createdAt?: string
  updatedAt?: string
}

export interface InventoryRecord {
  id?: number
  skuId: number
  totalStock?: number
  availableStock?: number
  lockedStock?: number
  warningStock?: number
  createdAt?: string
  updatedAt?: string
}

export interface ProductSku {
  id?: number
  spuId: number
  skuCode: string
  name: string
  specs?: any
  image?: string
  price: number
  originalPrice?: number
  costPrice?: number
  status?: number
  sort?: number
  createdAt?: string
  updatedAt?: string
  inventory?: InventoryRecord
}

export interface ProductSpu {
  id?: number
  name: string
  subtitle?: string
  categoryId: number
  brandId?: number
  mainImage?: string
  description?: string
  unit?: string
  status?: number
  sort?: number
  salesCount?: number
  viewCount?: number
  createdAt?: string
  updatedAt?: string
  category?: Category
  brand?: Brand
  skus?: ProductSku[]
  images?: ProductImage[]
  minPrice?: number
  maxPrice?: number
}

export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}

export interface ResponseBase<T> {
  code: number
  message: string
  data?: T
}

const API_BASE = '/api/v1'

export const categoryApi = {
  getTree: () => request.get<ResponseBase<Category[]>>(`${API_BASE}/categories/tree`),
  getList: (parentId?: number) => request.get<ResponseBase<Category[]>>(`${API_BASE}/categories`, { params: { parentId } }),
  get: (id: number) => request.get<ResponseBase<Category>>(`${API_BASE}/categories/${id}`),
  create: (data: Category) => request.post<ResponseBase<Category>>(`${API_BASE}/categories`, data),
  update: (id: number, data: Partial<Category>) => request.put<ResponseBase<Category>>(`${API_BASE}/categories/${id}`, data),
  delete: (id: number) => request.delete<ResponseBase<Category>>(`${API_BASE}/categories/${id}`)
}

export const brandApi = {
  getList: () => request.get<ResponseBase<Brand[]>>(`${API_BASE}/products/brands`),
  get: (id: number) => request.get<ResponseBase<Brand>>(`${API_BASE}/products/brands/${id}`),
  create: (data: Brand) => request.post<ResponseBase<Brand>>(`${API_BASE}/products/brands`, data),
  update: (id: number, data: Partial<Brand>) => request.put<ResponseBase<Brand>>(`${API_BASE}/products/brands/${id}`, data),
  delete: (id: number) => request.delete<ResponseBase<Brand>>(`${API_BASE}/products/brands/${id}`)
}

export const productApi = {
  getList: (params: {
    page?: number
    pageSize?: number
    categoryId?: number
    brandId?: number
    status?: number
    keyword?: string
  }) => request.get<ResponseBase<PageResult<ProductSpu>>>(`${API_BASE}/products/spus`, { params }),
  
  get: (id: number) => request.get<ResponseBase<ProductSpu>>(`${API_BASE}/products/spus/${id}`),
  
  create: (data: ProductSpu) => request.post<ResponseBase<ProductSpu>>(`${API_BASE}/products/spus`, data),
  
  update: (id: number, data: Partial<ProductSpu>) => request.put<ResponseBase<ProductSpu>>(`${API_BASE}/products/spus/${id}`, data),
  
  delete: (id: number) => request.delete<ResponseBase<ProductSpu>>(`${API_BASE}/products/spus/${id}`),
  
  publish: (id: number) => request.post<ResponseBase<ProductSpu>>(`${API_BASE}/products/spus/${id}/publish`),
  
  unpublish: (id: number) => request.post<ResponseBase<ProductSpu>>(`${API_BASE}/products/spus/${id}/unpublish`)
}

export const skuApi = {
  getList: (spuId: number) => request.get<ResponseBase<ProductSku[]>>(`${API_BASE}/products/spus/${spuId}/skus`),
  
  get: (id: number) => request.get<ResponseBase<ProductSku>>(`${API_BASE}/products/skus/${id}`),
  
  create: (data: ProductSku) => request.post<ResponseBase<ProductSku>>(`${API_BASE}/products/skus`, data),
  
  update: (id: number, data: Partial<ProductSku>) => request.put<ResponseBase<ProductSku>>(`${API_BASE}/products/skus/${id}`, data),
  
  delete: (id: number) => request.delete<ResponseBase<ProductSku>>(`${API_BASE}/products/skus/${id}`)
}

export const productImageApi = {
  getList: (spuId: number, imageType?: number) => request.get<ResponseBase<ProductImage[]>>(`${API_BASE}/products/spus/${spuId}/images`, { params: { imageType } }),
  
  create: (data: ProductImage) => request.post<ResponseBase<ProductImage>>(`${API_BASE}/products/images`, data),
  
  update: (id: number, data: Partial<ProductImage>) => request.put<ResponseBase<ProductImage>>(`${API_BASE}/products/images/${id}`, data),
  
  delete: (id: number) => request.delete<ResponseBase<ProductImage>>(`${API_BASE}/products/images/${id}`)
}

export const inventoryApi = {
  getBySku: (skuId: number) => request.get<ResponseBase<InventoryRecord>>(`${API_BASE}/inventory/sku/${skuId}`),
  
  create: (data: InventoryRecord) => request.post<ResponseBase<InventoryRecord>>(`${API_BASE}/inventory`, data),
  
  update: (id: number, data: Partial<InventoryRecord>) => request.put<ResponseBase<InventoryRecord>>(`${API_BASE}/inventory/${id}`, data),
  
  delete: (id: number) => request.delete<ResponseBase<InventoryRecord>>(`${API_BASE}/inventory/${id}`),
  
  adjustStock: (skuId: number, quantity: number, isAdd: boolean = true) => 
    request.post<ResponseBase<InventoryRecord>>(`${API_BASE}/inventory/sku/${skuId}/adjust`, null, { params: { quantity, isAdd } }),
  
  lockStock: (skuId: number, quantity: number) => 
    request.post<ResponseBase<InventoryRecord>>(`${API_BASE}/inventory/sku/${skuId}/lock`, null, { params: { quantity } }),
  
  unlockStock: (skuId: number, quantity: number) => 
    request.post<ResponseBase<InventoryRecord>>(`${API_BASE}/inventory/sku/${skuId}/unlock`, null, { params: { quantity } }),
  
  deductStock: (skuId: number, quantity: number) => 
    request.post<ResponseBase<InventoryRecord>>(`${API_BASE}/inventory/sku/${skuId}/deduct`, null, { params: { quantity } })
}
