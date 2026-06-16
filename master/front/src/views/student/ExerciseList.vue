<template>
  <div class="exercise-page">
    <div class="card">
      <div class="exercise-grid">
        <div class="book-card" v-for="book in bookList" :key="book.id" @click="showDetail(book)">
          <div class="book-cover">
            <span class="cover-text">{{ book.name }}</span>
          </div>
          <div class="book-price">¥{{ book.price }}</div>
        </div>
      </div>
      <div class="bottom-bar">
        <span class="total-count">共 {{ total }} 本习题集</span>
        <div class="pagination" v-if="total > pageSize">
          <button class="btn btn-sm" @click="page = 1">首页</button>
          <button class="btn btn-sm" @click="page--" :disabled="page <= 1">上一页</button>
          <button class="btn btn-sm page-current">{{ page }}</button>
          <button class="btn btn-sm" @click="page++" :disabled="page * pageSize >= total">下一页</button>
          <button class="btn btn-sm" @click="page = Math.ceil(total / pageSize)">尾页</button>
        </div>
      </div>
    </div>

    <!-- 习题集详情弹窗 -->
    <ExerciseDetailModal v-if="selectedBook" :book="selectedBook" @close="selectedBook = null" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ExerciseDetailModal from './ExerciseDetailModal.vue'

const bookList = ref([])
const page = ref(1)
const pageSize = ref(8)
const total = ref(0)
const selectedBook = ref(null)

function showDetail(book) { selectedBook.value = book }
</script>

<style scoped>
.exercise-grid { display: flex; gap: 24px; flex-wrap: wrap; }
.book-card { width: 240px; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,.06); overflow: hidden; cursor: pointer; transition: transform .2s; }
.book-card:hover { transform: translateY(-2px); }
.book-cover { height: 300px; background: linear-gradient(135deg, #4A90D9, #6EB1FF); display: flex; align-items: center; justify-content: center; color: #fff; font-size: 18px; font-weight: 600; padding: 20px; text-align: center; }
.book-price { padding: 12px 16px; text-align: center; font-size: 16px; color: #FF4D4F; font-weight: 600; }
.bottom-bar { display: flex; justify-content: space-between; align-items: center; margin-top: 24px; padding-top: 16px; border-top: 1px solid #f0f0f0; }
.total-count { font-size: 13px; color: #999; }
</style>
