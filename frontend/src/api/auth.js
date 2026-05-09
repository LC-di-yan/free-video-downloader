import axios from 'axios'

const TOKEN_KEY = 'auth_token'
const USER_KEY = 'auth_user'

axios.interceptors.request.use(config => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export function isLoggedIn() {
  return !!localStorage.getItem(TOKEN_KEY)
}

export function getSavedUser() {
  const data = localStorage.getItem(USER_KEY)
  return data ? JSON.parse(data) : null
}

export function saveAuth(token, user) {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export async function register(email, password) {
  const res = await axios.post('/api/auth/register', { email, password })
  const { token, user } = res.data.data
  saveAuth(token, user)
  return user
}

export async function login(email, password) {
  const res = await axios.post('/api/auth/login', { email, password })
  const { token, user } = res.data.data
  saveAuth(token, user)
  return user
}

export async function fetchMe() {
  const res = await axios.get('/api/auth/me')
  const user = res.data.data
  localStorage.setItem(USER_KEY, JSON.stringify(user))
  return user
}

export function logout() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}
