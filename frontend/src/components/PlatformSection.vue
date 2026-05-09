<template>
  <section ref="sectionRef" class="py-20 sm:py-24 bg-gradient-to-b from-white to-gray-50 relative overflow-hidden">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 text-center">
      <div class="mb-14">
        <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-100/50 text-blue-600 text-xs font-medium mb-4">
          Platforms
        </span>
        <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-3">支持的海量平台</h2>
        <p class="text-gray-500">基于 yt-dlp 核心引擎，覆盖全球主流视频平台</p>
      </div>

      <div class="flex flex-wrap justify-center gap-3">
        <span v-for="(p, i) in platforms" :key="p"
          :class="[
            'px-5 py-2.5 rounded-full border text-sm shadow-sm transition-all duration-300',
            'opacity-0 scale-90',
            visible ? 'opacity-100 scale-100' : '',
            hoveredPlatform === p
              ? 'border-blue-300 bg-blue-50 text-blue-700 shadow-md -translate-y-0.5'
              : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300 hover:shadow-md hover:-translate-y-0.5'
          ]"
          :style="{ transitionDelay: `${i * 50}ms` }"
          @mouseenter="hoveredPlatform = p"
          @mouseleave="hoveredPlatform = null"
        >
          {{ p }}
        </span>
      </div>

      <p class="text-sm text-gray-400 mt-8 flex items-center justify-center gap-2">
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        ...以及 1800+ 其他平台
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const platforms = [
  'YouTube', 'Bilibili', '抖音', 'Twitter/X', 'Instagram',
  'Facebook', 'TikTok', 'Vimeo', 'Twitch', 'SoundCloud',
  'Reddit', 'Pinterest', 'DailyMotion', 'LinkedIn',
]

const hoveredPlatform = ref(null)
const visible = ref(false)
const sectionRef = ref(null)
let observer = null

onMounted(() => {
  if (!sectionRef.value) return
  observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        visible.value = true
        observer?.disconnect()
      }
    },
    { threshold: 0.1 }
  )
  observer.observe(sectionRef.value)
})

onUnmounted(() => observer?.disconnect())
</script>
