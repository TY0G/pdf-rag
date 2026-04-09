import { http } from './http'

export interface DocumentItem {
  id: number
  file_name: string
  file_size: number
  content_type: string
  parse_status: string
  parse_error?: string | null
  page_count: number
  summary?: string | null
  created_at: string
}

export const documentApi = {
  async list() {
    const { data } = await http.get('/documents')
    return data as DocumentItem[]
  },
  async detail(id: number) {
    const { data } = await http.get(`/documents/${id}`)
    return data
  },
  async upload(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    const { data } = await http.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return data
  },
  async reparse(id: number) {
    const { data } = await http.post(`/documents/${id}/parse`)
    return data
  },
  fileUrl(id: number) {
    return `/api/v1/documents/${id}/file`
  }
}
