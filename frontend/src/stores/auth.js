// src/stores/auth.js
import { defineStore } from 'pinia'
import api from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,         // { id, username, email, role }
    accessToken: null,
    refreshToken: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.user && !!state.accessToken,
    userId: (state) => state.user?.id ?? null,
    isAdmin: (state) => state.user?.role === 'admin',
  },

  actions: {
    // ── Извлечение ошибок Django ──────────────────────────────────────────
    extractAuthError(error, fallback = 'Произошла ошибка') {
      const data = error?.response?.data
      if (!data) return error?.message || fallback

      // Поля: username, email, password, password2, non_field_errors
      for (const key of ['username', 'email', 'password', 'password2', 'non_field_errors']) {
        if (data[key]) {
          const val = data[key]
          return Array.isArray(val) ? val[0] : val
        }
      }
      if (data.detail) return data.detail
      if (typeof data === 'string') return data
      if (Array.isArray(data)) return data[0]
      return fallback
    },

    // ── Сохранение данных сессии ─────────────────────────────────────────
    _saveSession({ user, access, refresh }) {
      this.user = user
      this.accessToken = access
      this.refreshToken = refresh
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
    },

    // ── Регистрация ───────────────────────────────────────────────────────
    async register({ username, email, password, password2 }) {
      try {
        const res = await api.post('/auth/register/', {
          username: username.trim(),
          email: email.trim(),
          password,
          password2,
        })
        this._saveSession({
          user: res.data.user,
          access: res.data.access,
          refresh: res.data.refresh,
        })
        return res.data.user
      } catch (error) {
        throw new Error(this.extractAuthError(error, 'Не удалось выполнить регистрацию'))
      }
    },

    // ── Вход ─────────────────────────────────────────────────────────────
    async login({ username, password }) {
      try {
        const res = await api.post('/auth/login/', {
          username: username.trim(),
          password,
        })
        this._saveSession({
          user: res.data.user,
          access: res.data.access,
          refresh: res.data.refresh,
        })
        return res.data.user
      } catch (error) {
        throw new Error(this.extractAuthError(error, 'Не удалось выполнить вход'))
      }
    },

    // ── Выход ─────────────────────────────────────────────────────────────
    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('user')
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },

    // ── Восстановление при перезагрузке страницы ─────────────────────────
    initializeFromStorage() {
      try {
        const user = JSON.parse(localStorage.getItem('user') || 'null')
        const access = localStorage.getItem('access_token')
        const refresh = localStorage.getItem('refresh_token')
        if (user && access) {
          this.user = user
          this.accessToken = access
          this.refreshToken = refresh
        }
      } catch {
        console.warn('Не удалось восстановить сессию из localStorage')
      }
    },
  },
})
