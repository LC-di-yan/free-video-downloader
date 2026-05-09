import axios from 'axios'

export async function parseVideo(url) {
  const res = await axios.post('/api/parse', { url })
  return res.data
}

export async function downloadViaServer(url, formatId) {
  return await axios.post('/api/download', { url, format_id: formatId }, {
    responseType: 'blob',
  })
}

export async function getDirectUrl(url, formatId) {
  const res = await axios.post('/api/direct-url', { url, format_id: formatId })
  return res.data.data
}
