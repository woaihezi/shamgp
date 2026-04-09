import request from '@/utils/request'

export interface Permission {
  id: number
  name: string
  code: string
  type: string
  path?: string
  method?: string
  parent_id: number
  sort: number
  description?: string
}

export interface Role {
  id: number
  name: string
  code: string
  description?: string
  sort: number
  permissions: Permission[]
  created_at?: string
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface ListResponse<T> {
  data: T[]
  total: number
}

// 权限相关API
export const getPermissionList = (params?: {
  type?: string
  page?: number
  page_size?: number
}) => {
  return request.get<ApiResponse<ListResponse<Permission>>>('/roles/permissions', { params })
}

export const createPermission = (data: {
  name: string
  code: string
  type?: string
  path?: string
  method?: string
  parent_id?: number
  sort?: number
  description?: string
}) => {
  return request.post<ApiResponse<{ id: number; name: string; code: string }>>('/roles/permissions', data)
}

export const updatePermission = (id: number, data: {
  name?: string
  type?: string
  path?: string
  method?: string
  parent_id?: number
  sort?: number
  description?: string
}) => {
  return request.put<ApiResponse<{ id: number; name: string }>>(`/roles/permissions/${id}`, data)
}

export const deletePermission = (id: number) => {
  return request.delete<ApiResponse<any>>(`/roles/permissions/${id}`)
}

// 角色相关API
export const getRoleList = (params?: {
  page?: number
  page_size?: number
}) => {
  return request.get<ApiResponse<ListResponse<Role>>>('/roles/roles', { params })
}

export const createRole = (data: {
  name: string
  code: string
  description?: string
  sort?: number
  permission_ids?: number[]
}) => {
  return request.post<ApiResponse<{ id: number; name: string; code: string }>>('/roles/roles', data)
}

export const updateRole = (id: number, data: {
  name?: string
  description?: string
  sort?: number
  permission_ids?: number[]
}) => {
  return request.put<ApiResponse<{ id: number; name: string }>>(`/roles/roles/${id}`, data)
}

export const deleteRole = (id: number) => {
  return request.delete<ApiResponse<any>>(`/roles/roles/${id}`)
}

// 用户角色分配API
export const getUserRoles = (userId: number) => {
  return request.get<ApiResponse<Role[]>>(`/roles/users/${userId}/roles`)
}

export const assignUserRoles = (userId: number, roleIds: number[]) => {
  return request.post<ApiResponse<any>>(`/roles/users/${userId}/roles`, { role_ids: roleIds })
}
