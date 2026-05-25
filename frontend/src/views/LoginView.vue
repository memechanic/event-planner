<!-- src/views/LoginView.vue -->
<template>
  <div class="min-h-[80vh] flex items-center justify-center p-4">
    <div class="w-full max-w-sm">
      <div class="mb-8">
        <h1 class="text-2xl font-semibold text-gray-900">Вход</h1>
        <p class="text-sm text-gray-500 mt-1">
          Нет аккаунта?
          <router-link to="/register" class="text-gray-900 underline underline-offset-2 hover:text-gray-600">
            Зарегистрироваться
          </router-link>
        </p>
      </div>

      <form @submit.prevent="submit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Имя пользователя</label>
          <input
            v-model="username"
            type="text"
            autocomplete="username"
            required
            placeholder="Ваш логин"
            class="w-full px-3 py-2.5 border rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 transition-colors"
            :class="{ 'border-red-400': error, 'border-gray-200': !error }"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
          <div class="relative">
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="current-password"
              required
              placeholder="••••••••"
              class="w-full px-3 py-2.5 border rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 transition-colors pr-10"
              :class="{ 'border-red-400': error, 'border-gray-200': !error }"
            />
            <button
              type="button"
              tabindex="-1"
              @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 text-xs"
            >
              {{ showPassword ? 'скрыть' : 'показать' }}
            </button>
          </div>
        </div>

        <p v-if="error" class="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">
          {{ error }}
        </p>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-gray-900 hover:bg-gray-700 disabled:opacity-40 text-white text-sm font-medium py-2.5 rounded-lg transition-colors"
        >
          {{ loading ? 'Выполняется вход...' : 'Войти' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const submit = async () => {
  error.value = ''
  loading.value = true
  try {
    await authStore.login({ username: username.value, password: password.value })
    router.push(route.query.redirect || '/')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>
