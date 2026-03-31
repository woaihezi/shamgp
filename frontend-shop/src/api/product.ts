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
  categoryId?: number
  brandId?: number
  cover_image?: string
  mainImage?: string
  description?: string
  unit?: string
  status?: number
  sort?: number
  sales?: number
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
  price?: number
  original_price?: number
  is_hot?: boolean
  is_new?: boolean
  views?: number
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

export const shopProductApi = {
  getCategories: () => request.get<ResponseBase<Category[]>>('/categories'),

  getBrands: () => request.get<ResponseBase<Brand[]>>('/brands').catch(() => ({ data: [] })),

  getProducts: (params: {
    page?: number
    pageSize?: number
    categoryId?: number
    brandId?: number
    keyword?: string
  }) => {
    const p: any = { page: params?.page || 1, page_size: params?.pageSize || 12 }
    if (params?.categoryId) p.category_id = params.categoryId
    if (params?.keyword) p.keyword = params.keyword
    return request.get<ResponseBase<PageResult<ProductSpu>>>('/products', { params: p })
  },

  getProduct: (id: number) => request.get<ResponseBase<ProductSpu>>(`/products/${id}`),

  getProductSkus: (spuId: number) =>
    request.get<ResponseBase<ProductSku[]>>(`/products/${spuId}/skus`).catch(() => ({ data: [] })),

  getProductImages: (spuId: number, imageType?: number) =>
    request
      .get<ResponseBase<ProductImage[]>>(`/products/${spuId}/images`, { params: { imageType } })
      .catch(() => ({ data: [] })),

  addBrowseHistory: (productId: number) =>
    request.post('/api/v1/products/browse', { product_id: productId }),

  addFavorite: (productId: number) =>
    request.post('/api/v1/products/favorites', { product_id: productId }),

  removeFavorite: (productId: number) =>
    request.delete(`/api/v1/products/favorites/${productId}`),

  getFavorites: () =>
    request.get('/api/v1/products/favorites'),
}
