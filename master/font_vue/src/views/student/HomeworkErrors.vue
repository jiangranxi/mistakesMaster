<template>
  <div class="page">
    <div class="sub-nav">
      <span class="sub-tab" @click="$router.push('/student/homework/latest')">最新作业</span>
      <span class="sub-tab" @click="$router.push('/student/homework/history')">历次作业</span>
      <span class="sub-tab active">错题集</span>
    </div>
    <div class="content-body">
      <!-- 搜索区 -->
      <div class="search-row">
        <div class="filter-item">
          <label>作业名称:</label>
          <input type="text" v-model="filters.name" placeholder="作业名称" class="filter-input" />
        </div>
        <div class="filter-item">
          <label>书目名称:</label>
          <input type="text" v-model="filters.book" placeholder="书目名称" class="filter-input" />
        </div>
        <div class="filter-item">
          <label>提交时间:</label>
          <DatePicker v-model="filters.startTime" placeholder="开始时间" style="width: 200px" />
          <DatePicker v-model="filters.endTime" placeholder="结束时间" style="width: 200px" />
        </div>
        <span class="search-icon"><i class="ri-search-line"></i></span>
      </div>
      <div class="filter-row">
        <label class="filter-label">学 科:</label>
      </div>

      <!-- 表格 -->
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th class="col-index">序号</th>
              <th class="col-name sortable" @click="toggleSort('name')">作业名称<span class="sort-arrows" :data-sort="sortState['name']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-source sortable" @click="toggleSort('source')">作业来源<span class="sort-arrows" :data-sort="sortState['source']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-subject sortable" @click="toggleSort('subject')">学科<span class="sort-arrows" :data-sort="sortState['subject']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-time sortable" @click="toggleSort('submitTime')">提交时间<span class="sort-arrows" :data-sort="sortState['submitTime']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-error sortable" @click="toggleSort('errorNo')">错题序号<span class="sort-arrows" :data-sort="sortState['errorNo']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-action">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!list.length" class="empty-row"><td colspan="7">暂无数据</td></tr>
            <tr v-for="(item, idx) in list" :key="item.id">
              <td>{{ idx + 1 }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.source }}</td>
              <td>{{ item.subject }}</td>
              <td>{{ item.submitTime }}</td>
              <td>{{ item.errorSeq }}</td>
              <td><a href="#" @click.prevent="viewDetail(item)">查看</a></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="spacer-16"></div>

      <!-- 分页 -->
      <PaginationBar
        variant="student"
        :page="page"
        :pageSize="pageSize"
        :totalPages="totalPages"
        @page-change="changePage"
        @page-size-change="val => { pageSize = val; loadData() }"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { homeworkApi } from '@/api/homework'
import DatePicker from '@/components/DatePicker.vue'
import PaginationBar from '@/components/PaginationBar.vue'

const list = ref([])
const page = ref(1)
const pageSize = ref(15)
const totalPages = ref(0)
const sortState = reactive({ name: 'asc', source: 'asc', subject: 'asc', submitTime: 'asc', errorNo: 'asc' })
function toggleSort(key) { sortState[key] = sortState[key] === 'asc' ? 'desc' : 'asc' }
const filters = reactive({ name: '', book: '', startTime: '', endTime: '' })

async function loadData() {
  try {
    const res = await homeworkApi.getErrors({
      page: page.value, pageSize: pageSize.value,
      ...filters
    })
    if (res) {
      list.value = res.list || []
      totalPages.value = Math.ceil((res.total || 0) / pageSize.value) || 0
    }
  } catch {}
}

function changePage(p) {
  if (p >= 1 && p <= totalPages.value) { page.value = p; loadData() }
}

function viewDetail(item) { /* TODO */ }

loadData()
</script>

<style scoped>
.page { display: flex; flex-direction: column; flex: 1; min-height: 0; }

.sub-nav {
  height: 40px;
  background: #005538;
  display: flex;
  align-items: center;
  padding-left: 200px;
  gap: 4px;
  flex-shrink: 0;
}
.sub-tab {
  font-size: 13px; color: #fff; cursor: pointer;
  padding: 2px 18px; line-height: 28px;
  border-radius: 9999px;
  display: flex; align-items: center;
}
.sub-tab:hover:not(.active) { background: rgba(255,255,255,0.15); }
.sub-tab.active {
  background: #FF6600;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
}

.content-body { padding: 32px 100px; flex: 1; overflow-y: auto; }

/* 搜索 */
.search-row { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
.filter-item { display: flex; align-items: center; gap: 10px; }
.filter-item label { font-size: 14px; color: #333; white-space: nowrap; }
.filter-input {
  width: 200px; height: 36px;
  border: 1px solid #D1D5DB; padding: 0 12px;
  font-size: 14px; color: #333; outline: none;
}
.filter-input::placeholder { color: #999; }
.filter-input:focus { box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }
.search-icon { width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; cursor: pointer; }
.search-icon i { font-size: 22px; color: #6B7280; }
.filter-row { display: flex; align-items: center; margin-bottom: 24px; }
.filter-label { font-size: 14px; color: #333; }

/* 表格 */
.table-wrapper { border: 1px solid #E5E7EB; }
.data-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.data-table th {
  height: 49px;
  background: #F3F4F6;
  font-size: 14px;
  font-family: 'SourceHanSans-Bold', 'Noto Sans SC', sans-serif;
  color: #333;
  padding: 12px 16px;
  border: 1px solid #E5E7EB;
  text-align: left;
}
.data-table th.sortable { color: #165DFF; cursor: pointer; }
.data-table th.sortable i { font-size: 16px; }
.col-index { width: 90px; }
.col-name { width: 270px; }
.col-source { width: 210px; }
.col-subject { width: 110px; }
.col-time { width: 170px; }
.col-error { width: 170px; }
.col-action { width: 110px; }

.data-table td {
  font-size: 14px; color: #333;
  padding: 12px 16px;
  border: 1px solid #E5E7EB;
}
.spacer-16 { height: 16px; }
.data-table td a { color: #2B7CD3; text-decoration: none; }
.empty-row td { text-align: center; color: #999; padding: 32px 16px; height: 86px; }
</style>
