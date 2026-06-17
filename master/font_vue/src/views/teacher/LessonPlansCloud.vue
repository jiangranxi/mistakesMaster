<template>
  <div class="page">
    <div class="sub-nav">
      <span class="sub-tab active">云教案</span>
      <span class="sub-tab" @click="$router.push('/teacher/lesson-plans/own')">自有教案</span>
    </div>
    <div class="page-padded">
      <table class="data-table">
        <thead><tr><th>序号</th><th>教案名称</th><th>学科</th><th>来源</th><th>操作</th></tr></thead>
        <tbody><tr class="empty-row"><td colspan="5">暂无数据</td></tr></tbody>
      </table>
    </div>
  </div>
</template>
<style scoped>
.page { display: flex; flex-direction: column; height: 100%; }
.sub-nav { height: 40px; background: #005538; display: flex; align-items: center; padding-left: 336px; gap: 24px; }
.sub-tab { font-size: 14px; color: #fff; cursor: pointer; padding: 6px 16px; border-radius: 9999px; }
.sub-tab.active { background: #FF6600; }
.page-padded { padding: 32px 64px; flex: 1; }
</style>
