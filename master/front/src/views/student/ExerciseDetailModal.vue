<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <span class="close-btn" @click="$emit('close')">✕</span>
      </div>
      <div class="modal-body">
        <div class="book-info">
          <h3>{{ book.name }}</h3>
          <p><span>学科：</span>{{ book.subject || '-' }}</p>
          <p><span>价格：</span><span class="price">¥{{ book.price }}</span></p>
          <p><span>作者：</span>{{ book.author || '-' }}</p>
          <p><span>出版社：</span>{{ book.publisher || '-' }}</p>
          <button class="btn btn-primary purchase-btn" @click="handlePurchase">
            <span>💰</span>
            <span>购买</span>
          </button>
        </div>
        <div class="section">
          <h4>简介</h4>
          <p>{{ book.description || '暂无简介' }}</p>
        </div>
        <div class="section">
          <h4>目录</h4>
          <div class="catalog">
            <p v-for="(ch, idx) in catalogList" :key="idx">• {{ ch }}</p>
            <p v-if="catalogList.length === 0">暂无目录</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { exerciseApi } from '@/api/exercise'

const props = defineProps({ book: Object })
const emit = defineEmits(['close'])

const catalogList = computed(() => {
  if (!props.book?.catalog) return []
  return props.book.catalog.split('\n').filter(Boolean)
})

async function handlePurchase() {
  try {
    await exerciseApi.purchaseBook(props.book.id)
    alert('购买成功')
    emit('close')
  } catch { /* 错误由拦截器处理 */ }
}
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.4); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: #fff; border-radius: 12px; width: 1000px; max-height: 80vh; overflow-y: auto; }
.modal-header { padding: 12px 24px; display: flex; justify-content: flex-end; }
.close-btn { cursor: pointer; font-size: 22px; color: #999; }
.modal-body { padding: 0 48px 48px; }
.book-info { margin-bottom: 24px; }
.book-info h3 { font-size: 20px; margin-bottom: 16px; }
.book-info p { font-size: 14px; color: #666; margin-bottom: 8px; }
.book-info p span:first-child { color: #999; }
.price { color: #FF4D4F; font-weight: 600; }
.purchase-btn { display: flex; align-items: center; gap: 8px; margin-top: 16px; }
.section { margin-bottom: 24px; }
.section h4 { font-size: 16px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #f0f0f0; }
.section p { font-size: 14px; color: #666; line-height: 1.8; }
.catalog p { font-size: 14px; color: #333; line-height: 1.8; }
</style>
