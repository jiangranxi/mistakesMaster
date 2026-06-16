<template>
  <div class="class-list-page">
    <!-- 我创建的班级 -->
    <section class="section">
      <h3 class="section-title">我创建的班级</h3>
      <div class="class-grid">
        <div v-for="cls in createdClasses" :key="cls.id" class="class-card">
          <div class="card-cover">{{ cls.name?.charAt(0) }}</div>
          <div class="card-info">
            <div class="card-name">{{ cls.name }}</div>
            <div class="card-count">{{ cls.studentCount || 0 }}名学生</div>
          </div>
        </div>
        <!-- 创建新班级卡片 -->
        <div class="class-card create-card" @click="showCreateModal = true">
          <div class="create-icon">+</div>
          <div class="create-text">创建新班级</div>
        </div>
      </div>
    </section>

    <!-- 我加入的班级 -->
    <section class="section">
      <h3 class="section-title">我加入的班级</h3>
      <div class="class-grid">
        <div v-for="cls in joinedClasses" :key="cls.id" class="class-card">
          <div class="card-cover">{{ cls.name?.charAt(0) }}</div>
          <div class="card-info">
            <div class="card-name">{{ cls.name }}</div>
            <div class="card-count">{{ cls.studentCount || 0 }}名学生</div>
          </div>
        </div>
        <!-- 加入班级卡片 -->
        <div class="class-card create-card" @click="showJoinModal = true">
          <div class="create-icon">+</div>
          <div class="create-text">加入班级</div>
        </div>
      </div>
    </section>

    <!-- 创建班级弹窗 -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal" style="width:500px">
        <div class="modal-header">
          <h4>创建班级</h4>
          <button class="btn btn-sm" @click="showCreateModal = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">班级名称</label>
            <input v-model="createForm.name" class="form-input" placeholder="请输入班级名称" />
          </div>
          <div class="form-group">
            <label class="form-label">班级介绍</label>
            <textarea v-model="createForm.description" class="form-textarea" placeholder="请输入班级介绍" rows="4"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn" @click="showCreateModal = false">关闭</button>
          <button class="btn btn-primary" @click="handleCreate">创建</button>
        </div>
      </div>
    </div>

    <!-- 加入班级弹窗 -->
    <div v-if="showJoinModal" class="modal-overlay" @click.self="showJoinModal = false">
      <div class="modal" style="width:500px">
        <div class="modal-header">
          <h4>加入班级</h4>
          <button class="btn btn-sm" @click="showJoinModal = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">班级号</label>
            <input v-model="joinForm.classCode" class="form-input" placeholder="请输入班级号" />
          </div>
          <div class="form-group">
            <label class="form-label">验证消息</label>
            <textarea v-model="joinForm.message" class="form-textarea" placeholder="请输入验证消息（选填）" rows="3"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn" @click="showJoinModal = false">关闭</button>
          <button class="btn btn-primary" @click="handleJoin">加入</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { classApi } from '@/api/class'

const createdClasses = ref([])
const joinedClasses = ref([])
const showCreateModal = ref(false)
const showJoinModal = ref(false)
const createForm = reactive({ name: '', description: '' })
const joinForm = reactive({ classCode: '', message: '' })

onMounted(async () => {
  try {
    const [created, joined] = await Promise.all([
      classApi.getMyCreatedClasses(),
      classApi.getMyJoinedClasses()
    ])
    createdClasses.value = created?.list || []
    joinedClasses.value = joined?.list || []
  } catch (e) { /* 加载失败 */ }
})

async function handleCreate() {
  if (!createForm.name) { alert('请输入班级名称'); return }
  try {
    await classApi.createClass(createForm)
    showCreateModal.value = false
    // 刷新列表
    const res = await classApi.getMyCreatedClasses()
    createdClasses.value = res?.list || []
  } catch (e) { alert(e.message || '创建失败') }
}

async function handleJoin() {
  if (!joinForm.classCode) { alert('请输入班级号'); return }
  try {
    await classApi.joinClass(joinForm.classCode)
    showJoinModal.value = false
    const res = await classApi.getMyJoinedClasses()
    joinedClasses.value = res?.list || []
  } catch (e) { alert(e.message || '加入失败') }
}
</script>

<style scoped>
.section { margin-bottom: 32px; }
.section-title { font-size: 16px; margin-bottom: 16px; color: #333; }
.class-grid { display: flex; flex-wrap: wrap; gap: 20px; }
.class-card {
  width: 280px; height: 280px; background: #fff; border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,.06); display: flex; flex-direction: column;
  cursor: pointer; transition: box-shadow .2s;
}
.class-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,.1); }
.card-cover {
  height: 180px; background: #4A90D9; display: flex; align-items: center;
  justify-content: center; font-size: 48px; color: #fff; border-radius: 8px 8px 0 0;
}
.card-info { padding: 16px; }
.card-name { font-size: 15px; font-weight: 500; }
.card-count { font-size: 12px; color: #999; margin-top: 4px; }
.create-card {
  border: 2px dashed #d9d9d9; background: transparent;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.create-card:hover { border-color: #4A90D9; }
.create-icon { font-size: 40px; color: #d9d9d9; }
.create-card:hover .create-icon { color: #4A90D9; }
.create-text { font-size: 14px; color: #999; margin-top: 8px; }
</style>
