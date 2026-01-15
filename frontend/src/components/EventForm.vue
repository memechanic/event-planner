<template>
  <div class="w-full max-w-2xl mx-auto p-4">
    <div class="bg-white rounded-xl shadow-lg p-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-2">
        Создайте новое событие
      </h2>
      <p class="text-gray-600 mb-6">
        Заполните форму и пригласите друзей для совместного планирования
      </p>
      
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Название события -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Название события *
          </label>
          <input
            v-model="form.title"
            type="text"
            required
            placeholder="Например: Встреча команды, День рождения, Совещание"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
          >
        </div>
        
        <!-- Описание -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Описание
          </label>
          <textarea
            v-model="form.description"
            rows="3"
            placeholder="Дополнительная информация о событии..."
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition resize-none"
          ></textarea>
        </div>
        
        <!-- Варианты дат -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="block text-sm font-medium text-gray-700">
              Варианты дат для голосования *
            </label>
            <button
              @click="addDate"
              type="button"
              class="text-sm text-blue-600 hover:text-blue-800 font-medium"
            >
              + Добавить дату
            </button>
          </div>
          
          <div class="space-y-3">
            <div
              v-for="(date, index) in form.dates"
              :key="index"
              class="flex items-center gap-3"
            >
              <input
                v-model="form.dates[index]"
                type="datetime-local"
                required
                :class="[
                  'flex-1 px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition',
                  dateError[index] ? 'border-red-500' : 'border-gray-300'
                ]"
              >
              <button
                v-if="form.dates.length > 1"
                @click="removeDate(index)"
                type="button"
                class="px-3 py-3 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg transition"
                title="Удалить дату"
              >
                ✕
              </button>
            </div>
          </div>
          
          <p class="mt-2 text-sm text-gray-500">
            Добавьте несколько дат, чтобы участники могли проголосовать
          </p>
        </div>
        
        <!-- Кнопка отправки -->
        <div class="pt-4">
          <button
            type="submit"
            :disabled="loading || !isFormValid"
            :class="[
              'w-full py-3 px-4 rounded-lg font-medium transition flex items-center justify-center',
              loading || !isFormValid
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:opacity-90'
            ]"
          >
            <span v-if="loading" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Создание...
            </span>
            <span v-else>
              🎉 Создать событие
            </span>
          </button>
          
          <p v-if="error" class="mt-3 p-3 bg-red-50 text-red-700 rounded-lg text-sm">
            {{ error }}
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useEventStore } from '../stores/event'

const router = useRouter()
const eventStore = useEventStore()

const form = ref({
  title: '',
  description: '',
  dates: ['']
})

const dateError = ref([])
const loading = computed(() => eventStore.loading)
const error = computed(() => eventStore.error)

// Валидация дат
watch(form.value.dates, (newDates) => {
  dateError.value = newDates.map(date => {
    if (!date.trim()) return 'Дата не может быть пустой'
    if (new Date(date) < new Date()) return 'Дата не может быть в прошлом'
    return null
  })
}, { deep: true })

const isFormValid = computed(() => {
  return form.value.title.trim() && 
         form.value.dates.length > 0 && 
         form.value.dates.every(date => date.trim()) &&
         !dateError.value.some(error => error)
})

const addDate = () => {
  form.value.dates.push('')
}

const removeDate = (index) => {
  form.value.dates.splice(index, 1)
}

const handleSubmit = async () => {
  if (!isFormValid.value) return
  
  try {
    const event = await eventStore.createEvent(form.value)
    
    // Сброс формы
    form.value = {
      title: '',
      description: '',
      dates: ['']
    }
    
    // Переход на страницу события
    router.push(`/event/${event.id || 'demo'}`)
    
  } catch (err) {
    console.error('Ошибка создания события:', err)
  }
}
</script>