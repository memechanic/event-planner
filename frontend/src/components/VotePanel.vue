<template>
  <div class="bg-white rounded-xl shadow-lg p-6">
    <!-- Заголовок -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-800">
        🗳️ Голосование за даты
      </h2>
      <div class="text-sm text-gray-500">
        Всего голосов: {{ totalVotes }}
      </div>
    </div>

    <!-- Сообщение если нет дат -->
    <div v-if="!dates || dates.length === 0" class="text-center py-8">
      <div class="text-gray-400 text-5xl mb-4">📅</div>
      <p class="text-gray-500">Даты для голосования не добавлены</p>
    </div>

    <!-- Список дат для голосования -->
    <div v-else class="space-y-4">
      <div
        v-for="dateOption in dates"
        :key="dateOption.id || dateOption"
        class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
        :class="{ 'border-blue-300 bg-blue-50': isVotedFor(dateOption) }"
      >
        <div class="flex items-center justify-between mb-3">
          <!-- Дата и время -->
          <div>
            <div class="font-medium text-gray-800 text-lg">
              {{ formatDateTime(dateOption) }}
            </div>
            <div class="text-sm text-gray-500 mt-1">
              {{ formatRelativeTime(dateOption) }}
            </div>
          </div>

          <!-- Кнопка голосования -->
          <button
            @click="handleVote(dateOption)"
            :disabled="isVotedFor(dateOption)"
            :class="[
              'px-5 py-2 rounded-lg font-medium transition-all',
              isVotedFor(dateOption)
                ? 'bg-blue-600 text-white cursor-default'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200 hover:shadow-sm'
            ]"
          >
            <span v-if="isVotedFor(dateOption)">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                Ваш выбор
              </span>
            </span>
            <span v-else>
              Выбрать
            </span>
          </button>
        </div>

        <!-- Прогресс голосования -->
        <div class="mt-3">
          <div class="flex justify-between text-sm text-gray-600 mb-1">
            <span>Голосов: {{ getVoteCount(dateOption) }}</span>
            <span>{{ getVotePercentage(dateOption) }}%</span>
          </div>
          <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              class="h-full bg-blue-500 transition-all duration-500"
              :style="{ width: getVotePercentage(dateOption) + '%' }"
            ></div>
          </div>

          <!-- Список проголосовавших -->
          <div v-if="getVoters(dateOption).length > 0" class="mt-3">
            <div class="text-sm text-gray-500 mb-1">Проголосовали:</div>
            <div class="flex flex-wrap gap-2">
              <div
                v-for="voter in getVoters(dateOption)"
                :key="voter"
                class="inline-flex items-center px-2 py-1 bg-gray-100 rounded text-sm"
              >
                <div class="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
                {{ voter }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Результаты голосования -->
    <div v-if="totalVotes > 0 && dates.length > 0" class="mt-8 pt-6 border-t">
      <h3 class="font-bold text-gray-700 mb-4">📊 Итоги голосования</h3>
      <div class="space-y-3">
        <div
          v-for="dateOption in sortedDatesByVotes"
          :key="dateOption.id || dateOption"
          class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
        >
          <div class="flex-1">
            <div class="font-medium text-gray-800">
              {{ formatDateTimeShort(dateOption) }}
            </div>
            <div class="text-sm text-gray-500">
              {{ getVoteCount(dateOption) }} голосов
            </div>
          </div>
          <div class="text-right">
            <div class="text-lg font-bold text-blue-600">
              {{ getVotePercentage(dateOption) }}%
            </div>
            <div class="text-xs text-gray-500">
              {{ getVoteCount(dateOption) }} из {{ totalVotes }}
            </div>
          </div>
        </div>
      </div>

      <!-- Победитель -->
      <div v-if="winningDate" class="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
        <div class="flex items-center">
          <div class="text-green-600 mr-3">🏆</div>
          <div>
            <div class="font-medium text-green-800">Наиболее удобная дата:</div>
            <div class="text-green-600">{{ formatDateTime(winningDate) }}</div>
            <div class="text-sm text-green-500 mt-1">
              Подходит для {{ getVoteCount(winningDate) }} из {{ totalVotes }} участников
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Сообщение о успешном голосовании -->
    <div
      v-if="showVoteSuccess"
      class="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg animate-fade-in"
    >
      <div class="flex items-center">
        <div class="text-green-600 mr-3">✓</div>
        <div class="text-green-800">Ваш голос учтён!</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useEventStore } from '../stores/event'
