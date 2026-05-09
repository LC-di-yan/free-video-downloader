<template>
  <section ref="sectionRef" class="py-20 sm:py-24 bg-white relative overflow-hidden">
    <!-- 背景装饰 -->
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-gradient-to-b from-blue-50/60 via-indigo-50/30 to-transparent rounded-full blur-3xl"></div>
    </div>

    <div class="max-w-4xl mx-auto px-4 sm:px-6 text-center relative z-10">
      <div class="mb-12">
        <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-100/50 text-blue-600 text-xs font-medium mb-4">
          Pricing
        </span>
        <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-3">选择最适合的方案</h2>
        <p class="text-gray-500">免费体验，升级解锁全部 AI 能力</p>
      </div>

      <div class="grid md:grid-cols-2 gap-8 max-w-2xl mx-auto">
        <!-- 免费版 -->
        <div :class="[
          'rounded-2xl p-8 border transition-all duration-500 text-left relative overflow-hidden',
          'opacity-0 translate-x-[-20px]',
          visible ? 'opacity-100 translate-x-0' : '',
          selectedPlan === 'free' ? 'border-blue-200 shadow-lg shadow-blue-100/50' : 'border-gray-200 shadow-sm hover:shadow-md'
        ]"
        :style="{ transitionDelay: '100ms' }"
        @mouseenter="selectedPlan = 'free'"
        >
          <h3 class="text-lg font-semibold text-gray-900 mb-1">免费版</h3>
          <p class="text-sm text-gray-400 mb-6">适合偶尔使用</p>
          <div class="mb-8">
            <span class="text-5xl font-bold text-gray-900">¥0</span>
          </div>
          <ul class="space-y-4 text-sm mb-10">
            <li v-for="item in freeFeatures" :key="item" class="flex items-start gap-3 text-gray-600">
              <svg class="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              {{ item }}
            </li>
          </ul>
          <div class="w-full py-3 rounded-xl bg-gray-100 text-gray-400 text-center font-medium text-sm cursor-not-allowed">
            当前使用中
          </div>
        </div>

        <!-- VIP 版 -->
        <div :class="[
          'rounded-2xl p-8 border-2 transition-all duration-500 text-left relative overflow-hidden',
          'opacity-0 translate-x-[20px]',
          visible ? 'opacity-100 translate-x-0' : '',
          selectedPlan === 'vip' ? 'border-blue-500 shadow-xl shadow-blue-500/20' : 'border-blue-500 shadow-md'
        ]"
        :style="{ transitionDelay: '200ms' }"
        @mouseenter="selectedPlan = 'vip'"
        >
          <!-- 推荐标签 -->
          <div class="absolute top-0 right-0">
            <div class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-xs font-medium px-8 py-1.5 -mr-8 -mt-1 rotate-45 translate-x-4 translate-y-4">
              推荐
            </div>
          </div>

          <h3 class="text-lg font-semibold text-gray-900 mb-1">VIP 会员</h3>
          <p class="text-sm text-gray-400 mb-6">解锁全部 AI 能力</p>
          <div class="mb-2">
            <span class="text-5xl font-bold text-gray-900">¥9.90</span>
            <span class="text-base font-normal text-gray-400 ml-1">/月</span>
          </div>
          <p class="text-xs text-gray-400 mb-8">开通后所有功能无限使用</p>
          <ul class="space-y-4 text-sm mb-10">
            <li v-for="item in vipFeatures" :key="item" class="flex items-start gap-3 text-gray-600">
              <svg class="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              {{ item }}
            </li>
          </ul>
          <button @click="$emit('open-vip')"
            class="w-full py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-medium text-sm
                   hover:shadow-lg hover:shadow-blue-500/25 transition-all duration-200 active:scale-[0.98]">
            开通 VIP
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

defineEmits(['open-vip', 'need-login'])

const freeFeatures = ['多平台视频解析下载', '每日 3 次 AI 总结', '基础画质选项']
const vipFeatures = ['免费版全部功能', 'AI 总结无限次使用', '思维导图 / AI 问答', '字幕文件导出']

const selectedPlan = ref('vip')
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
