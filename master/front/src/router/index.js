import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // 登录注册模块
  {
    path: '/auth',
    component: () => import('@/views/auth/AuthLayout.vue'),
    children: [
      { path: 'login', name: 'Login', component: () => import('@/views/auth/LoginView.vue') },
      { path: 'register-teacher', name: 'RegisterTeacher', component: () => import('@/views/auth/RegisterTeacher.vue') },
      { path: 'register-student', name: 'RegisterStudent', component: () => import('@/views/auth/RegisterStudent.vue') },
      { path: 'forgot-password', name: 'ForgotPassword', component: () => import('@/views/auth/ForgotPassword.vue') },
      { path: 'forgot-verify', name: 'ForgotVerify', component: () => import('@/views/auth/ForgotVerify.vue') },
      { path: 'forgot-reset', name: 'ForgotReset', component: () => import('@/views/auth/ForgotReset.vue') },
      { path: 'forgot-success', name: 'ForgotSuccess', component: () => import('@/views/auth/ForgotSuccess.vue') },
    ]
  },

  // 教师端模块
  {
    path: '/teacher',
    component: () => import('@/views/teacher/TeacherLayout.vue'),
    redirect: '/teacher/classes',
    children: [
      { path: 'classes', name: 'TeacherClasses', component: () => import('@/views/teacher/ClassList.vue') },
      { path: 'review', name: 'TeacherReview', component: () => import('@/views/teacher/ReviewReport.vue') },
      { path: 'lesson-plans', name: 'TeacherLessonPlans', component: () => import('@/views/teacher/LessonPlans.vue') },
      { path: 'homework', name: 'TeacherHomework', component: () => import('@/views/teacher/HomeworkManage.vue') },
      { path: 'exercises', name: 'TeacherExercises', component: () => import('@/views/teacher/ExerciseList.vue') },
      { path: 'member', name: 'TeacherMember', component: () => import('@/views/teacher/MemberCenter.vue') },
      { path: 'download', name: 'TeacherDownload', component: () => import('@/views/teacher/DownloadClient.vue') },
      { path: 'messages', name: 'TeacherMessages', component: () => import('@/views/teacher/MessageList.vue') },
    ]
  },

  // 学生端模块
  {
    path: '/student',
    component: () => import('@/views/student/StudentLayout.vue'),
    redirect: '/student/homework',
    children: [
      { path: 'homework', name: 'StudentHomework', component: () => import('@/views/student/HomeworkView.vue') },
      { path: 'classes', name: 'StudentClasses', component: () => import('@/views/student/ClassList.vue') },
      { path: 'exercises', name: 'StudentExercises', component: () => import('@/views/student/ExerciseList.vue') },
      { path: 'member', name: 'StudentMember', component: () => import('@/views/student/MemberCenter.vue') },
      { path: 'messages', name: 'StudentMessages', component: () => import('@/views/student/MessageList.vue') },
    ]
  },

  // 默认重定向
  { path: '/', redirect: '/auth/login' },
  { path: '/:pathMatch(.*)*', redirect: '/auth/login' },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