import dayjs from 'dayjs'
import 'dayjs/locale/ru'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.locale('ru')
dayjs.extend(relativeTime)

const props = defineProps({
  eventId: {
    type: String,
    required: true
  },
  dates: {
    type: Array,
    default: () => []
  },
  votes: {
    type: Array,
    default: () => []
  },
  currentUserId: {
    type: String,
    default: 'current-user' // Временное решение
  }
})

const eventStore = useEventStore()
const userVote = ref(null)
const showVoteSuccess = ref(false)

// Вычисляемые свойства
const totalVotes = computed(() => {
  return props.votes?.length || 0
})

const getVoteCount = (dateOption) => {
  const dateStr = typeof dateOption === 'string' ? dateOption : dateOption.date
  return props.votes?.filter(vote => vote.date === dateStr).length || 0
}

const getVotePercentage = (dateOption) => {
  if (totalVotes.value === 0) return 0
  return Math.round((getVoteCount(dateOption) / totalVotes.value) * 100)
}

const getVoters = (dateOption) => {
  const dateStr = typeof dateOption === 'string' ? dateOption : dateOption.date
  return props.votes
    ?.filter(vote => vote.date === dateStr)
    .map(vote => vote.voter || 'Аноним')
    .slice(0, 5) || [] // Показываем только первых 5
}

const isVotedFor = (dateOption) => {
  const dateStr = typeof dateOption === 'string' ? dateOption : dateOption.date
  return userVote.value === dateStr
}

const sortedDatesByVotes = computed(() => {
  return [...props.dates].sort((a, b) => {
    return getVoteCount(b) - getVoteCount(a)
  })
})

const winningDate = computed(() => {
  if (sortedDatesByVotes.value.length === 0) return null
  return sortedDatesByVotes.value[0]
})

// Форматирование дат
const formatDateTime = (dateString) => {
  return dayjs(dateString).format('D MMMM YYYY, HH:mm')
}

const formatDateTimeShort = (dateString) => {
  return dayjs(dateString).format('D MMM HH:mm')
}

const formatRelativeTime = (dateString) => {
  return dayjs(dateString).fromNow()
}

// Обработка голосования
const handleVote = async (dateOption) => {
  const dateStr = typeof dateOption === 'string' ? dateOption : dateOption.date
  
  // Если уже голосовали за эту дату, отменяем голос
  if (isVotedFor(dateOption)) {
    console.log('Отмена голоса за дату:', dateStr)
    userVote.value = null
    
    // Удаляем голос из store
    if (eventStore.currentEvent && eventStore.currentEvent.votes) {
      eventStore.currentEvent.votes = eventStore.currentEvent.votes.filter(
        vote => vote.voter !== props.currentUserId && vote.voter !== 'Вы'
      )
    }
    
    return
  }
  
  try {
    // Сохраняем локально для мгновенной обратной связи
    userVote.value = dateStr
    
    // Отправляем на сервер
    await eventStore.voteForEvent(props.eventId, dateStr)
    
    // Показываем сообщение об успехе
    showVoteSuccess.value = true
    setTimeout(() => {
      showVoteSuccess.value = false
    }, 3000)
    
    console.log(`Голос за дату ${dateStr} учтён`)
    
    // Обновляем данные события
    if (eventStore.currentEvent) {
      // Форсируем обновление компонента
      // Vue должен автоматически отследить изменения через реактивность
    }
    
  } catch (error) {
    console.error('Ошибка при голосовании:', error)
    userVote.value = null // Сбрасываем если ошибка
  }
}

// При монтировании проверяем, голосовал ли уже пользователь
watch(() => props.votes, (newVotes) => {
  if (newVotes && props.currentUserId) {
    const userVoteObj = newVotes.find(vote => 
      vote.voter === props.currentUserId || vote.voter === 'Вы'
    )
    if (userVoteObj) {
      userVote.value = userVoteObj.date
    } else {
      userVote.value = null
    }
  }
}, { immediate: true, deep: true })
</script>

<style>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}
</style>