<template>
  <div class="homework-page">
    <div class="sub-nav">
      <span class="sub-tab" @click="$router.push('/student/homework/latest')">最新作业</span>
      <span class="sub-tab active">历次作业</span>
      <span class="sub-tab" @click="$router.push('/student/homework/errors')">错题集</span>
    </div>
    <div class="content-area">
      <div class="search-bar">
        <span class="search-label">学科：</span>
      </div>
      <div class="spacer-24"></div>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width:131px">序号</th><th style="width:197px" class="sortable">班级 <i class="ri-arrow-up-down-line"></i></th>
            <th style="width:328px" class="sortable">作业名称 <i class="ri-arrow-up-down-line"></i></th>
            <th style="width:246px" class="sortable">作业来源 <i class="ri-arrow-up-down-line"></i></th>
            <th style="width:164px" class="sortable">学科 <i class="ri-arrow-up-down-line"></i></th>
            <th style="width:246px" class="sortable">布置作业时间 <i class="ri-arrow-up-down-line"></i></th>
            <th style="width:246px" class="sortable">要求交作业时间 <i class="ri-arrow-up-down-line"></i></th>
            <th style="width:164px">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!list.length" class="empty-row"><td colspan="8">暂无数据</td></tr>
          <tr v-for="(item, idx) in list" :key="item.id">
            <td>{{ idx + 1 }}</td><td>{{ item.className }}</td><td>{{ item.name }}</td><td>{{ item.source }}</td>
            <td>{{ item.subject }}</td><td>{{ item.createTime }}</td><td>{{ item.deadline }}</td>
            <td><a href="#" @click.prevent="viewDetail(item)">查看</a></td>
          </tr>
        </tbody>
      </table>
      <div class="spacer-24"></div>
      <div class="pagination">
        <button @click="changePage(1)">首页</button><button @click="changePage(page-1)">上一页</button>
        <button @click="changePage(page+1)">下一页</button><button @click="changePage(totalPages)">尾页</button>
        <input class="page-input" :value="page" /><span>{{ page }}/{{ totalPages }}</span>
        <select class="page-size"><option :value="15">15</option></select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { homeworkApi } from '@/api/homework'
const list = ref([]); const page = ref(1); const pageSize = ref(15); const totalPages = ref(0)
async function loadData() { try { const res = await homeworkApi.getHistoryHomework({ page: page.value, pageSize: pageSize.value }); list.value = res.list||[]; totalPages.value = res.totalPages||0 } catch {} }
function changePage(p) { if(p>=1 && p<=totalPages.value){ page.value=p; loadData() } }
function viewDetail(i) { alert(`查看作业详情: ${i.name}`) }
loadData()
</script>

<style scoped>
.homework-page { display: flex; flex-direction: column; height: 100%; }
.sub-nav { height: 34px; background: #005538; display: flex; align-items: center; padding-left: 296px; gap: 4px; }
.sub-tab { font-size: 13px; color: #fff; cursor: pointer; padding: 2px 18px; line-height: 28px; border-radius: 9999px; }
.sub-tab:not(.active):hover { background: rgba(255,255,255,0.15); }
.sub-tab.active { background: #FF7700; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; }
.content-area { padding: 40px 100px; flex: 1; }
.search-bar { display: flex; align-items: center; }
.search-label { font-size: 14px; color: #333; }
.spacer-24 { height: 24px; }
.sortable { color: #165DFF; cursor: pointer; }
</style>
