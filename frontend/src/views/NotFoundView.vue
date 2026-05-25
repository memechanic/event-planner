<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 p-4">
    <div class="text-center max-w-md">
      <!-- <div class="text-6xl mb-4">🔍</div> -->
      <h1 class="text-4xl font-bold text-gray-800 mb-4">Страница не найдена</h1>
      <p class="text-gray-600 mb-8">
        Кажется, такой страницы не существует. Возможно, событие было удалено или ссылка устарела.
      </p>
      <router-link 
        to="/" 
        class="inline-flex items-center px-6 py-3 bg-gray-900 text-white font-medium rounded-lg hover:bg-gray-700 transition"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
        </svg>
        Вернуться на главную
      </router-link>
    </div>
  </div>
</template>

<script setup>
// text-2xl font-semibold text-gray-900
</script>