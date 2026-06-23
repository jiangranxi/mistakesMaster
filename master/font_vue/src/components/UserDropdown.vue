<template>
  <div class="dropdown-container" ref="container">
    <div class="trigger" :class="{ active: open }" @click="open = !open">
      <div class="avatar"><i class="ri-user-3-fill"></i></div>
      <span class="username">{{ displayName }}</span>
      <span class="username role-suffix">{{ roleLabel }}</span>
      <i class="ri-arrow-down-s-line arrow-icon"></i>
    </div>

    <div v-if="open" class="dropdown-menu" @click.stop>
      <div class="menu-item" @click="goMember">
        <span>个人中心</span>
      </div>
      <div class="menu-item" @click="showHelp">
        <span>帮助</span>
      </div>
      <div class="menu-divider"></div>
      <div class="menu-item" @click="handleLogout">
        <span>退出</span>
      </div>
    </div>

    <div v-if="open" class="backdrop" @click="open = false"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()
const open = ref(false)

const role = authStore.userRole
const roleLabel = computed(() => role === 'teacher' ? '老师' : (role === 'student' ? '同学' : ''))
// 去掉 name 中可能包含的角色后缀，避免重复显示
const displayName = computed(() => {
  const name = authStore.userName || ''
  return name.replace(/\s*(老师|同学|学生)$/, '')
})
const memberPath = role === 'teacher' ? '/teacher/member' : '/student/member'

function goMember() { open.value = false; router.push(memberPath) }
function showHelp() { open.value = false; toast.info('帮助中心：请联系客服 400-xxx-xxxx') }
function handleLogout() { open.value = false; authStore.logout(); router.push('/auth/login') }

function onClickOutside(e) {
  const el = document.querySelector('.dropdown-container')
  if (el && !el.contains(e.target)) { open.value = false }
}

onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))
</script>

<style scoped>
.dropdown-container { position: relative; align-self: stretch; display: flex; align-items: center; }
.trigger { display: flex; align-items: center; gap: 8px; cursor: pointer; user-select: none; padding: 0 16px; height: 100%; }
.trigger:hover .username, .trigger:hover .arrow-icon { color: #A8E6C3; }
.trigger.active { background: #005538; }
.trigger.active .username, .trigger.active .arrow-icon { color: #fff; }
.avatar { width: 32px; height: 32px; border-radius: 50%; background: #fff; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.avatar i { font-size: 20px; color: #006644; }
.username { font-size: 16px; color: #fff; }
.role-suffix { margin-left: 6px; }
.arrow-icon { font-size: 16px; color: #fff; }

.dropdown-menu {
  position: absolute;
  top: calc(100% + 2px);
  right: 0;
  left: 0;
  background: #006644;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  z-index: 1001;
  overflow: hidden;
  padding: 4px 0;
}

.menu-item {
  display: flex; align-items: center;
  padding: 10px 20px;
  font-size: 14px;
  color: #fff;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.menu-item:hover { background: #fff; color: #374151; }

.menu-divider { height: 1px; background: rgba(255,255,255,0.3); margin: 4px 0; }
.backdrop { position: fixed; inset: 0; z-index: 1000; }
</style>
