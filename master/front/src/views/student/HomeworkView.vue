<template>
  <div class="homework-page">
    <div class="card">
      <!-- 次级导航 -->
      <div class="sub-tabs">
        <div class="sub-tab" :class="{ active: activeTab === 'latest' }" @click="activeTab = 'latest'">最新作业</div>
        <div class="sub-tab" :class="{ active: activeTab === 'history' }" @click="activeTab = 'history'">历次作业</div>
        <div class="sub-tab" :class="{ active: activeTab === 'errors' }" @click="activeTab = 'errors'">错题集</div>
      </div>

      <!-- 最新作业 -->
      <template v-if="activeTab === 'latest'">
        <div class="search-bar">
          <span class="search-icon">🔍</span>
          <input v-model="latestSearch" class="form-input" placeholder="搜索作业名称" style="width:240px" />
        </div>
        <table class="table">
          <thead>
            <tr>
              <th>序号</th>
              <th>班级</th>
              <th>作业名称</th>
              <th>作业来源</th>
              <th>学科</th>
              <th>布置作业时间</th>
              <th>要求交作业时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="latestList.length === 0">
              <td colspan="8" style="text-align:center;padding:40px;color:#999">暂无最新作业</td>
            </tr>
            <tr v-for="(item, idx) in latestList" :key="item.id">
              <td>{{ (latestPage - 1) * latestPageSize + idx + 1 }}</td>
              <td>{{ item.className }}</td>
              <td>{{ item.homeworkName }}</td>
              <td>{{ item.source }}</td>
              <td>{{ item.subject }}</td>
              <td>{{ item.assignTime }}</td>
              <td>{{ item.deadline }}</td>
              <td><button class="btn btn-sm btn-primary">做作业</button></td>
            </tr>
          </tbody>
        </table>
        <div class="pagination" v-if="latestTotal > latestPageSize">
          <button class="btn btn-sm" @click="latestPage = 1">首页</button>
          <button class="btn btn-sm" @click="latestPage--" :disabled="latestPage <= 1">上一页</button>
          <button class="btn btn-sm" @click="latestPage++" :disabled="latestPage * latestPageSize >= latestTotal">下一页</button>
          <button class="btn btn-sm" @click="latestPage = Math.ceil(latestTotal / latestPageSize)">尾页</button>
        </div>
      </template>

      <!-- 历次作业 -->
      <template v-if="activeTab === 'history'">
        <div class="search-bar">
          <div class="search-item">
            <label>书目名称</label>
            <input v-model="historyFilters.bookName" class="form-input" style="width:180px" />
          </div>
          <div class="search-item">
            <label>作业名称</label>
            <input v-model="historyFilters.homeworkName" class="form-input" style="width:180px" />
          </div>
          <div class="search-item">
            <label>提交时间</label>
            <input v-model="historyFilters.submitTime" class="form-input" type="date" style="width:180px" />
          </div>
          <button class="btn btn-primary btn-sm" @click="searchHistory">🔍</button>
        </div>
        <div class="filter-bar">
          <span>学科：</span>
          <span class="filter-tag" v-for="s in subjects" :key="s.value" :class="{ active: historyFilters.subject === s.value }" @click="historyFilters.subject = s.value">{{ s.label }}</span>
        </div>
        <table class="table">
          <thead>
            <tr>
              <th>序号</th>
              <th>提交时间</th>
              <th>作业名称</th>
              <th>作业来源</th>
              <th>学科</th>
              <th>试卷总分</th>
              <th>我的得分</th>
              <th>班级排名</th>
              <th>批改详情</th>
              <th>分析报告</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="historyList.length === 0">
              <td colspan="10" style="text-align:center;padding:40px;color:#999">暂无历次作业</td>
            </tr>
            <tr v-for="(item, idx) in historyList" :key="item.id">
              <td>{{ (historyPage - 1) * historyPageSize + idx + 1 }}</td>
              <td>{{ item.submitTime }}</td>
              <td>{{ item.homeworkName }}</td>
              <td>{{ item.source }}</td>
              <td>{{ item.subject }}</td>
              <td>{{ item.totalScore }}</td>
              <td>{{ item.myScore }}</td>
              <td>{{ item.rank }}</td>
              <td><button class="btn btn-sm">查看</button></td>
              <td><button class="btn btn-sm btn-primary">分析</button></td>
            </tr>
          </tbody>
        </table>
        <div class="pagination" v-if="historyTotal > historyPageSize">
          <button class="btn btn-sm" @click="historyPage = 1">首页</button>
          <button class="btn btn-sm" @click="historyPage--" :disabled="historyPage <= 1">上一页</button>
          <button class="btn btn-sm" @click="historyPage++" :disabled="historyPage * historyPageSize >= historyTotal">下一页</button>
          <button class="btn btn-sm" @click="historyPage = Math.ceil(historyTotal / historyPageSize)">尾页</button>
        </div>
      </template>

      <!-- 错题集 -->
      <template v-if="activeTab === 'errors'">
        <div class="search-bar">
          <div class="search-item">
            <label>作业名称</label>
            <input v-model="errorFilters.homeworkName" class="form-input" style="width:180px" />
          </div>
          <div class="search-item">
            <label>书目名称</label>
            <input v-model="errorFilters.bookName" class="form-input" style="width:180px" />
          </div>
          <div class="search-item">
            <label>时间范围</label>
            <input v-model="errorFilters.startDate" class="form-input" type="date" style="width:150px" />
            <span style="margin:0 4px">-</span>
            <input v-model="errorFilters.endDate" class="form-input" type="date" style="width:150px" />
          </div>
          <button class="btn btn-primary btn-sm" @click="searchErrors">🔍</button>
        </div>
        <div class="filter-bar">
          <span>学科：</span>
          <span class="filter-tag" v-for="s in subjects" :key="s.value" :class="{ active: errorFilters.subject === s.value }" @click="errorFilters.subject = s.value">{{ s.label }}</span>
        </div>
        <table class="table">
          <thead>
            <tr>
              <th>序号</th>
              <th>作业名称</th>
              <th>作业来源</th>
              <th>学科</th>
              <th>提交时间</th>
              <th>错题序号</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="errorList.length === 0">
              <td colspan="7" style="text-align:center;padding:40px;color:#999">暂无错题记录</td>
            </tr>
            <tr v-for="(item, idx) in errorList" :key="item.id">
              <td>{{ (errorPage - 1) * errorPageSize + idx + 1 }}</td>
              <td>{{ item.homeworkName }}</td>
              <td>{{ item.source }}</td>
              <td>{{ item.subject }}</td>
              <td>{{ item.submitTime }}</td>
              <td>{{ item.errorNumbers }}</td>
              <td><button class="btn btn-sm btn-primary">查看详情</button></td>
            </tr>
          </tbody>
        </table>
        <div class="pagination" v-if="errorTotal > errorPageSize">
          <button class="btn btn-sm" @click="errorPage = 1">首页</button>
          <button class="btn btn-sm" @click="errorPage--" :disabled="errorPage <= 1">上一页</button>
          <button class="btn btn-sm" @click="errorPage++" :disabled="errorPage * errorPageSize >= errorTotal">下一页</button>
          <button class="btn btn-sm" @click="errorPage = Math.ceil(errorTotal / errorPageSize)">尾页</button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const activeTab = ref('latest')

