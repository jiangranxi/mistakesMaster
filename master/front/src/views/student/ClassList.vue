<template>
  <div class="class-page">
    <div class="card">
      <h3 class="page-title">我的班级</h3>
      <div class="class-grid">
        <div class="class-card" v-for="cls in classList" :key="cls.id">
          <div class="card-cover">📚</div>
          <div class="card-info">
            <h4>{{ cls.name }}</h4>
            <p>{{ cls.description || '班级暂无介绍' }}</p>
            <span class="student-count">{{ cls.studentCount || 0 }} 名学生</span>
          </div>
        </div>
        <!-- 加入新班级卡片 -->
        <div class="class-card join-card" @click="showJoinModal = true">
          <div class="card-cover">➕</div>
          <div class="card-info">
            <h4>加入新班级</h4>
          </div>
        </div>
      </div>
    </div>

    <!-- 加入班级弹窗 -->
    <JoinClassModal v-if="showJoinModal" @close="showJoinModal = false" @joined="handleJoined" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import JoinClassModal from './JoinClassModal.vue'

const showJoinModal = ref(false)
const classList = ref([])

function handleJoined() {
  showJoinModal.value = false
  // 刷新列表
}
</script>

<style scoped>
.page-title { font-size: 18px; margin-bottom: 20px; }
.class-grid { display: flex; gap: 24px; flex-wrap: wrap; }
.class-card { width: 280px; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,.06); overflow: hidden; cursor: pointer; transition: transform .2s, box-shadow .2s; }
.class-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,.1); }
.card-cover { height: 120px; background: #f0f5ff; display: flex; align-items: center; justify-content: center; font-size: 48px; }
.card-info { padding: 16px; }
.card-info h4 { font-size: 16px; margin-bottom: 8px; }
.card-info p { font-size: 13px; color: #999; margin-bottom: 8px; }
.student-count { font-size: 12px; color: #4A90D9; }
.join-card .card-cover { background: #fafafa; }
.join-card .card-info h4 { color: #4A90D9; }
</style>
