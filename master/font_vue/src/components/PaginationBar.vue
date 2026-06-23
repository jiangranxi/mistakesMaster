<template>
  <div class="pagination-bar">
    <button
      class="nav-btn"
      :class="variant"
      :disabled="page <= 1"
      @click="$emit('page-change', 1)"
    >首页</button>
    <button
      class="nav-btn"
      :class="variant"
      :disabled="page <= 1"
      @click="$emit('page-change', page - 1)"
    >上一页</button>
    <button
      class="nav-btn"
      :class="variant"
      :disabled="page >= totalPages"
      @click="$emit('page-change', page + 1)"
    >下一页</button>
    <button
      class="nav-btn"
      :class="variant"
      :disabled="page >= totalPages"
      @click="$emit('page-change', totalPages)"
    >尾页</button>
    <input
      class="page-input"
      :class="variant"
      :value="page"
      @keydown.enter="onInputConfirm"
      @blur="onInputConfirm"
    />
    <span class="page-info">{{ page }}/{{ totalPages || 0 }}</span>
    <select
      class="page-size-select"
      :class="variant"
      :value="pageSize"
      @change="$emit('page-size-change', Number(($event.target).value))"
    >
      <option v-for="n in sizeOptions" :key="n" :value="n">{{ n }}</option>
    </select>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  page: { type: Number, default: 1 },
  pageSize: { type: Number, default: 15 },
  totalPages: { type: Number, default: 0 },
  variant: { type: String, default: 'teacher' }
})

const emit = defineEmits(['page-change', 'page-size-change'])

const sizeOptions = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

// 同步外部 page 到内部 inputValue，用于回退
const inputEl = ref(null)
watch(() => props.page, (val) => {
  // page 变化时无需额外操作，:value 绑定自动更新
})

function onInputConfirm(e) {
  const raw = e.target.value.trim()
  if (raw === '') { e.target.value = props.page; return }
  const val = Number(raw)
  if (isNaN(val)) { e.target.value = props.page; return }
  let p = val
  if (p < 1) p = 1
  else if (props.totalPages > 0 && p > props.totalPages) p = props.totalPages
  e.target.value = p
  emit('page-change', p)
}
</script>

<style scoped>
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.nav-btn {
  height: 36px;
  border: 1px solid #E5E7EB;
  background: #fff;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.nav-btn.teacher { min-width: 60px; border-color: #E5E7EB; }
.nav-btn.student { min-width: 70px; border-color: #D1D5DB; }
.nav-btn:hover:not(:disabled) { border-color: #2563EB; color: #2563EB; }
.nav-btn:disabled { color: #ccc; cursor: not-allowed; }

.page-input {
  height: 36px;
  border: 1px solid #E5E7EB;
  background: #fff;
  font-size: 14px;
  color: #333;
  text-align: center;
  outline: none;
  box-sizing: border-box;
  font-family: inherit;
}
.page-input.teacher { width: 48px; border-color: #E5E7EB; }
.page-input.student { width: 60px; border-color: #D1D5DB; }
.page-input:focus { box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }

.page-info {
  font-size: 14px;
  color: #333;
  text-align: center;
  white-space: nowrap;
}

.page-size-select {
  height: 36px;
  background: #fff;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  outline: none;
  text-align: center;
  appearance: none;
  padding-right: 16px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%236B7280' d='M12 16l-6-6h12z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 4px center;
  font-family: inherit;
}
.page-size-select.teacher { width: 60px; border-color: #E5E7EB; }
.page-size-select.student { width: 70px; border-color: #D1D5DB; }
</style>
