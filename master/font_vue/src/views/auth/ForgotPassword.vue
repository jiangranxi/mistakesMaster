<template>
  <div class="page-container">
    <h2 class="page-title">修改密码</h2>
    <div class="spacer-48"></div>

    <!-- 步骤指示器 -->
    <div class="steps-wrapper">
      <div class="steps">
        <StepItem :num="1" label="用户信息" :active="true" />
        <span class="step-line active"></span>
        <StepItem :num="2" label="验证用户" />
        <span class="step-line"></span>
        <StepItem :num="3" label="修改密码" />
        <span class="step-line"></span>
        <div class="step-col">
          <div class="step-circle">4</div>
          <span class="step-label">修改成功</span>
        </div>
      </div>
    </div>

    <div class="spacer-64"></div>

    <!-- 表单 -->
    <div class="form-wrapper">
      <div class="form">
        <div class="form-row">
          <label class="form-label">手机</label>
          <input class="form-input" v-model="phone" placeholder="手机" />
          <span class="spacer-16-h"></span>
          <span class="hint">请输入手机号</span>
        </div>
        <div class="spacer-32"></div>

        <div class="form-row">
          <label class="form-label">验证码</label>
          <div class="code-group">
            <input class="code-input" v-model="code" placeholder="验证码" />
            <button class="btn-code" @click="sendCode">{{ codeText }}</button>
          </div>
          <span class="spacer-16-h"></span>
          <span class="hint"></span>
        </div>

        <div class="spacer-48"></div>

        <div class="btn-wrapper">
          <button class="btn-submit" @click="handleSubmit">提交</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/api/auth'
import { useToast } from '@/composables/useToast'
import StepItem from './StepItem.vue'

const router = useRouter()
const toast = useToast()
const phone = ref('')
const code = ref('')
const codeText = ref('获取验证码')
const codeSending = ref(false)

async function sendCode() {
  if (!phone.value || codeSending.value) return
  codeSending.value = true
  try {
    await authApi.sendForgotCode(phone.value)
    let count = 60
    codeText.value = `${count}s`
    const timer = setInterval(() => { count--; codeText.value = `${count}s`; if (count <= 0) { clearInterval(timer); codeText.value = '获取验证码'; codeSending.value = false } }, 1000)
  } catch { codeText.value = '获取验证码'; codeSending.value = false }
}

async function handleSubmit() {
  if (!phone.value || !code.value) return
  try {
    await authApi.verifyUser({ phone: phone.value, code: code.value })
    router.push('/auth/forgot-verify')
  } catch (e) {
    toast.error(e?.response?.data?.message || '验证失败')
  }
}
</script>

<style scoped>
.page-container { min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 48px 16px; background: #fff; }
.page-title { font-size: 32px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #6B7280; }
.spacer-16-h { width: 16px; flex-shrink: 0; }
.spacer-32 { height: 32px; }
.spacer-48 { height: 48px; }
.spacer-64 { height: 64px; }

.steps-wrapper { padding: 0 320px; }
.steps { width: 768px; display: flex; align-items: flex-start; justify-content: center; }
.step-line { width: 179px; height: 4px; background: #D1D5DB; margin-top: 18px; }
.step-line.active { background: #3B82F6; }

.step-col { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.step-circle { width: 40px; height: 40px; border-radius: 50%; background: #D1D5DB; color: #6B7280; font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; display: flex; align-items: center; justify-content: center; }
.step-circle.active { background: #3B82F6; color: #fff; }
.step-label { font-size: 16px; color: #6B7280; white-space: nowrap; }
.step-label.active { color: #374151; }

.form-wrapper { padding: 0 320px; }
.form { width: 768px; display: flex; flex-direction: column; }
.form-row { display: flex; align-items: center; }
.form-label { width: 128px; text-align: right; font-size: 16px; color: #374151; }
.form-input { flex: 1; height: 44px; padding: 12px 16px; border: 0.8px solid #D1D5DB; border-radius: 4px; font-size: 16px; color: #374151; outline: none; }
.form-input::placeholder { color: #9CA3AF; }
.hint { width: 224px; font-size: 14px; color: #6B7280; }
.code-group { flex: 1; display: flex; }
.code-input { flex: 1; height: 44px; padding: 12px 16px; border: 0.8px solid #D1D5DB; border-radius: 4px 0 0 4px; font-size: 16px; outline: none; }
.btn-code { width: 192px; height: 44px; border: none; border-radius: 0 4px 4px 0; background: #22C55E; color: #fff; font-size: 16px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; }
.btn-wrapper { padding: 0 160px; }
.btn-submit { width: 448px; height: 60px; border: none; border-radius: 8px; background: #60A5FA; color: #fff; font-size: 20px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; }
</style>
