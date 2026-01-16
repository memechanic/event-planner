<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <router-link 
        to="/" 
        class="inline-flex items-center text-gray-600 hover:text-blue-600 mb-4 group transition-colors"
      >
        <svg 
          class="w-5 h-5 mr-2 transform group-hover:-translate-x-0.5 transition-transform" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
        На главную
      </router-link>
      
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center shadow-sm">
          <span class="text-white text-lg">📅</span>
        </div>
        <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
          Создать новое событие
        </h1>
      </div>
      <p class="text-gray-600 mt-2 max-w-3xl">
        Заполните форму и создайте событие для совместного планирования с друзьями или коллегами
      </p>
    </div>
    
    <!-- Форма -->
    <div class="bg-white rounded-2xl shadow-xl p-6 md:p-8 border border-gray-100">
      <form @submit.prevent="handleSubmit" class="space-y-8">
        <!-- Название -->
        <div>
          <label for="title" class="block text-sm font-semibold text-gray-800 mb-2">
            Название события <span class="text-red-500">*</span>
          </label>
          <input
            id="title"
            v-model="title"
            type="text"
            placeholder="Например: Встреча команды, День рождения, Встреча с клиентом"
            required
            :disabled="loading"
            class="w-full px-4 py-3.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 placeholder-gray-400"
          />
        </div>
        
        <!-- Описание -->
        <div>
          <label for="description" class="block text-sm font-semibold text-gray-800 mb-2">
            Описание
          </label>
          <textarea
            id="description"
            v-model="description"
            rows="3"
            placeholder="Детали события, адрес, что взять с собой..."
            :disabled="loading"
            class="w-full px-4 py-3.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 resize-none placeholder-gray-400"
          ></textarea>
        </div>
        
        <!-- Даты для голосования -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="block text-sm font-semibold text-gray-800">
              Даты для голосования <span class="text-red-500">*</span>
            </label>
            <button
              type="button"
              @click="addDate"
              :disabled="loading"
              class="text-sm text-blue-600 hover:text-blue-800 font-semibold transition-colors disabled:opacity-50"
            >
              + Добавить дату
            </button>
          </div>
          
          <p class="text-sm text-gray-500 mb-4">
            Укажите несколько вариантов, участники выберут подходящие
          </p>
          
          <div class="space-y-3">
            <div
              v-for="(date, index) in dates"
              :key="index"
              class="flex items-center gap-3"
            >
              <input
                v-model="dates[index]"
                type="datetime-local"
                :min="getMinDate()"
                required
                :disabled="loading"
                class="flex-1 px-4 py-3.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200"
              />
              <button
                type="button"
                @click="removeDate(index)"
                :disabled="dates.length <= 1 || loading"
                class="p-3 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all duration-200 disabled:opacity-30 disabled:cursor-not-allowed"
                title="Удалить дату"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Кнопки -->
        <div class="pt-4">
          <div class="flex flex-col sm:flex-row gap-4">
            <button
              type="submit"
              :disabled="loading || !isFormValid"
              class="flex-1 py-4 px-6 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow"
            >
              <span v-if="loading" class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Создание...
              </span>
              <span v-else class="flex items-center justify-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                🎉 Создать событие
              </span>
            </button>
            
            <router-link 
              to="/" 
              class="py-4 px-6 border-2 border-gray-200 hover:border-gray-300 text-gray-700 hover:text-gray-900 font-semibold rounded-xl hover:bg-gray-50 transition-all duration-200 text-center"
            >
              Отмена
            </router-link>
          </div>
          
          <!-- Ошибка -->
          <div 
            v-if="error" 
            class="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-start"
          >
            <svg class="w-5 h-5 text-red-500 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span class="text-red-700">{{ error }}</span>
          </div>
        </div>
        
        <!-- Информационный блок -->
        <div class="p-5 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 rounded-xl">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <div>
              <p class="text-blue-800 font-medium mb-1">
                💡 После создания вы получите уникальную ссылку
              </p>
              <p class="text-blue-700 text-sm">
                Отправьте её участникам — голосование работает без регистрации на любом устройстве
              </p>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useEventStore } from '@/stores/event'

const router = useRouter()
const eventStore = useEventStore()

// Данные формы
const title = ref('')
const description = ref('')
const getTomorrowDate = () => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  tomorrow.setHours(18, 0, 0, 0)
  return tomorrow.toISOString().slice(0, 16)
}
const dates = ref([getTomorrowDate()]) // Начинаем с одной даты (завтра)

// Состояние
const loading = computed(() => eventStore.loading)
const error = computed(() => eventStore.error)

// Валидация формы
const isFormValid = computed(() => {
  return title.value.trim().length > 0 &&
         dates.value.length > 0 &&
         dates.value.every(date => date && date.trim() !== '')
})

// Получить минимальную дату (текущее время)
const getMinDate = () => {
  const now = new Date()
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
  return now.toISOString().slice(0, 16)
}

// Добавить новую дату (последняя + 1 день)
const addDate = () => {
  const lastDate = new Date(dates.value[dates.value.length - 1] || getTomorrowDate())
  lastDate.setDate(lastDate.getDate() + 1)
  dates.value.push(lastDate.toISOString().slice(0, 16))
}

// Удалить дату
const removeDate = (index) => {
  if (dates.value.length > 1) {
    dates.value.splice(index, 1)
  }
}

// Обработка отправки формы
const handleSubmit = async () => {
  if (!isFormValid.value) {
    alert('Заполните название и все даты')
    return
  }
  const processedDates = dates.value.map(dateStr => {
    try {
      // input[type="datetime-local"] возвращает строку в формате "YYYY-MM-DDTHH:mm"
      // Нужно добавить временную зону
      const dateObj = new Date(dateStr);
      
      // Проверяем, что дата валидна
      if (isNaN(dateObj.getTime())) {
        console.error('❌ Неверная дата:', dateStr);
        return null;
      }
      
      // Преобразуем в ISO строку (с часовым поясом UTC)
      const isoString = dateObj.toISOString();
      console.log(`✅ Преобразовано: ${dateStr} → ${isoString}`);
      return isoString;
      
    } catch (error) {
      console.error('❌ Ошибка преобразования даты:', dateStr, error);
      return null;
    }
  }).filter(date => date !== null); // Убираем невалидные даты
  
  if (processedDates.length === 0) {
    alert('Нет валидных дат для события');
    return;
  }
  console.log('Отправка данных:', {
    title: title.value,
    description: description.value,
    dates: dates.value
  })

  // Подготавливаем данные для API
  const eventData = {
    title: title.value.trim(),
    description: description.value.trim(),
    dates: dates.value.map(date => {
      // Преобразуем local datetime в ISO строку
      const dateObj = new Date(date)
      return dateObj.toISOString()
    })
  }
  
  try {
    // Используем store для создания
    const createdEvent = await eventStore.createEvent(eventData)
    
    console.log('✅ Событие создано, ID:', createdEvent.id)
    
    // Переходим на страницу события
    router.push(`/event/${createdEvent.id}`)
    
  } catch (err) {
    console.error('❌ Ошибка при создании:', err)
    // Ошибка уже в store.error
  }
}
</script>

<style scoped>
/* Все стили заменены на Tailwind классы */
</style>