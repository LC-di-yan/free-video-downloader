<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="fixed inset-0 z-[100] flex items-center justify-center" @click.self="$emit('close')">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 p-8 animate-scale-in">
          <!-- 关闭按钮 -->
          <button @click="$emit('close')"
            class="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-all">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>

          <!-- 标题 -->
          <div class="text-center mb-8">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center mx-auto mb-4 shadow-lg shadow-blue-500/20">
              <span class="text-white text-lg font-bold">V</span>
            </div>
            <h2 class="text-2xl font-bold text-gray-900">
              {{ mode === 'login' ? '欢迎回来' : '创建账号' }}
            </h2>
            <p class="text-sm text-gray-500 mt-1">
              {{ mode === 'login' ? '登录后即可使用 AI 总结功能' : '注册免费账号，体验 AI 视频总结' }}
            </p>
          </div>

          <!-- 表单 -->
          <form @submit.prevent="handleSubmit" class="space-y-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">邮箱</label>
              <div class="relative">
                <svg class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                <input v-model="email" type="email" required placeholder="name@example.com"
                  class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 bg-gray-50/50 text-sm
                         focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:bg-white
                         outline-none transition-all duration-200 placeholder:text-gray-400" />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">密码</label>
              <div class="relative">
                <svg class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                <input v-model="password" type="password" required minlength="6" placeholder="至少 6 位密码"
                  class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 bg-gray-50/50 text-sm
                         focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:bg-white
                         outline-none transition-all duration-200 placeholder:text-gray-400" />
              </div>
            </div>

            <!-- 错误提示 -->
            <Transition name="error">
              <p v-if="error"
                class="flex items-center gap-2 text-sm text-red-500 bg-red-50 rounded-lg px-4 py-2.5">
                <svg class="w-4 h-4 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                {{ error }}
              </p>
            </Transition>

            <button type="submit" :disabled="loading"
              class="w-full py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-medium text-sm
                     hover:shadow-lg hover:shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed
                     transition-all duration-200 active:scale-[0.98]">
              <span class="flex items-center justify-center gap-2">
                <svg v-if="loading" class="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                </svg>
                {{ loading ? '处理中...' : (mode === 'login' ? '登录' : '注册') }}
              </span>
            </button>
          </form>

          <div class="text-sm text-gray-500 text-center mt-6">
            {{ mode === 'login' ? '还没有账号？' : '已有账号？' }}
            <button @click="mode = mode === 'login' ? 'register' : 'login'"
              class="text-blue-600 hover:text-blue-700 font-medium transition-colors">
              {{ mode === 'login' ? '去注册' : '去登录' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import { login, register } from '../api/auth.js'

const props = defineProps({
  visible: Boolean,
  initialMode: { type: String, default: 'login' },
})
const emit = defineEmits(['close', 'success'])

const mode = ref('login')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

watch(() => props.visible, (v) => {
  if (v) {
    mode.value = props.initialMode
    email.value = ''
    password.value = ''
    error.value = ''
  }
})

async function handleSubmit() {
  loading.value = true
  error.value = ''
  try {
    const user = mode.value === 'login'
      ? await login(email.value, password.value)
      : await register(email.value, password.value)
    emit('success', user)
    emit('close')
  } catch (err) {
    error.value = err.response?.data?.detail || '操作失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-enter-active {
  transition: all 0.3s ease-out;
}
.modal-leave-active {
  transition: all 0.2s ease-in;
}
.modal-enter-from { opacity: 0; }
.modal-enter-from > div:last-child { transform: scale(0.95); }
.modal-leave-to { opacity: 0; }
.modal-leave-to > div:last-child { transform: scale(0.95); }

.error-enter-active { transition: all 0.3s ease-out; }
.error-leave-active { transition: all 0.2s ease-in; }
.error-enter-from { opacity: 0; transform: translateY(-8px); }
.error-leave-to { opacity: 0; transform: translateY(-8px); }
</style>
