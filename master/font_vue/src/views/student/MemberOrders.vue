<template>
  <div class="member-page">
    <div class="sidebar">
      <h3 class="sidebar-title">会员中心</h3>
      <div class="menu-list">
        <div class="menu-item" @click="$router.push('/student/member')">基本设置</div>
        <div class="menu-item" @click="$router.push('/student/member/security')">安全设置</div>
        <div class="menu-item active">我的订单</div>
      </div>
    </div>
    <div class="main-area">
      <table class="data-table">
        <thead><tr><th>序号</th><th>订单编号</th><th>产品名称</th><th>金额</th><th>时间</th><th>状态</th></tr></thead>
        <tbody><tr class="empty-row"><td colspan="6">暂无数据</td></tr></tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.member-page { display: flex; height: 100%; }
.sidebar { width: 200px; background: #EEE; padding-top: 16px; flex-shrink: 0; }
.sidebar-title { padding: 16px; font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; }
.menu-list { padding: 8px 0; }
.menu-item { padding: 8px 16px; font-size: 14px; color: #2B7CD3; cursor: pointer; }
.menu-item.active { background: #337AB7; color: #fff; }
.main-area { flex: 1; padding: 32px; }
</style>
