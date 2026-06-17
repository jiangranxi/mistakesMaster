<template>
  <div class="member-page">
    <div class="sidebar">
      <h3 class="sidebar-title">会员中心</h3>
      <div class="menu-list">
        <div class="menu-item" @click="$router.push('/teacher/member')">基本设置</div>
        <div class="menu-item active">安全设置</div>
        <div class="menu-item" @click="$router.push('/teacher/member/orders')">我的订单</div>
      </div>
    </div>
    <div class="main-area">
      <div class="form-container">
        <div class="form-field">
          <label class="field-label">原密码</label>
          <input class="field-input" v-model="oldPassword" type="password" placeholder="请输入原密码" />
        </div>
        <div class="spacer-16"></div>
        <div class="form-field">
          <label class="field-label">新密码</label>
          <input class="field-input" v-model="newPassword" type="password" placeholder="6-20个数字、字母组成！" />
        </div>
        <div class="spacer-16"></div>
        <div class="form-field">
          <label class="field-label">确认密码</label>
          <input class="field-input" v-model="confirmPassword" type="password" placeholder="再次输入密码" />
        </div>
        <div class="spacer-24"></div>
        <button class="btn-save" @click="handleChange">保存</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { memberApi } from '@/api/member'
const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
async function handleChange() {
  if (!oldPassword.value || !newPassword.value) return
  if (newPassword.value !== confirmPassword.value) { alert('两次密码不一致'); return }
  try { await memberApi.changePassword({ oldPassword: oldPassword.value, newPassword: newPassword.value }); alert('修改成功') } catch { alert('修改失败') }
}
</script>

<style scoped>
.member-page { display: flex; height: 100%; }
.sidebar { width: 200px; background: #EEE; padding-top: 16px; flex-shrink: 0; }
.sidebar-title { padding: 16px; font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; }
.menu-list { padding: 8px 0; }
.menu-item { padding: 8px 16px; font-size: 14px; color: #2B7CD3; cursor: pointer; }
.menu-item.active { background: #337AB7; color: #fff; }
.main-area { flex: 1; padding: 32px; }
.form-container { width: 600px; }
.form-field { display: flex; align-items: center; }
.field-label { width: 100px; text-align: right; padding-right: 16px; font-size: 14px; color: #333; flex-shrink: 0; }
.field-input { flex: 1; height: 36px; padding: 0 12px; border: 0.8px solid #E5E7EB; border-radius: 4px; font-size: 14px; outline: none; }
.field-input::placeholder { color: #999; }
.spacer-16 { height: 16px; }
.spacer-24 { height: 24px; }
.btn-save { width: 100%; height: 40px; border: none; border-radius: 4px; background: #337AB7; color: #fff; font-size: 16px; cursor: pointer; }
</style>
