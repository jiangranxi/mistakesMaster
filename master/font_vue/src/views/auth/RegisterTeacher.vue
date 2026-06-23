<template>
  <div class="page-container">
    <h2 class="page-title">用户注册</h2>
    <div class="title-divider"></div>
    <div class="spacer-32"></div>

    <!-- 身份切换标签 -->
    <div class="tab-switcher-wrapper">
      <div class="tab-switcher">
        <div class="tab active">老师注册</div>
        <div class="tab" @click="$router.push('/auth/register-student')">学生注册</div>
      </div>
    </div>

    <div class="spacer-32"></div>

    <div class="form-wrapper">
      <div class="register-form">
        <!-- 职务 -->
        <div class="form-row">
          <label class="form-label">职务</label>
          <div class="select-box" :class="{ 'input-error': errors.job }" @click="showJobPicker = !showJobPicker" @focus="errors.job = ''">
            <span :class="{ placeholder: !job }">{{ job || '请选择职务' }}</span>
            <i class="ri-arrow-down-s-line dropdown-icon"></i>
          </div>
          <div v-if="showJobPicker" class="picker-dropdown">
            <div v-for="opt in jobOptions" :key="opt" class="picker-item" @click="job = opt; showJobPicker = false">{{ opt }}</div>
          </div>
          <span class="hint" :class="{ 'hint-error': errors.job }">{{ errors.job || '' }}</span>
        </div>
        <div class="spacer-16"></div>

        <!-- 真实姓名 -->
        <div class="form-row">
          <label class="form-label">真实姓名</label>
          <input class="form-input" :class="{ 'input-error': errors.realName }" v-model="realName" placeholder="请输入真实姓名" @focus="errors.realName = ''" />
          <span class="hint" :class="{ 'hint-error': errors.realName }">{{ errors.realName || '字母、数字、字符、汉字组成' }}</span>
        </div>
        <div class="spacer-16"></div>

        <!-- 密码 -->
        <div class="form-row">
          <label class="form-label">密码</label>
          <input class="form-input" :class="{ 'input-error': errors.password }" v-model="password" type="password" placeholder="密码" @focus="errors.password = ''" />
          <span class="hint" :class="{ 'hint-error': errors.password }">{{ errors.password || '6-20个数字、字母组成！' }}</span>
        </div>
        <div class="spacer-16"></div>

        <!-- 确认密码 -->
        <div class="form-row">
          <label class="form-label">确认密码</label>
          <input class="form-input" :class="{ 'input-error': errors.confirmPassword }" v-model="confirmPassword" type="password" placeholder="确认密码" @focus="errors.confirmPassword = ''" />
          <span class="hint" :class="{ 'hint-error': errors.confirmPassword }">{{ errors.confirmPassword || '再次输入密码' }}</span>
        </div>
        <div class="spacer-16"></div>

        <!-- 学科 -->
        <div class="form-row">
          <label class="form-label">学科</label>
          <div class="select-box" :class="{ 'input-error': errors.subject }" @click="showSubjectPicker = !showSubjectPicker" @focus="errors.subject = ''">
            <span :class="{ placeholder: !subject }">{{ subject || '请选择学科' }}</span>
            <i class="ri-arrow-down-s-line dropdown-icon"></i>
          </div>
          <div v-if="showSubjectPicker" class="picker-dropdown subject-picker">
            <div v-for="opt in subjectOptions" :key="opt" class="picker-item" @click="subject = opt; showSubjectPicker = false">{{ opt }}</div>
          </div>
          <span class="hint" :class="{ 'hint-error': errors.subject }">{{ errors.subject || '' }}</span>
        </div>
        <div class="spacer-16"></div>

        <!-- 手机 -->
        <div class="form-row">
          <label class="form-label">手机</label>
          <input class="form-input" :class="{ 'input-error': errors.phone }" v-model="phone" placeholder="手机" maxlength="11" @focus="errors.phone = ''" />
          <span class="hint" :class="{ 'hint-error': errors.phone }">{{ errors.phone || '通过手机可以找回密码' }}</span>
        </div>
        <div class="spacer-16"></div>

        <!-- 验证码 -->
        <div class="form-row">
          <label class="form-label">验证码</label>
          <input class="form-input" :class="{ 'input-error': errors.code }" v-model="code" placeholder="验证码" @focus="errors.code = ''" />
          <span class="hint" :class="{ 'hint-error': errors.code }">{{ errors.code || '' }}</span>
          <button class="btn-code" @click="sendCode">{{ codeText }}</button>
        </div>

        <div class="spacer-40"></div>

        <div class="btn-wrapper">
          <button class="btn-register" @click="handleRegister">注册</button>
        </div>

        <div class="spacer-20"></div>

        <div class="has-account">
          <span class="text-gray">已有帐号</span>
          <span class="text-blue" @click="$router.push('/auth/login')">立即登录</span>
        </div>
      </div>
    </div>

    <!-- 点击遮罩关闭选择器 -->
    <div v-if="showJobPicker || showSubjectPicker" class="picker-mask" @click="showJobPicker = false; showSubjectPicker = false"></div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/api/auth'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const toast = useToast()

const jobOptions = ['老师', '年级组长', '年级大组长', '校长']
const subjectOptions = ['数学', '语文', '英语', '物理', '化学', '生物', '地理', '历史', '政治', '道德与法治']

