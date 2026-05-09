import { ref, onMounted, onUnmounted } from 'vue'

/**
 * 侦测元素是否进入视口，自动添加 visible class 触发 CSS 动画
 * 用法：<div ref="elRef" class="section-enter" v-useSectionAnimation />
 */
export function useSectionAnimation() {
  const elRef = ref(null)
  let observer = null

  onMounted(() => {
    if (!elRef.value) return
    observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible')
          observer?.unobserve(entry.target)
        }
      },
      { threshold: 0.1 }
    )
    observer.observe(elRef.value)
  })

  onUnmounted(() => {
    observer?.disconnect()
  })

  return elRef
}
