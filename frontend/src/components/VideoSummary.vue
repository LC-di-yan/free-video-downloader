<template>
  <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden card-hover">
    <!-- Tab 导航 -->
    <div class="flex border-b border-gray-100 bg-gray-50/30">
      <button v-for="tab in tabs" :key="tab.key"
        @click="activeTab = tab.key"
        :class="[
          'flex-1 py-3.5 text-sm font-medium transition-all duration-200 relative',
          activeTab === tab.key
            ? 'text-blue-600 bg-white'
            : 'text-gray-400 hover:text-gray-600 hover:bg-gray-50/50'
        ]">
        <span class="flex items-center justify-center gap-1.5">
          <component :is="tab.icon" v-if="tab.icon" class="w-4 h-4" />
          {{ tab.label }}
        </span>
        <div v-if="activeTab === tab.key"
          class="absolute bottom-0 left-3 right-3 h-0.5 bg-gradient-to-r from-blue-600 to-indigo-500 rounded-full"></div>
      </button>
    </div>

    <!-- Tab 内容 -->
    <div class="p-5 min-h-[200px]">
      <!-- 空状态 -->
      <div v-if="!videoUrl" class="flex flex-col items-center justify-center py-12 text-gray-400">
        <svg class="w-12 h-12 mb-3 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
        </svg>
        <p class="text-sm">⬆ 粘贴视频链接开始解析</p>
      </div>

      <!-- 总结摘要 -->
      <div v-else-if="activeTab === 'summary'" class="prose prose-slate max-w-none prose-headings:text-gray-900 prose-headings:font-semibold prose-p:text-gray-600 prose-p:leading-relaxed prose-strong:text-gray-900">
        <div v-if="noSubtitle" class="flex flex-col items-center justify-center py-10 text-gray-400">
          <svg class="w-10 h-10 mb-2 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <p class="text-sm">该视频没有可用字幕，无法生成总结</p>
        </div>
        <div v-else-if="errorMsg" class="flex items-center gap-3 text-red-500 bg-red-50 rounded-xl px-4 py-3 text-sm">{{ errorMsg }}</div>
        <div v-else-if="!summaryMd && loading" class="space-y-3">
          <div class="skeleton h-5 w-3/4"></div>
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-5/6"></div>
          <div class="skeleton h-4 w-2/3"></div>
          <div class="text-center text-gray-400 text-sm mt-4 animate-pulse">AI 正在分析视频内容...</div>
        </div>
        <div v-else v-html="renderedSummary" class="animate-fade-in"></div>
      </div>

      <!-- 字幕文本 -->
      <div v-else-if="activeTab === 'subtitle'" class="text-sm text-gray-600">
        <div v-if="errorMsg" class="flex items-center gap-3 text-red-500 bg-red-50 rounded-xl px-4 py-3 text-sm">{{ errorMsg }}</div>
        <div v-else-if="!subtitleData && loading" class="space-y-2">
          <div v-for="n in 6" :key="n" class="skeleton h-4" :style="{ width: `${60 + Math.random() * 30}%` }"></div>
          <div class="text-center text-gray-400 text-sm mt-4 animate-pulse">提取字幕中...</div>
        </div>
        <div v-else-if="subtitleData?.has_subtitle">
          <div class="flex items-center gap-2 text-xs text-gray-400 mb-3 bg-gray-50 rounded-lg px-3 py-2">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            共 {{ subtitleData.segments?.length || 0 }} 条字幕
          </div>
          <p class="whitespace-pre-wrap leading-relaxed">{{ subtitleData.full_text }}</p>
        </div>
        <div v-else class="flex flex-col items-center justify-center py-10 text-gray-400">
          <svg class="w-10 h-10 mb-2 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <p class="text-sm">该视频没有可用字幕</p>
        </div>
      </div>

      <!-- 思维导图 -->
      <div v-else-if="activeTab === 'mindmap'" class="w-full">
        <div v-if="noSubtitle" class="flex flex-col items-center justify-center py-10 text-gray-400">
          <svg class="w-10 h-10 mb-2 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <p class="text-sm">该视频没有可用字幕，无法生成思维导图</p>
        </div>
        <div v-else-if="errorMsg" class="flex items-center gap-3 text-red-500 bg-red-50 rounded-xl px-4 py-3 text-sm">{{ errorMsg }}</div>
        <div v-else-if="!mindmapMd && loading" class="space-y-3">
          <div class="skeleton h-5 w-1/2"></div>
          <div class="skeleton h-4 w-2/3 ml-4"></div>
          <div class="skeleton h-4 w-1/2 ml-4"></div>
          <div class="skeleton h-4 w-3/4 ml-8"></div>
          <div class="text-center text-gray-400 text-sm mt-4 animate-pulse">生成思维导图中...</div>
        </div>
        <div v-else-if="mindmapMd && mindmapRenderFailed" class="prose prose-slate max-w-none text-sm">
          <div class="flex items-center gap-2 text-yellow-600 bg-yellow-50 rounded-xl px-4 py-2.5 mb-4 text-xs">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            思维导图渲染失败，显示原始内容：
          </div>
          <pre class="whitespace-pre-wrap text-gray-600 bg-gray-50 rounded-xl p-4 text-xs">{{ mindmapMd }}</pre>
        </div>
        <div v-else-if="mindmapMd" ref="markmapContainer" class="w-full h-[400px] animate-fade-in"></div>
        <div v-else class="flex flex-col items-center justify-center py-10 text-gray-400">
          <svg class="w-10 h-10 mb-2 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <p class="text-sm">暂无思维导图</p>
        </div>
      </div>

      <!-- AI 问答 -->
      <div v-else-if="activeTab === 'chat'" class="space-y-4">
        <div class="flex gap-2">
          <div class="relative flex-1">
            <svg class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            <input v-model="chatQuestion" type="text" placeholder="输入关于视频的问题..."
              class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 bg-gray-50/50 text-sm
                     focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:bg-white
                     outline-none transition-all duration-200"
              @keyup.enter="handleChat" />
          </div>
          <button @click="handleChat" :disabled="chatLoading || !chatQuestion.trim()"
            class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm font-medium
                   hover:shadow-lg hover:shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed
                   transition-all duration-200 active:scale-95 whitespace-nowrap flex items-center gap-2">
            <svg v-if="chatLoading" class="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            {{ chatLoading ? '思考中...' : '提问' }}
          </button>
        </div>
        <div v-if="noSubtitle" class="flex flex-col items-center justify-center py-8 text-gray-400">
          <svg class="w-10 h-10 mb-2 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <p class="text-sm">该视频没有可用字幕，无法回答问题</p>
        </div>
        <div v-else-if="errorMsg" class="flex items-center gap-3 text-red-500 bg-red-50 rounded-xl px-4 py-3 text-sm">{{ errorMsg }}</div>
        <div v-else-if="chatAnswer" class="prose prose-slate max-w-none text-sm animate-fade-in">
          <div v-html="renderedChatAnswer"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { marked } from 'marked'
