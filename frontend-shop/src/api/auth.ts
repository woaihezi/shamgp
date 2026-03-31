import request from '@/api/request'

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
  access_token: string
}

export function login(data: LoginParams) {
  // 路径 /auth/login → FastAPI 最终路由 /api/v1/auth/login
  return request.post<LoginResponse>('/auth/login', data)
}

export function register(data: RegisterParams) {
  return request.post<LoginResponse>('/auth/register', data)
}

export function getUserInfo() {
  return request.get('/auth/userinfo')
}

export function logout() {
  return request.post('/auth/logout')
}
