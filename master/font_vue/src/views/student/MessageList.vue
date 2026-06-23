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
        <tr v-if="!list.length" class="empty-row"><td :colspan="7">暂无数据</td></tr>
        <tr v-for="(item, idx) in list" :key="item.id">
          <td>{{ idx + 1 }}</td><td>{{ item.from }}</td><td>{{ item.role }}</td>
          <td>{{ item.content }}</td><td>{{ item.time }}</td>
          <td>{{ item.read ? '已读' : '未读' }}</td>
          <td><a href="#" @click.prevent="markRead(item)">标记已读</a></td>
        </tr>
      </tbody>
    </table>
    <div class="spacer-24"></div>
    <PaginationBar
      variant="student"
      :page="page"
      :pageSize="pageSize"
      :totalPages="totalPages"
      @page-change="changePage"
      @page-size-change="val => { pageSize = val }"
    />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { messageApi } from '@/api/message'
import PaginationBar from '@/components/PaginationBar.vue'
const list = ref([])
const page = ref(1)
const pageSize = ref(15)
const totalPages = ref(0)
const sortState = reactive({ from: 'asc', role: 'asc', content: 'asc', time: 'asc' })
function toggleSort(key) { sortState[key] = sortState[key] === 'asc' ? 'desc' : 'asc' }
function changePage(p) {
  if (p >= 1 && p <= totalPages.value) { page.value = p }
}
async function loadData() { try { const res = await messageApi.getMessages(); list.value = res.list || [] } catch {} }
async function markRead(item) { try { await messageApi.markRead(item.id); item.read = true } catch {} }
loadData()
</script>

<style scoped>
.page-padded { padding: 32px 64px; }
.page-title { font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; }
.spacer-16 { height: 16px; }
.spacer-24 { height: 24px; }
.sortable { color: #2B7CD3; cursor: pointer; }
</style>
