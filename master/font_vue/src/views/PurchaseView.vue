<template>
  <div class="purchase-page">
    <div class="purchase-container">
      <h2 class="page-title">确认订单</h2>

      <div class="order-card">
        <!-- 书籍信息 -->
        <div class="book-row">
          <div class="book-cover">
            <img v-if="book.cover" :src="book.cover" :alt="book.name" />
            <div v-else class="cover-placeholder">
              <i class="ri-book-2-line"></i>
            </div>
          </div>
          <div class="book-info">
            <h3 class="book-name">《{{ book.name || '加载中...' }}》</h3>
            <div class="book-meta">
              <span v-if="book.publisher">出版社：{{ book.publisher }}</span>
              <span v-if="book.subject">学科：{{ book.subject }}</span>
              <span v-if="book.version">版本：{{ book.version }}</span>
              <span v-if="book.gradeTerm">年级学期：{{ book.gradeTerm }}</span>
            </div>
            <div class="price-row">
              <span class="price-label">单价：</span>
              <span class="price-value">¥ {{ (book.price || 0).toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- 支付方式 -->
        <div class="payment-section">
          <h4 class="section-label">支付方式</h4>
          <div class="payment-options">
            <label
              class="payment-option"
              :class="{ active: paymentMethod === 'wechat' }"
              @click="paymentMethod = 'wechat'"
            >
              <i class="ri-wechat-line"></i>
              <span>微信支付</span>
            </label>
            <label
              class="payment-option"
              :class="{ active: paymentMethod === 'alipay' }"
              @click="paymentMethod = 'alipay'"
            >
              <i class="ri-bank-card-line"></i>
              <span>支付宝</span>
            </label>
          </div>
        </div>

        <div class="divider"></div>

        <!-- 合计 -->
        <div class="total-row">
          <span class="total-label">实付金额：</span>
          <span class="total-price">¥ {{ (book.price || 0).toFixed(2) }}</span>
        </div>

        <!-- 按钮 -->
        <div class="button-row">
          <button class="btn-back" @click="goBack">返回</button>
          <button class="btn-pay" :disabled="paying" @click="confirmPay">
            {{ paying ? '支付中...' : '确认支付' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { exerciseApi } from '@/api/exercise'
import { memberApi } from '@/api/member'
import { useToast } from '@/composables/useToast'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const book = ref({})
const paymentMethod = ref('wechat')
const paying = ref(false)

onMounted(async () => {
  const id = route.params.id
  if (!id) {
    toast.error('缺少书籍信息')
    goBack()
    return
  }
  try {
    const res = await exerciseApi.getBookDetail(id)
    if (res) book.value = res
  } catch {
    toast.error('获取书籍信息失败')
  }
})

function goBack() {
  const role = authStore.userRole
  router.push(`/${role}/exercises`)
}

async function confirmPay() {
  if (paying.value) return
  paying.value = true
  try {
    await memberApi.createOrder({
      bookId: book.value.id,
      paymentMethod: paymentMethod.value
    })
    toast.success('支付成功')
    // 跳转到订单页
    const role = authStore.userRole
    router.push(`/${role}/member/orders`)
  } catch {
    toast.error('支付失败，开发中')
  } finally {
    paying.value = false
  }
}
</script>

<style scoped>
.purchase-page {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  background: #F5F5F5;
  display: flex;
  justify-content: center;
  padding: 48px 0;
}

.purchase-container {
  width: 640px;
}

.page-title {
  text-align: center;
  font-size: 22px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  color: #333;
  margin-bottom: 32px;
}

.order-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.06);
  padding: 32px;
}

/* 书籍信息行 */
.book-row {
  display: flex;
  gap: 24px;
}

.book-cover {
  width: 140px;
  height: 180px;
  flex-shrink: 0;
  border: 1px solid #E5E7EB;
  border-radius: 4px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9f9f9;
}
.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: fill;
}
.cover-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ccc;
}
.cover-placeholder i {
  font-size: 48px;
}

.book-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.book-name {
  font-size: 18px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  color: #333;
  margin-bottom: 12px;
}

.book-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 14px;
  color: #6B7280;
}

.price-row {
  display: flex;
  align-items: baseline;
  margin-top: 8px;
}
.price-label {
  font-size: 14px;
  color: #6B7280;
}
.price-value {
  font-size: 20px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  color: #FF4D4F;
}

/* 分割线 */
.divider {
  height: 1px;
  background: #E5E7EB;
  margin: 24px 0;
}

/* 支付方式 */
.section-label {
  font-size: 16px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  color: #333;
  margin-bottom: 16px;
}

.payment-options {
  display: flex;
  gap: 16px;
}

.payment-option {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 48px;
  border: 1px solid #D1D5DB;
  border-radius: 4px;
  cursor: pointer;
  font-size: 15px;
  color: #333;
  transition: border-color 0.2s, color 0.2s;
}
.payment-option i {
  font-size: 22px;
}
.payment-option.active {
  border-color: #2563EB;
  color: #2563EB;
}
.payment-option.active i {
  color: #2563EB;
}

/* 合计 */
.total-row {
  display: flex;
  align-items: baseline;
  justify-content: flex-end;
}
.total-label {
  font-size: 16px;
  color: #333;
}
.total-price {
  font-size: 24px;
  font-family: 'SourceHanSans-Bold', 'Noto Sans SC', sans-serif;
  color: #FF4D4F;
}

/* 按钮 */
.button-row {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 32px;
}

.btn-back {
  width: 100px;
  height: 40px;
  border: 1px solid #D1D5DB;
  border-radius: 8px;
  background: #fff;
  font-size: 15px;
  color: #6B7280;
  cursor: pointer;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
}
.btn-back:hover {
  border-color: #2563EB;
  color: #2563EB;
}

.btn-pay {
  width: 140px;
  height: 40px;
  border: none;
  border-radius: 8px;
  background: #FF0000;
  font-size: 16px;
  color: #fff;
  cursor: pointer;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
}
.btn-pay:hover {
  background: #E50000;
}
.btn-pay:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
