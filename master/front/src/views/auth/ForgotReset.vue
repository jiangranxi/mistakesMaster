<template>
  <div class="forgot-view">
    <h2 class="page-title">忘记密码</h2>

    <div class="steps">
      <div class="step done"><div class="step-num">✓</div><span>用户信息</span></div>
      <div class="step-line done"></div>
      <div class="step done"><div class="step-num">✓</div><span>验证用户</span></div>
      <div class="step-line done"></div>
      <div class="step active"><div class="step-num">3</div><span>修改密码</span></div>
      <div class="step-line"></div>
      <div class="step"><div class="step-num">4</div><span>修改成功</span></div>
    </div>

    <div class="form-group">
      <label class="form-label">新密码</label>
      <input v-model="form.password" class="form-input" type="password" placeholder="请输入新密码（6-20位）" />
    </div>

    <div class="form-group">
      <label class="form-label">确认密码</label>
      <input v-model="form.confirmPassword" class="form-input" type="password" placeholder="请再次输入新密码" />
      <span v-if="pwdError" class="hint">{{ pwdError }}</span>
    </div>

    <button class="btn btn-primary btn-lg" style="width:100%;height:44px;margin-top:24px" :disabled="loading" @click="handleReset">
      {{ loading ? '修改中...' : '修 改' }}
    </button>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const form = reactive({ password: '', confirmPassword: '' })

const pwdError = computed(() => {
  if (form.confirmPassword && form.password !== form.confirmPassword) return '两次密码不一致'
  return ''
})

async function handleReset() {
  if (pwdError.value) return
  if (!form.password) { alert('请输入新密码'); return }
  loading.value = true
  try {
    await auth.resetPassword({ password: form.password })
    router.push('/auth/forgot-success')
  } catch (e) { alert(e.message || '修改失败') }
  finally { loading.value = false }
}
</script>

<style scoped>
.page-title { font-size: 20px; margin-bottom: 24px; text-align: center; }
.steps { display: flex; align-items: center; justify-content: center; margin-bottom: 32px; }
.step { display: flex; flex-direction: column; align-items: center; gap: 4px; font-size: 11px; color: #999; }
.step.done .step-num { background: #52C41A; color: #fff; }
.step.done span { color: #52C41A; }
.step.active .step-num { background: #4A90D9; color: #fff; }
.step.active span { color: #4A90D9; }
.step-num { width: 28px; height: 28px; line-height: 28px; text-align: center; border-radius: 50%; background: #f0f0f0; color: #999; font-size: 13px; font-weight: 500; }
.step-line { width: 40px; height: 2px; background: #f0f0f0; margin-bottom: 16px; }
.step-line.done { background: #52C41A; }
.hint { color: #FF4D4F; font-size: 12px; margin-top: 4px; }
</style>
