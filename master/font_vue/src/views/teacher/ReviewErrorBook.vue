<template>
  <div class="page">
    <!-- 页签栏 -->
    <div class="tab-bar">
      <span class="tab-item" @click="$router.push('/teacher/review/homework')">网络作业讲评报告</span>
      <span class="tab-item active">错题本讲评报告</span>
    </div>

    <div class="content-body">
      <!-- 筛选区域 -->
      <div class="filter-area">
        <div class="filter-row">
          <div class="filter-item">
            <label>讲评报告:</label>
            <input type="text" v-model="filters.report" placeholder="讲评报告" class="filter-input" />
          </div>
          <div class="filter-item">
            <label>书目名称:</label>
            <input type="text" v-model="filters.book" placeholder="书目名称" class="filter-input" />
          </div>
          <div class="filter-item">
            <label>时间:</label>
            <DatePicker v-model="filters.startTime" placeholder="开始时间" style="width: 180px" />
            <DatePicker v-model="filters.endTime" placeholder="结束时间" style="width: 180px" />
            <span class="search-btn"><i class="ri-search-line"></i></span>
          </div>
        </div>
        <div class="filter-row">
          <label class="filter-label">学 科:</label>
          <div class="tag-group">
            <span class="subject-tag" v-for="s in subjects" :key="s" :class="{ active: filters.subject === s }" @click="filters.subject = filters.subject === s ? '' : s">{{ s }}</span>
          </div>
        </div>
        <div class="filter-row">
          <label class="filter-label">班 级:</label>
          <div class="tag-group">
            <span class="subject-tag" v-for="c in classes" :key="c" :class="{ active: filters.class === c }" @click="filters.class = filters.class === c ? '' : c">{{ c }}</span>
          </div>
        </div>
      </div>

      <!-- 表格 -->
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th class="col-index">序号</th>
              <th class="col-date sortable" @click="toggleSort('date')">日期<span class="sort-arrows" :data-sort="sortState['date']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-report sortable" @click="toggleSort('report')">讲评报告<span class="sort-arrows" :data-sort="sortState['report']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-book sortable" @click="toggleSort('book')">书目名称<span class="sort-arrows" :data-sort="sortState['book']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-score sortable" @click="toggleSort('max')">最高分<span class="sort-arrows" :data-sort="sortState['max']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-score sortable" @click="toggleSort('min')">最低分<span class="sort-arrows" :data-sort="sortState['min']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-score sortable" @click="toggleSort('avg')">平均数<span class="sort-arrows" :data-sort="sortState['avg']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-score sortable" @click="toggleSort('median')">中位数<span class="sort-arrows" :data-sort="sortState['median']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-mode sortable" @click="toggleSort('mode')">众数<span class="sort-arrows" :data-sort="sortState['mode']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-action">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, i) in tableData" :key="i">
              <td>{{ row.seq || i + 1 }}</td>
              <td>{{ row.date }}</td>
              <td>{{ row.report }}</td>
              <td>{{ row.book }}</td>
              <td>{{ row.max }}</td>
              <td>{{ row.min }}</td>
              <td>{{ row.avg }}</td>
              <td>{{ row.median }}</td>
              <td>{{ row.mode }}</td>
              <td class="action-cell">
                <a href="javascript:void(0)">讲评报告</a>
                <a href="javascript:void(0)">讲评概述</a>
              </td>
            </tr>
            <tr v-if="!tableData.length" class="empty-row">
              <td colspan="10">暂无数据</td>
            </tr>
          </tbody>
        </table>
      </div>

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
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import DatePicker from '@/components/DatePicker.vue'
import PaginationBar from '@/components/PaginationBar.vue'

const filters = reactive({
  report: '',
  book: '',
  startTime: '',
  endTime: '',
  subject: '',
  class: ''
})

