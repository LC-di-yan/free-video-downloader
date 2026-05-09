<template>
  <header ref="headerRef" :class="[
    'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
    scrolled
      ? 'bg-white/90 backdrop-blur-xl shadow-sm border-b border-gray-100/80'
      : 'bg-transparent'
  ]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <!-- Logo -->
      <div class="flex items-center gap-2.5 group cursor-pointer">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center shadow-sm group-hover:shadow-md transition-shadow">
          <span class="text-white text-xs font-bold">V</span>
        </div>
        <div class="flex items-baseline gap-1.5">
          <span class="text-lg font-bold text-gray-900">VidDown</span>
          <span class="text-lg font-light text-blue-600">AI</span>
        </div>
      </div>

      <!-- Desktop Actions -->
      <div class="flex items-center gap-2">
        <template v-if="user">
          <div class="flex items-center gap-2 mr-1">
            <span class="text-sm text-gray-400 hidden sm:block max-w-[120px] truncate">{{ user.email }}</span>
            <span v-if="user.is_vip"
              class="inline-flex items-center gap-1 text-xs bg-gradient-to-r from-yellow-50 to-yellow-100 text-yellow-700 px-2.5 py-0.5 rounded-full font-medium border border-yellow-200/60">
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
              VIP
            </span>
          </div>
          <button @click="$emit('logout')"
            class="text-sm text-gray-400 hover:text-gray-600 transition-colors px-3 py-1.5 rounded-lg hover:bg-gray-100">
            退出
          </button>
        </template>
        <template v-else>
          <button @click="$emit('login')"
            class="text-sm text-gray-600 hover:text-gray-900 transition-colors px-4 py-1.5 rounded-lg hover:bg-gray-100">
            登录
          </button>
          <button @click="$emit('register')"
            class="relative text-sm bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-5 py-1.5 rounded-full hover:shadow-lg hover:shadow-blue-500/25 transition-all duration-200 active:scale-95 overflow-hidden group">
            <span class="relative z-10">注册</span>
            <div class="absolute inset-0 bg-gradient-to-r from-indigo-600 to-blue-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </button>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

defineProps({
  user: { type: Object, default: null },
})
defineEmits(['login', 'register', 'logout', 'open-vip'])

const scrolled = ref(false)
const headerRef = ref(null)

function onScroll() {
  scrolled.value = window.scrollY > 20
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>
