<template>
  <div class="teacher-layout">
    <!-- 顶部导航栏 -->
    <header class="top-nav">
      <div class="nav-left">
        <span class="logo">错题通</span>
        <span class="nav-spacer"></span>
        <nav class="nav-menu">
          <div
            v-for="item in navItems"
            :key="item.key"
            class="nav-item"
            :class="{ active: currentNav === item.key }"
            @click="goNav(item)"
          >
            <span>{{ item.label }}</span>
            <i v-if="item.hasSub" class="ri-arrow-down-s-line"></i>
          </div>
        </nav>
      </div>
      <div class="nav-right">
        <span class="msg-icon" :class="{ active: isMessages }" @click="$router.push('/teacher/messages')">消息</span>
        <span class="right-spacer"></span>
        <UserDropdown />
      </div>
    </header>

    <!-- 内容区域 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import UserDropdown from '@/components/UserDropdown.vue'

const router = useRouter()
const route = useRoute()

const currentNav = ref('lessonPlans')

const navItems = [
  { key: 'lessonPlans', label: '我的教案', hasSub: true, path: '/teacher/lesson-plans/cloud' },
  { key: 'homework', label: '布置作业', hasSub: true, path: '/teacher/homework/cloud' },
  { key: 'review', label: '讲评', path: '/teacher/review/homework' },
  { key: 'classes', label: '班级管理', path: '/teacher/classes' },
  { key: 'exercises', label: '习题集', path: '/teacher/exercises' },
  { key: 'download', label: '下载客户端', path: '/teacher/download' },
]

// 根据路由更新当前高亮导航
watch(() => route.path, (path) => {
  if (path.includes('lesson-plan')) currentNav.value = 'lessonPlans'
  else if (path.includes('review')) currentNav.value = 'review'
  else if (path.includes('homework')) currentNav.value = 'homework'
  else if (path.includes('class')) currentNav.value = 'classes'
  else if (path.includes('exercise')) currentNav.value = 'exercises'
  else if (path.includes('download')) currentNav.value = 'download'
  else currentNav.value = ''
}, { immediate: true })

const isMessages = computed(() => route.path.includes('/messages'))

function goNav(item) {
  currentNav.value = item.key
  router.push(item.path)
}
</script>

<style scoped>
.teacher-layout { min-height: 100vh; display: flex; flex-direction: column; background: #fff; }

.top-nav {
  height: 60px;
  background: #006644;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  flex-shrink: 0;
}

.nav-left { display: flex; align-items: center; }
.logo { width: 80px; font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #fff; flex-shrink: 0; }
.nav-spacer { width: 80px; }

.nav-menu { display: flex; align-items: center; gap: 0; }
.nav-item {
  display: flex; align-items: center; gap: 4px;
  padding: 18px 16px;
  font-size: 16px; color: #fff; cursor: pointer;
  white-space: nowrap;
}
.nav-item.active { background: #005538; color: #fff; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; }
.nav-item:hover { color: #A8E6C3; }

.nav-right { display: flex; align-items: center; }
.msg-icon { font-size: 16px; color: #fff; cursor: pointer; padding: 18px 16px; }
.msg-icon:hover { color: #A8E6C3; }
.msg-icon.active { background: #005538; color: #fff; }
.right-spacer { width: 20px; }

.main-content { flex: 1; display: flex; flex-direction: column; min-height: 0; overflow-y: auto; }
</style>
