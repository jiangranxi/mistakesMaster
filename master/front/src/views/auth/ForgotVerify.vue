<template>
  <div class="forgot-view">
    <h2 class="page-title">忘记密码</h2>

    <div class="steps">
      <div class="step done"><div class="step-num">✓</div><span>用户信息</span></div>
      <div class="step-line done"></div>
      <div class="step active"><div class="step-num">2</div><span>验证用户</span></div>
      <div class="step-line"></div>
      <div class="step"><div class="step-num">3</div><span>修改密码</span></div>
      <div class="step-line"></div>
      <div class="step"><div class="step-num">4</div><span>修改成功</span></div>
    </div>

    <div class="verify-result">
      <div class="result-icon">✓</div>
      <p class="result-text">用户验证成功</p>
      <p class="result-desc">请点击下一步继续修改密码</p>
    </div>

    <button class="btn btn-primary btn-lg" style="width:100%;height:44px;margin-top:24px" @click="$router.push('/auth/forgot-reset')">
      下一步
    </button>
  </div>
</template>

<script setup>
</script>

<style scoped>
.page-title { font-size: 20px; margin-bottom: 24px; text-align: center; }
.steps { display: flex; align-items: center; justify-content: center; margin-bottom: 32px; gap: 0; }
.step { display: flex; flex-direction: column; align-items: center; gap: 4px; font-size: 11px; color: #999; }
.step.done .step-num { background: #52C41A; color: #fff; }
.step.done span { color: #52C41A; }
.step.active .step-num { background: #4A90D9; color: #fff; }
.step.active span { color: #4A90D9; }
.step-num { width: 28px; height: 28px; line-height: 28px; text-align: center; border-radius: 50%; background: #f0f0f0; color: #999; font-size: 13px; font-weight: 500; }
.step-line { width: 40px; height: 2px; background: #f0f0f0; margin-bottom: 16px; }
.step-line.done { background: #52C41A; }
.verify-result { text-align: center; padding: 32px 0; }
.result-icon { width: 60px; height: 60px; line-height: 60px; border-radius: 50%; background: #f6ffed; color: #52C41A; font-size: 28px; margin: 0 auto 16px; }
.result-text { font-size: 18px; font-weight: 500; }
.result-desc { color: #999; margin-top: 8px; }
</style>
