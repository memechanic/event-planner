<!-- src/views/LoginView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 p-4">
    <div class="w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6">Вход</h1>
      <form @submit.prevent="login" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
          <input
            v-model="username"
            type="text"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Ваше имя"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="example@email.com"
          />
        </div>
        <button
          type="submit"
          class="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 transition"
          :disabled="loading"
        >
          {{ loading ? 'Загрузка...' : 'Войти' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const username = ref('')
const email = ref('')
const loading = ref(false)
const router = useRouter()
const authStore = useAuthStore()

const login = async () => {
  loading.value = true
  try {
    const response = await api.post('/auth/login/', {
      username: username.value,
      email: email.value
    })
    // Ожидаем ответ вида: { id: 1, username: "...", email: "..." }
    authStore.setUser(response.data)
    router.push('/') // или '/my-events', если есть отдельная страница
  } catch (error) {
    console.error('Login error:', error)
    alert('Не удалось войти. Проверьте данные.')
  } finally {
    loading.value = false
  }
}
</script>