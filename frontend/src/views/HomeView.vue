<template>
  <div class="max-w-6xl mx-auto px-4 py-8 md:py-12 lg:py-16">
    <!-- Hero Section -->
    <div class="text-center mb-16 lg:mb-24">
      <h1 class="text-5xl md:text-6xl lg:text-7xl font-bold mb-4 md:mb-6">
        <span class="inline-block mr-3">🗓️</span>
        <span class="bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 bg-clip-text text-transparent">
          Event Planner
        </span>
      </h1>
      
      <p class="text-lg md:text-xl lg:text-2xl text-gray-600 mb-8 md:mb-12 max-w-3xl mx-auto px-4">
        Простое планирование встреч с друзьями и коллегами
      </p>
      
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center px-4">
        <router-link 
          to="/create" 
          class="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-2 text-lg"
        >
          <span class="text-xl">📅</span>
          Создать событие
        </router-link>
        
        <router-link 
          to="/event/demo" 
          class="w-full sm:w-auto px-8 py-4 bg-white border-2 border-blue-600 text-blue-600 hover:bg-blue-50 font-semibold rounded-xl shadow-md hover:shadow-lg transform hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-2 text-lg"
        >
          <span class="text-xl">🎯</span>
          Посмотреть демо
        </router-link>
      </div>
    </div>
    
    <!-- Features Section -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 mb-16 lg:mb-24 px-4">
      <div class="bg-white rounded-2xl p-6 md:p-8 shadow-lg hover:shadow-2xl border border-gray-100 transition-all duration-300 transform hover:-translate-y-2">
        <div class="text-5xl md:text-6xl mb-6 text-center">📱</div>
        <h3 class="text-xl md:text-2xl font-bold text-gray-800 mb-4 text-center">Просто и понятно</h3>
        <p class="text-gray-600 leading-relaxed text-center">
          Создайте событие за минуту, отправьте ссылку участникам
        </p>
      </div>
      
      <div class="bg-white rounded-2xl p-6 md:p-8 shadow-lg hover:shadow-2xl border border-gray-100 transition-all duration-300 transform hover:-translate-y-2">
        <div class="text-5xl md:text-6xl mb-6 text-center">🗳️</div>
        <h3 class="text-xl md:text-2xl font-bold text-gray-800 mb-4 text-center">Голосование за даты</h3>
        <p class="text-gray-600 leading-relaxed text-center">
          Участники выбирают удобное время, вы видите результаты
        </p>
      </div>
      
      <div class="bg-white rounded-2xl p-6 md:p-8 shadow-lg hover:shadow-2xl border border-gray-100 transition-all duration-300 transform hover:-translate-y-2">
        <div class="text-5xl md:text-6xl mb-6 text-center">👥</div>
        <h3 class="text-xl md:text-2xl font-bold text-gray-800 mb-4 text-center">Без регистрации</h3>
        <p class="text-gray-600 leading-relaxed text-center">
          Никаких сложных форм, работает сразу по ссылке
        </p>
      </div>
    </div>
    
    <!-- How It Works Section -->
    <div class="bg-gradient-to-br from-gray-50 to-gray-100 rounded-3xl p-6 md:p-10 lg:p-12 shadow-xl mb-8">
      <h2 class="text-3xl md:text-4xl font-bold text-gray-800 mb-8 md:mb-12 text-center">
        Как это работает
      </h2>
      
      <div class="max-w-3xl mx-auto">
        <ol class="space-y-6 md:space-y-8">
          <li class="flex items-start gap-4 md:gap-6">
            <div class="flex-shrink-0 w-12 h-12 md:w-14 md:h-14 bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-xl flex items-center justify-center text-xl md:text-2xl font-bold shadow-lg">
              1
            </div>
            <div class="pt-2">
              <p class="text-lg md:text-xl font-medium text-gray-800 leading-relaxed">
                Создайте событие с названием и вариантами дат
              </p>
            </div>
          </li>
          
          <li class="flex items-start gap-4 md:gap-6">
            <div class="flex-shrink-0 w-12 h-12 md:w-14 md:h-14 bg-gradient-to-br from-green-500 to-green-600 text-white rounded-xl flex items-center justify-center text-xl md:text-2xl font-bold shadow-lg">
              2
            </div>
            <div class="pt-2">
              <p class="text-lg md:text-xl font-medium text-gray-800 leading-relaxed">
                Отправьте ссылку друзьям или коллегам
              </p>
            </div>
          </li>
          
          <li class="flex items-start gap-4 md:gap-6">
            <div class="flex-shrink-0 w-12 h-12 md:w-14 md:h-14 bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-xl flex items-center justify-center text-xl md:text-2xl font-bold shadow-lg">
              3
            </div>
            <div class="pt-2">
              <p class="text-lg md:text-xl font-medium text-gray-800 leading-relaxed">
                Участники голосуют за удобные даты
              </p>
            </div>
          </li>
          
          <li class="flex items-start gap-4 md:gap-6">
            <div class="flex-shrink-0 w-12 h-12 md:w-14 md:h-14 bg-gradient-to-br from-orange-500 to-orange-600 text-white rounded-xl flex items-center justify-center text-xl md:text-2xl font-bold shadow-lg">
              4
            </div>
            <div class="pt-2">
              <p class="text-lg md:text-xl font-medium text-gray-800 leading-relaxed">
                Вы видите результаты и выбираете лучшую дату
              </p>
            </div>
          </li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script setup>
// Главная страница не требует логики
</script>

<style scoped>
/* Все стили заменены на Tailwind классы */
</style>