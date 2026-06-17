<template>
  <div class="page-padded">
    <h3 class="page-title">习题集</h3>
    <div class="spacer-16"></div>
    <table class="data-table">
      <thead><tr><th>序号</th><th>书名</th><th>学科</th><th>出版社</th><th>操作</th></tr></thead>
      <tbody>
        <tr v-if="!list.length" class="empty-row"><td colspan="5">暂无数据</td></tr>
        <tr v-for="(item, idx) in list" :key="item.id">
          <td>{{ idx + 1 }}</td><td>{{ item.name }}</td><td>{{ item.subject }}</td><td>{{ item.publisher }}</td>
          <td><a href="#" @click.prevent="showDetail(item)">查看详情</a></td>
        </tr>
      </tbody>
    </table>

    <div v-if="detailVisible" class="dialog-overlay" @click.self="detailVisible = false">
      <div class="dialog">
        <h3 class="dialog-title">{{ currentBook?.name }}</h3>
        <div class="dialog-body">
          <p>学科: {{ currentBook?.subject }}</p><p>出版社: {{ currentBook?.publisher }}</p>
        </div>
        <div class="dialog-footer">
          <button class="btn-cancel" @click="detailVisible = false">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { exerciseApi } from '@/api/exercise'
const list = ref([])
const detailVisible = ref(false)
const currentBook = ref(null)
async function loadData() { try { const res = await exerciseApi.getBookList(); list.value = res.list || [] } catch {} }
function showDetail(item) { currentBook.value = item; detailVisible.value = true }
loadData()
</script>

<style scoped>
.page-padded { padding: 32px 64px; }
.page-title { font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; }
.spacer-16 { height: 16px; }
.dialog-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.dialog { background: #fff; border-radius: 8px; width: 500px; }
.dialog-title { padding: 24px 24px 0; font-size: 18px; color: #333; }
.dialog-body { padding: 24px; }
.dialog-body p { margin-bottom: 8px; font-size: 14px; }
.dialog-footer { display: flex; justify-content: flex-end; padding: 0 24px 24px; }
.btn-cancel { padding: 8px 24px; border: 0.8px solid #D1D5DB; border-radius: 4px; background: #fff; cursor: pointer; }
</style>
