import axios from 'axios'

// Создаём экземпляр axios для работы с Django через Vite прокси
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 5000,
})

// ── Request interceptor: добавляем JWT-токен ──────────────────────────────
api.interceptors.request.use(
  (config) => {
    const access = localStorage.getItem('access_token')
    if (access) {
      config.headers['Authorization'] = `Bearer ${access}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

// ── Response interceptor: обрабатываем 401, пробуем обновить токен ────────
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Если 401 и ещё не пробовали refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refresh = localStorage.getItem('refresh_token')

      if (refresh) {
        try {
          const res = await axios.post('/api/auth/refresh/', { refresh })
          const newAccess = res.data.access
          localStorage.setItem('access_token', newAccess)
          originalRequest.headers['Authorization'] = `Bearer ${newAccess}`
          return api(originalRequest)
        } catch {
          // refresh тоже истёк — разлогиниваем
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
          window.location.href = '/login'
        }
      }
    }

    // Логируем и нормализуем ошибки Django
    console.error('API Error:', {
      status: error.response?.status,
      message: error.message,
      url: error.config?.url,
    })

    if (error.response?.data) {
      const djangoError = error.response.data
      if (djangoError.detail) {
        error.message = djangoError.detail
      } else if (typeof djangoError === 'string') {
        error.message = djangoError
      } else if (Array.isArray(djangoError)) {
        error.message = djangoError.join(', ')
      }
    }

    return Promise.reject(error)
  },
)

export { api }
export default api