import { Transformer } from 'markmap-lib'
import { Markmap } from 'markmap-view'
import { summarizeVideo, chatWithVideo } from '../api/summarize.js'

const props = defineProps({
  videoUrl: String,
  videoTitle: String,
  user: Object,
})

const activeTab = ref('summary')
const tabs = [
  { key: 'summary', label: '总结摘要', icon: null },
  { key: 'mindmap', label: '思维导图', icon: null },
  { key: 'subtitle', label: '字幕文本', icon: null },
  { key: 'chat', label: 'AI 问答', icon: null },
]

const loading = ref(false)
const summaryMd = ref('')
const mindmapMd = ref('')
const subtitleData = ref(null)
const errorMsg = ref('')
const noSubtitle = ref(false)
const renderedSummary = computed(() => summaryMd.value ? marked(summaryMd.value) : '')
const markmapContainer = ref(null)
const mindmapRenderFailed = ref(false)

const chatQuestion = ref('')
const chatAnswer = ref('')
const chatLoading = ref(false)
const renderedChatAnswer = computed(() => chatAnswer.value ? marked(chatAnswer.value) : '')

let markmapInstance = null

function sanitizeMindmap(md) {
  const idx = md.search(/^# /m)
  return idx >= 0 ? md.slice(idx) : md
}

function renderMindmap() {
  if (!markmapContainer.value || !mindmapMd.value) return
  mindmapRenderFailed.value = false
  try {
    if (markmapInstance) {
      markmapInstance.destroy()
      markmapInstance = null
    }
    markmapContainer.value.innerHTML = ''
    const transformer = new Transformer()
    const { root } = transformer.transform(sanitizeMindmap(mindmapMd.value))
    markmapInstance = Markmap.create(markmapContainer.value, {
      zoom: true,
      pan: true,
      maxWidth: 600,
    }, root)
  } catch (e) {
    console.error('Markmap render error:', e)
    mindmapRenderFailed.value = true
  }
}

watch(mindmapMd, (val) => {
  if (val && activeTab.value === 'mindmap') {
    nextTick(() => renderMindmap())
  }
})

watch(activeTab, (tab) => {
  if (tab === 'mindmap' && mindmapMd.value) {
    nextTick(() => renderMindmap())
  }
})

watch(() => props.videoUrl, (newUrl) => {
  if (!newUrl) return
  loading.value = true
  summaryMd.value = ''
  mindmapMd.value = ''
  subtitleData.value = null
  errorMsg.value = ''
  noSubtitle.value = false
  chatAnswer.value = ''

  summarizeVideo(newUrl, 'zh', {
    onSubtitle: (data) => {
      subtitleData.value = data
    },
    onSummary: (token) => {
      summaryMd.value += token
    },
    onMindmap: (data) => {
      mindmapMd.value = data.markdown
    },
    onQuota: () => {},
    onError: (err) => {
      if (err.message.includes('没有可用的字幕')) {
        noSubtitle.value = true
      } else {
        errorMsg.value = err.message
      }
    },
    onDone: () => {
      loading.value = false
    },
  })
}, { immediate: true })

async function handleChat() {
  if (!chatQuestion.value.trim()) return
  chatLoading.value = true
  chatAnswer.value = ''
  await chatWithVideo(props.videoUrl, chatQuestion.value, subtitleData.value?.full_text || '', {
    onAnswer: (token) => {
      chatAnswer.value += token
    },
    onError: (err) => {
      chatAnswer.value = `错误：${err.message}`
    },
    onDone: () => {
      chatLoading.value = false
    },
  })
}
</script>
