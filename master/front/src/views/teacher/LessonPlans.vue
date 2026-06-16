<template>
  <div class="lesson-plans-page">
    <div class="card">
      <!-- 二级页签 -->
      <div class="sub-tabs">
        <div class="tab" :class="{ active: activeTab === 'cloud' }" @click="activeTab = 'cloud'">云教案</div>
        <div class="tab" :class="{ active: activeTab === 'own' }" @click="activeTab = 'own'">自有教案</div>
      </div>

      <div class="layout">
        <!-- 左侧导航 -->
        <div class="sidebar">
          <div v-for="item in sidebarItems" :key="item.id" class="sidebar-item" :class="{ active: selectedSide === item.id }" @click="selectedSide = item.id">
            {{ item.name }}
          </div>
          <div v-if="sidebarItems.length === 0" class="empty-state" style="padding:20px">暂无数据</div>
        </div>

        <!-- 右侧表格 -->
        <div class="table-area">
          <table class="table">
            <thead>
              <tr>
                <th>课件名称</th>
                <th>文件大小</th>
                <th>创建时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="planList.length === 0">
                <td colspan="4" style="text-align:center;padding:40px;color:#999">暂无教案</td>
              </tr>
              <tr v-for="item in planList" :key="item.id">
                <td>{{ item.name }}</td>
                <td>{{ item.fileSize }}</td>
                <td>{{ item.createTime }}</td>
                <td>
                  <button class="btn btn-sm" @click="downloadPlan(item)">下载</button>
                  <button class="btn btn-sm" @click="deletePlan(item)">删除</button>
                </td>
              </tr>
            </tbody>
          </table>

          <div class="pagination">
            <button class="btn btn-sm" :disabled="page === 1" @click="page--">首页</button>
            <button class="btn btn-sm" :disabled="page === 1" @click="page--">上一页</button>
            <button class="btn btn-sm btn-primary">{{ page }}</button>
            <button class="btn btn-sm" @click="page++">下一页</button>
            <button class="btn btn-sm" @click="page = totalPages">尾页</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('own')
const selectedSide = ref('')
const page = ref(1)
const totalPages = ref(1)
const sidebarItems = ref([])
const planList = ref([])

function downloadPlan(item) { /* 下载教案 */ }
function deletePlan(item) { /* 删除教案 */ }
</script>

<style scoped>
.sub-tabs { margin-bottom: 16px; }
.layout { display: flex; gap: 20px; }
.sidebar { width: 200px; border-right: 1px solid #f0f0f0; min-height: 300px; }
.sidebar-item { padding: 10px 16px; cursor: pointer; border-radius: 4px; font-size: 14px; color: #333; }
.sidebar-item:hover { background: #f0f5ff; }
.sidebar-item.active { background: #f0f5ff; color: #4A90D9; }
.table-area { flex: 1; }
</style>
