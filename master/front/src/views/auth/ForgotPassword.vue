<template>
  <div class="forgot-view">
    <h2 class="page-title">忘记密码</h2>

    <!-- 步骤指示器 -->
    <div class="steps">
      <div class="step active"><div class="step-num">1</div><span>用户信息</span></div>
      <div class="step-line"></div>
      <div class="step"><div class="step-num">2</div><span>验证用户</span></div>
      <div class="step-line"></div>
      <div class="step"><div class="step-num">3</div><span>修改密码</span></div>
      <div class="step-line"></div>
      <div class="step"><div class="step-num">4</div><span>修改成功</span></div>
    </div>

    <div class="form-group">
      <label class="form-label">手机号</label>
      <input v-model="form.phone" class="form-input" placeholder="请输入注册手机号" maxlength="11" />
    </div>

    <div class="form-group">
      <label class="form-label">验证码</label>
      <div class="verify-row">
        <input v-model="form.verifyCode" class="form-input" placeholder="请输入验证码" />
        <button class="btn verify-btn" :disabled="countdown > 0" @click="sendCode">
          {{ countdown > 0 ? countdown + 's' : '获取验证码' }}
        </button>
      </div>
    </div>

    <button class="btn btn-primary btn-lg" style="width:100%;height:44px;margin-top:24px" :disabled="loading" @click="handleSubmit">
      {{ loading ? '提交中...' : '提 交' }}
    </button>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const countdown = ref(0)
const form = reactive({ phone: '', verifyCode: '' })

async function sendCode() {
  if (!form.phone) { alert('请先输入手机号'); return }
  try {
    await auth.sendVerifyCode(form.phone)
    countdown.value = 60
    const timer = setInterval(() => { countdown.value--; if (countdown.value <= 0) clearInterval(timer) }, 1000)
  } catch (e) { alert(e.message || '发送失败') }
}

async function handleSubmit() {
  if (!form.phone || !form.verifyCode) { alert('请填写完整信息'); return }
  loading.value = true
  try {
    await authApi.verifyUser({ phone: form.phone, code: form.verifyCode })
    router.push('/auth/forgot-verify')
  } catch (e) { alert(e.message || '验证失败') }
  finally { loading.value = false }
}
</script>

<script>import { authApi } from '@/api/auth'; export default {} </script>

<style scoped>
.page-title { font-size: 20px; margin-bottom: 24px; text-align: center; }
.steps { display: flex; align-items: center; justify-content: center; margin-bottom: 32px; gap: 0; }
.step { display: flex; flex-direction: column; align-items: center; gap: 4px; font-size: 11px; color: #999; }
.step.active .step-num { background: #4A90D9; color: #fff; }
.step.active span { color: #4A90D9; }
.step-num { width: 28px; height: 28px; line-height: 28px; text-align: center; border-radius: 50%; background: #f0f0f0; color: #999; font-size: 13px; font-weight: 500; }
.step-line { width: 40px; height: 2px; background: #f0f0f0; margin: 0 4px; margin-bottom: 16px; }
.verify-row { display: flex; gap: 12px; }
.verify-btn { min-width: 110px; height: 36px; white-space: nowrap; }
</style>
