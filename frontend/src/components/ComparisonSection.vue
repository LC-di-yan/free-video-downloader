<template>
  <section ref="sectionRef" class="py-20 sm:py-24 bg-gradient-to-b from-gray-50 to-white relative overflow-hidden">
    <div class="max-w-5xl mx-auto px-4 sm:px-6">
      <div class="text-center mb-14">
        <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-100/50 text-blue-600 text-xs font-medium mb-4">
          Comparison
        </span>
        <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-3">为什么选择我们</h2>
        <p class="text-gray-500">全方位对比，看看 VidDownAI 的优势</p>
      </div>

      <div :class="[
        'overflow-hidden rounded-2xl border border-gray-200/80 shadow-sm transition-all duration-700',
        'opacity-0 translate-y-6',
        visible ? 'opacity-100 translate-y-0' : ''
      ]">
        <table class="w-full text-sm">
          <thead>
            <tr>
              <th class="text-left py-4 px-5 text-gray-500 font-medium bg-gray-50/80 w-[140px]">对比项</th>
              <th class="text-center py-4 px-5 font-semibold bg-gradient-to-r from-blue-50 to-indigo-50/80 text-blue-700 w-1/3">
                <span class="flex items-center justify-center gap-2">
                  <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="20 6 9 17 4 12"/>
                  </svg>
                  VidDownAI
                </span>
              </th>
              <th class="text-center py-4 px-5 font-medium text-gray-400 bg-gray-50/80 w-1/3">其他工具</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, i) in rows" :key="row.label"
              :class="[
                'transition-colors duration-200',
                i % 2 === 0 ? 'bg-white' : 'bg-gray-50/40',
                hoverRow === i ? 'bg-blue-50/40' : ''
              ]"
              @mouseenter="hoverRow = i"
              @mouseleave="hoverRow = null"
            >
              <td class="py-4 px-5 text-gray-700 font-medium">{{ row.label }}</td>
              <td class="py-4 px-5 text-center">
                <span class="inline-flex items-center gap-1.5 text-emerald-600 font-medium">
                  <svg class="w-4 h-4 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"/>
                  </svg>
                  {{ row.us }}
                </span>
              </td>
              <td class="py-4 px-5 text-center">
                <span class="inline-flex items-center gap-1.5 text-gray-400">
                  <svg class="w-4 h-4 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                  {{ row.them }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const rows = [
  { label: '支持平台', us: '1800+', them: '单一平台' },
  { label: 'AI 功能', us: '总结 + 导图 + 问答', them: '无或收费附加' },
  { label: '无水印', us: '抖音无水印（内置）', them: '需额外工具' },
  { label: '价格', us: '免费版 + 低价 VIP', them: '按次收费或高价' },
]

const hoverRow = ref(null)
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
