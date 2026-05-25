import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from '@/stores/auth'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

// Инициализируем auth ДО подключения роутера,
// чтобы навигационные гарды видели актуальное состояние
const authStore = useAuthStore()
authStore.initializeFromStorage()

app.use(router)
app.mount('#app')