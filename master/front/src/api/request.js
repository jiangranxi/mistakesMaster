import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const request = axios.create({
  baseURL: '/api',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' }
})

// 请求拦截器 - 附加 Token
request.interceptors.request.use(
  config => {
    const auth = useAuthStore()
    if (auth.token) {
      config.headers.Authorization = `Bearer ${auth.token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器 - 统一错误处理
request.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response) {
      const { status, data } = error.response
      if (status === 401) {
        const auth = useAuthStore()
        auth.logout()
        router.push('/auth/login')
      }
      return Promise.reject({ status, message: data?.message || '请求失败' })
    }
    return Promise.reject({ message: '网络异常，请重试' })
  }
)

export default request
