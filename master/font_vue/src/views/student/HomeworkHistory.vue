<template>
  <div class="page">
    <div class="sub-nav">
      <span class="sub-tab" @click="$router.push('/student/homework/latest')">最新作业</span>
      <span class="sub-tab active">历次作业</span>
      <span class="sub-tab" @click="$router.push('/student/homework/errors')">错题集</span>
    </div>
    <div class="content-body">
      <!-- 搜索区 -->
      <div class="search-row">
        <div class="filter-item">
          <label>书目名称:</label>
          <input type="text" v-model="filters.book" placeholder="书目名称" class="filter-input" />
        </div>
        <div class="filter-item">
          <label>作业名称:</label>
          <input type="text" v-model="filters.name" placeholder="作业名称" class="filter-input" />
        </div>
        <div class="filter-item">
          <label>提交时间:</label>
          <DatePicker v-model="filters.time" placeholder="提交时间" style="width: 200px" />
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
              <th class="col-time sortable">提交时间 <i class="ri-arrow-up-down-line"></i></th>
              <th class="col-name sortable">作业名称 <i class="ri-arrow-up-down-line"></i></th>
              <th class="col-source sortable">作业来源 <i class="ri-arrow-up-down-line"></i></th>
              <th class="col-subject sortable">学科 <i class="ri-arrow-up-down-line"></i></th>
              <th class="col-score sortable">试卷总分 <i class="ri-arrow-up-down-line"></i></th>
              <th class="col-score sortable">我的得分 <i class="ri-arrow-up-down-line"></i></th>
              <th class="col-score sortable">班级排名 <i class="ri-arrow-up-down-line"></i></th>
              <th class="col-action">批改详情</th>
              <th class="col-action">分析报告</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!list.length" class="empty-row"><td colspan="10">暂无数据</td></tr>
            <tr v-for="(item, idx) in list" :key="item.id">
              <td>{{ idx + 1 }}</td>
              <td>{{ item.submitTime }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.source }}</td>
              <td>{{ item.subject }}</td>
              <td>{{ item.totalScore }}</td>
              <td>{{ item.myScore }}</td>
              <td>{{ item.rank }}</td>
              <td><a href="#" @click.prevent="viewDetail(item)">查看</a></td>
              <td><a href="#" @click.prevent="viewReport(item)">查看</a></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="pagination-bar">
        <div class="pagination">
          <button class="page-btn" :disabled="page <= 1" @click="changePage(1)">首页</button>
          <button class="page-btn" :disabled="page <= 1" @click="changePage(page - 1)">上一页</button>
          <button class="page-btn" :disabled="page >= totalPages" @click="changePage(page + 1)">下一页</button>
          <button class="page-btn" :disabled="page >= totalPages" @click="changePage(totalPages)">尾页</button>
          <span class="page-input">{{ page }}</span>
          <span class="page-info">{{ page }}/{{ totalPages || 0 }}</span>
          <select class="page-size-select" v-model.number="pageSize" @change="loadData">
            <option v-for="n in pageSizes" :key="n" :value="n">{{ n }}</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { homeworkApi } from '@/api/homework'
import DatePicker from '@/components/DatePicker.vue'

const list = ref([])
const page = ref(1)
const pageSize = ref(15)
const totalPages = ref(0)
const filters = reactive({ book: '', name: '', time: '' })

const pageSizes = computed(() => {
  const sizes = []
  for (let i = 4; i <= 40; i += 4) sizes.push(i)
  return sizes
})

async function loadData() {
  try {
    const res = await homeworkApi.getHistoryHomework({
      page: page.value, pageSize: pageSize.value,
      ...filters
    })
    if (res?.data) {
      list.value = res.data.list || []
      totalPages.value = Math.ceil((res.data.total || 0) / pageSize.value) || 0
    }
  } catch {}
}

function changePage(p) {
  if (p >= 1 && p <= totalPages.value) { page.value = p; loadData() }
}

function viewDetail(item) { /* TODO */ }
function viewReport(item) { /* TODO */ }

loadData()
</script>

<style scoped>
.page { display: flex; flex-direction: column; flex: 1; min-height: 0; }

.sub-nav {
  height: 34px;
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
  background: #FF7700;
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
.col-index { width: 120px; }
.col-time { width: 180px; }
.col-name { width: 299px; }
.col-source { width: 225px; }
.col-subject { width: 150px; }
.col-score { width: 150px; }
.col-action { width: 150px; }

.data-table td {
  font-size: 14px; color: #333;
  padding: 12px 16px;
  border: 1px solid #E5E7EB;
}
.data-table td a { color: #2B7CD3; text-decoration: none; }
.empty-row td { text-align: center; color: #999; padding: 32px 16px; height: 86px; }

/* 分页 */
.pagination-bar { margin-top: 24px; display: flex; justify-content: flex-end; }
.pagination { display: flex; align-items: center; gap: 8px; }
.page-btn {
  min-width: 70px; height: 36px;
  border: 1px solid #D1D5DB; background: #fff;
  font-size: 14px; color: #333; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}
.page-btn:hover:not(:disabled) { border-color: #2563EB; color: #2563EB; }
.page-btn:disabled { color: #ccc; cursor: not-allowed; }
.page-input {
  width: 60px; height: 36px;
  border: 1px solid #D1D5DB; background: #fff;
  font-size: 14px; color: #333;
  display: flex; align-items: center; justify-content: center;
}
.page-info { font-size: 14px; color: #333; min-width: 23px; text-align: center; margin: 0 2px; }
.page-size-select {
  width: 70px; height: 36px;
  border: 1px solid #D1D5DB; background: #fff;
  font-size: 14px; color: #333; cursor: pointer; outline: none;
  text-align: center; appearance: none; padding-right: 16px; margin-left: 2px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%236B7280' d='M12 16l-6-6h12z'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: right 4px center;
}
</style>
