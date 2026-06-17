<template>
  <div class="page">
    <div class="sub-nav">
      <span class="sub-tab" @click="$router.push('/teacher/homework/cloud')">云作业/试卷</span>
      <span class="sub-tab" @click="$router.push('/teacher/homework/papers')">我的组卷</span>
      <span class="sub-tab active">自有作业/试卷</span>
      <span class="sub-tab">扩展组卷</span>
    </div>
    <div class="empty-content">
      <p>云作业/试卷列表页</p>
    </div>
  </div>
</template>

<style scoped>
.page { display: flex; flex-direction: column; height: 100%; }
.sub-nav { height: 40px; background: #005538; display: flex; align-items: center; padding: 0 40px; gap: 24px; }
.sub-tab { font-size: 14px; color: #fff; cursor: pointer; padding: 6px 16px; border-radius: 9999px; }
.sub-tab.active { background: #FF6600; }
.empty-content { flex: 1; display: flex; align-items: center; justify-content: center; color: #666; }
</style>
