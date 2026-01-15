<template>
  <div class="bg-white rounded-xl shadow-lg p-6">
    <!-- Заголовок -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-800">
        👥 Участники
        <span class="ml-2 text-sm font-normal text-gray-500">
          ({{ participants.length }})
        </span>
      </h2>
      <button
        v-if="showInviteButton"
        @click="$emit('invite')"
        class="px-4 py-2 bg-blue-100 text-blue-700 rounded-lg text-sm font-medium hover:bg-blue-200 transition"
      >
        + Пригласить
      </button>
    </div>

    <!-- Пустой список -->
    <div v-if="participants.length === 0" class="text-center py-8">
      <div class="text-gray-400 text-5xl mb-4">👤</div>
      <p class="text-gray-500 mb-4">Пока нет участников</p>
      <button
        @click="$emit('invite')"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Пригласить друзей
      </button>
    </div>

    <!-- Список участников -->
    <div v-else>
      <!-- Поиск (если много участников) -->
      <div v-if="participants.length > 5" class="mb-4">
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Найти участника..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
          <div class="absolute left-3 top-2.5 text-gray-400">
            🔍
          </div>
        </div>
      </div>

      <!-- Отфильтрованные участники -->
      <div class="space-y-3">
        <div
          v-for="participant in filteredParticipants"
          :key="participant.id || participant"
          class="flex items-center p-3 rounded-lg hover:bg-gray-50 transition"
          :class="{ 'bg-blue-50': isCurrentUser(participant) }"
        >
          <!-- Аватар -->
          <div class="flex-shrink-0 mr-4">
            <div
              class="w-12 h-12 rounded-full flex items-center justify-center text-white text-lg font-bold"
              :class="getAvatarColor(participant)"
            >
              {{ getInitials(participant) }}
            </div>
          </div>

          <!-- Информация -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center">
              <span class="font-medium text-gray-800 truncate">
                {{ getDisplayName(participant) }}
              </span>
              <span v-if="isCurrentUser(participant)" class="ml-2 px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded">
                Вы
              </span>
              <span v-if="isOrganizer(participant)" class="ml-2 px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded">
                Организатор
              </span>
            </div>
            <div class="text-sm text-gray-500 mt-1">
              {{ getParticipantInfo(participant) }}
            </div>
          </div>

          <!-- Статистика -->
          <div class="flex-shrink-0 ml-4 text-right">
            <div v-if="getVoteCount(participant) > 0" class="text-sm">
              <div class="font-medium text-gray-800">
                {{ getVoteCount(participant) }}
              </div>
              <div class="text-xs text-gray-500">
                голосов
              </div>
            </div>
            <div v-else class="text-sm text-gray-400">
              Не голосовал
            </div>
          </div>
        </div>
      </div>

      <!-- Информация о группах -->
      <div v-if="hasGroups" class="mt-6 pt-4 border-t">
        <h4 class="font-medium text-gray-700 mb-3">Группы участников</h4>
        <div class="flex flex-wrap gap-2">
          <div class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
            Организаторы: {{ organizerCount }}
          </div>
          <div class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
            Проголосовали: {{ votedCount }}
          </div>
          <div class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
            Новые: {{ newParticipantsCount }}
          </div>
        </div>
      </div>

      <!-- Кнопка приглашения внизу -->
      <div v-if="showInviteButton && participants.length > 0" class="mt-6">
        <button
          @click="$emit('invite')"
          class="w-full py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg font-medium hover:opacity-90 transition"
        >
          Пригласить ещё участников
        </button>
      </div>
    </div>

    <!-- Модальное окно приглашения -->
    <div v-if="showInviteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-2xl max-w-md w-full p-6">
        <h3 class="text-xl font-bold text-gray-800 mb-4">Пригласить участников</h3>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Ссылка для приглашения
          </label>
          <div class="flex">
            <input
              :value="inviteLink"
              type="text"
              readonly
              class="flex-1 px-4 py-2 border border-gray-300 rounded-l-lg bg-gray-50"
            >
            <button
              @click="copyInviteLink"
              class="px-4 py-2 bg-blue-600 text-white rounded-r-lg hover:bg-blue-700"
            >
              Копировать
            </button>
          </div>
        </div>

        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Или отправьте по email
          </label>
          <div class="flex">
            <input
              v-model="emailInput"
              type="email"
              placeholder="email@example.com"
              class="flex-1 px-4 py-2 border border-gray-300 rounded-l-lg"
            >
            <button
              @click="sendEmailInvite"
              class="px-4 py-2 bg-green-600 text-white rounded-r-lg hover:bg-green-700"
            >
              Отправить
            </button>
          </div>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            @click="showInviteModal = false"
            class="px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            Закрыть
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  participants: {
    type: Array,
    default: () => []
  },
  votes: {
    type: Array,
    default: () => []
  },
  eventId: {
    type: String,
    required: true
  },
  showInviteButton: {
    type: Boolean,
    default: true
  },
  currentUserId: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['invite', 'participant-click'])