const subjects = ref([])
const classes = ref([])
const tableData = ref([])
const page = ref(1)
const pageSize = ref(15)
const totalPages = computed(() => Math.ceil(tableData.value.length / pageSize.value) || 0)
const sortState = reactive({ date: 'asc', report: 'asc', book: 'asc', max: 'asc', min: 'asc', avg: 'asc', median: 'asc', mode: 'asc' })
function toggleSort(key) { sortState[key] = sortState[key] === 'asc' ? 'desc' : 'asc' }
function changePage(p) {
  if (p >= 1 && p <= totalPages.value) { page.value = p }
}
</script>

<style scoped>
.page { flex: 1; min-height: 0; display: flex; flex-direction: column; }

/* 页签栏 — 卡片化标签，左右对齐内容区，中间融合 */
.tab-bar {
  display: flex;
  align-items: center;
  padding: 16px 64px 0;
  height: 49px;
  background: #fff;
}
.tab-item {
  flex: 1;
  text-align: center;
  padding: 12px 24px;
  font-size: 16px;
  font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif;
  color: #6B7280;
  cursor: pointer;
  border: 1px solid #E5E7EB;
  background: #fff;
}
/* 未选中：隐藏顶部线和外边线 */
.tab-item:first-child {
  border-right: none;
  border-radius: 4px 0 0 0;
  border-top-color: transparent;
  border-left-color: transparent;
}
.tab-item:last-child {
  border-radius: 0 4px 0 0;
  border-top-color: transparent;
  border-right-color: transparent;
}
/* 选中：显示全部边线 */
.tab-item.active {
  color: #FF7700;
  border-color: #E5E7EB;
  border-bottom-color: #fff;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
}
.tab-item:first-child.active {
  border-left-color: #E5E7EB;
  border-top-color: #E5E7EB;
}
.tab-item:last-child.active {
  border-right-color: #E5E7EB;
  border-top-color: #E5E7EB;
}

.content-body { padding: 24px 64px 32px; flex: 1; overflow-y: auto; }

/* 筛选区域 */
.filter-area { margin-bottom: 24px; }
.filter-row {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  gap: 24px;
  flex-wrap: wrap;
}
.filter-item {
  display: flex;
  align-items: center;
  gap: 12px;
}
.filter-item label {
  font-size: 14px;
  color: #333;
  white-space: nowrap;
}
.filter-input {
  width: 180px;
  height: 36px;
  border: 1px solid #E5E7EB;
  padding: 0 12px;
  font-size: 14px;
  color: #333;
  outline: none;
}
.filter-input::placeholder { color: #999; }
.filter-input:focus { box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }
.search-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.search-btn i { font-size: 22px; color: #6B7280; }

.filter-label {
  font-size: 14px;
  color: #333;
  text-align: right;
  min-width: 61px;
}
.tag-group { display: flex; gap: 12px; flex-wrap: wrap; }
.subject-tag {
  font-size: 14px;
  color: #333;
  cursor: pointer;
  padding: 4px 16px;
  border-radius: 9999px;
}
.subject-tag.active { background: #FF6600; color: #fff; }

/* 表格 */
.table-wrapper { border: 1px solid #E5E7EB; }
.data-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.data-table th {
  height: 38px;
  background: #F5F5F5;
  font-size: 14px;
  font-family: 'SourceHanSans-Bold', 'Noto Sans SC', sans-serif;
  color: #333;
  padding: 8px 16px;
  border: 1px solid #E5E7EB;
  text-align: left;
}
.data-table th.sortable i { color: #6B7280; margin-left: 4px; font-size: 14px; }
.col-index { width: 80px; }
.col-date { width: 100px; }
.col-report { width: 140px; }
.col-book { width: 140px; }
.col-score { width: 120px; }
.col-mode { width: 100px; }
.col-action { width: 190px; }

.data-table td {
  height: 37px;
  font-size: 14px;
  color: #333;
  padding: 8px 16px;
  border: 1px solid #E5E7EB;
}
.action-cell { display: flex; gap: 8px; }
.action-cell a { color: #2B7CD3; text-decoration: none; font-size: 14px; }
.empty-row td { text-align: center; color: #666; }
</style>
