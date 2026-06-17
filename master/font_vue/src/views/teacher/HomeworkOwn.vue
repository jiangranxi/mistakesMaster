<template>
  <div class="page">
    <div class="sub-nav">
      <span class="sub-tab" @click="$router.push('/teacher/homework/cloud')">云作业/试卷</span>
      <span class="sub-tab" @click="$router.push('/teacher/homework/papers')">我的组卷</span>
      <span class="sub-tab active">自有作业/试卷</span>
      <span class="sub-tab" @click="showPermissionModal = true">扩展组卷</span>
    </div>
    <div class="content-area">
      <!-- 左侧导航栏 -->
      <div class="left-sidebar">
        <div class="sidebar-item">
          <div class="sidebar-item-header">
            <i class="ri-file-copy-2-line"></i>
            <span>组卷作业</span>
          </div>
          <p class="sidebar-empty">没有作业/试卷</p>
        </div>
      </div>

      <!-- 中间章节目录 -->
      <div class="middle-panel">
        <h4 class="panel-title">章节目录</h4>
        <p class="panel-empty">没有章节</p>
      </div>

      <!-- 右侧内容区域 -->
      <div class="right-content">
        <p class="empty-text">没有作业/试卷</p>
      </div>
    </div>

    <!-- 扩展组卷权限弹窗 -->
    <div v-if="showPermissionModal" class="modal-overlay" @click.self="showPermissionModal = false">
      <div class="modal-dialog">
        <div class="modal-header">注意</div>
        <div class="modal-body">
          <div class="warning-icon"><i class="ri-error-warning-fill"></i></div>
          <div class="modal-text">
            <p class="modal-title-row">
              <span>此模块需要授权才能使用！</span>
              <span>你还未获得权限！</span>
            </p>
            <p>如果需要使用此项功能，请购买使用权限！</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-back" @click="showPermissionModal = false">返回</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showPermissionModal = ref(false)
</script>

<style scoped>
.page { display: flex; flex-direction: column; height: 100%; }

.sub-nav {
  height: 40px;
  background: #005538;
  display: flex;
  align-items: center;
  padding-left: 336px;
  gap: 24px;
  flex-shrink: 0;
}
.sub-tab {
  font-size: 14px;
  color: #fff;
  cursor: pointer;
  padding: 6px 16px;
  border-radius: 9999px;
}
.sub-tab.active { background: #FF6600; }

.content-area {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.left-sidebar {
  width: 200px;
  padding: 16px 0;
  flex-shrink: 0;
  overflow-y: auto;
}
.sidebar-item { padding: 12px 16px; }
.sidebar-item-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  color: #333;
}
.sidebar-item-header i { font-size: 18px; color: #6B7280; }
.sidebar-empty { font-size: 14px; color: #666; margin-top: 8px; }

.middle-panel {
  width: 240px;
  background: #EEE;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}
.panel-title {
  font-size: 16px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  color: #333;
  padding: 12px 16px;
  margin: 0;
}
.panel-empty {
  font-size: 14px;
  color: #666;
  text-align: center;
  padding: 24px 16px;
}

.right-content {
  flex: 1;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.empty-text { font-size: 14px; color: #666; }

/* 权限弹窗 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-dialog {
  width: 600px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 8px 10px rgba(0,0,0,0.1), 0 20px 25px rgba(0,0,0,0.1);
}
.modal-header {
  padding: 16px 24px;
  font-size: 18px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  color: #333;
}
.modal-body {
  padding: 32px 24px;
  display: flex;
  align-items: center;
  gap: 24px;
}
.warning-icon {
  width: 60px;
  height: 60px;
  background: #FF6600;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.warning-icon i { font-size: 32px; color: #fff; }
.modal-text { font-size: 16px; color: #333; }
.modal-title-row { display: flex; gap: 8px; margin-bottom: 8px; }
.modal-footer {
  padding: 16px 24px;
  display: flex;
  justify-content: flex-end;
}
.btn-back {
  width: 80px;
  height: 36px;
  background: #337AB7;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}
</style>
