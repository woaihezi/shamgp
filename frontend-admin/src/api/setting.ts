
import request from '@/utils/request'

export interface SystemConfig {
  id?: number
  config_key: string
  config_value?: string
  config_type: string
  config_group?: string
  description?: string
  is_public: boolean
  sort: number
  status: number
  created_at?: string
  updated_at?: string
}

export interface PageParams {
  page: number
  page_size: number
}

export interface PageResponse&lt;T&gt; {
  total: number
  page: number
  page_size: number
  items: T[]
}

export interface ApiResponse&lt;T = any&gt; {
  code: number
  message: string
  data: T
}

export const getConfigList = (params: PageParams &amp; {
  config_key?: string
  config_group?: string
  status?: number
}) =&gt; {
  return request.get&lt;ApiResponse&lt;PageResponse&lt;SystemConfig&gt;&gt;&gt;('/system-config', { params })
}

export const getConfigById = (id: number) =&gt; {
  return request.get&lt;ApiResponse&lt;SystemConfig&gt;&gt;(`/system-config/${id}`)
}

export const getConfigByKey = (key: string) =&gt; {
  return request.get&lt;ApiResponse&lt;SystemConfig&gt;&gt;(`/system-config/key/${key}`)
}

export const createConfig = (data: SystemConfig) =&gt; {
  return request.post&lt;ApiResponse&lt;SystemConfig&gt;&gt;('/system-config', data)
}

export const updateConfig = (id: number, data: Partial&lt;SystemConfig&gt;) =&gt; {
  return request.put&lt;ApiResponse&lt;SystemConfig&gt;&gt;(`/system-config/${id}`, data)
}

export const deleteConfig = (id: number) =&gt; {
  return request.delete&lt;ApiResponse&lt;any&gt;&gt;(`/system-config/${id}`)
}

export const getPublicConfigs = () =&gt; {
  return request.get&lt;ApiResponse&lt;SystemConfig[]&gt;&gt;('/system-config/public/list')
}
