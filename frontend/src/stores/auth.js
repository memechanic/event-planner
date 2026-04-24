// src/stores/auth.js
import { defineStore } from 'pinia'
import api from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null, // { id, username, email }
  }),

  actions: {
    normalizeCredentials(credentials) {
      const payload = {
        username: credentials?.username?.trim(),
        email: credentials?.email?.trim(),
      }

      if (!payload.username || !payload.email) {
        throw new Error('Имя и email обязательны')
      }
      return payload
    },

    extractAuthError(error, fallbackMessage) {
      return (
        error?.response?.data?.username?.[0] ||
        error?.response?.data?.email?.[0] ||
        error?.response?.data?.detail ||
        error?.message ||
        fallbackMessage
      )
    },

    async login(credentials) {
      const payload = this.normalizeCredentials(credentials)

      try {
        const response = await api.post('/auth/login/', payload)
        this.setUser(response.data)
        return response.data
      } catch (error) {
        throw new Error(this.extractAuthError(error, 'Не удалось выполнить вход'))
      }
    },

    async register(credentials) {
      const payload = this.normalizeCredentials(credentials)

      try {
        const response = await api.post('/auth/register/', payload)
        this.setUser(response.data)
        return response.data
      } catch (error) {
        throw new Error(this.extractAuthError(error, 'Не удалось выполнить регистрацию'))
      }
    },

    setUser(userData) {
      this.user = userData
      // Сохраняем в localStorage для перезагрузки страницы
      localStorage.setItem('user', JSON.stringify(userData))
    },

    logout() {
      this.user = null
      localStorage.removeItem('user')
    },

    // Восстанавливаем при старте приложения
    initializeFromStorage() {
      const saved = localStorage.getItem('user')
      if (saved) {
        try {
          this.user = JSON.parse(saved)
        } catch (e) {
          console.warn('Failed to parse user from localStorage')
        }
      }
    }
  },

  getters: {
    isAuthenticated: (state) => !!state.user,
    userId: (state) => state.user?.id || null,
  }
})