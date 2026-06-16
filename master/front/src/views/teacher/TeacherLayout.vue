<template>
  <div class="teacher-layout">
    <!-- 顶部导航栏 -->
    <header class="top-nav">
      <div class="nav-inner">
        <div class="nav-left">
          <div class="logo" @click="$router.push('/teacher/classes')">
            <span class="logo-icon">📘</span>
            <span class="logo-text">错题通</span>
          </div>
          <nav class="nav-menu">
            <router-link to="/teacher/lesson-plans" class="nav-item" :class="{ active: $route.path.startsWith('/teacher/lesson-plans') }">
              我的教案
            </router-link>
            <router-link to="/teacher/homework" class="nav-item" :class="{ active: $route.path.startsWith('/teacher/homework') }">
              布置作业
            </router-link>
            <router-link to="/teacher/review" class="nav-item" :class="{ active: $route.path.startsWith('/teacher/review') }">
              讲评
            </router-link>
            <router-link to="/teacher/classes" class="nav-item" :class="{ active: $route.path.startsWith('/teacher/classes') }">
              班级管理
            </router-link>
            <router-link to="/teacher/exercises" class="nav-item" :class="{ active: $route.path.startsWith('/teacher/exercises') }">
              习题集
            </router-link>
            <router-link to="/teacher/download" class="nav-item" :class="{ active: $route.path.startsWith('/teacher/download') }">
              下载客户端
            </router-link>
          </nav>
        </div>
        <div class="nav-right">
          <router-link to="/teacher/messages" class="nav-item msg-btn" title="消息">📬</router-link>
          <div class="user-info" @click="showDropdown = !showDropdown">
            <div class="avatar">{{ auth.userInfo?.realName?.charAt(0) || 'U' }}</div>
            <span class="username">{{ auth.userInfo?.realName || '用户' }}</span>
            <span class="arrow">▾</span>
          </div>
          <!-- 用户下拉菜单 -->
          <div v-if="showDropdown" class="dropdown-menu">
            <router-link to="/teacher/member" class="dropdown-item" @click="showDropdown = false">个人中心</router-link>
            <a class="dropdown-item" href="#">帮助</a>
            <a class="dropdown-item" @click="handleLogout">退出</a>
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const showDropdown = ref(false)

function handleLogout() {
  auth.logout()
  router.push('/auth/login')
}
</script>

<style scoped>
.teacher-layout {
  min-height: 100vh;
  background: #F5F5F5;
}

.top-nav {
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
  height: 60px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-inner {
  max-width: 1920px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 24px;
}

.nav-left { display: flex; align-items: center; gap: 40px; }

.logo { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.logo-icon { font-size: 24px; }
.logo-text { font-size: 18px; font-weight: 600; }

.nav-menu { display: flex; gap: 4px; }
.nav-item { padding: 8px 16px; color: #666; border-radius: 4px; font-size: 14px; text-decoration: none; transition: all .2s; }
.nav-item:hover, .nav-item.active { background: #F0F5FF; color: #4A90D9; }

.nav-right { display: flex; align-items: center; gap: 12px; position: relative; }
.msg-btn { font-size: 18px; }

.user-info { display: flex; align-items: center; gap: 8px; cursor: pointer; padding: 4px 8px; border-radius: 4px; }
.user-info:hover { background: #f5f5f5; }
.avatar { width: 32px; height: 32px; border-radius: 50%; background: #4A90D9; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 14px; }
.username { font-size: 14px; color: #333; }
.arrow { font-size: 10px; color: #999; }

.dropdown-menu {
  position: absolute; top: 48px; right: 0; background: #fff;
  border: 1px solid #e8e8e8; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,.1);
  min-width: 150px; z-index: 200;
}
.dropdown-item { display: block; padding: 10px 16px; color: #333; cursor: pointer; text-decoration: none; }
.dropdown-item:hover { background: #f5f5f5; }

.main-content {
  max-width: 1920px;
  margin: 0 auto;
  padding: 20px 24px;
}
</style>
