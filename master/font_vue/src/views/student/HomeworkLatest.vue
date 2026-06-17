<template>
  <div class="homework-page">
    <!-- 次级导航 -->
    <div class="sub-nav">
      <span class="sub-tab active">最新作业</span>
      <span class="sub-tab" @click="$router.push('/student/homework/history')">历次作业</span>
      <span class="sub-tab" @click="$router.push('/student/homework/errors')">错题集</span>
    </div>

    <!-- 内容区域 -->
    <div class="content-area">
      <!-- 搜索区域 - 学科选项 -->
      <div class="search-bar">
        <span class="search-label">学科:</span>
        <span
          v-for="opt in subjectOptions"
          :key="opt.value"
          class="subject-tag"
          :class="{ active: searchSubject === opt.value }"
          @click="searchSubject = searchSubject === opt.value ? '' : opt.value; loadData()"
        >{{ opt.label }}</span>
      </div>

      <div class="spacer-24"></div>

      <!-- 作业表格 -->
      <table class="data-table">
        <thead>
          <tr>
            <th style="width:131px">序号</th>
            <th style="width:197px" class="sortable">班级 <i class="ri-arrow-up-down-line"></i></th>
            <th style="width:328px" class="sortable">作业名称 <i class="ri-arrow-up-down-line"></i></th>
            <th style="width:246px" class="sortable">作业来源 <i class="ri-arrow-up-down-line"></i></th>
            <th style="width:164px" class="sortable">学科 <i class="ri-arrow-up-down-line"></i></th>
            <th style="width:246px" class="sortable">布置作业时间 <i class="ri-arrow-up-down-line"></i></th>
            <th style="width:246px" class="sortable">要求交作业时间 <i class="ri-arrow-up-down-line"></i></th>
            <th style="width:164px">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!homeworkList.length" class="empty-row">
            <td colspan="8">暂无数据</td>
          </tr>
          <tr v-for="(item, idx) in homeworkList" :key="item.id">
            <td>{{ idx + 1 }}</td>
            <td>{{ item.className }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.source }}</td>
            <td>{{ item.subject }}</td>
            <td>{{ item.createTime }}</td>
            <td>{{ item.deadline }}</td>
            <td><a href="#" @click.prevent="doHomework(item)">做作业</a></td>
          </tr>
        </tbody>
      </table>

      <div class="spacer-24"></div>

      <div class="pagination">
        <button @click="changePage(1)">首页</button>
        <button @click="changePage(page - 1)">上一页</button>
        <button @click="changePage(page + 1)">下一页</button>
        <button @click="changePage(totalPages)">尾页</button>
        <input class="page-input" :value="page" @change="e => changePage(Number(e.target.value))" />
        <span>{{ page }}/{{ totalPages }}</span>
        <select class="page-size" :value="pageSize" @change="e => { pageSize = Number(e.target.value); loadData() }">
          <option :value="15">15</option>
          <option :value="30">30</option>
          <option :value="50">50</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { homeworkApi } from '@/api/homework'

const subjectOptions = [
  { value: '数学', label: '数学' },
  { value: '语文', label: '语文' },
  { value: '英语', label: '英语' },
  { value: '物理', label: '物理' },
  { value: '化学', label: '化学' },
  { value: '生物', label: '生物' },
]

const searchSubject = ref('')
const homeworkList = ref([])
const page = ref(1)
const pageSize = ref(15)
const totalPages = ref(0)

async function loadData() {
  try {
    const res = await homeworkApi.getLatestHomework({ page: page.value, pageSize: pageSize.value, subject: searchSubject.value })
    homeworkList.value = res.list || []
    totalPages.value = res.totalPages || 0
  } catch {}
}
function changePage(p) { if (p >= 1 && p <= totalPages.value) { page.value = p; loadData() } }
function doHomework(item) { alert(`开始做作业: ${item.name}`) }

loadData()
</script>

<style scoped>
.homework-page { display: flex; flex-direction: column; height: 100%; }

.sub-nav {
  height: 40px;
  background: #005538;
  display: flex;
  align-items: center;
  padding-left: 220px;
  gap: 4px;
}
.sub-tab {
  font-size: 14px; color: #fff; cursor: pointer;
  padding: 4px 20px; line-height: 32px;
  border-radius: 9999px;
  transition: background 0.2s;
}
.sub-tab:not(.active):hover { background: rgba(255,255,255,0.15); }
.sub-tab.active { background: #FF7700; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; }

.content-area { padding: 32px 100px; flex: 1; }

.search-bar { display: flex; align-items: center; gap: 8px; }
.search-label { font-size: 14px; color: #333; white-space: nowrap; }

.subject-tag {
  display: inline-block;
  padding: 4px 14px;
  border: 0.8px solid #D1D5DB;
  border-radius: 9999px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}
.subject-tag:hover { border-color: #2563EB; color: #2563EB; }
.subject-tag.active { background: #2563EB; color: #fff; border-color: #2563EB; }

.spacer-24 { height: 24px; }
.sortable { color: #165DFF; cursor: pointer; }
</style>
