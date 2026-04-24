<!-- src/views/LoginView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 p-4">
    <div class="w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6">Вход и регистрация</h1>
      <form class="space-y-4">
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
          type="button"
          class="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 transition"
          :disabled="loading"
          @click="submitAuth('login')"
        >
          {{ loading && actionType === 'login' ? 'Загрузка...' : 'Войти' }}
        </button>
        <button
          type="button"
          class="w-full bg-emerald-600 text-white py-2 rounded hover:bg-emerald-700 transition"
          :disabled="loading"
          @click="submitAuth('register')"
        >
          {{ loading && actionType === 'register' ? 'Загрузка...' : 'Зарегистрироваться' }}
        </button>
        <p v-if="errorMessage" class="text-sm text-red-600">
          {{ errorMessage }}
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const email = ref('')
const loading = ref(false)
const actionType = ref('')
const errorMessage = ref('')
const router = useRouter()
const authStore = useAuthStore()

const submitAuth = async (type) => {
  actionType.value = type
  loading.value = true
  errorMessage.value = ''

  const payload = {
    username: username.value,
    email: email.value
  }

  try {
    if (type === 'register') {
      await authStore.register(payload)
    } else {
      await authStore.login(payload)
    }

    router.push('/') // или '/my-events', если есть отдельная страница
  } catch (error) {
    console.error('Login error:', error)
    errorMessage.value = error.message || 'Не удалось выполнить запрос.'
  } finally {
    loading.value = false
    actionType.value = ''
  }
}
</script>