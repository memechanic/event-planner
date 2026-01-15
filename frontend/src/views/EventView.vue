<template>
  <div class="event-view">
    <!-- Загрузка -->
    <div v-if="loading" class="loading">
      ⌛ Загрузка события...
    </div>
    
    <!-- Ошибка -->
    <div v-else-if="error && (!event || !event.id)" class="error">
      ⚠️ {{ error }}
      <router-link to="/" class="home-link">На главную</router-link>
    </div>
    
    <!-- Контент события -->
    <div v-else-if="event" class="event-content">
      <div class="event-header">
        <h1>{{ event.title }}</h1>
        <div class="event-meta">
          <span>📅 Создано: {{ formatDate(event.created_at) }}</span>
          <span>👥 Участники: {{ uniqueParticipants.length }}</span>
        </div>
      </div>
      
      <div class="event-description">
        {{ event.description || 'Нет описания' }}
      </div>
      
      <!-- Даты для голосования -->
      <div class="dates-section">
        <h2>📋 Варианты дат</h2>
        <div class="dates-grid">
          <div 
            v-for="date in dates" 
            :key="date" 
            class="date-card"
            :class="{ selected: selectedDate === date }"
            @click="selectDate(date)"
          >
            <div class="date-display">
              {{ formatDateTime(date) }}
            </div>
            <div class="vote-count">
              👍 {{ (votesByDate[date] || []).length }}
            </div>
            <div v-if="votesByDate[date]" class="voters">
              {{ votesByDate[date].join(', ') }}
            </div>
          </div>
        </div>
        
        <button 
          @click="submitVote" 
          :disabled="!selectedDate || voting"
          class="vote-btn"
        >
          {{ voting ? 'Голосую...' : 'Проголосовать' }}
        </button>
      </div>
      
      <!-- Участники -->
      <div class="participants-section">
        <h2>👥 Участники</h2>
        <div class="participants-list">
          <span v-for="participant in uniqueParticipants" :key="participant" class="participant">
            {{ participant }}
          </span>
        </div>
      </div>
      
      <!-- Ссылка для приглашения -->
      <div class="invite-section">
        <h2>🔗 Ссылка для приглашения</h2>
        <div class="invite-link">
          <input :value="eventUrl" readonly />
          <button @click="copyLink" class="copy-btn">
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
/* Стили аналогичные EventCreate.vue - для единого дизайна */
.event-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error {
  color: #c62828;
}

.home-link {
  display: block;
  margin-top: 20px;
  color: #2196F3;
}

.event-header {
  margin-bottom: 30px;
}

.event-header h1 {
  margin: 0 0 10px 0;
  color: #333;
}

.event-meta {
  display: flex;
  gap: 20px;
  color: #666;
  font-size: 14px;
}

.event-description {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  line-height: 1.6;
}

.dates-section {
  margin-bottom: 30px;
}

.dates-section h2 {
  margin-bottom: 15px;
  color: #333;
}

.dates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.date-card {
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.2s;
}

.date-card:hover {
  border-color: #2196F3;
  transform: translateY(-2px);
}

.date-card.selected {
  border-color: #4CAF50;
  background: #f1f8e9;
}

.date-display {
  font-weight: 600;
  margin-bottom: 8px;
}

.vote-count {
  color: #4CAF50;
  font-weight: bold;
}

.voters {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.vote-btn {
  background: linear-gradient(135deg, #4CAF50, #2E7D32);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}

.vote-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.participants-section, .invite-section {
  margin-bottom: 30px;
}

.participants-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.participant {
  background: #e3f2fd;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 14px;
}

.invite-link {
  display: flex;
  gap: 10px;
}

.invite-link input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #f8f9fa;
}

.copy-btn {
  background: #2196F3;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  white-space: nowrap;
}

.copy-btn:hover {
  background: #1976D2;
}
</style>