<template>
  <div class="auth-layout">
    <div class="auth-container">
      <div class="auth-brand">
        <div class="brand-logo">📘</div>
        <div class="brand-name">错题通</div>
        <div class="brand-subtitle">智能教学管理平台</div>
      </div>
      <router-view />
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #E8F0FE 0%, #F5F5F5 100%);
}

.auth-container {
  width: 448px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  padding: 48px 40px;
}

.auth-brand {
  text-align: center;
  margin-bottom: 40px;
}

.brand-logo {
  width: 80px;
  height: 80px;
  line-height: 80px;
  font-size: 40px;
  margin: 0 auto 12px;
  border-radius: 16px;
  background: #F0F5FF;
}

.brand-name {
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.brand-subtitle {
  font-size: 13px;
  color: #999;
  margin-top: 4px;
}
</style>
