<template>
  <div class="student-layout">
    <!-- 顶部主导航 -->
    <header class="top-nav">
      <div class="nav-inner">
        <div class="nav-left">
          <div class="logo">
            <span class="logo-icon">📘</span>
            <span class="logo-text">错题通</span>
          </div>
          <nav class="nav-menu">
            <router-link
              class="nav-item" :class="{ active: $route.path.startsWith('/student/homework') }"
              to="/student/homework"
            >我的作业</router-link>
            <router-link
              class="nav-item" :class="{ active: $route.path.startsWith('/student/classes') }"
              to="/student/classes"
            >我的班级</router-link>
            <router-link
              class="nav-item" :class="{ active: $route.path.startsWith('/student/exercises') }"
              to="/student/exercises"
            >习题集</router-link>
          </nav>
        </div>
        <div class="nav-right">
          <router-link class="icon-btn" to="/student/messages" title="消息">
            📬
            <span class="badge" v-if="unreadCount > 0">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
          </router-link>
          <div class="user-info" @click="showDropdown = !showDropdown" v-click-outside="() => showDropdown = false">
            <div class="avatar">{{ (auth.userInfo?.realName || 'U').charAt(0) }}</div>
            <span class="username">{{ auth.userInfo?.realName || '用户' }}</span>
            <span class="arrow">▾</span>
            <!-- 下拉菜单 -->
            <div class="dropdown" v-if="showDropdown">
              <div class="dropdown-item" @click="$router.push('/student/member')">个人中心</div>
              <div class="dropdown-item">帮助</div>
              <div class="dropdown-item" @click="handleLogout">退出</div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- 内容区域 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { messageApi } from '@/api/message'

const router = useRouter()
const auth = useAuthStore()
const showDropdown = ref(false)
const unreadCount = ref(0)

onMounted(async () => {
  try {
    const res = await messageApi.getUnreadCount()
    unreadCount.value = res.count || 0
  } catch { /* ignore */ }
})

function handleLogout() {
  showDropdown.value = false
  auth.logout()
  router.push('/auth/login')
}

// 点击外部关闭指令
const vClickOutside = {
  mounted(el, binding) {
    el.__clickOutside = (e) => {
      if (!el.contains(e.target)) binding.value()
    }
    document.addEventListener('click', el.__clickOutside)
  },
  unmounted(el) {
    document.removeEventListener('click', el.__clickOutside)
  }
}
</script>

<style scoped>
.student-layout { min-height: 100vh; background: #F5F5F5; }
.top-nav { background: #fff; border-bottom: 1px solid #e8e8e8; height: 60px; position: sticky; top: 0; z-index: 100; }
.nav-inner { max-width: 1920px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; height: 100%; padding: 0 24px; }
.nav-left { display: flex; align-items: center; gap: 40px; }
.logo { display: flex; align-items: center; gap: 8px; }
.logo-icon { font-size: 24px; }
.logo-text { font-size: 18px; font-weight: 600; }
.nav-menu { display: flex; gap: 4px; }
.nav-item { padding: 8px 16px; color: #666; border-radius: 4px; text-decoration: none; font-size: 14px; }
.nav-item:hover, .nav-item.active { background: #F0F5FF; color: #4A90D9; }
.nav-right { display: flex; align-items: center; gap: 20px; }
.icon-btn { position: relative; background: none; border: none; font-size: 20px; cursor: pointer; text-decoration: none; }
.badge { position: absolute; top: -4px; right: -8px; background: #FF4D4F; color: #fff; font-size: 10px; padding: 1px 5px; border-radius: 10px; }
.user-info { display: flex; align-items: center; gap: 8px; cursor: pointer; position: relative; user-select: none; }
.avatar { width: 32px; height: 32px; border-radius: 50%; background: #4A90D9; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 14px; }
.username { font-size: 14px; }
.arrow { font-size: 10px; color: #999; }
.dropdown { position: absolute; top: 42px; right: 0; background: #fff; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,.1); width: 150px; z-index: 200; overflow: hidden; }
.dropdown-item { padding: 12px 20px; cursor: pointer; font-size: 14px; color: #333; }
.dropdown-item:hover { background: #F0F5FF; color: #4A90D9; }
.main-content { max-width: 1920px; margin: 0 auto; padding: 20px 24px; }
</style>
