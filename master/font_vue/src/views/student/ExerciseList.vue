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

      <hr class="divider" />

      <!-- <div class="spacer-16"></div> -->

      <div class="pagination-bar">
        <span class="count-info">数量: {{ pagination.total }}</span>
        <PaginationBar
          variant="student"
          :page="pagination.page"
          :pageSize="pagination.pageSize"
          :totalPages="totalPages"
          @page-change="goPage"
          @page-size-change="val => { pagination.pageSize = val; loadData() }"
        />
      </div>
    </div>

    <!-- 详情弹窗 -->
    <div v-if="detailVisible" class="detail-overlay">
      <div class="detail-panel">
        <div class="detail-header">
          <span class="close-btn" @click="detailVisible = false"><i class="ri-close-line"></i></span>
          <div class="header-info">
            <h2 class="book-title">《{{ currentBook?.name }}》</h2>
            <div class="book-version">出版社：{{ currentBook?.publisher }}</div>
            <div class="book-meta">
              <span v-if="currentBook?.updateTime">更新时间: {{ currentBook.updateTime }}</span>
              <span v-if="currentBook?.version">教材版本: {{ currentBook.version }}</span>
              <span v-if="currentBook?.subject">学 科: {{ currentBook.subject }}</span>
              <span v-if="currentBook?.gradeTerm">年级学期: {{ currentBook.gradeTerm }}</span>
            </div>
            <button class="buy-btn" @click.stop="goBuy(currentBook)">购买 ¥ {{ (currentBook?.price || 0).toFixed(2) }}</button>
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
                <ChapterTree :nodes="currentBook.chapters" />
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
import { useRouter } from 'vue-router'
import { exerciseApi } from '@/api/exercise'
import PaginationBar from '@/components/PaginationBar.vue'
import ChapterTree from '@/components/ChapterTree.vue'

const router = useRouter()
const list = ref([])
const pagination = ref({ page: 1, pageSize: 15, total: 0 })
const detailVisible = ref(false)
const currentBook = ref(null)

const totalPages = computed(() => Math.ceil(pagination.value.total / pagination.value.pageSize) || 0)
function goPage(p) {
  if (p < 1 || p > totalPages.value) return
  pagination.value.page = p
  loadData()
}

async function loadData() {
  try {
    const res = await exerciseApi.getBookList({ page: pagination.value.page, pageSize: pagination.value.pageSize })
    if (res) {
      list.value = res.list || []
      pagination.value.total = res.total || 0
    }
  } catch {}
}

function showDetail(item) {
  currentBook.value = item
  detailVisible.value = true
}

function goBuy(book) {
  if (book?.id) {
    router.push(`/student/exercises/buy/${book.id}`)
  }
}

onMounted(() => loadData())
</script>

<style scoped>
.page { height: 100%; }
.page-padded { padding: 32px 100px; }

.book-grid { display: flex; flex-wrap: wrap; gap: 32px; }
.empty-state { font-size: 14px; color: #666; padding: 24px 0; }

.book-card {
  width: 240px;
  cursor: pointer;
  border: 1px solid #E5E7EB;
  border-radius: 4px;
  overflow: hidden;
}
.book-cover {
  width: 240px; height: 300px;
  background: #fff;
  display: flex; align-items: center; justify-content: center;
}
.book-cover img { width: 181px; height: 240px; object-fit: fill; }
.cover-placeholder {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  color: #999; font-size: 14px; padding: 16px; text-align: center;
}
.cover-placeholder i { font-size: 36px; color: #ccc; }

.book-price {
  height: 60px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  color: #FF4D4F;
}

.pagination-bar {
  margin-top: 0px; padding-top: 0px;
  display: flex; align-items: center; justify-content: space-between;
}
.count-info { font-size: 14px; color: #333; }

.detail-overlay { position: fixed; inset: 0; background: #F5F5F5; z-index: 1000; overflow-y: auto; }
.detail-panel { min-height: 100vh; }
.detail-header { background: #006644; padding: 32px 80px; position: relative; min-height: 200px; }
.close-btn { position: absolute; top: 1px; right: 80px; cursor: pointer; }
.close-btn i { font-size: 24px; color: #fff; }
.header-info { color: #fff; }
.book-title { font-size: 20px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; margin-bottom: 8px; }
.book-version { font-size: 16px; margin-bottom: 8px; }
.book-meta { font-size: 16px; display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px; }
.buy-btn { width: 120px; height: 40px; background: #FF0000; color: #fff; border: none; border-radius: 4px; font-size: 16px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; }
.detail-body { padding: 0 80px; margin-top: -10px; }
.detail-card { background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.1); padding: 32px; min-height: 600px; }
.section { margin-bottom: 32px; }
.section:last-child { margin-bottom: 0; }
.section-title { font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; padding-bottom: 8px; }
.section-content { font-size: 16px; color: #333; padding-top: 16px; }
.chapter-list { padding-top: 16px; display: flex; flex-direction: column; gap: 8px; }
.spacer-16 { height: 16px; }
.divider {
  border: none;           /* 去掉默认边框 */
  height: 1px;            /* 线条粗细 */
  background-color: #e0e0e0; /* 线条颜色 */
  margin: 20px 0;         /* 上下间距，左右为0实现充满 */
  width: 100%;            /* 宽度100%填满父容器 */
}
</style>
