<template>
  <div class="page">
    <div class="sub-nav">
      <span class="sub-tab" @click="$router.push('/teacher/lesson-plans/cloud')">云教案</span>
      <span class="sub-tab active">自有教案</span>
    </div>
    <div class="content-area">
      <!-- 左侧导航栏 -->
      <div class="left-sidebar">
        <div class="class-item">
          <div class="class-item-header">
            <i class="ri-file-copy-2-line"></i>
            <span>自有教案Class</span>
          </div>
          <p class="class-item-empty">没有教案</p>
        </div>
      </div>

      <!-- 中间章节目录 -->
      <div class="middle-panel">
        <h4 class="panel-title">章节目录</h4>
        <p class="panel-empty">没有章节</p>
      </div>

      <!-- 右侧内容区域 -->
      <div class="right-content">
        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th class="col-index">序号</th>
                <th class="col-name sortable" @click="toggleSort('name')">
                  课件名称<span class="sort-arrows" :data-sort="sortState['name']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span>
                </th>
                <th class="col-size sortable" @click="toggleSort('size')">
                  文件大小<span class="sort-arrows" :data-sort="sortState['size']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span>
                </th>
                <th class="col-time sortable" @click="toggleSort('time')">
                  创建时间<span class="sort-arrows" :data-sort="sortState['time']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span>
                </th>
                <th class="col-action">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr class="empty-row">
                <td colspan="5">没有教案</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 分页 -->
        <PaginationBar
          variant="teacher"
          :page="pagination.page"
          :pageSize="pagination.pageSize"
          :totalPages="totalPages"
          @page-change="goPage"
          @page-size-change="val => { pagination.pageSize = val; fetchData() }"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { lessonPlanApi } from '@/api/lessonPlan'
import PaginationBar from '@/components/PaginationBar.vue'

const tableData = ref([])
const pagination = ref({ page: 1, pageSize: 15, total: 0 })
const sortState = reactive({ name: 'asc', size: 'asc', time: 'asc' })
function toggleSort(key) { sortState[key] = sortState[key] === 'asc' ? 'desc' : 'asc'; fetchData() }

const totalPages = computed(() => Math.ceil(pagination.value.total / pagination.value.pageSize) || 0)
function goPage(p) {
  if (p < 1 || p > totalPages.value) return
  pagination.value.page = p
  fetchData()
}

async function fetchData() {
  try {
    const res = await lessonPlanApi.getOwnPlans({
      page: pagination.value.page,
      pageSize: pagination.value.pageSize,
      sortState
    })
    if (res?.data) {
      tableData.value = res.data.list || res.data
      pagination.value.total = res.data.total || 0
    }
  } catch {
    // 接口未实现时展示空状态
  }
}

onMounted(() => fetchData())
</script>

<style scoped>
.page { display: flex; flex-direction: column; flex: 1; min-height: 0; }

.sub-nav {
  height: 40px;
  background: #005538;
  display: flex;
  align-items: center;
  padding-left: 220px;
  gap: 24px;
  flex-shrink: 0;
}
.sub-tab {
  font-size: 14px;
  color: #fff;
  cursor: pointer;
  padding: 6px 16px;
  border-radius: 9999px;
}
.sub-tab.active { background: #FF6600; }

.content-area {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* 左侧导航 */
.left-sidebar {
  width: 200px;
  padding: 16px 0;
  flex-shrink: 0;
  overflow-y: auto;
}
.class-item {
  padding: 12px 16px;
}
.class-item-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  color: #333;
}
.class-item-header i {
  font-size: 18px;
  color: #6B7280;
}
.class-item-empty {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
}

/* 中间章节目录 */
.middle-panel {
  width: 240px;
  background: #EEE;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}
.panel-title {
  font-size: 16px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  color: #333;
  padding: 12px 16px;
  margin: 0;
}
.panel-empty {
  font-size: 14px;
  color: #666;
  text-align: center;
  padding: 24px 16px;
}

/* 右侧内容 */
.right-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* 表格 */
.table-wrapper {
  border: 1px solid #E5E7EB;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}
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
.data-table th.sortable {
  color: #2B7CD3;
  cursor: pointer;
}
.sort-icon {
  font-size: 14px;
  color: #2B7CD3;
  margin-left: 4px;
}
.col-index { width: 80px; }
.col-name { width: auto; }
.col-size { width: 120px; }
.col-time { width: 160px; }
.col-action { width: 100px; }

.data-table td {
  height: 53px;
  font-size: 14px;
  color: #333;
  padding: 16px;
  border: 1px solid #E5E7EB;
}
.empty-row td {
  text-align: left;
  color: #666;
  height: 53px;
}
</style>
