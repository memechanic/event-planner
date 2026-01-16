<template>
  <div id="app" class="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 flex flex-col">
    <!-- Навигация -->
    <nav class="bg-white shadow-md sticky top-0 z-50 border-b border-gray-200">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Логотип -->
          <router-link 
            to="/" 
            class="flex items-center space-x-3 hover:opacity-90 transition-opacity"
          >
            <div class="w-9 h-9 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center shadow-sm">
              <span class="text-white text-lg font-bold">🗓️</span>
            </div>
            <span class="text-xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
              Event Planner
            </span>
          </router-link>
          <div class="flex items-center space-x-2 sm:space-x-4">
            <!-- Основные ссылки -->
            <router-link 
              to="/" 
              class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 hover:bg-blue-50 hover:text-blue-700 text-gray-700"
              active-class="bg-blue-100 text-blue-700"
            >
              <span class="hidden sm:inline">Главная</span>
              <span class="sm:hidden">🏠</span>
            </router-link>
            
            <router-link 
              to="/create" 
              class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 hover:bg-blue-50 hover:text-blue-700 text-gray-700"
              active-class="bg-blue-100 text-blue-700"
            >
              <span class="hidden sm:inline">Создать</span>
              <span class="sm:hidden">➕</span>
            </router-link>
            
            <!-- <router-link 
              to="/event/demo" 
              class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 hover:bg-blue-50 hover:text-blue-700 text-gray-700"
              active-class="bg-blue-100 text-blue-700"
            >
              <span class="hidden sm:inline">Демо</span>
              <span class="sm:hidden">👁️</span>
            </router-link> -->

            <!-- Кнопка авторизации / выхода -->
            <button
              v-if="authStore.isAuthenticated"
              @click="logout"
              class="px-3 py-2 rounded-lg text-sm font-medium text-red-600 hover:bg-red-50 transition-colors"
            >
              <span class="hidden sm:inline">Выйти</span>
              <span class="sm:hidden">🚪</span>
            </button>

            <router-link
              v-else
              to="/login"
              class="px-3 py-2 rounded-lg text-sm font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition-colors"
            >
              <span class="hidden sm:inline">Войти</span>
              <span class="sm:hidden">🔑</span>
            </router-link>
          </div>
        </div>
      </div>
    </nav>
    
    <!-- Основное содержимое -->
    <main class="flex-grow container mx-auto px-4 py-6 sm:py-8">
      <router-view />
    </main>
    
    <!-- Футер -->
    <footer class="bg-gray-800 text-gray-300 mt-auto border-t border-gray-700">
      <div class="container mx-auto px-4 py-6">
        <p class="text-sm text-center">
          © 2024 Event Planner
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