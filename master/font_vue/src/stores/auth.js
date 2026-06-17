import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  // 用户角色: 'teacher' | 'student' | null
  const userRole = computed(() => userInfo.value?.role || null)
  const isLoggedIn = computed(() => !!token.value)
  const userName = computed(() => userInfo.value?.name || '')

  // 登录
  async function login(phone, password) {
    const res = await authApi.login({ phone, password })
    token.value = res.token
    userInfo.value = res.userInfo
    localStorage.setItem('token', res.token)
    localStorage.setItem('userInfo', JSON.stringify(res.userInfo))
    return res.userInfo
  }

  // 获取用户信息
  async function fetchUserInfo() {
    const res = await authApi.getUserInfo()
    userInfo.value = res
    localStorage.setItem('userInfo', JSON.stringify(res))
    return res
  }

  // 模拟登录（开发调试用）
  function mockLogin(role) {
    const mockData = role === 'teacher'
      ? { token: 'demo-teacher-token', userInfo: { id: '1', name: '江李 老师', role: 'teacher', phone: '13800000001' } }
      : { token: 'demo-student-token', userInfo: { id: '2', name: '江染惜 同学', role: 'student', phone: '13800000002' } }
    token.value = mockData.token
    userInfo.value = mockData.userInfo
    localStorage.setItem('token', mockData.token)
    localStorage.setItem('userInfo', JSON.stringify(mockData.userInfo))
  }

  // 登出
  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  return { token, userInfo, userRole, isLoggedIn, userName, login, mockLogin, fetchUserInfo, logout }
})
