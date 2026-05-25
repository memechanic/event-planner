<template>
  <div class="max-w-7xl mx-auto px-4 py-8">

    <!-- Загрузка -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20">
      <div class="w-16 h-16 border-4 border-gray-200 border-t-gray-600 rounded-full animate-spin mb-4"></div>
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
      <router-link to="/" class="inline-flex items-center px-5 py-2.5 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-700 transition-colors">
        На главную
      </router-link>
    </div>

    <!-- Контент -->
    <div v-else-if="event">

      <!-- HEADER -->
      <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-6">
        <div class="flex-1">
          <h1 class="text-2xl font-semibold text-gray-900 mb-1">{{ event.title }}</h1>
          <p class="text-sm text-gray-500">{{ event.description || '' }}</p>
        </div>

        <div class="flex gap-2 flex-wrap items-start">
          <span
            v-if="isOrganizer"
            class="inline-flex items-center px-3 py-1.5 border border-gray-900 text-gray-900 rounded text-sm font-medium"
          >
            Организатор
          </span>
          <span
            v-else-if="isMember"
            class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-gray-600 rounded text-sm"
          >
            Участник
          </span>
          <button
            v-else
            @click="joinEvent"
            :disabled="joining"
            class="px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-700 disabled:opacity-40 transition-colors"
          >
            {{ joining ? 'Подождите...' : 'Присоединиться' }}
          </button>
          <button
            @click="scrollToLink"
            class="px-4 py-2 border border-gray-200 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors"
          >
            Пригласить
          </button>
        </div>
      </div>

      <!-- Ошибка вступления -->
      <div v-if="joinError" class="mb-4 text-sm text-red-600 border border-red-200 bg-red-50 px-4 py-3 rounded-lg">
        {{ joinError }}
      </div>

      <!-- ДВУХКОЛОНОЧНЫЙ МАКЕТ -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">

        <!-- ЛЕВАЯ КОЛОНКА: основной контент -->
        <div class="lg:col-span-2 space-y-6">

          <!-- ГОЛОСОВАНИЕ -->
          <div class="bg-white border-2 border-gray-300 rounded-md p-5">
            <h2 class="text-sm font-semibold text-gray-900 mb-4 uppercase tracking-wide">Голосование за дату</h2>

            <div class="space-y-2">
              <div
                v-for="option in dateOptions"
                :key="option.id"
                @click="isMember && selectOption(option)"
                class="flex items-center justify-between px-4 py-3 border rounded-lg transition-colors"
                :class="[
                  selectedOptionId === option.id ? 'bg-gray-100 border-gray-900' : 'border-gray-200',
                  isMember ? 'cursor-pointer hover:border-gray-400' : 'opacity-50 cursor-not-allowed'
                ]"
              >
                <div>
                  <div class="text-sm font-medium text-gray-800">{{ formatDateTime(option.date) }}</div>
                  <div class="text-xs text-gray-400 mt-0.5">{{ option.vote_count ?? 0 }} голосов</div>
                </div>
                <div v-if="selectedOptionId === option.id" class="text-gray-900 font-bold text-sm">✔</div>
              </div>
            </div>

            <div v-if="voteError" class="mt-3 text-xs text-red-600">{{ voteError }}</div>
            <div v-if="voteSuccess" class="mt-3 text-xs text-gray-500">Голос принят.</div>

            <div v-if="isMember" class="mt-4 flex flex-col gap-2">
              <button
                class="w-full py-2 bg-gray-900 hover:bg-gray-700 text-white text-sm rounded-lg disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                :disabled="!selectedOptionId || voting"
                @click="submitVote"
              >
                {{ voting ? 'Голосую...' : 'Проголосовать' }}
              </button>

              <button
                v-if="!showProposeForm"
                @click="showProposeForm = true"
                class="w-full py-2 border border-dashed border-gray-300 text-gray-400 rounded-lg hover:border-gray-500 hover:text-gray-600 transition-colors text-sm"
              >
                Предложить свою дату
              </button>
              <div v-else class="space-y-2">
                <input
                  v-model="proposedDate"
                  type="datetime-local"
                  class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900"
                />
                <div v-if="proposeError" class="text-xs text-red-600">{{ proposeError }}</div>
                <div class="flex gap-2">
                  <button @click="submitPropose" :disabled="!proposedDate || proposing"
                    class="flex-1 py-2 bg-gray-900 hover:bg-gray-700 text-white rounded-lg text-sm disabled:opacity-40 transition-colors">
                    {{ proposing ? 'Отправляю...' : 'Предложить' }}
                  </button>
                  <button @click="showProposeForm = false; proposedDate = ''; proposeError = ''"
                    class="px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">
                    Отмена
                  </button>
                </div>
              </div>
            </div>
            <p v-else class="mt-4 text-center text-xs text-gray-400">
              Присоединитесь, чтобы голосовать
            </p>
          </div>

          <!-- ЗАДАЧИ -->
          <div class="bg-white border-2 border-gray-300 rounded-md p-5">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-sm font-semibold text-gray-900 uppercase tracking-wide">
                Задачи <span class="font-normal text-gray-400 normal-case tracking-normal">({{ tasks.length }})</span>
              </h2>
              <button v-if="isMember" @click="showAddTaskForm = !showAddTaskForm"
                class="text-xs text-gray-500 hover:text-gray-900 transition-colors">
                + Добавить
              </button>
            </div>

            <div v-if="showAddTaskForm" class="mb-4 p-3 border border-gray-200 rounded-lg space-y-2">
              <input v-model="taskTitle" type="text" placeholder="Название задачи *"
                class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900" />
              <textarea v-model="taskDescription" placeholder="Описание (необязательно)" rows="2"
                class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 resize-none" />
              <div class="flex gap-2">
                <button @click="addTask" :disabled="!taskTitle.trim() || addingTask"
                  class="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm hover:bg-gray-700 disabled:opacity-40 transition-colors">
                  {{ addingTask ? 'Добавление...' : 'Добавить' }}
                </button>
                <button @click="showAddTaskForm = false; taskTitle = ''; taskDescription = ''"
                  class="px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">
                  Отмена
                </button>
              </div>
            </div>

            <div v-if="tasks.length" class="space-y-2">
              <div v-for="task in tasks" :key="task.id"
                class="flex items-start gap-3 px-3 py-2.5 border border-gray-200 rounded-lg"
                :class="task.is_done ? 'bg-gray-50' : 'bg-white'">
                <button v-if="canToggleDone(task)" @click="toggleDone(task)"
                  class="mt-0.5 flex-shrink-0 w-4 h-4 rounded border-2 flex items-center justify-center transition-colors"
                  :class="task.is_done ? 'bg-gray-900 border-gray-900' : 'border-gray-300 hover:border-gray-600'">
                  <span v-if="task.is_done" class="text-white text-xs leading-none">✓</span>
                </button>
                <div v-else class="mt-0.5 flex-shrink-0 w-4 h-4 rounded border-2 flex items-center justify-center"
                  :class="task.is_done ? 'bg-gray-900 border-gray-900' : 'border-gray-200'">
                  <span v-if="task.is_done" class="text-white text-xs leading-none">✓</span>
                </div>

                <div class="flex-1 min-w-0">
                  <p class="text-sm text-gray-800" :class="{ 'line-through text-gray-400': task.is_done }">{{ task.title }}</p>
                  <p v-if="task.description" class="text-xs text-gray-400 mt-0.5">{{ task.description }}</p>
                  <div class="mt-1 flex items-center gap-2 flex-wrap">
                    <span v-if="task.assigned_to_username" class="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">{{ task.assigned_to_username }}</span>
                    <button v-else-if="canSelfAssign(task)" @click="selfAssign(task.id)"
                      class="text-xs text-gray-500 hover:text-gray-900 underline underline-offset-2">Взять задачу</button>
                    <span v-else class="text-xs text-gray-300">Не назначено</span>
                    <select v-if="isOrganizer" :value="task.assigned_to || ''"
                      @change="assignTask(task.id, $event.target.value || null)"
                      class="text-xs border border-gray-200 rounded px-1 py-0.5 text-gray-600">
                      <option value="">— назначить —</option>
                      <option v-for="p in event.participants" :key="p.id" :value="p.id">{{ p.username }}</option>
                    </select>
                  </div>
                  <p class="text-xs text-gray-300 mt-0.5">{{ task.created_by_username }}</p>
                </div>

                <button v-if="canDeleteTask(task)" @click="deleteTask(task.id)"
                  class="flex-shrink-0 text-gray-300 hover:text-gray-600 text-lg leading-none transition-colors">×</button>
              </div>
            </div>
            <p v-else class="text-sm text-gray-400">
              {{ isMember ? 'Задач пока нет.' : 'Задач пока нет.' }}
            </p>
          </div>

        </div>

        <!-- ПРАВАЯ КОЛОНКА: сайдбар -->
        <div class="space-y-4 lg:sticky lg:top-20">

          <!-- ЧАТ -->
          <div class="bg-white border-2 border-gray-300 rounded-md flex flex-col" style="height: 420px;">
            <div class="px-4 py-3 border-b border-gray-100">
              <h2 class="text-sm font-semibold text-gray-900 uppercase tracking-wide">Чат</h2>
            </div>

            <div ref="chatContainer" class="flex-1 overflow-y-auto px-4 py-3 space-y-2">
              <div v-if="messages.length === 0" class="text-xs text-gray-400 text-center pt-6">
                Сообщений пока нет
              </div>
              <div v-for="msg in messages" :key="msg.id" class="flex flex-col"
                :class="msg.sender_username === authStore.user?.username ? 'items-end' : 'items-start'">
                <span v-if="msg.sender_username !== authStore.user?.username"
                  class="text-xs text-gray-400 mb-1 px-1">
                  {{ msg.sender_username || 'Аноним' }}<span v-if="msg.sender_is_organizer" class="ml-1 text-gray-300">(орг)</span>
                </span>
                <div class="max-w-[85%] px-3 py-1.5 rounded-2xl text-sm break-words"
                  :class="msg.sender_username === authStore.user?.username
                    ? 'bg-gray-900 text-white rounded-br-sm'
                    : 'bg-gray-100 text-gray-800 rounded-bl-sm'">
                  {{ msg.text }}
                </div>
                <span class="text-xs text-gray-300 mt-0.5 px-1">{{ formatTime(msg.created_at) }}</span>
              </div>
            </div>

            <div v-if="canChat" class="border-t border-gray-100 px-3 py-2.5">
              <div class="flex gap-2">
                <input v-model="chatText" @keydown.enter.prevent="sendMessage" type="text"
                  placeholder="Сообщение..."
                  class="flex-1 px-3 py-1.5 border border-gray-200 rounded-full text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 transition-colors"
                  :disabled="chatSending" />
                <button @click="sendMessage" :disabled="!chatText.trim() || chatSending"
                  class="w-8 h-8 bg-gray-900 text-white rounded-full flex items-center justify-center hover:bg-gray-700 disabled:opacity-40 transition-colors flex-shrink-0">
                  <svg v-if="!chatSending" class="w-3.5 h-3.5 translate-x-px" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M12 5l7 7-7 7"/>
                  </svg>
                  <span v-else class="text-xs">...</span>
                </button>
              </div>
              <p v-if="chatError" class="text-xs text-red-500 mt-1 px-1">{{ chatError }}</p>
            </div>
            <p v-else class="text-xs text-gray-400 text-center border-t border-gray-100 py-2.5">
              {{ authStore.isAuthenticated ? 'Присоединитесь, чтобы написать' : 'Войдите, чтобы написать' }}
            </p>
          </div>

          <!-- УЧАСТНИКИ -->
          <div class="bg-white border-2 border-gray-300 rounded-md p-4">
            <h2 class="text-sm font-semibold text-gray-900 uppercase tracking-wide mb-3">
              Участники <span class="font-normal text-gray-400 normal-case tracking-normal">({{ event.participants?.length ?? 0 }})</span>
            </h2>
            <div v-if="event.participants?.length" class="space-y-1">
              <div v-for="p in event.participants" :key="p.id"
                class="flex items-center justify-between py-1.5 border-b border-gray-100 last:border-0">
                <span class="flex items-center gap-2 text-sm">
                  <span class="text-gray-800">{{ p.username }}</span>
                  <span v-if="p.is_organizer" class="text-xs text-gray-400 border border-gray-200 px-1.5 py-0.5 rounded">орг</span>
                </span>
                <div class="flex gap-2">
                  <button v-if="isOrganizer && !p.is_organizer && p.event_user !== authStore.userId"
                    @click="assignOrganizer(p.id)" class="text-xs text-gray-400 hover:text-gray-700 transition-colors">
                    Орг
                  </button>
                  <button v-if="isEventCreator && p.is_organizer && p.event_user !== event.event_user"
                    @click="removeOrganizer(p.id)" class="text-xs text-gray-400 hover:text-gray-700 transition-colors">
                    Снять
                  </button>
                </div>
              </div>
            </div>
            <p v-else class="text-xs text-gray-400">Пока нет участников.</p>
          </div>

          <!-- ССЫЛКА -->
          <div ref="linkSection" class="bg-white border-2 border-gray-300 rounded-md p-4">
            <h2 class="text-sm font-semibold text-gray-900 uppercase tracking-wide mb-3">Пригласить</h2>
            <div class="flex gap-2">
              <input :value="eventUrl" readonly class="flex-1 px-3 py-2 border border-gray-200 rounded-lg bg-gray-50 text-xs text-gray-500 min-w-0" />
              <button @click="copyLink"
                class="px-3 py-2 bg-gray-900 text-white text-xs font-medium rounded-lg hover:bg-gray-700 transition-colors whitespace-nowrap flex-shrink-0">
                {{ copied ? '✓' : 'Копировать' }}
              </button>
            </div>
          </div>

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
const dateOptions = computed(() => event.value?.date_options ?? [])
const isMember = computed(() => eventStore.isMember(authStore.userId))
const currentParticipant = computed(() =>
  event.value?.participants?.find(p => p.event_user === authStore.userId) ?? null
)
const isOrganizer = computed(() => currentParticipant.value?.is_organizer === true)
const isEventCreator = computed(() => !!event.value?.event_user && event.value.event_user === authStore.userId)

