import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

export const http = axios.create({
  baseURL: '/api/v1',
  timeout: 60000
})

http.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

http.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error?.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)