// Локальное состояние
const searchQuery = ref('')
const showInviteModal = ref(false)
const emailInput = ref('')
const inviteLink = computed(() => {
  return `${window.location.origin}/event/${props.eventId}`
})

// Отфильтрованные участники
const filteredParticipants = computed(() => {
  if (!searchQuery.value.trim()) {
    return props.participants
  }
  
  const query = searchQuery.value.toLowerCase()
  return props.participants.filter(participant => {
    const name = getDisplayName(participant).toLowerCase()
    return name.includes(query)
  })
})

// Группы участников
const organizerCount = computed(() => {
  return props.participants.filter(p => isOrganizer(p)).length
})

const votedCount = computed(() => {
  return props.participants.filter(p => getVoteCount(p) > 0).length
})

const newParticipantsCount = computed(() => {
  return props.participants.length - votedCount.value
})

const hasGroups = computed(() => {
  return organizerCount.value > 0 || votedCount.value > 0 || newParticipantsCount.value > 0
})

// Вспомогательные функции
const getDisplayName = (participant) => {
  if (typeof participant === 'string') return participant
  return participant.name || participant.email || 'Аноним'
}

const getInitials = (participant) => {
  const name = getDisplayName(participant)
  return name
    .split(' ')
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const getAvatarColor = (participant) => {
  const colors = [
    'bg-blue-500',
    'bg-green-500',
    'bg-purple-500',
    'bg-red-500',
    'bg-yellow-500',
    'bg-pink-500'
  ]
  const name = getDisplayName(participant)
  const index = name.charCodeAt(0) % colors.length
  return colors[index]
}

const isCurrentUser = (participant) => {
  const participantId = typeof participant === 'string' ? participant : participant.id
  return participantId === props.currentUserId || getDisplayName(participant) === 'Вы'
}

const isOrganizer = (participant) => {
  // Здесь можно добавить логику определения организатора
  return typeof participant === 'object' && participant.isOrganizer
}

const getVoteCount = (participant) => {
  const participantName = getDisplayName(participant)
  return props.votes?.filter(vote => vote.voter === participantName).length || 0
}

const getParticipantInfo = (participant) => {
  const voteCount = getVoteCount(participant)
  if (voteCount > 0) {
    return `Проголосовал ${voteCount} раз`
  }
  return 'Ещё не голосовал'
}

// Действия
const copyInviteLink = () => {
  navigator.clipboard.writeText(inviteLink.value)
    .then(() => {
      alert('Ссылка скопирована в буфер обмена!')
    })
    .catch(err => {
      console.error('Ошибка копирования:', err)
    })
}

const sendEmailInvite = () => {
  if (!emailInput.value.trim()) return
  
  console.log('Отправка приглашения на:', emailInput.value)
  // TODO: Реализовать отправку через API
  alert(`Приглашение отправлено на ${emailInput.value}`)
  emailInput.value = ''
  showInviteModal.value = false
}

const handleInvite = () => {
  showInviteModal.value = true
  emit('invite')
}
</script>