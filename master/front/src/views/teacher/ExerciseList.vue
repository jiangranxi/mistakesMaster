<template>
  <div class="exercise-page">
    <div class="card">
      <h3 class="page-title">习题集</h3>

      <div class="book-grid">
        <div v-for="book in bookList" :key="book.id" class="book-card" @click="showDetail(book)">
          <div class="book-cover">
            <div class="cover-placeholder">{{ book.name?.charAt(0) }}</div>
          </div>
          <div class="book-info">
            <div class="book-name">{{ book.name }}</div>
            <div class="book-price">&yen;{{ book.price }}</div>
          </div>
        </div>
      </div>

      <div v-if="bookList.length === 0" class="empty-state">暂无书籍</div>

      <!-- 分页 -->
      <div class="pagination" v-if="total > pageSize">
        <button class="btn btn-sm" :disabled="page === 1" @click="page--">首页</button>
        <button class="btn btn-sm" :disabled="page === 1" @click="page--">上一页</button>
        <button class="btn btn-sm btn-primary">{{ page }}</button>
        <button class="btn btn-sm" @click="page++">下一页</button>
        <button class="btn btn-sm" @click="page = totalPages">尾页</button>
        <span>共 {{ total }} 本</span>
      </div>
    </div>

    <!-- 书籍详情弹窗 -->
    <div v-if="detailBook" class="modal-overlay" @click.self="detailBook = null">
      <div class="modal" style="width:800px;max-height:80vh;overflow-y:auto">
        <div class="modal-header">
          <h4>书籍详情</h4>
          <button class="btn btn-sm" @click="detailBook = null">✕</button>
        </div>
        <div class="modal-body">
          <div class="detail-top">
            <div class="detail-cover">
              <div class="cover-placeholder large">{{ detailBook.name?.charAt(0) }}</div>
            </div>
            <div class="detail-info">
              <h3>{{ detailBook.name }}</h3>
              <p class="price">&yen;{{ detailBook.price }}</p>
              <button class="btn btn-primary" @click="purchaseBook(detailBook)">购买</button>
            </div>
          </div>
          <div class="detail-section">
            <h4>简介</h4>
            <p>{{ detailBook.description || '暂无简介' }}</p>
          </div>
          <div class="detail-section">
            <h4>目录</h4>
            <p>{{ detailBook.catalog || '暂无目录' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const bookList = ref([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const detailBook = ref(null)

function showDetail(book) { detailBook.value = book }
function purchaseBook(book) { /* 购买 */ alert('购买功能开发中') }
</script>

<style scoped>
.page-title { font-size: 18px; margin-bottom: 20px; }
.book-grid { display: flex; flex-wrap: wrap; gap: 20px; }
.book-card { width: 200px; cursor: pointer; transition: box-shadow .2s; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.book-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,.1); }
.book-cover { height: 280px; background: #f0f5ff; display: flex; align-items: center; justify-content: center; }
.cover-placeholder { width: 120px; height: 160px; background: #4A90D9; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 40px; border-radius: 8px; }
.cover-placeholder.large { width: 160px; height: 220px; font-size: 56px; }
.book-info { padding: 12px; background: #fff; }
.book-name { font-size: 14px; font-weight: 500; }
.book-price { font-size: 16px; color: #FF4D4F; margin-top: 4px; }
.detail-top { display: flex; gap: 24px; margin-bottom: 24px; }
.detail-info h3 { font-size: 20px; margin-bottom: 8px; }
.detail-info .price { font-size: 24px; color: #FF4D4F; margin-bottom: 16px; }
.detail-section { margin-bottom: 20px; }
.detail-section h4 { font-size: 15px; margin-bottom: 8px; color: #333; }
.detail-section p { color: #666; line-height: 1.8; }
</style>
