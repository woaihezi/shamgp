import request from './request'

export const productApi = {
  getProducts: (params) => request.get('/products/simple', { params }),
  createProduct: (data) => request.post('/products/simple', data),
  updateProduct: (id, data) => request.put(`/products/simple/${id}`, data),
}
