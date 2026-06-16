<template>
  <div class="review-page">
    <div class="card">
      <!-- 页签栏 -->
      <div class="tabs">
        <div class="tab" :class="{ active: activeTab === 'online' }" @click="activeTab = 'online'">网络作业讲评报告</div>
        <div class="tab" :class="{ active: activeTab === 'errorbook' }" @click="activeTab = 'errorbook'">错题本讲评报告</div>
      </div>

      <!-- 筛选区域 -->
      <div class="filter-area">
        <div class="filter-row">
          <div class="filter-item">
            <label>讲评报告</label>
            <select v-model="filters.reportName" class="form-input" style="width:180px">
              <option value="">全部</option>
              <option v-for="r in reportOptions" :key="r" :value="r">{{ r }}</option>
            </select>
          </div>
          <div class="filter-item">
            <label>书目名称</label>
            <select v-model="filters.bookName" class="form-input" style="width:180px">
              <option value="">全部</option>
              <option v-for="b in bookOptions" :key="b" :value="b">{{ b }}</option>
            </select>
          </div>
          <div class="filter-item">
            <label>时间范围</label>
            <input v-model="filters.startDate" class="form-input" type="date" style="width:160px" />
            <span style="margin:0 8px">-</span>
            <input v-model="filters.endDate" class="form-input" type="date" style="width:160px" />
          </div>
          <button class="btn btn-primary" @click="search">搜索</button>
        </div>
        <div v-if="activeTab === 'online'" class="filter-row">
          <button class="btn">全部班级</button>
        </div>
      </div>

      <!-- 表格 -->
      <table class="table">
        <thead>
          <tr>
            <th>序号</th>
            <th>日期</th>
            <th>讲评报告</th>
            <th>书目名称</th>
            <th v-if="activeTab === 'online'">学科</th>
            <th v-if="activeTab === 'online'">班级</th>
            <th>最高分</th>
            <th>最低分</th>
            <th>平均数</th>
            <th>中位数</th>
            <th>众数</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="reportList.length === 0">
            <td :colspan="activeTab === 'online' ? 13 : 11" style="text-align:center;padding:40px;color:#999">
              暂无数据
            </td>
          </tr>
          <tr v-for="(item, idx) in reportList" :key="item.id">
            <td>{{ idx + 1 }}</td>
            <td>{{ item.date }}</td>
            <td>{{ item.reportName }}</td>
            <td>{{ item.bookName }}</td>
            <td v-if="activeTab === 'online'">{{ item.subject }}</td>
            <td v-if="activeTab === 'online'">{{ item.className }}</td>
            <td>{{ item.maxScore }}</td>
            <td>{{ item.minScore }}</td>
            <td>{{ item.avgScore }}</td>
            <td>{{ item.medianScore }}</td>
            <td>{{ item.modeScore }}</td>
            <td>
              <button class="btn btn-sm" @click="viewDetail(item)">查看</button>
              <button class="btn btn-sm" @click="exportReport(item)">导出</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 分页 -->
      <div class="pagination">
        <button class="btn btn-sm" :disabled="page === 1" @click="page--">首页</button>
        <button class="btn btn-sm" :disabled="page === 1" @click="page--">上一页</button>
        <button class="btn btn-sm btn-primary">{{ page }}</button>
        <button class="btn btn-sm" @click="page++">下一页</button>
        <button class="btn btn-sm" @click="page = totalPages">尾页</button>
        <span class="page-info">共 {{ totalPages }} 页</span>
        <select v-model="pageSize" class="form-input" style="width:80px">
          <option :value="10">10条</option>
          <option :value="20">20条</option>
          <option :value="50">50条</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const activeTab = ref('online')
const page = ref(1)
const pageSize = ref(10)
const totalPages = ref(1)
const reportList = ref([])

const reportOptions = ref([])
const bookOptions = ref([])
const filters = reactive({ reportName: '', bookName: '', startDate: '', endDate: '' })

function search() { page.value = 1; /* fetchData */ }
function viewDetail(item) { /* 查看详情 */ }
function exportReport(item) { /* 导出报告 */ }
</script>

<style scoped>
.tabs { margin-bottom: 16px; }
.filter-area { margin-bottom: 16px; }
.filter-row { display: flex; align-items: center; gap: 16px; margin-bottom: 8px; flex-wrap: wrap; }
.filter-item { display: flex; align-items: center; gap: 8px; }
.filter-item label { font-size: 13px; color: #666; white-space: nowrap; }
.pagination { margin-top: 16px; gap: 4px; }
.page-info { font-size: 13px; color: #999; margin: 0 8px; }
</style>
