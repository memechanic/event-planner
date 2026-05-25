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
      <router-link to="/" class="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-all">
        На главную
      </router-link>
    </div>

    <!-- Контент -->
    <div v-else-if="event" class="space-y-8">

      <!-- HEADER -->
      <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
        <div class="flex-1">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ event.title }}</h1>
          <p class="text-gray-600">{{ event.description || 'Нет описания' }}</p>
          <div class="flex gap-4 text-sm text-gray-500 mt-3">
            <span>{{ dateOptions.length }} вариантов дат</span>
            <span>{{ uniqueParticipants.length }} участников</span>
          </div>
        </div>

        <div class="flex gap-2 flex-wrap">
          <span
            v-if="isMember || isCreator"
            class="inline-flex items-center gap-1 px-4 py-2 bg-green-100 text-green-700 rounded-xl font-medium text-sm"
          >
            Вы участник
          </span>
          <button
            v-else-if="!isCreator"
            @click="joinEvent"
            :disabled="joining"
            class="px-5 py-2 bg-green-600 text-white rounded-xl shadow hover:bg-green-700 disabled:opacity-50 transition"
          >
            {{ joining ? 'Подождите...' : 'Присоединиться' }}
          </button>
          <button
            @click="scrollToLink"
            class="px-5 py-2 bg-indigo-600 text-white rounded-xl shadow hover:bg-indigo-700 transition"
          >
            Пригласить
          </button>
        </div>
      </div>

      <!-- Ошибка вступления -->
      <div v-if="joinError" class="bg-red-50 text-red-600 px-4 py-3 rounded-xl text-sm">
        {{ joinError }}
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
              @click="(isMember || isCreator) && selectOption(option)"
              class="border rounded-xl p-4 transition"
              :class="[
                selectedOptionId === option.id ? 'bg-green-50 border-green-500' : 'border-gray-200',
                (isMember || isCreator) ? 'cursor-pointer hover:border-green-400' : 'opacity-60 cursor-not-allowed'
              ]"
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
            v-if="isMember || isCreator"
            class="mt-6 w-full py-3 bg-green-600 hover:bg-green-700 text-white rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition"
            :disabled="!selectedOptionId || voting"
            @click="submitVote"
          >
            {{ voting ? 'Голосую...' : 'Проголосовать' }}
          </button>
          <p v-else class="mt-6 text-center text-sm text-gray-400">
            Присоединитесь к событию, чтобы голосовать
          </p>

          <!-- Предложить дату -->
          <div v-if="isMember || isCreator" class="mt-4 border-t pt-4">
            <button
              v-if="!showProposeForm"
              @click="showProposeForm = true"
              class="w-full py-2 border-2 border-dashed border-gray-300 text-gray-500 rounded-xl hover:border-blue-400 hover:text-blue-600 transition text-sm"
            >
              + Предложить свою дату
            </button>
            <div v-else class="space-y-2">
              <p class="text-sm font-medium text-gray-700">Предложить новую дату:</p>
              <input
                v-model="proposedDate"
                type="datetime-local"
                class="w-full p-3 border rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <div v-if="proposeError" class="text-sm text-red-600">{{ proposeError }}</div>
              <div class="flex gap-2">
                <button
                  @click="submitPropose"
                  :disabled="!proposedDate || proposing"
                  class="flex-1 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-sm disabled:opacity-50 transition"
                >
                  {{ proposing ? 'Отправляю...' : 'Предложить' }}
                </button>
                <button
                  @click="showProposeForm = false; proposedDate = ''; proposeError = ''"
                  class="px-4 py-2 border rounded-xl text-sm text-gray-600 hover:bg-gray-50 transition"
                >
                  Отмена
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- CHAT -->
        <div class="bg-white rounded-xl shadow p-6 border flex flex-col" style="height: 480px;">
          <div class="flex items-center mb-3">
            <span class="text-xl mr-2">💬</span>
            <h2 class="text-lg font-semibold text-gray-800">Чат события</h2>
          </div>

          <div ref="chatContainer" class="flex-1 overflow-y-auto space-y-3 pr-1">
            <div v-if="messages.length === 0" class="text-sm text-gray-400 text-center pt-6">
              Сообщений пока нет
            </div>
            <div v-for="msg in messages" :key="msg.id">
              <span class="font-medium text-gray-800 text-sm">{{ msg.sender_username || 'Аноним' }}</span>
              <span class="text-xs text-gray-400 ml-2">{{ formatTime(msg.created_at) }}</span>
              <p class="text-sm text-gray-700 mt-0.5 break-words">{{ msg.text }}</p>
            </div>
          </div>

          <div v-if="canChat" class="border-t pt-3 mt-3">
            <div class="flex gap-2">
              <input
                v-model="chatText"
                @keydown.enter.prevent="sendMessage"
                type="text"
                placeholder="Написать сообщение..."
                class="flex-1 px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                :disabled="chatSending"
              />
              <button
                @click="sendMessage"
                :disabled="!chatText.trim() || chatSending"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 disabled:opacity-50 transition"
              >
                {{ chatSending ? '...' : '→' }}
              </button>
            </div>
            <p v-if="chatError" class="text-xs text-red-500 mt-1">{{ chatError }}</p>
          </div>
          <p v-else class="text-xs text-gray-400 text-center mt-3 border-t pt-3">
            {{ authStore.isAuthenticated ? 'Присоединитесь, чтобы написать' : 'Войдите, чтобы написать' }}
          </p>
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
          <button
            @click="copyLink"
            class="px-5 py-3 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 transition whitespace-nowrap"
          >
            {{ copied ? 'Скопировано!' : 'Копировать' }}
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEventStore } from '@/stores/event'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const eventStore = useEventStore()
const authStore = useAuthStore()

