<template>
  <div class="page-container">
    <!-- 品牌区域 -->
    <div class="brand-area">
      <div class="logo-wrapper">
        <img class="logo-img" src="@/assets/logo.svg" alt="logo" />
        <span class="spacer-16"></span>
        <div class="brand-name">
          <span class="brand-title">错题通</span>
          <span class="brand-subtitle">科学高效学习方法平台</span>
        </div>
      </div>
    </div>

    <div class="spacer-64"></div>

    <!-- 登录表单 -->
    <div class="login-form">
      <!-- 手机号输入 -->
      <div class="input-row">
        <i class="ri-smartphone-line input-icon"></i>
        <span class="spacer-16"></span>
        <input
          v-model="phone"
          class="input-field"
          type="text"
          placeholder="请输入手机号"
          maxlength="11"
        />
      </div>

      <div class="spacer-32"></div>

      <!-- 密码输入 -->
      <div class="input-row">
        <i class="ri-lock-password-line input-icon"></i>
        <span class="spacer-16"></span>
        <input
          v-model="password"
          class="input-field"
          type="password"
          placeholder="请输入密码"
        />
      </div>

      <div class="spacer-48"></div>

      <!-- 登录按钮 -->
      <button class="btn-login" @click="handleLogin">登录</button>

      <div class="spacer-24"></div>

      <!-- 模拟快捷入口（开发调试用） -->
      <div class="demo-btns">
        <button class="btn-demo teacher" @click="mockGo('teacher')">👨‍🏫 进入教师端</button>
        <button class="btn-demo student" @click="mockGo('student')">👩‍🎓 进入学生端</button>
      </div>

      <div class="spacer-24"></div>

      <!-- 底部链接 -->
      <div class="bottom-links">
        <a href="/auth/register-teacher" class="link">用户注册</a>
        <span class="flex-spacer"></span>
        <a href="/auth/forgot-password" class="link">忘记密码？</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const phone = ref('')
const password = ref('')

async function handleLogin() {
  if (!phone.value || !password.value) return
  try {
    const userInfo = await authStore.login(phone.value, password.value)
    if (userInfo.role === 'teacher') {
      router.push('/teacher')
    } else {
      router.push('/student')
    }
  } catch (e) {
    alert(e?.response?.data?.message || '登录失败')
  }
}

function mockGo(role) {
  authStore.mockLogin(role)
  router.push(role === 'teacher' ? '/teacher' : '/student')
}
</script>

<style scoped>
.page-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fff;
  padding: 48px 16px;
}

.brand-area {
  width: 336px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-img {
  width: 82px;
  height: 95px;
  object-fit: contain;
}

.brand-name {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.brand-title {
  font-size: 64px;
  font-family: 'SourceHanSans-ExtraBold', 'Noto Sans SC', sans-serif;
  color: #22C55E;
  line-height: 1.2;
}

.brand-subtitle {
  font-size: 24px;
  color: #6B7280;
  line-height: 1.2;
}

.spacer-16 { width: 16px; height: 16px; flex-shrink: 0; }
.spacer-24 { height: 24px; }
.spacer-32 { height: 32px; }
.spacer-48 { height: 48px; }
.spacer-64 { height: 64px; }

.login-form {
  width: 448px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.input-row {
  display: flex;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 0.8px solid #D1D5DB;
}

.input-icon {
  font-size: 24px;
  color: #2563EB;
  flex-shrink: 0;
}

.input-field {
  flex: 1;
  border: none;
  outline: none;
  font-size: 18px;
  color: #374151;
  font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif;
  background: transparent;
}

.input-field::placeholder {
  color: #9CA3AF;
}

.flex-spacer {
  flex: 1;
}

.btn-login {
  width: 100%;
  height: 60px;
  border: none;
  border-radius: 8px;
  background: #2563EB;
  color: #fff;
  font-size: 20px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  cursor: pointer;
}

.btn-login:hover {
  background: #3B82F6;
}

.bottom-links {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.link {
  font-size: 16px;
  color: #2563EB;
  font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif;
  cursor: pointer;
}

.demo-btns {
  display: flex;
  gap: 12px;
}

.btn-demo {
  flex: 1;
  height: 44px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  cursor: pointer;
  color: #fff;
}

.btn-demo.teacher {
  background: #006644;
}

.btn-demo.teacher:hover {
  background: #005538;
}

.btn-demo.student {
  background: #F97316;
}

.btn-demo.student:hover {
  background: #EA580C;
}
</style>
