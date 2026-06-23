<template>
  <div class="page-container">
    <h2 class="page-title">修改密码</h2>
    <div class="spacer-48"></div>

    <div class="steps-wrapper">
      <div class="steps">
        <StepItem :num="1" label="用户信息" :active="true" />
        <span class="step-line active"></span>
        <StepItem :num="2" label="验证用户" :active="true" />
        <span class="step-line active"></span>
        <StepItem :num="3" label="修改密码" :active="true" />
        <span class="step-line"></span>
        <StepItem :num="4" label="修改成功" />
      </div>
    </div>

    <div class="spacer-64"></div>

    <div class="form-wrapper">
      <div class="form">
        <div class="form-row">
          <label class="form-label">密码</label>
          <input
            class="form-input"
            :class="{ 'input-error': errors.password }"
            v-model="password"
            type="password"
            placeholder="密码"
            @focus="clearError('password')"
          />
          <span class="hint" :class="{ 'hint-error': errors.password }">{{ errors.password || '6-20个数字、字母组成！' }}</span>
        </div>
        <div class="spacer-16"></div>

        <div class="form-row">
          <label class="form-label">确认密码</label>
          <input
            class="form-input"
            :class="{ 'input-error': errors.confirm }"
            v-model="confirmPassword"
            type="password"
            placeholder="确认密码"
            @focus="clearError('confirm')"
          />
          <span class="hint" :class="{ 'hint-error': errors.confirm }">{{ errors.confirm || '再次输入密码' }}</span>
        </div>

        <div class="spacer-48"></div>

        <div class="btn-wrapper">
          <button class="btn-modify" @click="handleReset">修改</button>
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
const password = ref('')
const confirmPassword = ref('')
const errors = reactive({})

function clearError(field) {
  errors[field] = ''
}

async function handleReset() {
  if (!password.value) {
    errors.password = '密码为空！'
    return
  }
  if (password.value.length < 6 || password.value.length > 20) {
    errors.password = '6-20个数字、字母组成！'
    return
  }
  if (!confirmPassword.value) {
    errors.confirm = '请再次输入密码'
    return
  }
  if (password.value !== confirmPassword.value) {
    errors.confirm = '两次密码不一致'
    return
  }
  try {
    await authApi.resetPassword({ password: password.value })
    router.push('/auth/forgot-success')
  } catch (e) { toast.error(e?.response?.data?.message || '修改失败') }
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

.btn-wrapper { padding-left: 136px; }
.btn-modify { width: calc(768px - 120px - 16px - 200px - 16px); height: 44px; border: none; border-radius: 8px; background: #2563EB; color: #fff; font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; }
.btn-modify:hover { background: #3B82F6; }
</style>
