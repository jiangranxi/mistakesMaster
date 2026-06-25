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
          <input
            class="form-input"
            :class="{ 'input-error': errors.phone }"
            v-model="phone"
            placeholder="请输入手机号"
            maxlength="11"
            @focus="clearError('phone')"
          />
          <span class="hint" :class="{ 'hint-error': errors.phone }">{{ errors.phone || '请输入手机号' }}</span>
        </div>
        <div class="spacer-16"></div>

        <div class="form-row">
          <label class="form-label">验证码</label>
          <input
            class="form-input"
            :class="{ 'input-error': errors.code }"
            v-model="code"
            placeholder="验证码"
            @focus="clearError('code')"
          />
          <div class="code-area">
            <span class="hint-inline" v-if="errors.code">{{ errors.code }}</span>
            <button class="btn-code" @click="sendCode">{{ codeText }}</button>
          </div>
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
import { ref, reactive } from 'vue'
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
const errors = reactive({})

function clearError(field) {
  errors[field] = ''
}

async function sendCode() {
  if (codeSending.value) return
  if (!phone.value) {
    errors.phone = '手机号为空！'
    return
  }
  if (!/^\d{11}$/.test(phone.value)) {
    errors.phone = '手机号格式不正确'
    return
  }
  errors.phone = ''
  codeSending.value = true
  try {
    const res = await authApi.sendForgotCode(phone.value)
    if (res?.message) toast.info(res.message)
    let count = 60
    codeText.value = `${count}s`
    const timer = setInterval(() => {
      count--
      codeText.value = `${count}s`
      if (count <= 0) {
        clearInterval(timer)
        codeText.value = '获取验证码'
        codeSending.value = false
      }
    }, 1000)
  } catch (e) {
    toast.error(e?.response?.data?.message || '发送失败，请稍后重试')
    codeText.value = '获取验证码'
    codeSending.value = false
  }
}

async function handleSubmit() {
  if (!phone.value) {
    errors.phone = '手机号为空！'
    return
  }
  if (!/^\d{11}$/.test(phone.value)) {
    errors.phone = '手机号格式不正确'
    return
  }
  if (!code.value) {
    errors.code = '验证码为空！'
    return
  }
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
.spacer-16 { height: 16px; }
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
.form-label { width: 120px; padding-right: 16px; text-align: right; font-size: 15px; color: #374151; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif; flex-shrink: 0; }

.form-input {
  flex: 1;
  height: 40px;
  padding: 0 14px;
  border: 0.8px solid #D1D5DB;
  border-radius: 4px;
  font-size: 15px;
  color: #374151;
  font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif;
  outline: none;
  transition: box-shadow 0.2s, border-color 0.2s;
}
.form-input:focus { border-color: #2563EB; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15); }
.form-input::placeholder { color: #9CA3AF; }
.form-input.input-error { border-color: #EF4444; }
.form-input.input-error:focus { box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15); }

.hint { width: 200px; margin-left: 16px; font-size: 13px; color: #B0B0B0; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif; flex-shrink: 0; }
.hint.hint-error { color: #EF4444; }

.code-area { width: 200px; margin-left: 16px; flex-shrink: 0; display: flex; flex-direction: column; align-items: flex-start; }
.hint-inline { font-size: 13px; color: #EF4444; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif; margin-bottom: 4px; }
.btn-code { height: 40px; padding: 0 16px; border: none; border-radius: 4px; background: #22C55E; color: #fff; font-size: 13px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; white-space: nowrap; }
.btn-code:hover { background: #16A34A; }

.btn-wrapper { padding-left: 136px; }
.btn-submit { width: calc(768px - 120px - 16px - 200px - 16px); height: 44px; border: none; border-radius: 8px; background: #2563EB; color: #fff; font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; }
.btn-submit:hover { background: #3B82F6; }
</style>
