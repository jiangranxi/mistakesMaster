<template>
  <div class="member-page">
    <!-- 左侧菜单 -->
    <div class="sidebar">
      <h3 class="sidebar-title">会员中心</h3>
      <div class="menu-list">
        <div class="menu-item" @click="$router.push('/teacher/member')">基本设置</div>
        <div class="menu-item" @click="$router.push('/teacher/member/security')">安全设置</div>
        <div class="menu-item active">我的订单</div>
      </div>
    </div>

    <!-- 右侧内容 -->
    <div class="main-area">
      <!-- 订单页签 -->
      <div class="tab-area">
        <span class="tab-label">我的订单:</span>
        <span class="spacer-20"></span>
        <span
          v-for="t in orderTabs"
          :key="t.key"
          class="order-tab"
          :class="{ active: activeTab === t.key }"
          @click="activeTab = t.key"
        >{{ t.label }}</span>
      </div>

      <div class="spacer-24"></div>

      <!-- 订单表格 -->
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th class="col-index">序号</th>
              <th class="col-order sortable" @click="toggleSort('orderNo')">订单号<span class="sort-arrows" :data-sort="sortState['orderNo']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-name sortable" @click="toggleSort('name')">名称<span class="sort-arrows" :data-sort="sortState['name']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-type sortable" @click="toggleSort('resourceType')">资源类型<span class="sort-arrows" :data-sort="sortState['resourceType']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-price sortable" @click="toggleSort('price')">价格<span class="sort-arrows" :data-sort="sortState['price']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-status sortable" @click="toggleSort('status')">交易状态<span class="sort-arrows" :data-sort="sortState['status']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-time sortable" @click="toggleSort('time')">时间<span class="sort-arrows" :data-sort="sortState['time']"><span class="sort-arrow up"></span><span class="sort-arrow down"></span></span></th>
              <th class="col-action">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!orderList.length" class="empty-row">
              <td colspan="8">暂无数据</td>
            </tr>
            <tr v-for="(item, idx) in orderList" :key="item.id || idx">
              <td>{{ idx + 1 }}</td>
              <td>{{ item.orderNo }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.resourceType }}</td>
              <td>¥ {{ (item.price || 0).toFixed(2) }}</td>
              <td>{{ item.tradeStatus }}</td>
              <td>{{ item.time }}</td>
              <td><a href="javascript:void(0)" @click="viewDetail(item)">查看</a></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="spacer-24"></div>

      <!-- 分页 -->
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
import { memberApi } from '@/api/member'
import PaginationBar from '@/components/PaginationBar.vue'

const activeTab = ref('all')
const orderTabs = [
  { key: 'all', label: '全部订单' },
  { key: 'pending', label: '待付款' },
  { key: 'paid', label: '已付款' },
  { key: 'cancelled', label: '已取消' }
]

const orderList = ref([])
const page = ref(1)
const pageSize = ref(15)
const totalPages = ref(0)
const sortState = reactive({ orderNo: 'asc', name: 'asc', resourceType: 'asc', price: 'asc', status: 'asc', time: 'asc' })
function toggleSort(key) { sortState[key] = sortState[key] === 'asc' ? 'desc' : 'asc' }

async function loadData() {
  try {
    const res = await memberApi.getOrders({
      page: page.value,
      pageSize: pageSize.value,
      status: activeTab.value
    })
    if (res?.data) {
      orderList.value = res.data.list || []
      totalPages.value = Math.ceil((res.data.total || 0) / pageSize.value) || 0
    }
  } catch {}
}

function changePage(p) {
  if (p >= 1 && p <= totalPages.value) { page.value = p; loadData() }
}

function viewDetail(item) { /* TODO */ }

loadData()
</script>

<style scoped>
.member-page { display: flex; flex: 1; min-height: 0; }
.sidebar { width: 200px; background: #EEE; padding-top: 16px; flex-shrink: 0; align-self: stretch; }
.sidebar-title { padding: 16px; font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; }
.menu-list { padding: 8px 0; }
.menu-item { padding: 8px 16px; font-size: 14px; color: #2B7CD3; cursor: pointer; }
.menu-item.active { background: #337AB7; color: #fff; }

.main-area { flex: 1; padding: 32px 48px; overflow-y: auto; }

/* 页签区域 */
.tab-area { display: flex; align-items: center; }
.tab-label { font-size: 14px; color: #333; }
.spacer-20 { width: 20px; flex-shrink: 0; }
.order-tab {
  font-size: 14px;
  color: #165DFF;
  cursor: pointer;
  padding: 4px 16px;
  border-radius: 9999px;
  margin-right: 24px;
  font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif;
}
.order-tab.active { background: #FF7700; color: #fff; }

.spacer-24 { height: 24px; }

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
.data-table th.sortable i { font-size: 16px; margin-left: 4px; }
.col-index { width: 80px; }
.col-order { width: 160px; }
.col-name { width: 215px; }
.col-type { width: 130px; }
.col-price { width: 100px; }
.col-status { width: 100px; }
.col-time { width: 160px; }
.col-action { width: 100px; }

.data-table td {
  font-size: 14px;
  color: #333;
  padding: 12px 16px;
  border: 1px solid #E5E7EB;
}
.data-table td a { color: #2B7CD3; text-decoration: none; }
.empty-row td { text-align: center; color: #999; height: 86px; padding: 32px 16px; }
</style>
