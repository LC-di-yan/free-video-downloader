<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-b from-gray-50 to-white">
    <AppHeader
      :user="currentUser"
      @login="showAuthModal('login')"
      @register="showAuthModal('register')"
      @logout="handleLogout"
      @open-vip="handleOpenVip"
    />
    <main class="flex-1 pt-16">
      <HeroSection
        @parse="handleParse"
        :loading="loading"
        :compact="!!videoData"
        :showSlogan="!videoData || demoMode"
      />

      <!-- 视频结果区域 -->
      <Transition name="slide-up">
        <section v-if="videoData" class="py-6 sm:py-10">
          <div class="max-w-7xl mx-auto px-4 sm:px-6">
            <div class="flex flex-col lg:flex-row gap-6 lg:gap-8">
              <div class="w-full lg:w-2/5 lg:max-w-[420px] lg:flex-shrink-0">
                <VideoResult
                  :video="videoData"
                  :downloading="downloading"
                  @download="handleDownload"
                />
              </div>
              <div class="flex-1 min-w-0">
                <VideoSummary
                  :videoUrl="currentUrl"
                  :videoTitle="videoData.title"
                  :key="summaryKey"
                  :user="currentUser"
                />
              </div>
            </div>
          </div>
        </section>
      </Transition>

      <!-- 营销区域（仅在无视频数据时展示） -->
      <template v-if="!videoData || demoMode">
        <FeatureSection />
        <HowToSection />
        <ComparisonSection />
        <PricingSection @open-vip="handleOpenVip" @need-login="showAuthModal('login')" />
        <PlatformSection />
      </template>
    </main>

    <AppFooter />
    <AuthModal
      :visible="authModalVisible"
      :initialMode="authModalMode"
      @close="authModalVisible = false"
      @success="handleAuthSuccess"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { parseVideo, downloadViaServer } from './api/video.js'
import { getSavedUser, fetchMe, logout as logoutApi, isLoggedIn } from './api/auth.js'
import { createCheckoutSession } from './api/payment.js'

import AppHeader from './components/AppHeader.vue'
import HeroSection from './components/HeroSection.vue'
import VideoResult from './components/VideoResult.vue'
import VideoSummary from './components/VideoSummary.vue'
import FeatureSection from './components/FeatureSection.vue'
import HowToSection from './components/HowToSection.vue'
import ComparisonSection from './components/ComparisonSection.vue'
import PricingSection from './components/PricingSection.vue'
import PlatformSection from './components/PlatformSection.vue'
import AuthModal from './components/AuthModal.vue'
import AppFooter from './components/AppFooter.vue'

const currentUser = ref(getSavedUser())
const authModalVisible = ref(false)
const authModalMode = ref('login')

const loading = ref(false)
const downloading = ref(false)
const videoData = ref(null)
const currentUrl = ref('')
const summaryKey = ref(0)
const demoMode = ref(true)

async function handleParse(url) {
  loading.value = true
  videoData.value = null
  summaryKey.value++
  currentUrl.value = url
  try {
    const res = await parseVideo(url)
    if (res.success) {
      videoData.value = res.data
      demoMode.value = false
    } else {
      alert('解析失败：' + (res.error || '未知错误'))
    }
  } catch (err) {
    const msg = err.response?.data?.detail?.error || err.response?.data?.detail || err.message
    alert('解析失败：' + msg)
  } finally {
    loading.value = false
  }
}

async function handleDownload(formatId) {
  downloading.value = true
  try {
    const response = await downloadViaServer(currentUrl.value, formatId)
    const contentDisposition = response.headers['content-disposition']
    let filename = 'video.mp4'
    if (contentDisposition) {
      const match = contentDisposition.match(/filename\*?=(?:UTF-8'')?([^;\n]+)/i)
      if (match) filename = decodeURIComponent(match[1].replace(/"/g, ''))
    }
    const blob = new Blob([response.data])
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    window.URL.revokeObjectURL(url)
  } catch (err) {
    alert('下载失败：' + (err.message || '请稍后重试'))
  } finally {
    downloading.value = false
  }
}

function showAuthModal(mode) {
  authModalMode.value = mode
  authModalVisible.value = true
}

function handleAuthSuccess(user) {
  currentUser.value = user
}

function handleLogout() {
  logoutApi()
  currentUser.value = null
}

async function handleOpenVip() {
  if (!isLoggedIn()) {
    showAuthModal('login')
    return
  }
  try {
    const { checkout_url } = await createCheckoutSession('monthly')
    window.location.href = checkout_url
  } catch (err) {
    alert(err.response?.data?.detail || '创建支付失败')
  }
}

function checkPaymentResult() {
  const params = new URLSearchParams(window.location.search)
  if (params.get('payment') === 'success') {
    window.history.replaceState({}, '', window.location.pathname)
    if (isLoggedIn()) {
      setTimeout(async () => {
        try { currentUser.value = await fetchMe() } catch {}
      }, 1000)
    }
  }
}

onMounted(() => {
  checkPaymentResult()
})
</script>

<style>
/* 全局过渡动画 */
.slide-up-enter-active {
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-up-leave-active {
  transition: all 0.3s ease-in;
}
.slide-up-enter-from {
  opacity: 0;
  transform: translateY(30px);
}
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
