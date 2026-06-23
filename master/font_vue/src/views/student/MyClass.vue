<template>
  <div class="class-page">
    <div class="content-padded">
      <h3 class="page-title">我加入的班级</h3>
      <div class="spacer-16"></div>
      <div class="card-grid">
        <div class="class-card" v-for="cls in classList" :key="cls.id">
          <h4>{{ cls.name }}</h4>
          <p>{{ cls.teacherName }} · {{ cls.studentCount || 0 }} 名学生</p>
        </div>
        <div class="add-card" @click="showJoinDialog = true">
          <i class="ri-add-circle-line add-icon"></i>
          <span class="add-text">加入新班级</span>
        </div>
      </div>
    </div>

    <!-- 加入班级弹窗 -->
    <div v-if="showJoinDialog" class="dialog-overlay" @click.self="showJoinDialog = false">
      <div class="dialog">
        <h3 class="dialog-title">加入班级</h3>
        <div class="dialog-body">
          <div class="form-row">
            <label>班级号</label>
            <input class="form-input" v-model="joinCode" placeholder="请输入班级号" />
          </div>
          <div class="spacer-16"></div>
          <div class="form-row">
            <label>验证消息</label>
            <textarea class="form-textarea" v-model="joinMsg" placeholder="请输入验证消息" rows="4"></textarea>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn-cancel" @click="showJoinDialog = false">取消</button>
          <button class="btn-confirm" @click="handleJoin">加入</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { classApi } from '@/api/class'
import { useToast } from '@/composables/useToast'

const toast = useToast()

const classList = ref([])
const showJoinDialog = ref(false)
const joinCode = ref('')
const joinMsg = ref('')

async function loadData() {
  try { classList.value = await classApi.getJoinedClasses() } catch {}
}
async function handleJoin() {
  if (!joinCode.value) return
  try { await classApi.joinClass(joinCode.value, joinMsg.value); showJoinDialog.value = false; loadData() }
  catch (e) { toast.error(e?.response?.data?.message || '加入失败') }
}
loadData()
</script>

<style scoped>
.class-page { min-height: 100%; }
.content-padded { padding: 32px 64px; }
.page-title { font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; }
.spacer-16 { height: 16px; }
.spacer-32 { height: 32px; }
.card-grid { display: flex; flex-wrap: wrap; gap: 16px; }
.class-card, .add-card { width: 280px; height: 280px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.1); display: flex; flex-direction: column; align-items: center; justify-content: center; }
.class-card { background: #fff; padding: 24px; align-items: flex-start; justify-content: flex-start; }
.class-card h4 { font-size: 16px; color: #333; margin-bottom: 8px; }
.class-card p { font-size: 14px; color: #666; }
.add-card { background: #F5F5F5; cursor: pointer; }
.add-icon { font-size: 40px; color: #9CA3AF; }
.add-text { font-size: 16px; color: #999; margin-top: 16px; }
.dialog-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.dialog { background: #fff; border-radius: 8px; width: 480px; }
.dialog-title { padding: 24px 24px 0; font-size: 18px; color: #333; }
.dialog-body { padding: 24px; }
.form-row { display: flex; flex-direction: column; gap: 8px; }
.form-row label { font-size: 14px; color: #666; }
.form-input { width: 100%; height: 40px; padding: 8px 12px; border: 0.8px solid #D1D5DB; border-radius: 4px; font-size: 14px; outline: none; }
.form-textarea { width: 100%; min-height: 80px; padding: 8px 12px; border: 0.8px solid #D1D5DB; border-radius: 4px; font-size: 14px; outline: none; resize: vertical; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif; }
.dialog-footer { display: flex; justify-content: flex-end; gap: 12px; padding: 0 24px 24px; }
.btn-cancel { padding: 8px 24px; border: 0.8px solid #D1D5DB; border-radius: 4px; background: #fff; cursor: pointer; }
.btn-confirm { padding: 8px 24px; border: none; border-radius: 4px; background: #2563EB; color: #fff; cursor: pointer; }
</style>
