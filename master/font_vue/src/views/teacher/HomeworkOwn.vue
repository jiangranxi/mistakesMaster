<template>
  <div class="homework-own-page">
    <!-- 二级页签 -->
    <div class="sub-nav">
      <span class="sub-tab" @click="$router.push('/teacher/homework/cloud')">云作业/试卷</span>
      <span class="sub-tab" @click="$router.push('/teacher/homework/papers')">我的组卷</span>
      <span class="sub-tab active">自有作业/试卷</span>
      <span class="sub-tab">扩展组卷</span>
    </div>

    <div class="content-area">
      <!-- 左侧导航 -->
      <div class="left-sidebar">
        <div class="sidebar-item">
          <div class="sidebar-item-header">
            <i class="ri-file-list-3-line"></i>
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

      <!-- 右侧内容 -->
      <div class="right-content">
        <p class="empty-text">没有作业/试卷</p>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.homework-own-page { display: flex; flex-direction: column; height: 100%; }

.sub-nav {
  height: 40px;
  background: #005538;
  display: flex;
  align-items: center;
  padding: 0 40px;
  gap: 24px;
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
  padding: 16px;
  border-right: 1px solid #E5E7EB;
}
.sidebar-item-header {
  display: flex; align-items: center; gap: 8px;
  font-size: 16px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333;
}
.sidebar-empty { font-size: 14px; color: #666; margin-top: 8px; }

.middle-panel {
  width: 240px;
  background: #EEE;
  padding: 12px 16px;
}
.panel-title { font-size: 16px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; }
.panel-empty { font-size: 14px; color: #666; text-align: center; margin-top: 24px; }

.right-content {
  flex: 1;
  display: flex; align-items: center; justify-content: center;
  padding: 24px;
}
.empty-text { font-size: 14px; color: #666; }
</style>
