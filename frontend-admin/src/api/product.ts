import request from './request'

export const getProducts = (params: any) =>
  request.get('/api/v1/products/simple', { params })

export const createProduct = (data: any) =>
  request.post('/api/v1/products', data)

export const updateProduct = (id: number, data: any) =>
  request.put(`/api/v1/products/${id}`, data)
