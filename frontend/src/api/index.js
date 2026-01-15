import axios from 'axios'

// Создаём экземпляр axios для работы с Django через Vite прокси
const api = axios.create({
  baseURL: '/api', // Vite проксирует на Django (localhost:8000)
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 5000
})

// Перехватчик ошибок
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', {
      status: error.response?.status,
      message: error.message,
      url: error.config?.url
    })
    
    // Преобразуем Django ошибки
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
  }
)

export { api }
export default api