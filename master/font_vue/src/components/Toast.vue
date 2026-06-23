<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast">
        <div
          v-for="t in toasts"
          :key="t.id"
          class="toast-capsule"
          :class="'toast-' + t.type"
          @click="remove(t.id)"
        >
          <i v-if="t.type === 'success'" class="ri-check-line toast-icon"></i>
          <i v-else-if="t.type === 'error'" class="ri-close-line toast-icon"></i>
          <i v-else class="ri-information-line toast-icon"></i>
          <span class="toast-text">{{ t.message }}</span>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useToast } from '@/composables/useToast'

const { toasts, remove } = useToast()
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10000;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  pointer-events: none;
}

.toast-capsule {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  border-radius: 9999px;
  color: #fff;
  font-size: 15px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  white-space: nowrap;
  pointer-events: auto;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  backdrop-filter: blur(4px);
}

.toast-success { background: #22C55E; }
.toast-error { background: #EF4444; }
.toast-info { background: #6B7280; }

.toast-icon { font-size: 18px; flex-shrink: 0; }
.toast-text { line-height: 1; }

/* TransitionGroup 动画 */
.toast-enter-active { transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1); }
.toast-leave-active { transition: all 0.25s ease-in; }
.toast-enter-from { opacity: 0; transform: translateY(-20px) scale(0.85); }
.toast-leave-to { opacity: 0; transform: translateY(-12px) scale(0.9); }
.toast-move { transition: transform 0.25s ease; }
</style>
