import axios, { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios'

const service: AxiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 15000,
})

// 请求拦截器：自动附加 JWT token
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：统一处理 401 重定向
service.interceptors.response.use(
  (response: AxiosResponse) => {
    const res = response.data
    if (res.code !== 200) {
      console.error(res.message || 'Error')
      return Promise.reject(new Error(res.message || 'Error'))
    }
    return res
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    console.error(error.message || 'Request Error')
    return Promise.reject(error)
  }
)

export default service
