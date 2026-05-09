<template>
  <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden card-hover">
    <!-- 缩略图 -->
    <div class="relative aspect-video bg-gray-100 overflow-hidden">
      <img
        :src="proxyThumbnail(video.thumbnail)"
        :alt="video.title"
        class="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
      <span class="absolute bottom-3 right-3 bg-black/60 backdrop-blur-sm text-white text-xs px-2.5 py-1 rounded-full flex items-center gap-1.5">
        <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        {{ video.duration_string }}
      </span>
    </div>

    <!-- 视频信息 -->
    <div class="p-5 space-y-4">
      <div>
        <h3 class="font-semibold text-gray-900 line-clamp-2 leading-snug">{{ video.title }}</h3>
        <div class="flex items-center gap-2 text-sm text-gray-400 mt-2">
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          <span>{{ video.uploader }}</span>
          <span>·</span>
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
          <span>{{ video.platform }}</span>
        </div>
      </div>

      <!-- 格式选择 -->
      <div v-if="video.formats?.length">
        <label class="block text-sm font-medium text-gray-700 mb-2.5">选择画质</label>
        <div class="grid grid-cols-2 gap-2">
          <button
            v-for="fmt in video.formats"
            :key="fmt.format_id"
            @click="selectFormat(fmt)"
            :class="[
              'px-3 py-2.5 text-sm rounded-xl border transition-all duration-200 text-left relative overflow-hidden',
              selectedFormat?.format_id === fmt.format_id
                ? 'border-blue-500 bg-blue-50 text-blue-700 ring-1 ring-blue-500/20'
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
            ]"
          >
            <div class="font-medium">{{ fmt.resolution }}</div>
            <div class="text-xs text-gray-500 mt-0.5">{{ fmt.label }}</div>
          </button>
        </div>
      </div>

      <!-- 下载按钮 -->
      <button
        @click="handleDownload"
        :disabled="!selectedFormat || downloading"
        class="w-full py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-medium text-sm
               hover:shadow-lg hover:shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed
               transition-all duration-200 active:scale-[0.98] flex items-center justify-center gap-2"
      >
        <svg v-if="downloading" class="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        <svg v-else class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        {{ downloading ? '下载中...' : '下载视频' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  video: Object,
  downloading: Boolean,
})
const emit = defineEmits(['download'])

const selectedFormat = ref(null)

function selectFormat(fmt) {
  selectedFormat.value = fmt
}

function handleDownload() {
  if (!selectedFormat.value) return
  emit('download', selectedFormat.value.format_id)
}

function proxyThumbnail(url) {
  if (!url) return ''
  return '/api/proxy/thumbnail?url=' + encodeURIComponent(url)
}
</script>
