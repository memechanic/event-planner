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

      <div class="flex items-center gap-3">
        <h1 class="text-2xl font-semibold text-gray-900">Создать событие</h1>
      </div>
      <p class="text-gray-600 mt-2 max-w-3xl">
        Заполните форму и создайте событие для совместного планирования с друзьями или коллегами
      </p>
    </div>

    <!-- Форма -->
    <div class="bg-white rounded-xl p-6 md:p-8 border border-gray-200">
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
            class="w-full px-3 py-2.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 transition-colors placeholder-gray-400"
          />
        </div>

        <!-- Описание -->
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700 mb-1.5">
            Описание
          </label>
          <textarea
            id="description"
            v-model="description"
            rows="3"
            placeholder="Детали события, адрес, что взять с собой..."
            :disabled="loading"
            class="w-full px-3 py-2.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 transition-colors resize-none placeholder-gray-400"
          ></textarea>
        </div>

        <!-- Даты для голосования -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="block text-sm font-medium text-gray-700">
              Даты для голосования <span class="text-red-500">*</span>
            </label>
            <button
              type="button"
              @click="addDate"
              :disabled="loading"
              class="text-sm text-gray-700 hover:text-gray-900 font-semibold transition-colors disabled:opacity-50"
            >
              Добавить дату
            </button>
          </div>

          <p class="text-sm text-gray-500 mb-4">
            Укажите несколько вариантов, участники выберут подходящие
          </p>

          <div class="space-y-3">
            <div
              v-for="(_, index) in dates"
              :key="index"
              class="flex items-center gap-3"
            >
              <input
                v-model="dates[index]"
                type="datetime-local"
                :min="getMinDate()"
                required
                :disabled="loading"
                class="flex-1 px-3 py-2.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 transition-colors"
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
              class="flex-1 py-2.5 px-6 bg-gray-900 hover:bg-gray-700 text-white text-sm font-medium rounded-lg transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
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
                Создать событие
              </span>
            </button>

            <router-link
              to="/"
              class="py-2.5 px-6 border border-gray-200 text-gray-600 hover:text-gray-900 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors text-center"
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
        <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg">
          <p class="text-sm text-gray-600">
            После создания вы получите уникальную ссылку — отправьте её участникам для приглашения.
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEventStore } from '@/stores/event'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
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
const getInitialDate = () => {
  if (route.query.date) {
    const d = new Date(route.query.date)
    d.setHours(18, 0, 0, 0)
    if (!isNaN(d.getTime())) return d.toISOString().slice(0, 16)
  }
  return getTomorrowDate()
}
const dates = ref([getInitialDate()])

// Состояние
const loading = computed(() => eventStore.loading)
const error = computed(() => eventStore.error)

// Валидация формы
const isFormValid = computed(() => {
  return title.value.trim().length > 0 &&
         dates.value.length > 0 &&
         dates.value.every(date => date && date.trim() !== '')
})

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
  if (!authStore.userId) {
    alert('Сначала войдите в аккаунт, чтобы создать событие')
    router.push('/login')
    return
  }

  const processedDates = dates.value.map(dateStr => {
    const dateObj = new Date(dateStr)
    return isNaN(dateObj.getTime()) ? null : dateObj.toISOString()
  }).filter(Boolean)

  if (processedDates.length === 0) {
    alert('Нет валидных дат для события')
    return
  }

  const eventData = {
    title: title.value.trim(),
    event_user: authStore.userId,
    description: description.value.trim(),
    dates: processedDates,
  }

  try {
    const createdEvent = await eventStore.createEvent(eventData)
    router.push(`/event/${createdEvent.id}`)
  } catch (err) {
    console.error('Ошибка при создании:', err)
  }
}
</script>

<style scoped>
</style>
