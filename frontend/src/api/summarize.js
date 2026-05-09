import axios from 'axios'

export function parseSSELine(line) {
  if (!line || !line.startsWith('data: ')) return null
  const data = line.slice(6).trim()
  if (data === '[DONE]') return { event: 'done', data: null }
  try {
    return { event: null, data: JSON.parse(data) }
  } catch {
    return { event: null, data }
  }
}

export async function summarizeVideo(url, language, callbacks) {
  const { onSubtitle, onSummary, onMindmap, onQuota, onError, onDone } = callbacks
  try {
    const token = localStorage.getItem('auth_token')
    const res = await fetch('/api/summarize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({ url, language }),
    })

    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      let currentEvent = ''
      for (const line of lines) {
        if (line.startsWith('event: ')) {
          currentEvent = line.slice(7).trim()
        } else if (line.startsWith('data: ')) {
          const data = line.slice(6).trim()
          if (data === '[DONE]') {
            onDone?.()
          } else {
            try {
              const parsed = JSON.parse(data)
              switch (currentEvent) {
                case 'subtitle':  onSubtitle?.(parsed); break
                case 'summary':   onSummary?.(parsed); break
                case 'mindmap':   onMindmap?.(parsed); break
                case 'quota':     onQuota?.(parsed); break
                case 'error':     onError?.(parsed); break
              }
            } catch { /* skip malformed data */ }
          }
        }
      }
    }
  } catch (err) {
    onError?.({ message: err.message })
  }
}

export async function chatWithVideo(url, question, subtitleText, callbacks) {
  const { onAnswer, onError, onDone } = callbacks
  try {
    const token = localStorage.getItem('auth_token')
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({ url, question, subtitle_text: subtitleText }),
    })

    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      let currentEvent = ''
      for (const line of lines) {
        if (line.startsWith('event: ')) {
          currentEvent = line.slice(7).trim()
        } else if (line.startsWith('data: ')) {
          const data = line.slice(6).trim()
          if (data === '[DONE]') {
            onDone?.()
          } else {
            try {
              const parsed = JSON.parse(data)
              if (currentEvent === 'answer') onAnswer?.(parsed)
              if (currentEvent === 'error') onError?.(parsed)
            } catch { /* skip */ }
          }
        }
      }
    }
  } catch (err) {
    onError?.({ message: err.message })
  }
}
