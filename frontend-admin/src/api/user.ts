import request from '@/utils/request'

export interface UserInfo {
  id?: number
  username: string
  email?: string
  phone?: string
  nickname?: string
  avatar?: string
  is_active?: boolean
  is_superuser?: boolean
  roles?: any[]
  created_at?: string
  updated_at?: string
}

export interface UserCreate {
  username: string
  password: string
  email?: string
  phone?: string
  nickname?: string
  avatar?: string
}

export interface UserUpdate {
  email?: string
  phone?: string
  nickname?: string
  avatar?: string
  is_active?: boolean
}

export interface UserPasswordUpdate {
  old_password: string
  new_password: string
}

export interface PageParams {
  page: number
  page_size: number
}

export interface PageResponse<T> {
  total: number
  page: number
  page_size: number
  items: T[]
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export const getUserList = (params: PageParams) => {
  return request.get<ApiResponse<PageResponse<UserInfo>>>('/users', { params })
}

export const getUserById = (id: number) => {
  return request.get<ApiResponse<UserInfo>>(`/users/${id}`)
}

export const createUser = (data: UserCreate) => {
  return request.post<ApiResponse<UserInfo>>('/users', data)
}

export const updateUser = (id: number, data: UserUpdate) => {
  return request.put<ApiResponse<UserInfo>>(`/users/${id}`, data)
}

export const updateUserPassword = (id: number, data: UserPasswordUpdate) => {
  return request.put<ApiResponse<UserInfo>>(`/users/${id}/password`, data)
}

export const deleteUser = (id: number) => {
  return request.delete<ApiResponse<any>>(`/users/${id}`)
}
