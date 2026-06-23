<template>
  <div class="page-padded">
    <h3 class="page-title">消息管理</h3>
    <div class="spacer-16"></div>
    <table class="data-table">
      <thead>
        <tr>
          <th style="width:80px">序号</th>
          <th style="width:120px" class="sortable" @click="toggleSort('from')">来自<span class="sort-arrows" :data-sort="sortState['from']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
          <th style="width:120px" class="sortable" @click="toggleSort('role')">身份<span class="sort-arrows" :data-sort="sortState['role']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
          <th class="sortable" @click="toggleSort('content')">消息内容<span class="sort-arrows" :data-sort="sortState['content']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
          <th style="width:160px" class="sortable" @click="toggleSort('time')">时间<span class="sort-arrows" :data-sort="sortState['time']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
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
    <PaginationBar
      variant="teacher"
      :page="page"
      :pageSize="pageSize"
      :totalPages="totalPages"
      @page-change="changePage"
      @page-size-change="val => { pageSize = val }"
    />
  </div>
</template>
<script setup>
import { ref, reactive, computed } from 'vue'
import PaginationBar from '@/components/PaginationBar.vue'
const sortState = reactive({ from: 'asc', role: 'asc', content: 'asc', time: 'asc' })
function toggleSort(key) { sortState[key] = sortState[key] === 'asc' ? 'desc' : 'asc' }
const page = ref(1)
const pageSize = ref(15)
const totalPages = ref(0)
function changePage(p) {
  if (p >= 1 && p <= totalPages.value) { page.value = p }
}
</script>

<style scoped>
.page-padded { padding: 32px 64px; }
.page-title { font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; }
.spacer-16 { height: 16px; }
.spacer-24 { height: 24px; }
.sortable { color: #2B7CD3; cursor: pointer; }
</style>
