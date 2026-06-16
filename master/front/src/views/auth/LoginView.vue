<template>
  <div class="login-view">
    <div class="form-group">
      <label class="form-label">手机号</label>
      <div class="input-with-icon">
        <span class="input-icon">📱</span>
        <input
          v-model="form.phone"
          class="form-input"
          placeholder="请输入手机号"
          maxlength="11"
          @keyup.enter="handleLogin"
        />
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">密码</label>
      <div class="input-with-icon">
        <span class="input-icon">🔒</span>
        <input
          v-model="form.password"
          class="form-input"
          type="password"
          placeholder="请输入密码"
          @keyup.enter="handleLogin"
        />
      </div>
    </div>

    <button
      class="btn btn-primary btn-lg login-btn"
      :disabled="loading"
      @click="handleLogin"
    >
      {{ loading ? '登录中...' : '登 录' }}
    </button>

    <div class="login-links">
      <router-link to="/auth/register-teacher">注册账号</router-link>
      <router-link to="/auth/forgot-password">忘记密码</router-link>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const form = reactive({ phone: '', password: '' })

async function handleLogin() {
  if (!form.phone || !form.password) {
    alert('请填写手机号和密码')
    return
  }
  loading.value = true
  try {
    await auth.login(form.phone, form.password)
    const target = auth.isTeacher ? '/teacher/classes' : '/student/homework'
    router.push(target)
  } catch (e) {
    alert(e.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-btn {
  width: 100%;
  height: 44px;
  margin-top: 24px;
  font-size: 16px;
}

.login-links {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
  font-size: 13px;
}

.input-with-icon {
  display: flex;
  align-items: center;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  overflow: hidden;
}

.input-with-icon:focus-within {
  border-color: #4A90D9;
}

.input-icon {
  padding: 0 12px;
  font-size: 16px;
  border-right: 1px solid #e8e8e8;
}

.input-with-icon .form-input {
  border: none;
  flex: 1;
}

.input-with-icon .form-input:focus {
  outline: none;
}
</style>
