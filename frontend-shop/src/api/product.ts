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

// 后端实际路径：/api/v1/categories 和 /api/v1/products
const API_BASE = '/api/v1'

export const shopProductApi = {
  // 分类列表
  getCategories: () => request.get<ResponseBase<Category[]>>(`${API_BASE}/categories`),

  // 品牌列表（暂时用空数组，接口不存在）
  getBrands: () => request.get<ResponseBase<Brand[]>>(`${API_BASE}/brands`).catch(() => ({ data: [] })),

  // 商品列表
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
    return request.get<ResponseBase<PageResult<ProductSpu>>>(`${API_BASE}/products`, { params: p })
  },

  // 商品详情
  getProduct: (id: number) =>
    request.get<ResponseBase<ProductSpu>>(`${API_BASE}/products/${id}`),

  // SKU 列表
  getProductSkus: (spuId: number) =>
    request.get<ResponseBase<ProductSku[]>>(`${API_BASE}/products/${spuId}/skus`).catch(() => ({ data: [] })),

  // 商品图片
  getProductImages: (spuId: number, imageType?: number) =>
    request.get<ResponseBase<ProductImage[]>>(`${API_BASE}/products/${spuId}/images`, {
      params: { imageType }
    }).catch(() => ({ data: [] }))
}
