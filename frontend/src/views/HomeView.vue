<template>
  <div class="max-w-6xl mx-auto px-4 py-8 md:py-12 lg:py-16">
    <!-- Hero Section -->
    <div class="text-center mb-16 lg:mb-24">
      <h1 class="font-display text-5xl md:text-6xl lg:text-7xl mb-4 md:mb-6 text-gray-900">
        Event Planner
      </h1>
      
      <p class="text-lg md:text-xl lg:text-2xl text-gray-600 mb-8 md:mb-12 max-w-3xl mx-auto px-4">
        Совместный планировщик мероприятий
      </p>
      
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center px-4">
        <router-link
          to="/create"
          class="px-6 py-2.5 bg-gray-900 hover:bg-gray-700 text-white text-sm font-medium rounded-lg transition-colors"
        >
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
    <div class="bg-white rounded-md p-6 md:p-8 border-2 border-gray-300 mb-8">
      <div class="flex items-center justify-between flex-wrap gap-3 mb-6">
        <h2 class="text-xl font-semibold text-gray-900">
          Ваш календарь
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
                class="px-3 py-2 rounded-lg border border-gray-200 text-gray-700 hover:bg-gray-50 transition-colors"
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
                  ? 'border-gray-200 text-gray-800 hover:bg-gray-100'
                  : 'border-gray-100 text-gray-300 bg-gray-50',
                day.isToday ? 'ring-2 ring-gray-400' : '',
                day.isSelected ? 'bg-gray-900 text-white border-gray-900 hover:bg-gray-900' : '',
              ]"
              :disabled="!day.inCurrentMonth"
              @click="selectDate(day.date)"
            >
              <span>{{ day.dayNumber }}</span>
              <span
                v-if="day.eventsCount > 0"
                class="absolute bottom-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 rounded-full"
                :class="day.isSelected ? 'bg-white' : 'bg-gray-500'"
              />
            </button>
          </div>
        </div>

        <div class="bg-white rounded-md p-4 md:p-5 border border-gray-200">
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
          <div v-else class="flex flex-col gap-3">
            <p class="text-sm text-gray-500 bg-gray-50 border border-dashed border-gray-300 rounded-md p-4">
              В этот день событий пока нет
            </p>
            <router-link
              :to="`/create?date=${selectedDate.format('YYYY-MM-DD')}`"
              class="w-full py-2 text-sm font-medium text-center border-2 border-gray-300 rounded-md hover:bg-gray-50 transition-colors text-gray-700"
            >
              Создать событие в этот день
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- User Events Section -->
    <div class="bg-white rounded-md p-6 md:p-8 border-2 border-gray-300 mb-8">
      <div class="flex items-center justify-between flex-wrap gap-3 mb-6">
        <h2 class="text-xl font-semibold text-gray-900">
          Мои события
        </h2>
        <span v-if="authStore.isAuthenticated" class="text-sm md:text-base text-gray-500">
          Всего: {{ userEvents.length }}
        </span>
      </div>

      <div v-if="!authStore.isAuthenticated" class="text-sm text-gray-500 bg-white border border-dashed border-gray-300 rounded-xl p-4">
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
            class="bg-white rounded-md border-2 border-gray-200 p-4 flex items-start justify-between gap-4 hover:bg-gray-50 transition-colors cursor-pointer"
            @click.stop="$router.push(`/event/${event.id}`)"
          >
            <div>
              <p class="font-semibold text-gray-800">{{ event.title }}</p>
              <p class="text-sm text-gray-500 mt-1">
                {{ formatEventDate(event.created_at) }}
              </p>
            </div>

            <button
              class="px-3 py-2 text-sm rounded-lg border border-red-200 text-red-600 hover:bg-red-50 transition-colors disabled:opacity-50 flex-shrink-0"
              :disabled="deletingEventId === event.id"
              @click.stop="deleteUserEvent(event.id)"
            >
              {{ deletingEventId === event.id ? 'Удаление...' : 'Удалить' }}
            </button>
          </li>
        </ul>

        <div v-else class="text-sm text-gray-500 bg-white border border-dashed border-gray-300 rounded-xl p-4">
          У вас пока нет событий
        </div>
      </div>
    </div>

    <!-- How It Works Section -->
    <div class="bg-white rounded-md p-6 md:p-8 border-2 border-gray-300 mb-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-8 text-center">
        Как это работает
      </h2>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="border-2 border-gray-200 rounded-md p-5">
          <!-- <div class="text-4xl font-bold text-gray-200 mb-3 leading-none">01</div> -->
          <p class="text-sm font-semibold text-gray-900 mb-1">Создайте событие</p>
          <p class="text-sm text-gray-500">Укажите название и варианты дат для голосования</p>
        </div>

        <div class="border-2 border-gray-200 rounded-md p-5">
          <!-- <div class="text-4xl font-bold text-gray-200 mb-3 leading-none">02</div> -->
          <p class="text-sm font-semibold text-gray-900 mb-1">Пригласите участников</p>
          <p class="text-sm text-gray-500">Отправьте уникальную ссылку друзьям или коллегам</p>
        </div>

        <div class="border-2 border-gray-200 rounded-md p-5">
          <!-- <div class="text-4xl font-bold text-gray-200 mb-3 leading-none">03</div> -->
          <p class="text-sm font-semibold text-gray-900 mb-1">Голосуйте за дату</p>
          <p class="text-sm text-gray-500">Участники выбирают подходящее время, обсуждают в чате</p>
        </div>

        <div class="border-2 border-gray-200 rounded-md p-5">
          <!-- <div class="text-4xl font-bold text-gray-200 mb-3 leading-none">04</div> -->
          <p class="text-sm font-semibold text-gray-900 mb-1">Планируйте задачи</p>
          <p class="text-sm text-gray-500">Распределяйте задачи между участниками события</p>
        </div>
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
const currentMonth = ref(dayjs().startOf('month'))
const selectedDate = ref(dayjs())

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