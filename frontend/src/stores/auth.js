// src/stores/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null, // { id, username, email }
  }),

  actions: {
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