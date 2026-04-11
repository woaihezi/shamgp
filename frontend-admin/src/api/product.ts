import request from './request'

export const getProducts = (params: any) =>
  request.get('/products/simple', { params })

export const createProduct = (data: any) =>
  request.post('/products', data)

export const updateProduct = (id: number, data: any) =>
  request.put(`/products/${id}`, data)
