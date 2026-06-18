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
                <th class="col-name sortable">
                  课件名称
                  <i class="ri-arrow-down-s-line sort-icon"></i>
                </th>
                <th class="col-size sortable">
                  文件大小
                  <i class="ri-arrow-down-s-line sort-icon"></i>
                </th>
                <th class="col-time sortable">
                  创建时间
                  <i class="ri-arrow-down-s-line sort-icon"></i>
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
        <div class="pagination">
          <button class="page-btn">首页</button>
          <button class="page-btn">上一页</button>
          <button class="page-btn">下一页</button>
          <button class="page-btn">尾页</button>
          <span class="page-input">1</span>
          <span class="page-info">1/0</span>
          <span class="page-size">15 <i class="ri-arrow-down-s-line"></i></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { lessonPlanApi } from '@/api/lessonPlan'

const tableData = ref([])
const pagination = ref({ page: 1, pageSize: 15, total: 0 })
const sortField = ref('')
const sortOrder = ref('')

async function fetchData() {
  try {
    const res = await lessonPlanApi.getOwnPlans({
      page: pagination.value.page,
      pageSize: pagination.value.pageSize,
      sortField: sortField.value,
      sortOrder: sortOrder.value
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
.page-info {
  font-size: 14px;
  color: #333;
  min-width: 22px;
  text-align: center;
}
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
