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
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { memberApi } from '@/api/member'

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

const pageSizes = computed(() => {
  const sizes = []
  for (let i = 4; i <= 40; i += 4) sizes.push(i)
  return sizes
})

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
.col-index { width: 130px; }
.col-order { width: 244px; }
.col-name { width: 325px; }
.col-type { width: 195px; }
.col-price { width: 163px; }
.col-status { width: 163px; }
.col-time { width: 244px; }
.col-action { width: 163px; }

.data-table td {
  font-size: 14px;
  color: #333;
  padding: 12px 16px;
  border: 1px solid #E5E7EB;
}
.data-table td a { color: #2B7CD3; text-decoration: none; }
.empty-row td { text-align: center; color: #999; height: 86px; padding: 32px 16px; }

/* 分页 */
.pagination { display: flex; align-items: center; justify-content: flex-end; gap: 8px; }
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
