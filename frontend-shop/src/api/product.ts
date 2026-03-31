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

const API_BASE = '/api/v1/shop'

export const shopProductApi = {
  getCategories: () => request.get<ResponseBase<Category[]>>(`${API_BASE}/categories`),
  
  getBrands: () => request.get<ResponseBase<Brand[]>>(`${API_BASE}/brands`),
  
  getProducts: (params: {
    page?: number
    pageSize?: number
    categoryId?: number
    brandId?: number
    keyword?: string
  }) => request.get<ResponseBase<PageResult<ProductSpu>>>(`${API_BASE}/products`, { params }),
  
  getProduct: (id: number) => request.get<ResponseBase<ProductSpu>>(`${API_BASE}/products/${id}`),
  
  getProductSkus: (spuId: number) => request.get<ResponseBase<ProductSku[]>>(`${API_BASE}/products/${spuId}/skus`),
  
  getProductImages: (spuId: number, imageType?: number) => 
    request.get<ResponseBase<ProductImage[]>>(`${API_BASE}/products/${spuId}/images`, { params: { imageType } })
}
