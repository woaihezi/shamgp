import request from '@/utils/request'

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

export interface MenuTree {
  id: number
  parent_id: number
  name: string
  path?: string
  component?: string
  permission?: string
  type: string
  icon?: string
  sort: number
  is_visible: boolean
  is_keep_alive: boolean
  is_iframe: boolean
  redirect?: string
  children: MenuTree[]
}

export interface RouterMeta {
  title: string
  icon?: string
  permission?: string
  is_keep_alive: boolean
  is_iframe: boolean
  is_visible: boolean
}

export interface RouterItem {
  path: string
  name?: string
  component?: string
  redirect?: string
  meta?: RouterMeta
  children: RouterItem[]
}

export interface Response<T = any> {
  code: number
  message: string
  data: T
}

export interface PaginationResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export function login(data: LoginParams) {
  return request.post<Response<LoginResult>>('/api/v1/auth/login', data)
}

export function getUserInfo() {
  return request.get<Response<UserInfo>>('/api/v1/auth/userinfo')
}

export function getMenuTree() {
  return request.get<Response<MenuTree[]>>('/api/v1/auth/menu-tree')
}

export function getRouters() {
  return request.get<Response<RouterItem[]>>('/api/v1/auth/routers')
}

export function logout() {
  return request.post<Response>('/api/v1/auth/logout')
}
