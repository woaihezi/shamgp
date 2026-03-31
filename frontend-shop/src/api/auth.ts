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
  return request.post<LoginResponse>('/api/v1/auth/login', data)
}

export function register(data: RegisterParams) {
  return request.post<LoginResponse>('/api/v1/auth/register', data)
}

export function getUserInfo() {
  return request.get('/api/v1/auth/userinfo')
}

export function logout() {
  return request.post('/api/v1/auth/logout')
}
