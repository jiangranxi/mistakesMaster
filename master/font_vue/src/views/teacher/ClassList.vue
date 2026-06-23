<template>
  <div class="class-list-page">
    <div class="content-padded">
      <!-- 我创建的班级 -->
      <section class="section">
        <h3 class="section-title">我创建的班级</h3>
        <div class="spacer-16"></div>
        <div class="card-grid">
          <div class="add-card" @click="showCreateDialog = true">
            <i class="ri-add-circle-line add-icon"></i>
            <span class="add-text">创建新班级</span>
          </div>
          <div
            v-for="cls in createdClasses"
            :key="cls.id"
            class="class-card"
          >
            <h4>{{ cls.name }}</h4>
            <p>{{ cls.studentCount || 0 }} 名学生</p>
            <p class="code">班级码: {{ cls.code }}</p>
          </div>
        </div>
      </section>

      <div class="spacer-32"></div>

      <!-- 我加入的班级 -->
      <section class="section">
        <h3 class="section-title">我加入的班级</h3>
        <div class="spacer-16"></div>
        <div class="card-grid">
          <div class="add-card" @click="showJoinDialog = true">
            <i class="ri-add-circle-line add-icon"></i>
            <span class="add-text">加入新班级</span>
          </div>
          <div
            v-for="cls in joinedClasses"
            :key="cls.id"
            class="class-card"
          >
            <h4>{{ cls.name }}</h4>
            <p>{{ cls.teacherName }} · {{ cls.studentCount || 0 }} 名学生</p>
          </div>
        </div>
      </section>
    </div>

    <!-- 创建班级弹窗 -->
    <div v-if="showCreateDialog" class="dialog-overlay" @click.self="showCreateDialog = false">
      <div class="dialog">
        <h3 class="dialog-title">创建新班级</h3>
        <div class="dialog-body">
          <div class="form-row">
            <label>班级名称</label>
            <input class="form-input" v-model="createForm.name" placeholder="请输入班级名称" />
          </div>
          <div class="spacer-16"></div>
          <div class="form-row">
            <label>班级介绍</label>
            <textarea class="form-textarea" v-model="createForm.description" placeholder="请输入班级介绍" rows="4"></textarea>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn-cancel" @click="showCreateDialog = false">取消</button>
          <button class="btn-confirm" @click="handleCreate">创建</button>
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
import { ref, reactive } from 'vue'
import { classApi } from '@/api/class'
import { useToast } from '@/composables/useToast'

const toast = useToast()

const createdClasses = ref([])
const joinedClasses = ref([])
const showCreateDialog = ref(false)
const showJoinDialog = ref(false)
const joinCode = ref('')
const joinMsg = ref('')
const createForm = reactive({ name: '', description: '' })

async function loadData() {
  try { createdClasses.value = await classApi.getCreatedClasses() } catch {}
  try { joinedClasses.value = await classApi.getJoinedClasses() } catch {}
}

async function handleCreate() {
  if (!createForm.name) return
  try {
    await classApi.createClass(createForm)
    showCreateDialog.value = false
    loadData()
  } catch (e) { toast.error(e?.response?.data?.message || '创建失败') }
}

async function handleJoin() {
  if (!joinCode.value) return
  try {
    await classApi.joinClass(joinCode.value, joinMsg.value)
    showJoinDialog.value = false
    loadData()
  } catch (e) { toast.error(e?.response?.data?.message || '加入失败') }
}

loadData()
</script>

<style scoped>
.class-list-page { min-height: 100%; }
.content-padded { padding: 32px 64px; }

.section-title { font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; }
.spacer-16 { height: 16px; }
.spacer-32 { height: 32px; }

.card-grid { display: flex; flex-wrap: wrap; gap: 16px; }

.add-card, .class-card {
  width: 280px; height: 280px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.1);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  cursor: pointer;
}

.add-card { background: #F5F5F5; }
.add-icon { font-size: 40px; color: #9CA3AF; }
.add-text { font-size: 16px; color: #999; margin-top: 16px; }

.class-card { background: #fff; padding: 24px; align-items: flex-start; justify-content: flex-start; }
.class-card h4 { font-size: 16px; color: #333; margin-bottom: 8px; }
.class-card p { font-size: 14px; color: #666; }
.class-card .code { font-size: 12px; margin-top: 8px; }

/* Dialog */
.dialog-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.dialog { background: #fff; border-radius: 8px; width: 480px; overflow: hidden; }
.dialog-title { padding: 24px 24px 0; font-size: 18px; color: #333; }
.dialog-body { padding: 24px; }
.form-row { display: flex; flex-direction: column; gap: 8px; }
.form-row label { font-size: 14px; color: #666; }
.form-input { width: 100%; height: 40px; padding: 8px 12px; border: 0.8px solid #D1D5DB; border-radius: 4px; font-size: 14px; outline: none; }
.form-textarea { width: 100%; min-height: 80px; padding: 8px 12px; border: 0.8px solid #D1D5DB; border-radius: 4px; font-size: 14px; outline: none; resize: vertical; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif; }
.dialog-footer { display: flex; justify-content: flex-end; gap: 12px; padding: 0 24px 24px; }
.btn-cancel { padding: 8px 24px; border: 0.8px solid #D1D5DB; border-radius: 4px; background: #fff; font-size: 14px; cursor: pointer; }
.btn-confirm { padding: 8px 24px; border: none; border-radius: 4px; background: #2563EB; color: #fff; font-size: 14px; cursor: pointer; }
</style>
