<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- Загрузка -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20">
      <div class="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4"></div>
      <p class="text-lg font-medium text-gray-700">Загрузка события...</p>
    </div>
    
    <!-- Ошибка -->
    <div v-else-if="error && (!event || !event.id)" class="text-center py-20">
      <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
      </div>
      <h2 class="text-2xl font-bold text-gray-800 mb-2">Ошибка загрузки</h2>
      <p class="text-gray-600 mb-8">{{ error }}</p>
      <router-link 
        to="/" 
        class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold rounded-xl hover:shadow-lg transition-all duration-200"
      >
        На главную
      </router-link>
    </div>
    
    <!-- Контент события -->
    <div v-else-if="event" class="space-y-8">
      <!-- Заголовок -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 border border-gray-100">
        <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-6">
          <div class="flex-1">
            <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent mb-3">
              {{ event.title }}
            </h1>
            <div class="flex flex-wrap items-center gap-4 mb-4">
              <span class="inline-flex items-center px-3 py-1.5 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                Создано: {{ formatDate(event.created_at) }}
              </span>
              <span class="inline-flex items-center px-3 py-1.5 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">
                <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-7.5a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zM6.75 7.5a2.25 2.25 0 100 4.5 2.25 2.25 0 000-4.5z"/>
                </svg>
                Участники: {{ uniqueParticipants.length }}
              </span>
            </div>
            <div class="bg-gray-50 rounded-xl p-5 border border-gray-200">
              <p class="text-gray-700 leading-relaxed">
                {{ event.description || 'Нет описания' }}
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Даты для голосования -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 border border-gray-100">
        <div class="flex items-center mb-6">
          <div class="w-10 h-10 bg-gradient-to-br from-green-500 to-green-600 rounded-lg flex items-center justify-center mr-3 shadow-sm">
            <span class="text-white text-lg">📋</span>
          </div>
          <h2 class="text-2xl font-bold text-gray-800">Варианты дат</h2>
        </div>
        
        <div class="space-y-4">
          <div 
            v-for="date in dates" 
            :key="date" 
            class="date-card"
            :class="[
              'bg-white border-2 rounded-xl p-5 cursor-pointer transition-all duration-200 hover:shadow-md',
              selectedDate === date 
                ? 'border-green-500 bg-green-50' 
                : 'border-gray-200 hover:border-green-300'
            ]"
            @click="selectDate(date)"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="text-lg font-semibold text-gray-800 mb-2">
                  {{ formatDateTime(date) }}
                </div>
                <div class="flex items-center flex-wrap gap-3">
                  <span class="inline-flex items-center px-3 py-1.5 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                    👍 {{ (votesByDate[date] || []).length }} голосов
                  </span>
                  <span v-if="votesByDate[date] && votesByDate[date].length > 0" class="text-sm text-gray-600">
                    {{ votesByDate[date].join(', ') }}
                  </span>
                </div>
              </div>
              <div v-if="selectedDate === date" class="text-green-600 ml-4">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-8 pt-6 border-t border-gray-100">
          <button 
            @click="submitVote" 
            :disabled="!selectedDate || voting"
            class="w-full py-4 px-6 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow"
          >
            <span v-if="voting" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Голосую...
            </span>
            <span v-else class="flex items-center justify-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              Проголосовать
            </span>
          </button>
        </div>
      </div>
      
      <!-- Участники -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 border border-gray-100">
        <div class="flex items-center mb-6">
          <div class="w-10 h-10 bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg flex items-center justify-center mr-3 shadow-sm">
            <span class="text-white text-lg">👥</span>
          </div>
          <h2 class="text-2xl font-bold text-gray-800">Участники</h2>
        </div>
        
        <div class="flex flex-wrap gap-3">
          <span
            v-for="participant in uniqueParticipants"
            :key="participant"
            class="inline-flex items-center px-4 py-2.5 bg-gradient-to-r from-gray-50 to-gray-100 border border-gray-200 text-gray-800 rounded-xl text-sm font-medium hover:bg-gray-100 transition-colors"
          >
            <svg class="w-4 h-4 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            {{ participant }}
          </span>
        </div>
      </div>
      
      <!-- Ссылка для приглашения -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 border border-gray-100">
        <div class="flex items-center mb-6">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center mr-3 shadow-sm">
            <span class="text-white text-lg">🔗</span>
          </div>
          <h2 class="text-2xl font-bold text-gray-800">Ссылка для приглашения</h2>
        </div>
        
        <div class="space-y-4">
          <div class="flex flex-col sm:flex-row gap-3">
            <input 
              :value="eventUrl" 
              readonly 
              class="flex-1 px-4 py-3.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 focus:outline-none"
            />
            <button 
              @click="copyLink" 
              :class="[
                'px-6 py-3.5 font-semibold rounded-xl transition-all duration-200 flex items-center justify-center',
                copied 
                  ? 'bg-green-100 text-green-800 border border-green-200' 
                  : 'bg-gradient-to-r from-blue-600 to-blue-700 text-white hover:shadow-lg'
              ]"
            >
              <span v-if="copied" class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                </svg>
                Скопировано!
              </span>
              <span v-else class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
                Копировать
              </span>
            </button>
          </div>
          <p class="text-sm text-gray-500">
            Отправьте эту ссылку друзьям или коллегам, чтобы они могли проголосовать
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useEventStore } from '@/stores/event'

const route = useRoute()
const eventStore = useEventStore()

// Данные
const selectedDate = ref(null)
const voting = ref(false)
const copied = ref(false)

// Вычисляемые свойства
const event = computed(() => eventStore.currentEvent)
const loading = computed(() => eventStore.loading)
const error = computed(() => eventStore.error)
const votesByDate = computed(() => eventStore.votesByDate || {})
const uniqueParticipants = computed(() => eventStore.uniqueParticipants || [])

const dates = computed(() => {
  return event.value?.date_options?.map(d => d.date) || []
})

// URL события
const eventUrl = computed(() => {
  if (!event.value?.id) return ''
  return `${window.location.origin}/event/${event.value.id}`
})

// Загрузка события
onMounted(() => {
  loadEvent()
})

watch(() => route.params.id, () => {
  loadEvent()
})

const loadEvent = async () => {
  const eventId = route.params.id
  console.log('Загрузка события ID:', eventId)
  
  if (eventId) {
    await eventStore.getEvent(eventId)
    
    // Если это демо или новое событие, выбираем первую дату
    // if (event.value && event.value.dates?.length > 0 && !selectedDate.value) {
    //   selectedDate.value = event.value.dates[0]
    // }
    if (dates.value.length > 0 && !selectedDate.value) {
      selectedDate.value = dates.value[0]
    }
  }
}

// Выбор даты
const selectDate = (date) => {
  selectedDate.value = date
}

// Голосование
const submitVote = async () => {
  if (!selectedDate.value || !event.value?.id) return
  
  voting.value = true
  try {
    await eventStore.voteForEvent(event.value.id, selectedDate.value)
    console.log('✅ Голос принят')
  } catch (err) {
    console.error('Ошибка голосования:', err)
  } finally {
    voting.value = false
  }
}

// Копирование ссылки
const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(eventUrl.value)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Ошибка копирования:', err)
  }
}

// Форматирование дат
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ru-RU')
}

const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString('ru-RU', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
/* Все стили заменены на Tailwind классы */
</style>