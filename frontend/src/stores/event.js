import { defineStore } from 'pinia'
import { api } from '../api'

export const useEventStore = defineStore('event', {
  state: () => ({
    currentEvent: null,
    loading: false,
    error: null,
    eventsCache: {} // Кэш событий для оффлайн режима
  }),
  
  actions: {
    // СОЗДАНИЕ СОБЫТИЯ
    async createEvent(eventData) {
      this.loading = true
      this.error = null
      
      try {
        console.log('📝 Создание события:', eventData)
        
        // 1. Пробуем отправить на Django бэкенд
        try {
          const response = await api.post('/events/', eventData)
          const newEvent = response.data
          console.log('✅ Событие создано на сервере:', newEvent)
          
          // Сохраняем в кэш
          this.eventsCache[newEvent.id] = newEvent
          this.currentEvent = newEvent
          
          return newEvent
        } catch (apiError) {
          console.log('⚠️ Бэкенд недоступен, создаём локально:', apiError.message)
          
          // 2. Создаём локальное событие
          const localEvent = {
            id: 'evt_local_' + Date.now(),
            title: eventData.title || 'Новое событие',
            description: eventData.description || '',
            dates: eventData.dates || [],
            created_at: new Date().toISOString(),
            participants: ['Вы'],
            votes: [],
            messages: [
              {
                id: 1,
                text: 'Событие создано локально (сервер недоступен). Пригласите участников по ссылке.',
                username: 'Система',
                created_at: new Date().toISOString()
              }
            ]
          }
          
          // Сохраняем в localStorage для восстановления
          this.saveToLocalStorage(localEvent)
          
          this.eventsCache[localEvent.id] = localEvent
          this.currentEvent = localEvent
          
          console.log('✅ Событие создано локально:', localEvent)
          return localEvent
        }
        
      } catch (error) {
        console.error('❌ Критическая ошибка:', error)
        this.error = error.message || 'Не удалось создать событие'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // ЗАГРУЗКА СОБЫТИЯ
    async getEvent(eventId) {
      this.loading = true
      this.error = null
      
      try {
        console.log('🔍 Загрузка события:', eventId)
        
        // Демо-событие
        if (eventId === 'demo') {
          const demoEvent = this.createDemoEvent()
          this.currentEvent = demoEvent
          return demoEvent
        }
        
        // Проверяем кэш
        if (this.eventsCache[eventId]) {
          console.log('📦 Из кэша:', eventId)
          this.currentEvent = this.eventsCache[eventId]
          return this.currentEvent
        }
        
        // Пробуем загрузить с Django
        try {
          const response = await api.get(`/events/${eventId}/`)
          const serverEvent = response.data
          console.log('✅ С сервера:', serverEvent)
          
          this.eventsCache[eventId] = serverEvent
          this.currentEvent = serverEvent
          
          return serverEvent
        } catch (apiError) {
          console.log('⚠️ Сервер недоступен, пробуем localStorage')
          
          // Пробуем из localStorage
          const localEvent = this.loadFromLocalStorage(eventId)
          if (localEvent) {
            console.log('📱 Из localStorage:', localEvent)
            this.eventsCache[eventId] = localEvent
            this.currentEvent = localEvent
            return localEvent
          }
          
          throw new Error('Событие не найдено')
        }
        
      } catch (error) {
        console.error('❌ Ошибка загрузки:', error)
        this.error = error.message
        return null
      } finally {
        this.loading = false
      }
    },
    
    // ГОЛОСОВАНИЕ
    async voteForEvent(eventId, date, voterName = 'Вы') {
      try {
        console.log(`🗳 Голос за ${eventId}: ${date}`)
        
        // Обновляем локально
        if (this.currentEvent && this.currentEvent.id === eventId) {
          // Инициализируем votes если нет
          if (!this.currentEvent.votes) {
            this.currentEvent.votes = []
          }
          
          // Удаляем старый голос этого пользователя
          this.currentEvent.votes = this.currentEvent.votes.filter(
            vote => vote.voter !== voterName
          )
          
          // Добавляем новый голос
          const newVote = {
            id: Date.now(),
            date: date,
            voter: voterName,
            created_at: new Date().toISOString()
          }
          
          this.currentEvent.votes.push(newVote)
          
          // Сохраняем в кэш
          this.eventsCache[eventId] = this.currentEvent
          
          // Пробуем отправить на сервер (если это не локальное событие)
          if (!eventId.startsWith('evt_local_')) {
            try {
              await api.post(`/events/${eventId}/votes/`, {
                date: date,
                voter: voterName
              })
              console.log('✅ Голос сохранён на сервере')
            } catch (apiError) {
              console.log('⚠️ Голос только локально')
              this.saveToLocalStorage(this.currentEvent)
            }
          } else {
            this.saveToLocalStorage(this.currentEvent)
          }
          
          return newVote
        }
        
      } catch (error) {
        console.error('❌ Ошибка голосования:', error)
        throw error
      }
    },
    
    // СОХРАНЕНИЕ В localStorage
    saveToLocalStorage(event) {
      try {
        const events = JSON.parse(localStorage.getItem('localEvents') || '{}')
        events[event.id] = event
        localStorage.setItem('localEvents', JSON.stringify(events))
        console.log('💾 Сохранено в localStorage:', event.id)
      } catch (error) {
        console.error('Ошибка сохранения в localStorage:', error)
      }
    },
    
    // ЗАГРУЗКА ИЗ localStorage
    loadFromLocalStorage(eventId) {
      try {
        const events = JSON.parse(localStorage.getItem('localEvents') || '{}')
        return events[eventId] || null
      } catch (error) {
        console.error('Ошибка загрузки из localStorage:', error)
        return null
      }
    },
    
    // СОЗДАНИЕ ДЕМО-СОБЫТИЯ
    createDemoEvent() {
      const now = Date.now()
      return {
        id: 'demo',
        title: 'Демо: Планирование встречи команды',
        description: 'Пример события для тестирования функционала голосования',
        dates: [
          new Date(now + 86400000 * 1).toISOString(), // +1 день
          new Date(now + 86400000 * 2).toISOString(), // +2 дня
          new Date(now + 86400000 * 3).toISOString()  // +3 дня
        ],
        votes: [
          { id: 1, date: new Date(now + 86400000 * 2).toISOString(), voter: 'Анна' },
          { id: 2, date: new Date(now + 86400000 * 2).toISOString(), voter: 'Иван' },
          { id: 3, date: new Date(now + 86400000 * 3).toISOString(), voter: 'Мария' }
        ],
        participants: ['Анна', 'Иван', 'Мария', 'Алексей'],
        messages: [
          { 
            id: 1, 
            text: 'Привет всем! Кто сможет прийти на встречу?', 
            username: 'Анна', 
            created_at: new Date(now - 3600000 * 2).toISOString() 
          },
          { 
            id: 2, 
            text: 'Я могу в среду или четверг', 
            username: 'Иван', 
            created_at: new Date(now - 3600000 * 1.5).toISOString() 
          }
        ],
        created_at: new Date().toISOString()
      }
    },
    
    // ОЧИСТКА ТЕКУЩЕГО СОБЫТИЯ
    clearEvent() {
      this.currentEvent = null
      this.error = null
    }
  },
  
  getters: {
    // Голоса по датам (для статистики)
    votesByDate: (state) => {
      if (!state.currentEvent?.votes) return {}
      
      return state.currentEvent.votes.reduce((acc, vote) => {
        acc[vote.date] = acc[vote.date] || []
        acc[vote.date].push(vote.voter)
        return acc
      }, {})
    },
    
    // Уникальные участники
    uniqueParticipants: (state) => {
      if (!state.currentEvent) return []
      
      const participants = new Set(state.currentEvent.participants || [])
      state.currentEvent.votes?.forEach(vote => participants.add(vote.voter))
      
      return Array.from(participants)
    }
  }
})