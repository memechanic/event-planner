<!-- src/views/RegisterView.vue -->
<template>
  <div class="min-h-[80vh] flex items-center justify-center p-4">
    <div class="w-full max-w-sm">
      <div class="mb-8">
        <h1 class="text-2xl font-semibold text-gray-900">Регистрация</h1>
        <p class="text-sm text-gray-500 mt-1">
          Уже есть аккаунт?
          <router-link to="/login" class="text-gray-900 underline underline-offset-2 hover:text-gray-600">
            Войти
          </router-link>
        </p>
      </div>

      <form @submit.prevent="submit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Имя пользователя</label>
          <input
            v-model="form.username"
            type="text"
            autocomplete="username"
            required
            placeholder="Придумайте логин"
            class="w-full px-3 py-2.5 border rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 transition-colors"
            :class="{ 'border-red-400': fieldErrors.username, 'border-gray-200': !fieldErrors.username }"
          />
          <p v-if="fieldErrors.username" class="text-xs text-red-500 mt-1">{{ fieldErrors.username }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="form.email"
            type="email"
            autocomplete="email"
            required
            placeholder="example@mail.com"
            class="w-full px-3 py-2.5 border rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 transition-colors"
            :class="{ 'border-red-400': fieldErrors.email, 'border-gray-200': !fieldErrors.email }"
          />
          <p v-if="fieldErrors.email" class="text-xs text-red-500 mt-1">{{ fieldErrors.email }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
          <div class="relative">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="new-password"
              required
              placeholder="От 8 до 24 символов"
              class="w-full px-3 py-2.5 border rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 transition-colors pr-10"
              :class="{ 'border-red-400': fieldErrors.password, 'border-gray-200': !fieldErrors.password }"
            />
            <button
              type="button"
              tabindex="-1"
              @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 text-xs"
            >
              {{ showPassword ? 'скрыть' : 'показать' }}
            </button>
          </div>
          <p v-if="fieldErrors.password" class="text-xs text-red-500 mt-1">{{ fieldErrors.password }}</p>
          <ul class="mt-2 space-y-0.5 text-xs text-gray-400">
            <li :class="hints.length ? 'text-gray-700' : ''">{{ hints.length ? '✓' : '·' }} 8–24 символа</li>
            <li :class="hints.upper ? 'text-gray-700' : ''">{{ hints.upper ? '✓' : '·' }} Заглавная буква</li>
            <li :class="hints.lower ? 'text-gray-700' : ''">{{ hints.lower ? '✓' : '·' }} Строчная буква</li>
            <li :class="hints.special ? 'text-gray-700' : ''">{{ hints.special ? '✓' : '·' }} Специальный символ (!@#$%…)</li>
          </ul>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Подтвердите пароль</label>
          <input
            v-model="form.password2"
            :type="showPassword ? 'text' : 'password'"
            autocomplete="new-password"
            required
            placeholder="Повторите пароль"
            class="w-full px-3 py-2.5 border rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 transition-colors"
            :class="{ 'border-red-400': fieldErrors.password2, 'border-gray-200': !fieldErrors.password2 }"
          />
          <p v-if="fieldErrors.password2" class="text-xs text-red-500 mt-1">{{ fieldErrors.password2 }}</p>
        </div>

        <p v-if="generalError" class="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">
          {{ generalError }}
        </p>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-gray-900 hover:bg-gray-700 disabled:opacity-40 text-white text-sm font-medium py-2.5 rounded-lg transition-colors"
        >
          {{ loading ? 'Создание аккаунта...' : 'Зарегистрироваться' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = ref({ username: '', email: '', password: '', password2: '' })
const showPassword = ref(false)
const loading = ref(false)
const fieldErrors = ref({})
const generalError = ref('')

const hints = computed(() => ({
  length: form.value.password.length >= 8 && form.value.password.length <= 24,
  upper: /[A-Z]/.test(form.value.password),
  lower: /[a-z]/.test(form.value.password),
  special: /[!@#$%^&*()\-_=+\[\]{};:'",.<>?/\\|`~]/.test(form.value.password),
}))

const validate = () => {
  const errs = {}
  if (!form.value.username.trim()) errs.username = 'Введите имя пользователя'
  if (!form.value.email.trim()) errs.email = 'Введите email'
  if (!hints.value.length) errs.password = 'Пароль: от 8 до 24 символов'
  else if (!hints.value.upper) errs.password = 'Добавьте заглавную букву'
  else if (!hints.value.lower) errs.password = 'Добавьте строчную букву'
  else if (!hints.value.special) errs.password = 'Добавьте специальный символ'
  if (form.value.password !== form.value.password2) errs.password2 = 'Пароли не совпадают'
  return errs
}

const submit = async () => {
  fieldErrors.value = {}
  generalError.value = ''

  const errs = validate()
  if (Object.keys(errs).length) {
    fieldErrors.value = errs
    return
  }

  loading.value = true
  try {
    await authStore.register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      password2: form.value.password2,
    })
    router.push(route.query.redirect || '/')
  } catch (e) {
    const msg = e.message || ''
    if (msg.toLowerCase().includes('email')) fieldErrors.value.email = msg
    else if (msg.toLowerCase().includes('имя') || msg.toLowerCase().includes('username')) fieldErrors.value.username = msg
    else if (msg.toLowerCase().includes('пароль') || msg.toLowerCase().includes('password')) fieldErrors.value.password = msg
    else generalError.value = msg
  } finally {
    loading.value = false
  }
}
</script>
