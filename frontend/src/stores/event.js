import { defineStore } from 'pinia'
import { api } from '../api'

export const useEventStore = defineStore('event', {
  state: () => ({
    currentEvent: null,
    loading: false,
    error: null,
  }),

  actions: {
    async createEvent(eventData) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('/events/', eventData)
        this.currentEvent = response.data
        return response.data
      } catch (error) {
        this.error = error.message || 'Не удалось создать событие'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getEvent(eventId) {
      this.loading = true
      this.error = null
      try {
        const response = await api.get(`/events/${eventId}/`)
        this.currentEvent = response.data
        return response.data
      } catch (error) {
        this.error = error.message || 'Не удалось загрузить событие'
        return null
      } finally {
        this.loading = false
      }
    },

    async voteForEvent(eventId, dateOptionId) {
      const response = await api.post(`/events/${eventId}/votes/`, {
        date_option_id: dateOptionId,
      })
      // Перезагружаем событие, чтобы обновить vote_count
      await this.getEvent(eventId)
      return response.data
    },

    clearEvent() {
      this.currentEvent = null
      this.error = null
    },
  },

  getters: {
    // { dateOptionId: voteCount }
    votesByDateOptionId: (state) => {
      if (!state.currentEvent?.date_options) return {}
      return Object.fromEntries(
        state.currentEvent.date_options.map(d => [d.id, d.vote_count ?? 0])
      )
    },

    uniqueParticipants: (state) => {
      if (!state.currentEvent?.participants) return []
      return state.currentEvent.participants
        .map(p => p.username)
        .filter(Boolean)
    },
  },
})
