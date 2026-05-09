<template>
  <section ref="sectionRef" class="py-20 sm:py-24 relative overflow-hidden">
    <!-- 背景装饰 -->
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-1/3 right-0 w-72 h-72 bg-blue-50 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/3 left-0 w-72 h-72 bg-indigo-50 rounded-full blur-3xl"></div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 relative z-10">
      <div class="text-center mb-14">
        <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-100/50 text-blue-600 text-xs font-medium mb-4">
          Features
        </span>
        <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-3">核心功能</h2>
        <p class="text-gray-500 max-w-xl mx-auto">一站式视频处理工具，从下载到 AI 深度分析</p>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-5">
        <div v-for="(f, i) in features" :key="f.title"
          :class="[
            'group relative bg-white/80 backdrop-blur-sm p-6 sm:p-7 rounded-2xl border border-gray-100/80 card-hover cursor-default',
            'opacity-0 translate-y-6 transition-all duration-700 ease-out',
            visible ? 'opacity-100 translate-y-0' : ''
          ]"
          :style="{ transitionDelay: `${i * 100}ms` }"
        >
          <!-- 卡片顶部装饰线 -->
          <div class="absolute top-0 left-6 right-6 h-0.5 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>

          <!-- 图标 -->
          <div :class="[
            'w-11 h-11 rounded-xl flex items-center justify-center mb-4 transition-all duration-300 group-hover:scale-110 group-hover:shadow-lg',
            f.iconBg
          ]">
            <component :is="f.icon" class="w-5 h-5" :class="f.iconColor" />
          </div>

          <h3 class="font-semibold text-gray-900 mb-1.5 text-sm">{{ f.title }}</h3>
          <p class="text-xs text-gray-500 leading-relaxed">{{ f.desc }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useSectionAnimation } from '../composables/useSectionAnimation.js'

// 图标组件
import IconVideo from './icons/IconVideo.vue'
import IconZap from './icons/IconZap.vue'
import IconMapPin from './icons/IconMapPin.vue'
import IconFileText from './icons/IconFileText.vue'
import IconHeart from './icons/IconHeart.vue'

const features = [
  { icon: IconVideo, title: '多平台下载', desc: '支持 YouTube、B站、抖音等 1800+ 平台视频解析下载', iconBg: 'bg-blue-50 group-hover:bg-blue-100', iconColor: 'text-blue-600' },
  { icon: IconZap, title: 'AI 总结', desc: 'DeepSeek 智能分析视频内容，一键生成深度摘要', iconBg: 'bg-amber-50 group-hover:bg-amber-100', iconColor: 'text-amber-600' },
  { icon: IconMapPin, title: '思维导图', desc: '自动提取知识结构，生成可视化思维导图', iconBg: 'bg-emerald-50 group-hover:bg-emerald-100', iconColor: 'text-emerald-600' },
  { icon: IconFileText, title: '字幕导出', desc: 'SRT/VTT/TXT 多格式字幕下载，支持离线语音转写', iconBg: 'bg-purple-50 group-hover:bg-purple-100', iconColor: 'text-purple-600' },
  { icon: IconHeart, title: '免费试用', desc: '每日 3 次免费 AI 总结额度，开通 VIP 无限使用', iconBg: 'bg-rose-50 group-hover:bg-rose-100', iconColor: 'text-rose-600' },
]

const sectionRef = useSectionAnimation()
const visible = ref(false)
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