const subjects = [
  { label: '全部', value: '' },
  { label: '语文', value: 'chinese' },
  { label: '数学', value: 'math' },
  { label: '英语', value: 'english' },
  { label: '物理', value: 'physics' },
  { label: '化学', value: 'chemistry' },
]

// 最新作业
const latestSearch = ref('')
const latestList = ref([])
const latestPage = ref(1)
const latestPageSize = ref(10)
const latestTotal = ref(0)

// 历次作业
const historyFilters = reactive({ bookName: '', homeworkName: '', submitTime: '', subject: '' })
const historyList = ref([])
const historyPage = ref(1)
const historyPageSize = ref(10)
const historyTotal = ref(0)

function searchHistory() { /* API调用 */ }

// 错题集
const errorFilters = reactive({ homeworkName: '', bookName: '', startDate: '', endDate: '', subject: '' })
const errorList = ref([])
const errorPage = ref(1)
const errorPageSize = ref(10)
const errorTotal = ref(0)

function searchErrors() { /* API调用 */ }
</script>

<style scoped>
.sub-tabs { display: flex; gap: 0; margin-bottom: 20px; border-bottom: 1px solid #e8e8e8; }
.sub-tab { padding: 10px 24px; cursor: pointer; color: #666; font-size: 14px; border-bottom: 2px solid transparent; }
.sub-tab:hover { color: #4A90D9; }
.sub-tab.active { color: #4A90D9; border-bottom-color: #4A90D9; }
.search-bar { display: flex; gap: 16px; align-items: center; margin-bottom: 12px; flex-wrap: wrap; }
.search-item { display: flex; align-items: center; gap: 8px; }
.search-item label { font-size: 13px; color: #666; white-space: nowrap; }
.filter-bar { display: flex; gap: 8px; align-items: center; margin-bottom: 16px; font-size: 13px; color: #666; }
.filter-tag { padding: 2px 10px; border-radius: 3px; cursor: pointer; background: #f5f5f5; }
.filter-tag:hover, .filter-tag.active { background: #4A90D9; color: #fff; }
</style>
