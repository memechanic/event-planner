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

      </div>
    </div>
    
    <!-- Features Section -->
    <!-- <div class="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 mb-16 lg:mb-24 px-4">
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
    </div> -->
    
    <!-- Calendar Section -->
    <div class="bg-white rounded-3xl p-6 md:p-8 shadow-xl border border-gray-100 mb-10">
      <div class="flex items-center justify-between flex-wrap gap-3 mb-6">
        <h2 class="text-2xl md:text-3xl font-bold text-gray-800">
          Интерактивный календарь
        </h2>
        <span class="text-sm md:text-base text-gray-500">
          Выберите день и посмотрите события
        </span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2">
          <div class="flex items-center justify-between mb-4 gap-2 flex-wrap">
            <div class="flex items-center gap-2">
              <button
                class="px-3 py-2 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                @click="goToPreviousMonth"
              >
                ← Назад
              </button>
              <button
                class="px-3 py-2 rounded-lg border border-blue-200 text-blue-700 hover:bg-blue-50 transition-colors"
                @click="goToToday"
              >
                Сегодня
              </button>
            </div>
            <h3 class="text-lg md:text-xl font-semibold text-gray-800">
              {{ currentMonthLabel }}
            </h3>
            <button
              class="px-3 py-2 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
              @click="goToNextMonth"
            >
              Вперёд →
            </button>
          </div>

          <div class="grid grid-cols-7 gap-2 mb-2">
            <div
              v-for="dayName in weekDays"
              :key="dayName"
              class="text-center text-xs md:text-sm text-gray-500 font-medium py-1"
            >
              {{ dayName }}
            </div>
          </div>

          <div class="grid grid-cols-7 gap-2">
            <button
              v-for="day in calendarDays"
              :key="day.key"
              class="aspect-square rounded-xl border text-sm md:text-base transition-all duration-150 relative"
              :class="[
                day.inCurrentMonth
                  ? 'border-gray-200 text-gray-800 hover:bg-blue-50'
                  : 'border-gray-100 text-gray-300 bg-gray-50',
                day.isToday ? 'ring-2 ring-blue-300' : '',
                day.isSelected ? 'bg-blue-600 text-white border-blue-600 hover:bg-blue-600' : '',
              ]"
              :disabled="!day.inCurrentMonth"
              @click="selectDate(day.date)"
            >
              <span>{{ day.dayNumber }}</span>
              <span
                v-if="day.eventsCount > 0"
                class="absolute bottom-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 rounded-full"
                :class="day.isSelected ? 'bg-white' : 'bg-blue-500'"
              />
            </button>
          </div>
        </div>

        <div class="bg-gray-50 rounded-2xl p-4 md:p-5 border border-gray-100">
          <h4 class="text-lg font-semibold text-gray-800 mb-2">
            {{ selectedDateLabel }}
          </h4>
          <p class="text-sm text-gray-500 mb-4">
            События на выбранную дату
          </p>

          <ul v-if="selectedDateEvents.length > 0" class="space-y-3">
            <li
              v-for="event in selectedDateEvents"
              :key="event.id"
              class="bg-white rounded-xl border border-gray-200 p-3"
            >
              <p class="font-medium text-gray-800">{{ event.title }}</p>
              <p class="text-sm text-gray-500">{{ event.time }}</p>
            </li>
          </ul>
          <div v-else class="text-sm text-gray-500 bg-white border border-dashed border-gray-300 rounded-xl p-4">
            В этот день событий пока нет
          </div>
        </div>
      </div>
    </div>

    <!-- User Events Section -->
    <div class="bg-white rounded-3xl p-6 md:p-8 shadow-xl border border-gray-100 mb-10">
      <div class="flex items-center justify-between flex-wrap gap-3 mb-6">
        <h2 class="text-2xl md:text-3xl font-bold text-gray-800">
          Мои события
        </h2>
        <span v-if="authStore.isAuthenticated" class="text-sm md:text-base text-gray-500">
          Всего: {{ userEvents.length }}
        </span>
      </div>

      <div v-if="!authStore.isAuthenticated" class="text-sm text-gray-500 bg-gray-50 border border-dashed border-gray-300 rounded-xl p-4">
        Войдите в аккаунт, чтобы видеть и удалять свои события
      </div>

      <div v-else>
        <p v-if="eventsError" class="text-sm text-red-600 mb-4">
          {{ eventsError }}
        </p>

        <p v-if="eventsLoading" class="text-sm text-gray-500">
          Загрузка списка событий...
        </p>

        <ul v-else-if="userEvents.length > 0" class="space-y-3">
          <li
            v-for="event in userEvents"
            :key="event.id"
            class="bg-gray-50 rounded-xl border border-gray-200 p-4 flex items-start justify-between gap-4"
          >
            <div>
              <p class="font-semibold text-gray-800">{{ event.title }}</p>
              <p class="text-sm text-gray-500 mt-1">
                {{ formatEventDate(event.created_at) }}
              </p>
              <router-link
                :to="`/event/${event.id}`"
                class="inline-block text-sm text-blue-600 hover:text-blue-800 mt-2"
              >
                Открыть событие
              </router-link>
            </div>

            <button
              class="px-3 py-2 text-sm rounded-lg border border-red-200 text-red-600 hover:bg-red-50 transition-colors disabled:opacity-50"
              :disabled="deletingEventId === event.id"
              @click="deleteUserEvent(event.id)"
            >
              {{ deletingEventId === event.id ? 'Удаление...' : 'Удалить' }}
            </button>
          </li>
        </ul>

        <div v-else class="text-sm text-gray-500 bg-gray-50 border border-dashed border-gray-300 rounded-xl p-4">
          У вас пока нет событий
        </div>
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
import { computed, onMounted, ref, watch } from 'vue'
import dayjs from 'dayjs'
import 'dayjs/locale/ru'
import { api } from '@/api'
import { useAuthStore } from '@/stores/auth'

