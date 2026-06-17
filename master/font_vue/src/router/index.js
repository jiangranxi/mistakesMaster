import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    redirect: '/auth/login'
  },
  // === 认证页面 ===
  {
    path: '/auth',
    children: [
      { path: 'login', name: 'Login', component: () => import('@/views/auth/LoginView.vue') },
      { path: 'register-teacher', name: 'RegisterTeacher', component: () => import('@/views/auth/RegisterTeacher.vue') },
      { path: 'register-student', name: 'RegisterStudent', component: () => import('@/views/auth/RegisterStudent.vue') },
      { path: 'forgot-password', name: 'ForgotPassword', component: () => import('@/views/auth/ForgotPassword.vue') },
      { path: 'forgot-verify', name: 'ForgotVerify', component: () => import('@/views/auth/ForgotVerify.vue') },
      { path: 'forgot-reset', name: 'ForgotReset', component: () => import('@/views/auth/ForgotReset.vue') },
      { path: 'forgot-success', name: 'ForgotSuccess', component: () => import('@/views/auth/ForgotSuccess.vue') }
    ]
  },
  // === 教师端 ===
  {
    path: '/teacher',
    component: () => import('@/views/teacher/TeacherLayout.vue'),
    meta: { requiresAuth: true, role: 'teacher' },
    children: [
      { path: '', redirect: '/teacher/classes' },
      { path: 'classes', name: 'TeacherClasses', component: () => import('@/views/teacher/ClassList.vue') },
      { path: 'review/error-book', name: 'ReviewErrorBook', component: () => import('@/views/teacher/ReviewErrorBook.vue') },
      { path: 'review/homework', name: 'ReviewHomework', component: () => import('@/views/teacher/ReviewHomework.vue') },
      { path: 'homework/own', name: 'HomeworkOwn', component: () => import('@/views/teacher/HomeworkOwn.vue') },
      { path: 'homework/cloud', name: 'HomeworkCloud', component: () => import('@/views/teacher/HomeworkCloud.vue') },
      { path: 'homework/papers', name: 'HomeworkPapers', component: () => import('@/views/teacher/HomeworkPapers.vue') },
      { path: 'lesson-plans/own', name: 'LessonPlansOwn', component: () => import('@/views/teacher/LessonPlansOwn.vue') },
      { path: 'lesson-plans/cloud', name: 'LessonPlansCloud', component: () => import('@/views/teacher/LessonPlansCloud.vue') },
      { path: 'exercises', name: 'TeacherExercises', component: () => import('@/views/teacher/ExerciseList.vue') },
      { path: 'download', name: 'DownloadClient', component: () => import('@/views/teacher/DownloadClient.vue') },
      { path: 'messages', name: 'TeacherMessages', component: () => import('@/views/teacher/MessageList.vue') },
      { path: 'member', name: 'TeacherMember', component: () => import('@/views/teacher/MemberCenter.vue') },
      { path: 'member/security', name: 'TeacherSecurity', component: () => import('@/views/teacher/MemberSecurity.vue') },
      { path: 'member/orders', name: 'TeacherOrders', component: () => import('@/views/teacher/MemberOrders.vue') }
    ]
  },
  // === 学生端 ===
  {
    path: '/student',
    component: () => import('@/views/student/StudentLayout.vue'),
    meta: { requiresAuth: true, role: 'student' },
    children: [
      { path: '', redirect: '/student/homework/latest' },
      { path: 'homework/latest', name: 'HomeworkLatest', component: () => import('@/views/student/HomeworkLatest.vue') },
      { path: 'homework/history', name: 'HomeworkHistory', component: () => import('@/views/student/HomeworkHistory.vue') },
      { path: 'homework/errors', name: 'HomeworkErrors', component: () => import('@/views/student/HomeworkErrors.vue') },
      { path: 'classes', name: 'StudentClasses', component: () => import('@/views/student/MyClass.vue') },
      { path: 'exercises', name: 'StudentExercises', component: () => import('@/views/student/ExerciseList.vue') },
      { path: 'messages', name: 'StudentMessages', component: () => import('@/views/student/MessageList.vue') },
      { path: 'member', name: 'StudentMember', component: () => import('@/views/student/MemberCenter.vue') },
      { path: 'member/security', name: 'StudentSecurity', component: () => import('@/views/student/MemberSecurity.vue') },
      { path: 'member/orders', name: 'StudentOrders', component: () => import('@/views/student/MemberOrders.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫 - 权限控制
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth) {
    if (!authStore.isLoggedIn) {
      return next('/auth/login')
    }
    if (to.meta.role && authStore.userRole !== to.meta.role) {
      // 角色不匹配，重定向到对应端
      if (authStore.userRole === 'teacher') return next('/teacher')
      if (authStore.userRole === 'student') return next('/student')
      return next('/auth/login')
    }
  }
  // 已登录用户访问登录页，自动跳转
  if (to.path.startsWith('/auth/') && authStore.isLoggedIn) {
    if (authStore.userRole === 'teacher') return next('/teacher')
    if (authStore.userRole === 'student') return next('/student')
  }
  next()
})

export default router
