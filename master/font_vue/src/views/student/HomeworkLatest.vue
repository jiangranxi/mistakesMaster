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
      <div class="search-bar">
        <span class="search-label">学科：</span>
      </div>
      <div class="spacer-24"></div>
      <!-- 作业表格 -->
      <table class="data-table" style="table-layout:fixed">
        <thead>
          <tr>
            <th style="width:80px">序号</th>
            <th style="width:130px" class="sortable" @click="toggleSort('className')">班级<span class="sort-arrows" :data-sort="sortState['className']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
            <th style="width:220px" class="sortable" @click="toggleSort('name')">作业名称<span class="sort-arrows" :data-sort="sortState['name']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
            <th style="width:160px" class="sortable" @click="toggleSort('source')">作业来源<span class="sort-arrows" :data-sort="sortState['source']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
            <th style="width:100px" class="sortable" @click="toggleSort('subject')">学科<span class="sort-arrows" :data-sort="sortState['subject']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
            <th style="width:160px" class="sortable" @click="toggleSort('createTime')">布置作业时间<span class="sort-arrows" :data-sort="sortState['createTime']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
            <th style="width:160px" class="sortable" @click="toggleSort('deadline')">要求交作业时间<span class="sort-arrows" :data-sort="sortState['deadline']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
            <th style="width:100px">操作</th>
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

      <div class="spacer-16"></div>

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
import { useToast } from '@/composables/useToast'
import PaginationBar from '@/components/PaginationBar.vue'

const toast = useToast()

const homeworkList = ref([])
const page = ref(1)
const pageSize = ref(15)
const totalPages = ref(0)
const sortState = reactive({ className: 'asc', name: 'asc', source: 'asc', subject: 'asc', createTime: 'asc', deadline: 'asc' })
function toggleSort(key) { sortState[key] = sortState[key] === 'asc' ? 'desc' : 'asc' }

async function loadData() {
  try {
    const res = await homeworkApi.getLatestHomework({ page: page.value, pageSize: pageSize.value })
    homeworkList.value = res.list || []
    totalPages.value = res.totalPages || 0
  } catch {}
}
function changePage(p) { if (p >= 1 && p <= totalPages.value) { page.value = p; loadData() } }
function doHomework(item) { toast.info(`开始做作业: ${item.name}`) }

loadData()
</script>

<style scoped>
.homework-page { display: flex; flex-direction: column; flex: 1; min-height: 0; }

.sub-nav {
  height: 40px;
  background: #005538;
  display: flex;
  align-items: center;
  padding-left: 200px;
  gap: 4px;
}
.sub-tab {
  font-size: 13px; color: #fff; cursor: pointer;
  padding: 2px 18px; line-height: 28px;
  border-radius: 9999px;
}
.sub-tab:not(.active):hover { background: rgba(255,255,255,0.15); }
.sub-tab.active { background: #FF6600; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; }

.content-area { padding: 32px 100px; flex: 1; }

.search-bar { display: flex; align-items: center; }
.search-label { font-size: 14px; color: #333; }

.spacer-16 { height: 16px; }
.sortable { color: #165DFF; cursor: pointer; }
</style>
