<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h4>加入班级</h4>
        <span class="close-btn" @click="$emit('close')">✕</span>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label class="form-label">班级号 <span style="color:#FF4D4F">*</span></label>
          <input v-model="classCode" class="form-input" style="width:100%" placeholder="请输入班级号" />
        </div>
        <div class="form-group">
          <label class="form-label">验证消息</label>
          <textarea v-model="message" class="form-input" style="width:100%;height:100px" placeholder="请输入验证消息（选填）"></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-primary" @click="handleJoin" :disabled="!classCode">加入</button>
        <button class="btn" @click="$emit('close')">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { classApi } from '@/api/class'

const emit = defineEmits(['close', 'joined'])
const classCode = ref('')
const message = ref('')

async function handleJoin() {
  if (!classCode.value) return
  try {
    await classApi.joinClass(classCode.value)
    emit('joined')
  } catch { /* 错误由拦截器统一处理 */ }
}
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.4); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: #fff; border-radius: 12px; width: 600px; max-height: 80vh; overflow: hidden; }
.modal-header { padding: 16px 24px; border-bottom: 1px solid #f0f0f0; display: flex; justify-content: space-between; align-items: center; }
.modal-header h4 { font-size: 16px; }
.close-btn { cursor: pointer; font-size: 18px; color: #999; }
.modal-body { padding: 24px; }
.modal-footer { padding: 16px 24px; border-top: 1px solid #f0f0f0; display: flex; gap: 12px; justify-content: flex-end; }
</style>
