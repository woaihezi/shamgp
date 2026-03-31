import request from '@/utils/request'

export interface LoginParams {
  username: string
  password: string
}

export interface RegisterParams {
  username: string
  password: string
  email?: string
  phone?: string
}

export interface LoginResponse {
  token: string
  user: {
    id: number
    username: string
    email?: string
    phone?: string
    avatar?: string
  }
}

export function login(data: LoginParams) {
  return request.post<LoginResponse>('/shop/auth/login', data)
}

export function register(data: RegisterParams) {
  return request.post<LoginResponse>('/shop/auth/register', data)
}

export function getUserInfo() {
  return request.get('/shop/auth/user')
}

export function logout() {
  return request.post('/shop/auth/logout')
}
