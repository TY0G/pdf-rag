import { http } from './http'

export const authApi = {
  async sendCode(email: string) {
    const { data } = await http.post('/auth/send-code', { email })
    return data as { message: string; dev_code?: string }
  },
  async register(payload: { email: string; code: string; password: string; nickname: string }) {
    const { data } = await http.post('/auth/register', payload)
    return data
  },
  async login(payload: { email: string; password: string }) {
    const { data } = await http.post('/auth/login', payload)
    return data
  },
  async me() {
    const { data } = await http.get('/auth/me')
    return data
  }
}
