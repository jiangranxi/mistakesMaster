<template>
  <div class="register-view">
    <h2 class="page-title">学生注册</h2>

    <div class="tabs">
      <div class="tab" @click="$router.push('/auth/register-teacher')">老师注册</div>
      <div class="tab active">学生注册</div>
    </div>

    <div class="form-group">
      <label class="form-label">真实姓名</label>
      <input v-model="form.realName" class="form-input" placeholder="请输入真实姓名" />
      <span v-if="nameError" class="hint">{{ nameError }}</span>
    </div>

    <div class="form-group">
      <label class="form-label">密码</label>
      <input v-model="form.password" class="form-input" type="password" placeholder="请设置密码（6-20位）" />
    </div>

    <div class="form-group">
      <label class="form-label">确认密码</label>
      <input v-model="form.confirmPassword" class="form-input" type="password" placeholder="请再次输入密码" />
      <span v-if="pwdError" class="hint">{{ pwdError }}</span>
    </div>

    <div class="form-group">
      <label class="form-label">手机号</label>
      <input v-model="form.phone" class="form-input" placeholder="请输入手机号" maxlength="11" />
    </div>

    <div class="form-group">
      <label class="form-label">验证码</label>
      <div class="verify-row">
        <input v-model="form.verifyCode" class="form-input" placeholder="请输入验证码" />
        <button class="btn verify-btn" :disabled="countdown > 0" @click="sendCode">
          {{ countdown > 0 ? countdown + 's' : '获取验证码' }}
        </button>
      </div>
    </div>

    <button class="btn btn-primary btn-lg" style="width:100%;height:44px;margin-top:12px" :disabled="loading" @click="handleRegister">
      {{ loading ? '注册中...' : '注 册' }}
    </button>

    <div class="bottom-link">
      已有账号？<router-link to="/auth/login">立即登录</router-link>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const countdown = ref(0)
const form = reactive({
  realName: '', password: '', confirmPassword: '',
  phone: '', verifyCode: ''
})

const pwdError = computed(() => {
  if (form.confirmPassword && form.password !== form.confirmPassword) return '两次密码不一致'
  return ''
})

const nameError = computed(() => {
  if (form.realName && form.realName.length < 2) return '姓名至少2个字符'
  return ''
})

async function sendCode() {
  if (!form.phone) { alert('请先输入手机号'); return }
  try {
    await auth.sendVerifyCode(form.phone)
    countdown.value = 60
    const timer = setInterval(() => { countdown.value--; if (countdown.value <= 0) clearInterval(timer) }, 1000)
  } catch (e) { alert(e.message || '发送失败') }
}

async function handleRegister() {
  if (pwdError.value || nameError.value) return
  if (!form.phone || !form.password || !form.realName) {
    alert('请填写必填项'); return
  }
  loading.value = true
  try {
    await auth.register({ ...form, role: 'student' })
    alert('注册成功，请登录')
    router.push('/auth/login')
  } catch (e) { alert(e.message || '注册失败') }
  finally { loading.value = false }
}
</script>

<style scoped>
.page-title { font-size: 20px; margin-bottom: 20px; }
.tabs { margin-bottom: 24px; }
.tab { flex: 1; text-align: center; cursor: pointer; padding: 10px; border-bottom: 2px solid transparent; }
.tab.active { color: #4A90D9; border-bottom-color: #4A90D9; }
.verify-row { display: flex; gap: 12px; }
.verify-btn { min-width: 110px; height: 36px; white-space: nowrap; }
.hint { color: #FF4D4F; font-size: 12px; margin-top: 4px; }
.bottom-link { text-align: center; margin-top: 16px; font-size: 13px; color: #999; }
</style>
