<template>
  <div class="page-container">
    <h2 class="page-title">用户注册</h2>
    <div class="spacer-48"></div>

    <!-- 身份切换标签 -->
    <div class="tab-switcher-wrapper">
      <div class="tab-switcher">
        <div class="tab" @click="$router.push('/auth/register-teacher')">老师注册</div>
        <div class="tab active">学生注册</div>
      </div>
    </div>

    <div class="spacer-48"></div>

    <div class="form-wrapper">
      <div class="register-form">
        <!-- 真实姓名 -->
        <div class="form-row">
          <label class="form-label">真实姓名</label>
          <input class="form-input" v-model="realName" placeholder="请输入真实姓名" />
          <span class="spacer-16-h"></span>
          <span class="hint">字母、数字、字符、汉字组成</span>
        </div>
        <div class="spacer-32"></div>

        <!-- 密码 -->
        <div class="form-row">
          <label class="form-label">密码</label>
          <input class="form-input" v-model="password" type="password" placeholder="密码" />
          <span class="spacer-16-h"></span>
          <span class="hint">6-20个数字、字母组成！</span>
        </div>
        <div class="spacer-32"></div>

        <!-- 确认密码 -->
        <div class="form-row">
          <label class="form-label">确认密码</label>
          <input class="form-input" v-model="confirmPassword" type="password" placeholder="确认密码" />
          <span class="spacer-16-h"></span>
          <span class="hint">再次输入密码</span>
        </div>
        <div class="spacer-32"></div>

        <!-- 手机 -->
        <div class="form-row">
          <label class="form-label">手机</label>
          <input class="form-input" v-model="phone" placeholder="手机" maxlength="11" />
          <span class="spacer-16-h"></span>
          <span class="hint">通过手机可以找回密码</span>
        </div>
        <div class="spacer-32"></div>

        <!-- 验证码 -->
        <div class="form-row">
          <label class="form-label">验证码</label>
          <div class="code-group">
            <input class="code-input" v-model="code" placeholder="验证码" />
            <button class="btn-code" @click="sendCode">{{ codeText }}</button>
          </div>
          <span class="spacer-16-h"></span>
          <span class="hint"></span>
        </div>

        <div class="spacer-48"></div>

        <div class="btn-wrapper">
          <button class="btn-register" :disabled="!canRegister" @click="handleRegister">注册</button>
        </div>

        <div class="spacer-24"></div>

        <div class="has-account">
          <span class="text-gray">已有帐号</span>
          <span class="text-blue" @click="$router.push('/auth/login')">立即登录</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/api/auth'

const router = useRouter()
const realName = ref('')
const password = ref('')
const confirmPassword = ref('')
const phone = ref('')
const code = ref('')
const codeText = ref('获取验证码')
const codeSending = ref(false)

const canRegister = computed(() =>
  realName.value && password.value && confirmPassword.value && phone.value && code.value
)

async function sendCode() {
  if (!phone.value || codeSending.value) return
  codeSending.value = true
  try {
    await authApi.sendRegisterCode(phone.value)
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
  } catch {
    codeText.value = '获取验证码'
    codeSending.value = false
  }
}

async function handleRegister() {
  if (!canRegister.value) return
  if (password.value !== confirmPassword.value) {
    alert('两次密码不一致')
    return
  }
  try {
    await authApi.registerStudent({
      realName: realName.value,
      password: password.value,
      phone: phone.value,
      code: code.value
    })
    alert('注册成功，请登录')
    router.push('/auth/login')
  } catch (e) {
    alert(e?.response?.data?.message || '注册失败')
  }
}
</script>

<style scoped>
.page-container { min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 48px 16px; background: #fff; }
.page-title { font-size: 32px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #6B7280; text-align: center; }
.spacer-16-h { width: 16px; flex-shrink: 0; }
.spacer-24 { height: 24px; }
.spacer-32 { height: 32px; }
.spacer-48 { height: 48px; }
.tab-switcher-wrapper { padding: 0 320px; }
.tab-switcher { width: 768px; display: flex; border-bottom: 2px solid #E5E7EB; }
.tab { flex: 1; padding: 0 0 16px; text-align: center; font-size: 18px; color: #2563EB; cursor: pointer; }
.tab.active { color: #F97316; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; border-bottom: 2px solid #F97316; margin-bottom: -2px; }
.form-wrapper { padding: 0 320px; }
.register-form { width: 768px; display: flex; flex-direction: column; }
.form-row { display: flex; align-items: center; }
.form-label { width: 128px; text-align: right; font-size: 16px; color: #374151; }
.form-input { flex: 1; height: 44px; padding: 12px 16px; border: 0.8px solid #D1D5DB; border-radius: 4px; font-size: 16px; color: #374151; outline: none; }
.form-input::placeholder { color: #9CA3AF; }
.hint { width: 224px; font-size: 14px; color: #6B7280; }
.code-group { flex: 1; display: flex; }
.code-input { flex: 1; height: 44px; padding: 12px 16px; border: 0.8px solid #D1D5DB; border-radius: 4px 0 0 4px; font-size: 16px; outline: none; }
.btn-code { width: 128px; height: 44px; border: none; border-radius: 0 4px 4px 0; background: #22C55E; color: #fff; font-size: 16px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; }
.btn-wrapper { padding: 0 160px; }
.btn-register { width: 448px; height: 60px; border: none; border-radius: 8px; background: #60A5FA; color: #fff; font-size: 20px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; }
.btn-register:disabled { cursor: not-allowed; }
.has-account { text-align: center; }
.text-gray { font-size: 16px; color: #6B7280; }
.text-blue { font-size: 16px; color: #2563EB; cursor: pointer; }
</style>
