
import request from '@/utils/request'

export interface FileInfo {
  id?: number
  filename: string
  storage_name?: string
  file_path?: string
  file_url?: string
  file_size: number
  file_type?: string
  file_ext?: string
  upload_user_id?: number
  category?: string
  storage_type: string
  status: number
  created_at?: string
  updated_at?: string
}

export interface UploadResponse {
  file_id: number
  filename: string
  file_url: string
  file_size: number
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

export const uploadFile = (file: File, category?: string, upload_user_id?: number) =&gt; {
  const formData = new FormData()
  formData.append('file', file)
  if (category) formData.append('category', category)
  if (upload_user_id) formData.append('upload_user_id', String(upload_user_id))
  
  return request.post&lt;ApiResponse&lt;UploadResponse&gt;&gt;('/uploads', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const getFileList = (params: PageParams &amp; {
  filename?: string
  file_type?: string
  category?: string
  upload_user_id?: number
  status?: number
}) =&gt; {
  return request.get&lt;ApiResponse&lt;PageResponse&lt;FileInfo&gt;&gt;&gt;('/uploads', { params })
}

export const getFileById = (id: number) =&gt; {
  return request.get&lt;ApiResponse&lt;FileInfo&gt;&gt;(`/uploads/${id}`)
}

export const updateFile = (id: number, data: Partial&lt;FileInfo&gt;) =&gt; {
  return request.put&lt;ApiResponse&lt;FileInfo&gt;&gt;(`/uploads/${id}`, data)
}

export const deleteFile = (id: number) =&gt; {
  return request.delete&lt;ApiResponse&lt;any&gt;&gt;(`/uploads/${id}`)
}

export const importExcel = () =&gt; {
  return request.post&lt;ApiResponse&lt;any&gt;&gt;('/uploads/excel/import')
}

export const exportExcel = () =&gt; {
  return request.get&lt;ApiResponse&lt;any&gt;&gt;('/uploads/excel/export')
}