dayjs.locale('ru')

const authStore = useAuthStore()

const weekDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

const calendarEvents = ref([])
const userEvents = ref([])
const eventsLoading = ref(false)
const eventsError = ref('')
const deletingEventId = ref(null)
const currentMonth = ref(dayjs('2026-04-01'))
const selectedDate = ref(dayjs('2026-04-26'))

const currentMonthLabel = computed(() => currentMonth.value.format('MMMM YYYY'))
const selectedDateLabel = computed(() => selectedDate.value.format('D MMMM YYYY'))

const selectedDateEvents = computed(() => {
  const selectedKey = selectedDate.value.format('YYYY-MM-DD')
  return calendarEvents.value.filter((event) => event.date === selectedKey)
})

const calendarDays = computed(() => {
  const startOfMonth = currentMonth.value.startOf('month')
  const startWeekday = (startOfMonth.day() + 6) % 7
  const startGridDate = startOfMonth.subtract(startWeekday, 'day')

  return Array.from({ length: 42 }, (_, index) => {
    const date = startGridDate.add(index, 'day')
    const dateKey = date.format('YYYY-MM-DD')
    return {
      key: dateKey,
      date,
      dayNumber: date.date(),
      inCurrentMonth: date.month() === currentMonth.value.month(),
      isToday: date.isSame(dayjs(), 'day'),
      isSelected: date.isSame(selectedDate.value, 'day'),
      eventsCount: calendarEvents.value.filter((event) => event.date === dateKey).length,
    }
  })
})

const goToPreviousMonth = () => {
  currentMonth.value = currentMonth.value.subtract(1, 'month')
}

const goToNextMonth = () => {
  currentMonth.value = currentMonth.value.add(1, 'month')
}

const selectDate = (date) => {
  selectedDate.value = date
}

const goToToday = () => {
  const today = dayjs()
  selectedDate.value = today
  currentMonth.value = today.startOf('month')
}

const formatTimeRange = (dateString) => {
  const date = dayjs(dateString)
  const start = date.format('HH:mm')
  const end = date.add(1, 'hour').format('HH:mm')
  return `${start} - ${end}`
}

const formatEventDate = (dateString) => dayjs(dateString).format('D MMMM YYYY, HH:mm')

const buildEventsFromUserEvents = (events) => {
  return events.flatMap((event) =>
    (event.date_options || []).map((option) => ({
      id: `${event.id}-${option.id}`,
      date: dayjs(option.date).format('YYYY-MM-DD'),
      title: event.title,
      time: formatTimeRange(option.date),
    })),
  )
}

const loadUserCalendarEvents = async () => {
  eventsError.value = ''

  if (!authStore.userId) {
    userEvents.value = []
    calendarEvents.value = []
    return
  }

  eventsLoading.value = true
  try {
    const response = await api.get(`/users/${authStore.userId}/events/`)
    const events = response.data || []
    userEvents.value = events
    const mappedEvents = buildEventsFromUserEvents(events)

    if (mappedEvents.length > 0) {
      calendarEvents.value = mappedEvents
      selectedDate.value = dayjs(mappedEvents[0].date)
      currentMonth.value = dayjs(mappedEvents[0].date).startOf('month')
    } else {
      calendarEvents.value = []
      goToToday()
    }
  } catch (error) {
    eventsError.value = 'Не удалось загрузить события пользователя'
    console.warn('Не удалось загрузить события пользователя')
  } finally {
    eventsLoading.value = false
  }
}

const deleteUserEvent = async (eventId) => {
  const confirmed = window.confirm('Удалить это событие?')
  if (!confirmed) {
    return
  }

  deletingEventId.value = eventId
  try {
    await api.delete(`/events/${eventId}/delete/`)
    await loadUserCalendarEvents()
  } catch (error) {
    eventsError.value = 'Не удалось удалить событие'
    console.error('Ошибка удаления события', error)
  } finally {
    deletingEventId.value = null
  }
}

onMounted(() => {
  loadUserCalendarEvents()
})

watch(() => authStore.userId, () => {
  loadUserCalendarEvents()
})
</script>

<style scoped>
/* Все стили заменены на Tailwind классы */
</style>