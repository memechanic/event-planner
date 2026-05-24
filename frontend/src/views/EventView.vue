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
            <span>{{ dateOptions.length }} вариантов дат</span>
            <span>{{ uniqueParticipants.length }} участников</span>
          </div>
        </div>

        <button
          @click="scrollToLink"
          class="mt-4 md:mt-0 px-5 py-2 bg-indigo-600 text-white rounded-xl shadow hover:bg-indigo-700"
        >
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
              v-for="option in dateOptions"
              :key="option.id"
              @click="selectOption(option)"
              class="border rounded-xl p-4 cursor-pointer hover:border-green-400 transition"
              :class="selectedOptionId === option.id ? 'bg-green-50 border-green-500' : 'border-gray-200'"
            >
              <div class="flex justify-between items-center">
                <div>
                  <div class="font-medium text-gray-800">{{ formatDateTime(option.date) }}</div>
                  <div class="text-sm text-gray-500 mt-1">{{ option.vote_count ?? 0 }} голосов</div>
                </div>
                <div v-if="selectedOptionId === option.id" class="text-green-600 text-xl">✔</div>
              </div>
            </div>
          </div>

          <div v-if="voteError" class="mt-3 text-sm text-red-600">{{ voteError }}</div>
          <div v-if="voteSuccess" class="mt-3 text-sm text-green-600">Голос принят!</div>

          <button
            class="mt-6 w-full py-3 bg-green-600 hover:bg-green-700 text-white rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition"
            :disabled="!selectedOptionId || voting"
            @click="submitVote"
          >
            {{ voting ? 'Голосую...' : 'Проголосовать' }}
          </button>
        </div>

        <!-- CHAT (заглушка до реализации) -->
        <div class="bg-white rounded-xl shadow p-6 border flex flex-col">
          <div class="flex items-center mb-3">
            <span class="text-xl mr-2">💬</span>
            <h2 class="text-lg font-semibold text-gray-800">Чат события</h2>
          </div>
          <p class="text-sm text-gray-400 mt-auto text-center">Чат будет доступен в следующей версии</p>
        </div>

      </div>

      <!-- PARTICIPANTS -->
      <div class="bg-white rounded-xl shadow p-6 border">
        <div class="flex items-center mb-3">
          <span class="text-xl mr-2">👥</span>
          <h2 class="text-lg font-semibold text-gray-800">
            Участники
            <span class="ml-2 text-sm font-normal text-gray-400">({{ uniqueParticipants.length }})</span>
          </h2>
        </div>

        <div v-if="uniqueParticipants.length" class="flex flex-wrap gap-3 mt-3">
          <div
            v-for="name in uniqueParticipants"
            :key="name"
            class="px-4 py-2 border rounded-xl bg-gray-50 text-gray-800"
          >
            {{ name }}
          </div>
        </div>
        <p v-else class="text-sm text-gray-400 mt-2">Пока нет участников. Поделитесь ссылкой!</p>
      </div>

      <!-- INVITE LINK -->
      <div ref="linkSection" class="bg-white rounded-xl shadow p-6 border">
        <h2 class="text-lg font-semibold mb-3 flex items-center">
          <span class="mr-2 text-xl">🔗</span> Ссылка для приглашения
        </h2>

        <div class="flex flex-col sm:flex-row gap-3">
          <input :value="eventUrl" readonly class="flex-1 p-3 rounded-xl border bg-gray-50 text-sm" />
          <button @click="copyLink" class="px-5 py-3 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 transition whitespace-nowrap">
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

const selectedOptionId = ref(null)
const voting = ref(false)
const voteError = ref('')
const voteSuccess = ref(false)
const copied = ref(false)
const linkSection = ref(null)

const event = computed(() => eventStore.currentEvent)
const loading = computed(() => eventStore.loading)
const error = computed(() => eventStore.error)
const uniqueParticipants = computed(() => eventStore.uniqueParticipants)

const dateOptions = computed(() => event.value?.date_options ?? [])

const eventUrl = computed(() =>
  event.value?.id ? `${window.location.origin}/event/${event.value.id}` : ''
)

onMounted(() => loadEvent())
watch(() => route.params.id, () => loadEvent())

const loadEvent = async () => {
  if (!route.params.id) return
  selectedOptionId.value = null
  await eventStore.getEvent(route.params.id)
  if (dateOptions.value.length > 0) {
    selectedOptionId.value = dateOptions.value[0].id
  }
}

const selectOption = (option) => {
  selectedOptionId.value = option.id
}

const submitVote = async () => {
  if (!selectedOptionId.value || !event.value?.id) return
  voting.value = true
  voteError.value = ''
  voteSuccess.value = false
  try {
    await eventStore.voteForEvent(event.value.id, selectedOptionId.value)
    voteSuccess.value = true
    setTimeout(() => { voteSuccess.value = false }, 3000)
  } catch (err) {
    voteError.value = err.message || 'Ошибка голосования'
  } finally {
    voting.value = false
  }
}

const scrollToLink = () => {
  linkSection.value?.scrollIntoView({ behavior: 'smooth' })
}

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(eventUrl.value)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch {
    // fallback
  }
}

const formatDateTime = (dateString) =>
  new Date(dateString).toLocaleString('ru-RU', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
</script>