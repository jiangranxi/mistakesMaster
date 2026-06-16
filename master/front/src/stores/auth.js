import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))
  const userRole = ref(localStorage.getItem('userRole') || '') // 'teacher' | 'student'

  const isLoggedIn = computed(() => !!token.value)
  const isTeacher = computed(() => userRole.value === 'teacher')
  const isStudent = computed(() => userRole.value === 'student')

  async function login(phone, password) {
    const res = await authApi.login({ phone, password })
    token.value = res.token
    userInfo.value = res.userInfo
    userRole.value = res.userInfo.role
    localStorage.setItem('token', res.token)
    localStorage.setItem('userInfo', JSON.stringify(res.userInfo))
    localStorage.setItem('userRole', res.userInfo.role)
    return res
  }

  async function register(data) {
    const res = await authApi.register(data)
    return res
  }

  async function sendVerifyCode(phone) {
    return await authApi.sendVerifyCode(phone)
  }

  async function resetPassword(data) {
    return await authApi.resetPassword(data)
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    userRole.value = ''
    localStorage.clear()
  }

  return {
    token, userInfo, userRole, isLoggedIn, isTeacher, isStudent,
    login, register, sendVerifyCode, resetPassword, logout
  }
})
