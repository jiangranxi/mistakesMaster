<template>
  <div class="page-padded">
    <h3 class="page-title">消息管理</h3>
    <div class="spacer-16"></div>
    <table class="data-table">
      <thead>
        <tr>
          <th style="width:80px">序号</th>
          <th style="width:120px" class="sortable">来自 <i class="ri-arrow-up-down-line"></i></th>
          <th style="width:120px" class="sortable">身份 <i class="ri-arrow-up-down-line"></i></th>
          <th class="sortable">消息内容 <i class="ri-arrow-up-down-line"></i></th>
          <th style="width:160px" class="sortable">时间 <i class="ri-arrow-up-down-line"></i></th>
          <th style="width:100px">状态</th>
          <th style="width:100px">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr class="empty-row"><td :colspan="7">暂无数据</td></tr>
      </tbody>
    </table>

    <div class="spacer-24"></div>

    <!-- 分页 -->
    <div class="pagination">
      <button>首页</button>
      <button>上一页</button>
      <button>下一页</button>
      <button>尾页</button>
      <input class="page-input" value="0" />
      <span>0/0</span>
      <select class="page-size">
        <option>15</option>
        <option>30</option>
        <option>50</option>
      </select>
    </div>
  </div>
</template>
<style scoped>
.page-padded { padding: 32px 64px; }
.page-title { font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; }
.spacer-16 { height: 16px; }
.spacer-24 { height: 24px; }
.sortable { color: #2B7CD3; cursor: pointer; }
</style>
