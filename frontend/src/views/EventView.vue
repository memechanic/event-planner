<script> import ChatBox from "@/components/ChatBox.vue"; export default { components: { ChatBox } }; </script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-8">

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
        class="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-all"
      >
        На главную
      </router-link>
    </div>

    <!-- Контент -->
    <div v-else-if="event" class="space-y-8">

      <!-- HEADER -->
      <div class="flex flex-col md:flex-row md:items-start md:justify-between">
        <div class="flex-1">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ event.title }}</h1>
          <p class="text-gray-600">{{ event.description || 'Нет описания' }}</p>
          <div class="flex gap-4 text-sm text-gray-500 mt-3">
            <span>{{ dates.length }} вариантов дат</span>
            <span>{{ uniqueParticipants.length }} участников</span>
            <span>{{ eventStore.votes?.length || 0 }} голосов</span>
          </div>
        </div>

        <button class="mt-4 md:mt-0 px-5 py-2 bg-indigo-600 text-white rounded-xl shadow hover:bg-indigo-700">
          Пригласить
        </button>
      </div>

      <!-- GRID: Vote + Chat -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- VOTE SECTION -->
        <div class="lg:col-span-2 bg-white rounded-xl shadow p-6 border">
          <div class="flex items-center mb-4">
            <span class="text-2xl mr-2">📋</span>
            <h2 class="text-xl font-semibold text-gray-800">Голосование за даты</h2>
          </div>

          <div class="space-y-4">
            <div 
              v-for="date in dates"
              :key="date"
              @click="selectDate(date)"
              class="border rounded-xl p-4 cursor-pointer hover:border-green-400 transition"
              :class="selectedDate === date ? 'bg-green-50 border-green-500' : 'border-gray-200'"
            >
              <div class="flex justify-between">
                <div>
                  <div class="font-medium text-gray-800">{{ formatDateTime(date) }}</div>
                  <div class="text-sm text-gray-600">
                    {{ (votesByDate[date] || []).length }} голосов
                  </div>
                </div>
                <div v-if="selectedDate === date" class="text-green-600">
                  ✔
                </div>
              </div>
            </div>
          </div>

          <button
            class="mt-6 w-full py-3 bg-green-600 hover:bg-green-700 text-white rounded-xl disabled:bg-gray-300"
            :disabled="!selectedDate || voting"
            @click="submitVote"
          >
            {{ voting ? 'Голосую...' : 'Проголосовать' }}
          </button>
        </div>

        <!-- CHAT -->
        <div class="bg-white rounded-xl shadow p-6 border flex flex-col">
          <div class="flex items-center mb-3">
            <span class="text-xl mr-2">💬</span>
            <h2 class="text-lg font-semibold text-gray-800">Чат события</h2>
          </div>

          <ChatBox />
        </div>

      </div>

      <!-- PARTICIPANTS -->
      <div class="bg-white rounded-xl shadow p-6 border">
        <div class="flex items-center mb-3">
          <span class="text-xl mr-2">👥</span>
          <h2 class="text-lg font-semibold text-gray-800">Участники</h2>
        </div>

        <div class="flex flex-wrap gap-3 mt-3">
          <div v-for="p in uniqueParticipants" :key="p" class="px-4 py-2 border rounded-xl bg-gray-50 text-gray-800">
            {{ p }}
          </div>
        </div>
      </div>

      <!-- LINK -->
      <div class="bg-white rounded-xl shadow p-6 border">
        <h2 class="text-lg font-semibold mb-3 flex items-center">
          <span class="mr-2 text-xl">🔗</span> Ссылка для приглашения
        </h2>

        <div class="flex flex-col sm:flex-row gap-3">
          <input :value="eventUrl" readonly class="flex-1 p-3 rounded-xl border bg-gray-50" />
          <button @click="copyLink" class="px-5 py-3 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700">
            {{ copied ? 'Скопировано!' : 'Копировать' }}
          </button>
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