const eventUrl = computed(() =>
  event.value?.id ? `${window.location.origin}/event/${event.value.id}` : ''
)

// ── Tasks ─────────────────────────────────────────────────────────────────────
const tasks = ref([])
const taskTitle = ref('')
const taskDescription = ref('')
const showAddTaskForm = ref(false)
const addingTask = ref(false)

const canToggleDone = (task) => {
  if (isOrganizer.value) return true
  return !!currentParticipant.value && task.assigned_to === currentParticipant.value.id
}

const canSelfAssign = (task) =>
  isMember.value && !isOrganizer.value && !task.assigned_to

const canDeleteTask = (task) =>
  isOrganizer.value || task.created_by === authStore.userId

const loadTasks = async () => {
  if (!route.params.id) return
  try {
    const res = await api.get(`/events/${route.params.id}/tasks/`)
    tasks.value = res.data
  } catch {}
}

const addTask = async () => {
  if (!taskTitle.value.trim() || !event.value?.id) return
  addingTask.value = true
  try {
    await api.post(`/events/${event.value.id}/tasks/`, {
      title: taskTitle.value.trim(),
      description: taskDescription.value.trim(),
    })
    taskTitle.value = ''
    taskDescription.value = ''
    showAddTaskForm.value = false
    await loadTasks()
  } catch {} finally {
    addingTask.value = false
  }
}

