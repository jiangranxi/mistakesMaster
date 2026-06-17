<template>
  <div class="page">
    <div class="page-padded">
      <div class="book-grid">
        <div v-if="!list.length" class="empty-state">暂无数据</div>
        <div v-for="item in list" :key="item.id" class="book-card" @click="showDetail(item)">
          <div class="book-cover">
            <img v-if="item.cover" :src="item.cover" :alt="item.name" />
            <div v-else class="cover-placeholder">
              <i class="ri-book-2-line"></i>
              <span>{{ item.name }}</span>
            </div>
          </div>
          <div class="book-price">¥ {{ (item.price || 0).toFixed(2) }}</div>
        </div>
      </div>

      <div class="pagination-bar">
        <span class="count-info">数量: {{ pagination.total }}</span>
        <div class="pagination">
          <button class="page-btn" :disabled="pagination.page <= 1" @click="goPage(1)">首页</button>
          <button class="page-btn" :disabled="pagination.page <= 1" @click="goPage(pagination.page - 1)">上一页</button>
          <button class="page-btn active-page">{{ pagination.page }}</button>
          <button class="page-btn" :disabled="pagination.page >= totalPages" @click="goPage(pagination.page + 1)">下一页</button>
          <button class="page-btn" :disabled="pagination.page >= totalPages" @click="goPage(totalPages)">尾页</button>
          <span class="page-input">{{ pagination.page }}</span>
          <span class="page-info">{{ pagination.page }}/{{ totalPages || 1 }}</span>
          <select class="page-size-select" v-model.number="pagination.pageSize" @change="loadData">
            <option v-for="n in pageSizes" :key="n" :value="n">{{ n }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <div v-if="detailVisible" class="detail-overlay">
      <div class="detail-panel">
        <div class="detail-header">
          <span class="close-btn" @click="detailVisible = false"><i class="ri-close-line"></i></span>
          <div class="header-info">
            <h2 class="book-title">《{{ currentBook?.name }}》</h2>
            <div class="book-version">{{ currentBook?.publisher }}</div>
            <div class="book-meta">
              <span v-if="currentBook?.updateTime">更新时间: {{ currentBook.updateTime }}</span>
              <span v-if="currentBook?.version">教材版本: {{ currentBook.version }}</span>
              <span v-if="currentBook?.subject">学 科: {{ currentBook.subject }}</span>
              <span v-if="currentBook?.gradeTerm">年级学期: {{ currentBook.gradeTerm }}</span>
            </div>
            <button class="buy-btn">购买 ¥ {{ (currentBook?.price || 0).toFixed(2) }}</button>
          </div>
        </div>
        <div class="detail-body">
          <div class="detail-card">
            <div class="section">
              <h3 class="section-title">简介:</h3>
              <p class="section-content">{{ currentBook?.description || '生产中' }}</p>
            </div>
            <div class="section">
              <h3 class="section-title">目录:</h3>
              <p v-if="!currentBook?.chapters?.length" class="section-content">生产中</p>
              <div v-else class="chapter-list">
                <div v-for="(ch, i) in currentBook.chapters" :key="i" class="chapter-item">
                  <i class="ri-file-text-line"></i>
                  <a href="#">{{ ch }}</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { exerciseApi } from '@/api/exercise'

const list = ref([])
const pagination = ref({ page: 1, pageSize: 4, total: 0 })
const detailVisible = ref(false)
const currentBook = ref(null)

const totalPages = computed(() => Math.ceil(pagination.value.total / pagination.value.pageSize) || 0)
const pageSizes = computed(() => {
  const sizes = []
  for (let i = 4; i <= 40; i += 4) sizes.push(i)
  return sizes
})

function goPage(p) {
  if (p < 1 || p > totalPages.value) return
  pagination.value.page = p
  loadData()
}

async function loadData() {
  try {
    const res = await exerciseApi.getBookList({ page: pagination.value.page, pageSize: pagination.value.pageSize })
    if (res?.data) {
      list.value = res.data.list || []
      pagination.value.total = res.data.total || 0
    }
  } catch {}
}

function showDetail(item) {
  currentBook.value = item
  detailVisible.value = true
}

onMounted(() => loadData())
</script>

<style scoped>
.page { height: 100%; }
.page-padded { padding: 32px 64px; }

.book-grid { display: flex; flex-wrap: wrap; gap: 32px; }
.empty-state { font-size: 14px; color: #666; padding: 24px 0; }

.book-card { width: 200px; cursor: pointer; }
.book-cover {
  width: 200px; height: 280px;
  border: 1px solid #E5E7EB;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden; background: #f9f9f9;
}
.book-cover img { width: 181px; height: 260px; object-fit: fill; }
.cover-placeholder {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  color: #999; font-size: 14px; padding: 16px; text-align: center;
}
.cover-placeholder i { font-size: 36px; color: #ccc; }

.book-price {
  margin-top: 16px; text-align: center;
  font-size: 16px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  color: #FF0000;
}

.pagination-bar {
  margin-top: 32px; padding-top: 16px;
  display: flex; align-items: center; justify-content: space-between;
}
.count-info { font-size: 14px; color: #333; }
.pagination { display: flex; align-items: center; gap: 8px; }
.page-btn {
  min-width: 60px; height: 36px;
  border: 1px solid #E5E7EB; background: #fff;
  font-size: 14px; color: #333; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}
.page-btn:hover:not(:disabled) { border-color: #2563EB; color: #2563EB; }
.page-btn:disabled { color: #ccc; cursor: not-allowed; }
.page-btn.active-page { width: 36px; min-width: 36px; background: #EEE; border-color: #D1D5DB; }
.page-input {
  width: 48px; height: 36px;
  border: 1px solid #E5E7EB; background: #fff;
  font-size: 14px; color: #333;
  display: flex; align-items: center; justify-content: center;
}
.page-info { font-size: 14px; color: #333; min-width: 22px; text-align: center; }
.page-size-select {
  width: 60px; height: 36px;
  border: 1px solid #E5E7EB; background: #fff;
  font-size: 14px; color: #333; cursor: pointer; outline: none;
  text-align: center; appearance: none; padding-right: 16px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%236B7280' d='M12 16l-6-6h12z'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: right 4px center;
}

.detail-overlay { position: fixed; inset: 0; background: #F5F5F5; z-index: 1000; overflow-y: auto; }
.detail-panel { min-height: 100vh; }
.detail-header { background: #006644; padding: 32px 80px; position: relative; min-height: 200px; }
.close-btn { position: absolute; top: 1px; right: 80px; cursor: pointer; }
.close-btn i { font-size: 24px; color: #fff; }
.header-info { color: #fff; }
.book-title { font-size: 20px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; margin-bottom: 8px; }
.book-version { font-size: 16px; margin-bottom: 8px; }
.book-meta { font-size: 16px; display: flex; flex-wrap: wrap; gap: 8px 24px; margin-bottom: 16px; }
.buy-btn { width: 120px; height: 40px; background: #FF0000; color: #fff; border: none; border-radius: 4px; font-size: 16px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; }
.detail-body { padding: 0 80px; margin-top: -10px; }
.detail-card { background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.1); padding: 32px; min-height: 600px; }
.section { margin-bottom: 32px; }
.section:last-child { margin-bottom: 0; }
.section-title { font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; padding-bottom: 8px; }
.section-content { font-size: 16px; color: #333; padding-top: 16px; }
.chapter-list { padding-top: 16px; display: flex; flex-direction: column; gap: 8px; }
.chapter-item { display: flex; align-items: center; gap: 8px; }
.chapter-item i { font-size: 16px; color: #6B7280; }
.chapter-item a { font-size: 16px; color: #2B7CD3; text-decoration: none; }
</style>
