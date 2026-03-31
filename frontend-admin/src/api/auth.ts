import request from './request'

export interface LoginParams {
  username: string
  password: string
}

export interface LoginResult {
  access_token: string
  token_type: string
}

export interface UserInfo {
  id: number
  username: string
  nickname?: string
  avatar?: string
  email?: string
  phone?: string
  roles: string[]
  permissions: string[]
}

export function login(data: LoginParams) {
  return request.post<any, any>('/auth/login', data)
}

export function logout() {
  return request.post<any, any>('/auth/logout')
}

export function getUserInfo() {
  return request.get<any, any>('/auth/userinfo')
}
