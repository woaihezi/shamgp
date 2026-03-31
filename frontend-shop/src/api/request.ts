import axios, { AxiosInstance, AxiosResponse } from 'axios'

const service: AxiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 15000,
})

service.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

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
    console.error(error.message || 'Request Error')
    return Promise.reject(error)
  }
)

export default service
