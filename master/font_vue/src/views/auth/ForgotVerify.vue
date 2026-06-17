<template>
  <div class="page-container">
    <h2 class="page-title">修改密码</h2>
    <div class="spacer-48"></div>

    <div class="steps-wrapper">
      <div class="steps">
        <StepItem :num="1" label="用户信息" :active="true" />
        <span class="step-line active"></span>
        <StepItem :num="2" label="验证用户" :active="true" />
        <span class="step-line"></span>
        <StepItem :num="3" label="修改密码" />
        <span class="step-line"></span>
        <StepItem :num="4" label="修改成功" />
      </div>
    </div>

    <div class="spacer-64"></div>

    <div class="verify-wrapper">
      <p class="verify-text">用户身份验证合法</p>
    </div>

    <div class="spacer-48"></div>

    <div class="btn-wrapper">
      <button class="btn-next" @click="$router.push('/auth/forgot-reset')">下一步</button>
    </div>
  </div>
</template>

<script setup>
import StepItem from './StepItem.vue'
</script>

<style scoped>
.page-container { min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 48px 16px; background: #fff; }
.page-title { font-size: 32px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #6B7280; }
.spacer-48 { height: 48px; }
.spacer-64 { height: 64px; }
.steps-wrapper { padding: 0 320px; }
.steps { width: 768px; display: flex; align-items: flex-start; justify-content: center; }
.step-line { width: 179px; height: 4px; background: #D1D5DB; margin-top: 18px; }
.step-line.active { background: #3B82F6; }
.verify-wrapper { padding: 0 320px; text-align: center; }
.verify-text { font-size: 20px; color: #374151; }
.btn-wrapper { padding: 0 480px; }
.btn-next { width: 448px; height: 60px; border: none; border-radius: 8px; background: #60A5FA; color: #fff; font-size: 20px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; }
</style>
