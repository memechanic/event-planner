<template>
  <div id="app" class="min-h-screen bg-white flex flex-col">
    <!-- Навигация -->
    <nav class="bg-white sticky top-0 z-50 border-b border-gray-200">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-14">
          <!-- Логотип -->
          <router-link
            to="/"
            class="flex items-center gap-2 text-gray-900 hover:text-gray-600 transition-colors"
          >
            <span class="text-lg">🗓️</span>
            <span class="text-base font-semibold tracking-tight">Event Planner</span>
          </router-link>

          <div class="flex items-center gap-1">
            <router-link
              to="/"
              class="px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 rounded-md hover:bg-gray-100 transition-colors"
              active-class="text-gray-900 font-medium"
            >
              Главная
            </router-link>

            <router-link
              to="/create"
              class="px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 rounded-md hover:bg-gray-100 transition-colors"
              active-class="text-gray-900 font-medium"
            >
              Создать
            </router-link>

            <template v-if="authStore.isAuthenticated">
              <span class="hidden sm:inline text-sm text-gray-500 px-2">
                {{ authStore.user.username }}
              </span>
              <button
                @click="logout"
                class="px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 rounded-md hover:bg-gray-100 transition-colors"
              >
                Выйти
              </button>
            </template>

            <template v-else>
              <router-link
                to="/login"
                class="px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 rounded-md hover:bg-gray-100 transition-colors"
              >
                Войти
              </router-link>
              <router-link
                to="/register"
                class="px-3 py-1.5 text-sm bg-gray-900 text-white rounded-md hover:bg-gray-700 transition-colors"
              >
                Регистрация
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Основное содержимое -->
    <main class="flex-grow container mx-auto px-4 py-6 sm:py-8">
      <router-view />
    </main>

    <!-- Футер -->
    <footer class="border-t border-gray-200 mt-auto">
      <div class="container mx-auto px-4 py-5">
        <p class="text-sm text-center text-gray-400">
          © 2025 Event Planner
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  // Можно перенаправить на главную или оставить на текущей странице
  router.push('/')
}

// Статус соединения
const isOnline = ref(navigator.onLine)
const connectionStatus = ref(isOnline.value ? 'онлайн' : 'офлайн')

const updateOnlineStatus = () => {
  isOnline.value = navigator.onLine
  connectionStatus.value = isOnline.value ? 'онлайн' : 'офлайн'
  
  console.log(`Соединение: ${connectionStatus.value}`)
}

onMounted(() => {
  window.addEventListener('online', updateOnlineStatus)
  window.addEventListener('offline', updateOnlineStatus)
})

onUnmounted(() => {
  window.removeEventListener('online', updateOnlineStatus)
  window.removeEventListener('offline', updateOnlineStatus)
})
</script>

<style>
/* Убраны все встроенные стили - заменены на Tailwind классы */
</style>