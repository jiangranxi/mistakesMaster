<template>
  <div class="page">
    <!-- 页签栏 -->
    <div class="tab-bar">
      <span class="tab-item active">网络作业讲评报告</span>
      <span class="tab-item" @click="$router.push('/teacher/review/error-book')">错题本讲评报告</span>
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
            <input type="text" v-model="filters.startTime" placeholder="开始时间" class="filter-input" />
            <input type="text" v-model="filters.endTime" placeholder="结束时间" class="filter-input" />
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
            <span class="subject-tag" :class="{ active: filters.class === '' }" @click="filters.class = ''">全部</span>
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
              <th class="col-date sortable">日期 <i class="ri-arrow-down-s-line"></i></th>
              <th class="col-report sortable">讲评报告 <i class="ri-arrow-down-s-line"></i></th>
              <th class="col-book sortable">书目名称 <i class="ri-arrow-down-s-line"></i></th>
              <th class="col-subject sortable">学科 <i class="ri-arrow-down-s-line"></i></th>
              <th class="col-class sortable">班级 <i class="ri-arrow-down-s-line"></i></th>
              <th class="col-score sortable">最高分 <i class="ri-arrow-down-s-line"></i></th>
              <th class="col-score sortable">最低分 <i class="ri-arrow-down-s-line"></i></th>
              <th class="col-score sortable">平均数 <i class="ri-arrow-down-s-line"></i></th>
              <th class="col-score sortable">中位数 <i class="ri-arrow-down-s-line"></i></th>
              <th class="col-mode sortable">众数 <i class="ri-arrow-down-s-line"></i></th>
              <th class="col-action">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!tableData.length" class="empty-row">
              <td colspan="12">暂无数据</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <button class="page-btn">首页</button>
        <button class="page-btn">上一页</button>
        <button class="page-btn">下一页</button>
        <button class="page-btn">尾页</button>
        <span class="page-input">0</span>
        <span class="page-info">0/0</span>
        <span class="page-size">15 <i class="ri-arrow-down-s-line"></i></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

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
</script>

<style scoped>
.page { height: 100%; display: flex; flex-direction: column; }

/* 页签栏 */
.tab-bar {
  display: flex;
  align-items: stretch;
  padding: 0 64px;
  height: 49px;
}
.tab-item {
  padding: 12px 32px;
  font-size: 16px;
  font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif;
  color: #2B7CD3;
  cursor: pointer;
  display: flex;
  align-items: center;
}
.tab-item.active { color: #FF7700; }

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
.col-index { width: 106px; }
.col-date { width: 139px; }
.col-report { width: 188px; }
.col-book { width: 188px; }
.col-subject { width: 139px; }
.col-class { width: 139px; }
.col-score { width: 163px; }
.col-mode { width: 139px; }
.col-action { width: 106px; }

.data-table td {
  height: 33px;
  font-size: 14px;
  color: #333;
  padding: 8px 16px;
  border: 1px solid #E5E7EB;
}
.empty-row td { text-align: center; color: #666; }

/* 分页 */
.pagination {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 24px;
}
.page-btn {
  width: 60px;
  height: 36px;
  border: 1px solid #E5E7EB;
  background: #fff;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.page-btn:hover { border-color: #2563EB; color: #2563EB; }
.page-input {
  width: 48px;
  height: 36px;
  border: 1px solid #E5E7EB;
  background: #fff;
  font-size: 14px;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
}
.page-info { font-size: 14px; color: #333; min-width: 22px; text-align: center; }
.page-size {
  width: 60px;
  height: 36px;
  border: 1px solid #E5E7EB;
  background: #fff;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
.page-size i { font-size: 14px; color: #6B7280; }
</style>
