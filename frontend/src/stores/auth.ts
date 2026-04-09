import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'

export interface UserProfile {
  id: number
  email: string
  nickname: string
  role: string
  is_active: boolean
  created_at: string
}

const TOKEN_KEY = 'pdf_scan_token'
const USER_KEY = 'pdf_scan_user'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem(TOKEN_KEY) || '',
    user: localStorage.getItem(USER_KEY)
      ? (JSON.parse(localStorage.getItem(USER_KEY) as string) as UserProfile)
      : null
  }),
  actions: {
    setAuth(token: string, user: UserProfile) {
      this.token = token
      this.user = user
      localStorage.setItem(TOKEN_KEY, token)
      localStorage.setItem(USER_KEY, JSON.stringify(user))
    },
    clearAuth() {
      this.token = ''
      this.user = null
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(USER_KEY)
    },
    async refreshProfile() {
      if (!this.token) return
      const profile = await authApi.me()
      this.user = profile
      localStorage.setItem(USER_KEY, JSON.stringify(profile))
    }
  }
})