const job = ref('')
const realName = ref('')
const password = ref('')
const confirmPassword = ref('')
const subject = ref('')
const phone = ref('')
const code = ref('')
const showJobPicker = ref(false)
const showSubjectPicker = ref(false)
const codeText = ref('获取验证码')
const codeSending = ref(false)
const errors = reactive({})

function validate() {
  errors.job = ''
  errors.realName = ''
  errors.password = ''
  errors.confirmPassword = ''
  errors.subject = ''
  errors.phone = ''
  errors.code = ''

  if (!job.value) { errors.job = '职务为空！'; return false }
  if (!realName.value) { errors.realName = '真实姓名为空！'; return false }
  if (!/^[一-龥a-zA-Z0-9]+$/.test(realName.value)) { errors.realName = '字母、数字、字符、汉字组成'; return false }
  if (!password.value) { errors.password = '密码为空！'; return false }
  if (password.value.length < 6 || password.value.length > 20) { errors.password = '6-20个数字、字母组成！'; return false }
  if (!confirmPassword.value) { errors.confirmPassword = '请再次输入密码'; return false }
  if (password.value !== confirmPassword.value) { errors.confirmPassword = '两次密码不一致'; return false }
  if (!subject.value) { errors.subject = '学科为空！'; return false }
  if (!phone.value) { errors.phone = '手机号为空！'; return false }
  if (!/^\d{11}$/.test(phone.value)) { errors.phone = '手机号格式不正确'; return false }
  if (!code.value) { errors.code = '验证码为空！'; return false }
  return true
}

async function sendCode() {
  if (!phone.value || codeSending.value) return
  codeSending.value = true
  try {
    const res = await authApi.sendRegisterCode(phone.value)
    if (res?.message) toast.info(res.message)
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
  if (!validate()) return
  try {
    await authApi.registerTeacher({
      job: job.value,
      realName: realName.value,
      password: password.value,
      subject: subject.value,
      phone: phone.value,
      code: code.value
    })
    toast.success('注册成功，请登录')
    await new Promise(r => setTimeout(r, 600))
    router.push('/auth/login')
  } catch (e) {
    toast.error(e?.response?.data?.message || '注册失败')
  }
}
</script>

<style scoped>
.page-container { min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 40px 16px 0; background: #fff; }
.page-title { font-size: 28px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; text-align: center; }
.title-divider { width: 100%; height: 1px; background: #E5E7EB; margin-top: 12px; }
.spacer-16 { height: 16px; }
.spacer-20 { height: 20px; }
.spacer-32 { height: 32px; }
.spacer-40 { height: 40px; }

.tab-switcher-wrapper { padding: 0 320px; }
.tab-switcher { width: 768px; display: flex; border-bottom: 2px solid #E5E7EB; }
.tab { flex: 1; padding: 0 0 12px; text-align: center; font-size: 18px; color: #2563EB; cursor: pointer; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif; }
.tab.active { color: #F97316; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; border-bottom: 2px solid #F97316; margin-bottom: -2px; }

.form-wrapper { padding: 0 320px; }
.register-form { width: 768px; display: flex; flex-direction: column; }

.form-row { display: flex; align-items: flex-start; position: relative; }
.form-label { width: 120px; padding-right: 16px; text-align: right; font-size: 15px; color: #374151; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif; flex-shrink: 0; padding-top: 10px; }

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
.form-input:focus {
  border-color: #2563EB;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}
.form-input::placeholder { color: #9CA3AF; }
.form-input.input-error { border-color: #EF4444; }
.form-input.input-error:focus { box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15); }

.select-box {
  flex: 1;
  height: 40px;
  padding: 0 14px;
  border: 0.8px solid #D1D5DB;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 15px;
  color: #374151;
  font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif;
  cursor: pointer;
  transition: box-shadow 0.2s, border-color 0.2s;
}
.select-box:focus { border-color: #2563EB; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15); }
.select-box.input-error { border-color: #EF4444; }
.select-box .placeholder { color: #9CA3AF; }

.dropdown-icon { font-size: 16px; color: #6B7280; }

.picker-dropdown {
  position: absolute;
  top: 44px;
  left: 136px;
  right: 232px;
  background: #fff;
  border: 0.8px solid #D1D5DB;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  z-index: 100;
  max-height: 200px;
  overflow-y: auto;
}
.subject-picker { display: grid; grid-template-columns: 1fr 1fr; }
.picker-item { padding: 8px 14px; font-size: 14px; color: #374151; cursor: pointer; }
.picker-item:hover { background: #EFF6FF; color: #2563EB; }
.picker-mask { position: fixed; inset: 0; z-index: 50; }

.hint { width: 200px; margin-left: 16px; font-size: 13px; color: #B0B0B0; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif; flex-shrink: 0; padding-top: 10px; }
.hint.hint-error { color: #EF4444; }

.btn-code { width: 100px; height: 40px; border: none; border-radius: 4px; background: #22C55E; color: #fff; font-size: 13px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; white-space: nowrap; flex-shrink: 0; }
.btn-code:hover { background: #16A34A; }

.btn-wrapper { display: flex; justify-content: center; }
.btn-register { width: calc(768px - 120px - 16px - 200px - 16px); height: 44px; border: none; border-radius: 8px; background: #2563EB; color: #fff; font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; }
.btn-register:hover { background: #3B82F6; }

.has-account { text-align: center; }
.text-gray { font-size: 15px; color: #6B7280; }
.text-blue { font-size: 15px; color: #2563EB; cursor: pointer; margin-left: 8px; }
</style>