const selectedOptionId = ref(null)
const voting = ref(false)
const voteError = ref('')
const voteSuccess = ref(false)
const copied = ref(false)
const linkSection = ref(null)
const showProposeForm = ref(false)
const proposedDate = ref('')
const proposing = ref(false)
const proposeError = ref('')
const joining = ref(false)
const joinError = ref('')

const event = computed(() => eventStore.currentEvent)
const loading = computed(() => eventStore.loading)
const error = computed(() => eventStore.error)
const uniqueParticipants = computed(() => eventStore.uniqueParticipants)
const dateOptions = computed(() => event.value?.date_options ?? [])
const isMember = computed(() => eventStore.isMember(authStore.userId))
const isCreator = computed(() => !!event.value?.event_user && event.value.event_user === authStore.userId)

const eventUrl = computed(() =>
  event.value?.id ? `${window.location.origin}/event/${event.value.id}` : ''
)

// ── Chat ─────────────────────────────────────────────────────────────────────
const messages = ref([])
const chatText = ref('')
const chatSending = ref(false)
const chatError = ref('')
const chatContainer = ref(null)
let pollInterval = null

const canChat = computed(() => isMember.value || isCreator.value)

const scrollChatToBottom = async () => {
  await nextTick()
  if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight
}

const loadMessages = async () => {
  if (!route.params.id) return
  try {
    const res = await api.get(`/events/${route.params.id}/messages/`)
    messages.value = res.data
    scrollChatToBottom()
  } catch {}
}

const sendMessage = async () => {
  if (!chatText.value.trim() || !event.value?.id) return
  chatSending.value = true
  chatError.value = ''
  try {
    await api.post(`/events/${event.value.id}/messages/`, { text: chatText.value.trim() })
    chatText.value = ''
    await loadMessages()
  } catch (err) {
    chatError.value = err.message || 'Ошибка отправки'
  } finally {
    chatSending.value = false
  }
}

const startPolling = () => {
  stopPolling()
  loadMessages()
  pollInterval = setInterval(loadMessages, 3000)
}

const stopPolling = () => {
  if (pollInterval) { clearInterval(pollInterval); pollInterval = null }
}

const formatTime = (dateString) =>
  new Date(dateString).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })

// ─────────────────────────────────────────────────────────────────────────────

onMounted(() => { loadEvent(); startPolling() })
onUnmounted(() => stopPolling())
watch(() => route.params.id, () => { loadEvent(); startPolling() })

const loadEvent = async () => {
  if (!route.params.id) return
  selectedOptionId.value = null
  await eventStore.getEvent(route.params.id)
  if (dateOptions.value.length > 0) {
    selectedOptionId.value = dateOptions.value[0].id
  }
}

const joinEvent = async () => {
  if (!event.value?.id) return
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: route.fullPath } })
    return
  }
  joining.value = true
  joinError.value = ''
  try {
    await eventStore.joinEvent(event.value.id)
  } catch (err) {
    joinError.value = err.message || 'Ошибка при вступлении'
  } finally {
    joining.value = false
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

const submitPropose = async () => {
  if (!proposedDate.value || !event.value?.id) return
  proposing.value = true
  proposeError.value = ''
  try {
    await eventStore.proposeDate(event.value.id, new Date(proposedDate.value).toISOString())
    showProposeForm.value = false
    proposedDate.value = ''
  } catch (err) {
    proposeError.value = err.message || 'Ошибка при добавлении даты'
  } finally {
    proposing.value = false
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