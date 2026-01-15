<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-brand">
          🗓️ Event Planner
        </router-link>
        <div class="nav-links">
          <router-link to="/">Главная</router-link>
          <router-link to="/create">Создать событие</router-link>
          <router-link to="/event/demo">Демо</router-link>
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view />
    </main>
    
    <footer class="footer">
      <div class="footer-content">
        <p>© 2024 Event Planner. Проект для 24-часового хакатона.</p>
        <p class="connection-status">
          Статус соединения: 
          <span :class="connectionClass">
            {{ connectionStatus }}
          </span>
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// Статус соединения
const isOnline = ref(navigator.onLine)
const connectionStatus = ref(isOnline.value ? 'онлайн' : 'офлайн')
const connectionClass = ref(isOnline.value ? 'online' : 'offline')

const updateOnlineStatus = () => {
  isOnline.value = navigator.onLine
  connectionStatus.value = isOnline.value ? 'онлайн' : 'офлайн'
  connectionClass.value = isOnline.value ? 'online' : 'offline'
  
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  line-height: 1.6;
  color: #333;
  background: #f5f5f5;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.nav-brand {
  font-size: 20px;
  font-weight: bold;
  color: #2196F3;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  color: #666;
  text-decoration: none;
  font-weight: 500;
}

.nav-links a:hover {
  color: #2196F3;
}

.nav-links a.router-link-active {
  color: #2196F3;
  font-weight: 600;
}

.main-content {
  flex: 1;
  padding: 20px;
}

.footer {
  background: #333;
  color: white;
  padding: 20px;
  text-align: center;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

.footer p {
  margin: 5px 0;
}

.connection-status {
  font-size: 14px;
}

.online {
  color: #4CAF50;
}

.offline {
  color: #ff9800;
}

@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    height: auto;
    padding: 15px;
  }
  
  .nav-brand {
    margin-bottom: 10px;
  }
  
  .main-content {
    padding: 15px;
  }
}
</style>