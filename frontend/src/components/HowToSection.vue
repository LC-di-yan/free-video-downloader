<template>
  <section ref="sectionRef" class="py-20 sm:py-24 bg-white relative overflow-hidden">
    <div class="max-w-5xl mx-auto px-4 sm:px-6">
      <div class="text-center mb-16">
        <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-100/50 text-blue-600 text-xs font-medium mb-4">
          How It Works
        </span>
        <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-3">三步使用</h2>
        <p class="text-gray-500">从粘贴链接到获得 AI 总结，只需三步</p>
      </div>

      <div class="relative grid md:grid-cols-3 gap-8">
        <!-- 连接线 -->
        <div class="hidden md:block absolute top-16 left-[calc(16.67%+2rem)] right-[calc(16.67%+2rem)] h-0.5 bg-gradient-to-r from-blue-200 via-indigo-200 to-blue-200">
        </div>

        <div v-for="(step, i) in steps" :key="i"
          :class="[
            'relative flex flex-col items-center text-center transition-all duration-700 ease-out',
            'opacity-0 translate-y-8',
            visible ? 'opacity-100 translate-y-0' : ''
          ]"
          :style="{ transitionDelay: `${i * 200}ms` }"
        >
          <!-- 步骤编号 -->
          <div class="relative mb-6">
            <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20 text-white text-xl font-bold">
              {{ i + 1 }}
            </div>
          </div>

          <!-- 内容 -->
          <div class="bg-gray-50/80 rounded-2xl p-6 border border-gray-100/60 w-full card-hover">
            <div :class="[
              'w-10 h-10 rounded-xl flex items-center justify-center mx-auto mb-4',
              step.iconBg
            ]">
              <component :is="step.icon" class="w-5 h-5" :class="step.iconColor" />
            </div>
            <h3 class="font-semibold text-gray-900 mb-2">{{ step.title }}</h3>
            <p class="text-sm text-gray-500 leading-relaxed">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useSectionAnimation } from '../composables/useSectionAnimation.js'

import IconSearch from './icons/IconSearch.vue'
import IconPackage from './icons/IconPackage.vue'
import IconZap from './icons/IconZap.vue'

const steps = [
  { icon: IconSearch, title: '粘贴链接', desc: '复制你想下载的视频链接，粘贴到搜索框，点击解析', iconBg: 'bg-blue-50', iconColor: 'text-blue-600' },
  { icon: IconPackage, title: '解析下载', desc: '一键解析视频信息，选择清晰度，快速下载到本地', iconBg: 'bg-amber-50', iconColor: 'text-amber-600' },
  { icon: IconZap, title: 'AI 总结', desc: '自动生成视频摘要、思维导图，还可与 AI 对话提问', iconBg: 'bg-emerald-50', iconColor: 'text-emerald-600' },
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