const deleteTask = async (taskId) => {
  try {
    await api.delete(`/events/${event.value.id}/tasks/${taskId}/`)
    await loadTasks()
  } catch {}
}

const toggleDone = async (task) => {
  try {
    await api.patch(`/events/${event.value.id}/tasks/${task.id}/`, { is_done: !task.is_done })
    await loadTasks()
  } catch {}
}

const assignTask = async (taskId, participantId) => {
  try {
    await api.patch(`/events/${event.value.id}/tasks/${taskId}/`, {
      assigned_to: participantId,
    })
    await loadTasks()
  } catch {}
}

const selfAssign = (taskId) => assignTask(taskId, currentParticipant.value?.id)

// ── Chat ─────────────────────────────────────────────────────────────────────
const messages = ref([])
const chatText = ref('')
const chatSending = ref(false)
const chatError = ref('')
const chatContainer = ref(null)
let pollInterval = null

const canChat = computed(() => isMember.value || isOrganizer.value)

const assignOrganizer = async (participantId) => {
  try {
    await api.patch(`/events/${event.value.id}/participants/${participantId}/role/`, { is_organizer: true })
    await eventStore.getEvent(event.value.id)
  } catch {}
}

const removeOrganizer = async (participantId) => {
  try {
    await api.patch(`/events/${event.value.id}/participants/${participantId}/role/`, { is_organizer: false })
    await eventStore.getEvent(event.value.id)
  } catch {}
}

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

const refreshEvent = async () => {
  if (!route.params.id) return
  await eventStore.getEvent(route.params.id, { silent: true })
}

const startPolling = () => {
  stopPolling()
  loadMessages()
  loadTasks()
  pollInterval = setInterval(() => { refreshEvent(); loadMessages(); loadTasks() }, 3000)
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
  await loadTasks()
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