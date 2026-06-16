<template>
  <div class="homework-page">
    <div class="card">
      <!-- 三级页签 -->
      <div class="tabs">
        <div class="tab" :class="{ active: activeTab === 'cloud' }" @click="activeTab = 'cloud'">云作业/试卷</div>
        <div class="tab" :class="{ active: activeTab === 'mypaper' }" @click="activeTab = 'mypaper'">我的组卷</div>
        <div class="tab" :class="{ active: activeTab === 'own' }" @click="activeTab = 'own'">自有作业/试卷</div>
        <div class="tab" :class="{ active: activeTab === 'extend' }" @click="activeTab = 'extend'">扩展组卷</div>
      </div>

      <!-- 二级页签（自有作业下的子页签） -->
      <div v-if="activeTab === 'own'" class="sub-tabs">
        <div class="tab" :class="{ active: subTab === 'cloud2' }" @click="subTab = 'cloud2'">云作业/试卷</div>
        <div class="tab" :class="{ active: subTab === 'mypaper2' }" @click="subTab = 'mypaper2'">我的组卷</div>
        <div class="tab active">自有作业/试卷</div>
        <div class="tab" :class="{ active: subTab === 'extend2' }" @click="subTab = 'extend2'">扩展组卷</div>
      </div>

      <div class="layout">
        <!-- 左侧导航 -->
        <div class="sidebar">
          <div v-for="item in sidebarItems" :key="item.id" class="sidebar-item" :class="{ active: selectedSide === item.id }" @click="selectedSide = item.id">
            {{ item.name }}
          </div>
          <div v-if="sidebarItems.length === 0" class="empty-state" style="padding:20px">暂无分类</div>
        </div>

        <!-- 中间章节目录 -->
        <div class="chapter-panel">
          <h4 class="panel-title">章节目录</h4>
          <div v-for="ch in chapters" :key="ch.id" class="chapter-item">
            {{ ch.name }}
          </div>
          <div v-if="chapters.length === 0" class="empty-state" style="padding:20px">请先选择分类</div>
        </div>

        <!-- 右侧内容区 -->
        <div class="content-area">
          <div class="content-toolbar">
            <button class="btn btn-sm">网格视图</button>
            <button class="btn btn-sm">跨书跨章勾选试卷</button>
          </div>
          <div class="empty-state">
            请从左侧选择分类和章节查看内容
          </div>
        </div>
      </div>

      <!-- 扩展组卷权限提示弹窗 -->
      <div v-if="showPermissionModal" class="modal-overlay" @click.self="showPermissionModal = false">
        <div class="modal" style="width:420px">
          <div class="modal-body" style="text-align:center;padding:40px">
            <div style="font-size:48px;margin-bottom:16px">⚠️</div>
            <p style="font-size:16px;margin-bottom:8px">权限提示</p>
            <p style="color:#999">您暂无扩展组卷权限，请联系管理员</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-primary" @click="showPermissionModal = false">返回</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('own')
const subTab = ref('')
const selectedSide = ref('')
const sidebarItems = ref([])
const chapters = ref([])
const showPermissionModal = ref(false)

// 当切换到扩展组卷时检查权限
import { watch } from 'vue'
watch(activeTab, (val) => {
  if (val === 'extend') showPermissionModal.value = true
})
</script>

<style scoped>
.tabs { margin-bottom: 12px; }
.sub-tabs { margin-bottom: 12px; }
.layout { display: flex; gap: 16px; min-height: 300px; }
.sidebar { width: 200px; border-right: 1px solid #f0f0f0; }
.sidebar-item { padding: 10px 16px; cursor: pointer; border-radius: 4px; }
.sidebar-item:hover, .sidebar-item.active { background: #f0f5ff; color: #4A90D9; }
.chapter-panel { width: 240px; border-right: 1px solid #f0f0f0; }
.panel-title { padding: 10px 16px; font-size: 14px; color: #333; border-bottom: 1px solid #f0f0f0; }
.chapter-item { padding: 8px 16px; cursor: pointer; font-size: 13px; color: #666; }
.chapter-item:hover { color: #4A90D9; }
.content-area { flex: 1; }
.content-toolbar { display: flex; gap: 8px; margin-bottom: 16px; }
</style>
