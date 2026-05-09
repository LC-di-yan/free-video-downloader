<template>
  <section :class="[
    'flex flex-col items-center justify-center transition-all duration-700 ease-out relative overflow-hidden',
    compact ? 'px-4 py-8' : 'px-4 min-h-[70vh] pt-24 pb-16'
  ]">
    <!-- 背景装饰 -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-blue-100/60 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-100/60 rounded-full blur-3xl"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-br from-blue-50 via-transparent to-indigo-50 rounded-full blur-3xl"></div>
    </div>

    <div class="relative z-10 w-full max-w-3xl flex flex-col items-center">
      <!-- 标语 -->
      <Transition name="slogan">
        <div v-if="showSlogan" class="text-center mb-10">
          <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-50/80 border border-blue-100/50 text-blue-600 text-xs font-medium mb-6 animate-fade-in">
            <span class="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></span>
            支持 1800+ 平台
          </div>
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-4">
            <span class="text-gray-900">AI 万能</span>
            <span class="gradient-text">视频下载器</span>
          </h1>
          <p class="text-lg sm:text-xl text-gray-500 max-w-xl mx-auto leading-relaxed">
            粘贴链接，一键解析下载 + <span class="text-gray-700 font-medium">AI 智能总结</span>
          </p>
        </div>
      </Transition>

      <!-- 搜索框 -->
      <div :class="[
        'w-full max-w-2xl transition-all duration-500',
        showSlogan ? '' : 'mt-2'
      ]">
        <div class="relative group">
          <div class="absolute -inset-1 bg-gradient-to-r from-blue-500 via-indigo-500 to-blue-500 rounded-2xl blur-xl opacity-20 group-hover:opacity-30 transition-opacity duration-500"></div>
          <div class="relative flex items-center bg-white rounded-2xl shadow-lg shadow-gray-200/60 border border-gray-200/80 focus-within:border-blue-400 focus-within:ring-4 focus-within:ring-blue-100 transition-all duration-300">
            <svg class="ml-5 w-5 h-5 text-gray-400 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input
              v-model="url"
              type="url"
              placeholder="粘贴视频链接，例如 https://www.bilibili.com/video/BV..."
              class="flex-1 px-4 py-4 bg-transparent text-sm text-gray-700 placeholder-gray-400 focus:outline-none"
              @keyup.enter="handleParse"
            />
            <button
              @click="handleParse"
              :disabled="loading"
              class="mr-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm font-medium
                     hover:shadow-lg hover:shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed
                     transition-all duration-200 active:scale-95 whitespace-nowrap"
            >
              <span class="flex items-center gap-2">
                <svg v-if="loading" class="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                </svg>
                <svg v-else class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="8" y1="11" x2="14" y2="11"/>
                </svg>
                {{ loading ? '解析中...' : '解析' }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  loading: Boolean,
  compact: Boolean,
  showSlogan: Boolean,
})
const emit = defineEmits(['parse'])

const url = ref('')

function extractUrl(text) {
  const match = text.match(/https?:\/\/[^\s）\)"\'＞，。、；：！？》>\]]+/)
  return match ? match[0] : text
}

function handleParse() {
  const raw = url.value.trim()
  if (!raw) return
  const cleanUrl = extractUrl(raw)
  emit('parse', cleanUrl)
  if (cleanUrl !== raw) url.value = cleanUrl
}
</script>

<style scoped>
.slogan-enter-active, .slogan-leave-active {
  transition: all 0.5s ease-out;
}
.slogan-enter-from, .slogan-leave-to {
  opacity: 0;
  transform: translateY(-16px);
}
</style>
