<!-- src/views/RegisterView.vue -->
<template>
  <div class="min-h-[80vh] flex items-center justify-center bg-gray-50 p-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-md p-8">
      <!-- Заголовок -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-emerald-100 mb-4">
          <span class="text-3xl">📋</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-900">Регистрация</h1>
        <p class="text-sm text-gray-500 mt-1">Уже есть аккаунт?
          <router-link to="/login" class="text-blue-600 hover:underline font-medium">
            Войти
          </router-link>
        </p>
      </div>

      <form @submit.prevent="submit" class="space-y-5">
        <!-- Имя пользователя -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Имя пользователя</label>
          <input
            v-model="form.username"
            type="text"
            autocomplete="username"
            required
            placeholder="Придумайте логин"
            class="w-full px-4 py-2.5 border rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-colors"
            :class="{ 'border-red-400': fieldErrors.username }"
          />
          <p v-if="fieldErrors.username" class="text-xs text-red-500 mt-1">{{ fieldErrors.username }}</p>
        </div>

        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="form.email"
            type="email"
            autocomplete="email"
            required
            placeholder="example@mail.com"
            class="w-full px-4 py-2.5 border rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-colors"
            :class="{ 'border-red-400': fieldErrors.email }"
          />
          <p v-if="fieldErrors.email" class="text-xs text-red-500 mt-1">{{ fieldErrors.email }}</p>
        </div>

        <!-- Пароль -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
          <div class="relative">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="new-password"
              required
              placeholder="От 8 до 24 символов"
              class="w-full px-4 py-2.5 border rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-colors pr-11"
              :class="{ 'border-red-400': fieldErrors.password }"
            />
            <button
              type="button"
              tabindex="-1"
              @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              {{ showPassword ? '🙈' : '👁️' }}
            </button>
          </div>
          <p v-if="fieldErrors.password" class="text-xs text-red-500 mt-1">{{ fieldErrors.password }}</p>
          <!-- Подсказка -->
          <ul class="mt-2 space-y-0.5 text-xs text-gray-400">
            <li :class="hints.length ? 'text-emerald-600' : ''">✓ 8–24 символа</li>
            <li :class="hints.upper ? 'text-emerald-600' : ''">✓ Заглавная буква</li>
            <li :class="hints.lower ? 'text-emerald-600' : ''">✓ Строчная буква</li>
            <li :class="hints.special ? 'text-emerald-600' : ''">✓ Специальный символ (!@#$%…)</li>
          </ul>
        </div>

        <!-- Подтверждение пароля -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Подтвердите пароль</label>
          <div class="relative">
            <input
              v-model="form.password2"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="new-password"
              required
              placeholder="Повторите пароль"
              class="w-full px-4 py-2.5 border rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-colors pr-11"
              :class="{ 'border-red-400': fieldErrors.password2 }"
            />
          </div>
          <p v-if="fieldErrors.password2" class="text-xs text-red-500 mt-1">{{ fieldErrors.password2 }}</p>
        </div>

        <!-- Общая ошибка -->
        <p v-if="generalError" class="text-sm text-red-600 bg-red-50 rounded-lg px-3 py-2">
          {{ generalError }}
        </p>

        <!-- Кнопка -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-emerald-600 hover:bg-emerald-700 disabled:opacity-60 text-white font-semibold
                 py-2.5 rounded-xl transition-colors"
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

// Подсказки по сложности пароля (live-feedback)
const hints = computed(() => ({
  length: form.value.password.length >= 8 && form.value.password.length <= 24,
  upper: /[A-Z]/.test(form.value.password),
  lower: /[a-z]/.test(form.value.password),
  special: /[!@#$%^&*()\-_=+\[\]{};:'",.<>?/\\|`~]/.test(form.value.password),
}))

// Клиентская валидация перед отправкой
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
    // Пробуем разбить на поля
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

