<template>
  <div class="step-col">
    <div class="step-circle" :class="{ active }">{{ num }}</div>
    <div class="spacer-8"></div>
    <span class="step-label" :class="{ active }">{{ label }}</span>
  </div>
</template>

<script setup>
defineProps({
  num: Number,
  label: String,
  active: Boolean
})
</script>

<style scoped>
.step-col { display: flex; flex-direction: column; align-items: center; }
.spacer-8 { height: 8px; }
.step-circle { width: 40px; height: 40px; border-radius: 50%; background: #D1D5DB; color: #6B7280; font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; display: flex; align-items: center; justify-content: center; }
.step-circle.active { background: #3B82F6; color: #fff; }
.step-label { font-size: 16px; color: #6B7280; white-space: nowrap; }
.step-label.active { color: #374151; }
</style>
