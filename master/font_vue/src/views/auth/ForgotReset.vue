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
          <input class="form-input" v-model="password" type="password" placeholder="密码" />
          <span class="spacer-16-h"></span>
          <span class="hint">6-20个数字、字母组成！</span>
        </div>
        <div class="spacer-32"></div>

        <div class="form-row">
          <label class="form-label">确认密码</label>
          <input class="form-input" v-model="confirmPassword" type="password" placeholder="确认密码" />
          <span class="spacer-16-h"></span>
          <span class="hint">再次输入密码</span>
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/api/auth'
import { useToast } from '@/composables/useToast'
import StepItem from './StepItem.vue'

const router = useRouter()
const toast = useToast()
const password = ref('')
const confirmPassword = ref('')

async function handleReset() {
  if (!password.value) return
  if (password.value !== confirmPassword.value) { toast.error('两次密码不一致'); return }
  try {
    await authApi.resetPassword({ password: password.value })
    router.push('/auth/forgot-success')
  } catch (e) { toast.error(e?.response?.data?.message || '修改失败') }
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
.form-wrapper { padding: 0 320px; }
.form { width: 768px; display: flex; flex-direction: column; }
.form-row { display: flex; align-items: center; }
.form-label { width: 128px; text-align: right; font-size: 16px; color: #374151; }
.form-input { width: 256px; height: 44px; padding: 12px 16px; border: 0.8px solid #D1D5DB; border-radius: 4px; font-size: 16px; color: #374151; outline: none; }
.form-input::placeholder { color: #9CA3AF; }
.hint { width: 224px; font-size: 14px; color: #6B7280; }
.btn-wrapper { padding: 0 160px; }
.btn-modify { width: 448px; height: 60px; border: none; border-radius: 8px; background: #60A5FA; color: #fff; font-size: 20px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; }
</style>
