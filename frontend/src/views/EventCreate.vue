<template>
  <div class="event-create">
    <div class="header">
      <h1>📅 Создать новое событие</h1>
      <router-link to="/" class="back-link">← На главную</router-link>
    </div>
    
    <div class="form-container">
      <form @submit.prevent="handleSubmit" class="event-form">
        <!-- Название -->
        <div class="form-group">
          <label for="title">Название события *</label>
          <input
            id="title"
            v-model="title"
            type="text"
            placeholder="Например: Встреча команды, День рождения, Встреча с клиентом"
            required
            :disabled="loading"
          />
        </div>
        
        <!-- Описание -->
        <div class="form-group">
          <label for="description">Описание</label>
          <textarea
            id="description"
            v-model="description"
            rows="3"
            placeholder="Детали события, адрес, что взять с собой..."
            :disabled="loading"
          ></textarea>
        </div>
        
        <!-- Даты для голосования -->
        <div class="form-group">
          <label>Даты для голосования *</label>
          <p class="hint">Укажите несколько вариантов, участники выберут подходящие</p>
          
          <div v-for="(date, index) in dates" :key="index" class="date-row">
            <input
              v-model="dates[index]"
              type="datetime-local"
              :min="getMinDate()"
              required
              :disabled="loading"
              class="date-input"
            />
            <button
              type="button"
              @click="removeDate(index)"
              :disabled="dates.length <= 1 || loading"
              class="remove-date-btn"
              title="Удалить дату"
            >
              ×
            </button>
          </div>
          
          <button
            type="button"
            @click="addDate"
            :disabled="loading"
            class="add-date-btn"
          >
            + Добавить дату
          </button>
        </div>
        
        <!-- Кнопка отправки -->
        <div class="form-actions">
          <button
            type="submit"
            :disabled="loading || !isFormValid"
            class="submit-btn"
          >
            <span v-if="loading">⌛ Создание...</span>
            <span v-else>🎉 Создать событие</span>
          </button>
          
          <router-link to="/" class="cancel-btn">Отмена</router-link>
        </div>
        
        <!-- Ошибки -->
        <div v-if="error" class="error-message">
          ⚠️ {{ error }}
        </div>
        
        <!-- Подсказка -->
        <div class="info-box">
          <p>💡 После создания вы получите уникальную ссылку, которую можно отправить участникам.</p>
          <p>📱 Голосование работает даже без регистрации.</p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useEventStore } from '@/stores/event'

const router = useRouter()
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
const dates = ref([getTomorrowDate()]) // Начинаем с одной даты (завтра)

// Состояние
const loading = computed(() => eventStore.loading)
const error = computed(() => eventStore.error)

// Валидация формы
const isFormValid = computed(() => {
  return title.value.trim().length > 0 &&
         dates.value.length > 0 &&
         dates.value.every(date => date && date.trim() !== '')
})

// Получить минимальную дату (текущее время)
const getMinDate = () => {
  const now = new Date()
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
  return now.toISOString().slice(0, 16)
}

// Получить дату на завтра 18:00
//const getTomorrowDate = () => {
//  const tomorrow = new Date()
//  tomorrow.setDate(tomorrow.getDate() + 1)
//  tomorrow.setHours(18, 0, 0, 0)
//  return tomorrow.toISOString().slice(0, 16)
//}

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
  const processedDates = dates.value.map(dateStr => {
    try {
      // input[type="datetime-local"] возвращает строку в формате "YYYY-MM-DDTHH:mm"
      // Нужно добавить временную зону
      const dateObj = new Date(dateStr);
      
      // Проверяем, что дата валидна
      if (isNaN(dateObj.getTime())) {
        console.error('❌ Неверная дата:', dateStr);
        return null;
      }
      
      // Преобразуем в ISO строку (с часовым поясом UTC)
      const isoString = dateObj.toISOString();
      console.log(`✅ Преобразовано: ${dateStr} → ${isoString}`);
      return isoString;
      
    } catch (error) {
      console.error('❌ Ошибка преобразования даты:', dateStr, error);
      return null;
    }
  }).filter(date => date !== null); // Убираем невалидные даты
  
  if (processedDates.length === 0) {
    alert('Нет валидных дат для события');
    return;
  }
  console.log('Отправка данных:', {
    title: title.value,
    description: description.value,
    dates: dates.value
  })

  // Подготавливаем данные для API
  const eventData = {
    title: title.value.trim(),
    description: description.value.trim(),
    dates: dates.value.map(date => {
      // Преобразуем local datetime в ISO строку
      const dateObj = new Date(date)
      return dateObj.toISOString()
    })
  }
  
  try {
    // Используем store для создания
    const createdEvent = await eventStore.createEvent(eventData)
    
    console.log('✅ Событие создано, ID:', createdEvent.id)
    
    // Переходим на страницу события
    router.push(`/events/${createdEvent.id}`)
    
  } catch (err) {
    console.error('❌ Ошибка при создании:', err)
    // Ошибка уже в store.error
  }
}
</script>

<style scoped>
.event-create {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  margin: 0;
  color: #333;
}

.back-link {
  color: #666;
  text-decoration: none;
  font-size: 14px;
}

.back-link:hover {
  color: #2196F3;
}

.form-container {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.event-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.hint {
  font-size: 13px;
  color: #666;
  margin: 4px 0 12px 0;
}

input, textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  box-sizing: border-box;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #2196F3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.date-row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: center;
}

.date-input {
  flex: 1;
}

.remove-date-btn {
  background: #ff4444;
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-date-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.remove-date-btn:not(:disabled):hover {
  background: #ff2222;
}

.add-date-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  margin-top: 5px;
}

.add-date-btn:hover {
  background: #45a049;
}

.add-date-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-top: 20px;
}

.submit-btn {
  background: linear-gradient(135deg, #2196F3, #1976D2);
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  flex: 1;
}

.submit-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #1976D2, #1565C0);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

.cancel-btn {
  color: #666;
  text-decoration: none;
  padding: 12px 20px;
  border-radius: 6px;
  border: 1px solid #ddd;
  text-align: center;
}

.cancel-btn:hover {
  background: #f5f5f5;
}

.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 12px;
  border-radius: 6px;
  margin-top: 10px;
  border-left: 4px solid #c62828;
}

.info-box {
  background: #e8f4fd;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;
  border-left: 4px solid #2196F3;
}

.info-box p {
  margin: 5px 0;
  font-size: 14px;
  color: #1976D2;
}

@media (max-width: 768px) {
  .event-create {
    padding: 15px;
  }
  
  .form-container {
    padding: 20px;
  }
  
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .submit-btn, .cancel-btn {
    width: 100%;
  }
}
</style>