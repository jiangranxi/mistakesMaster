<template>
  <div class="register-page">
    <h2 class="page-title">用户注册</h2>
    <div class="title-divider"></div>
    <div class="spacer-16"></div>

    <!-- 身份切换标签 -->
    <div class="tab-switcher-wrapper">
      <div class="tab-switcher">
        <div class="tab" :class="{ active: isTeacher }" @click="switchTo('teacher')">老师注册</div>
        <div class="tab" :class="{ active: !isTeacher }" @click="switchTo('student')">学生注册</div>
      </div>
    </div>

    <div class="spacer-40"></div>
    <div class="page-container">
      <!-- ========== 老师注册表单 ========== -->
      <div class="form-wrapper" v-if="isTeacher">
        <div class="register-form">
        <!-- 职务 -->
        <div class="form-row">
          <label class="form-label">职务</label>
          <div class="select-box" :class="{ 'input-error': errors.job }" @click="showJobPicker = !showJobPicker">
            <span :class="{ placeholder: !form.job }">{{ form.job || '请选择职务' }}</span>
            <i class="ri-arrow-down-s-line dropdown-icon"></i>
          </div>
          <div v-if="showJobPicker" class="picker-dropdown">
            <div v-for="opt in jobOptions" :key="opt" class="picker-item" @click="form.job = opt; showJobPicker = false">{{ opt }}</div>
          </div>
          <span class="hint" :class="{ 'hint-error': errors.job }">{{ errors.job || '' }}</span>
        </div>
        <div class="spacer-16"></div>

        <!-- 真实姓名 -->
        <div class="form-row">
          <label class="form-label">真实姓名</label>
          <input class="form-input" :class="{ 'input-error': errors.realName }" v-model="form.realName" placeholder="请输入真实姓名" @focus="clearError('realName')" />
          <span class="hint" :class="{ 'hint-error': errors.realName }">{{ errors.realName || '字母、数字、字符、汉字组成' }}</span>
        </div>
        <div class="spacer-16"></div>

        <!-- 密码 -->
        <div class="form-row">
          <label class="form-label">密码</label>
          <input class="form-input" :class="{ 'input-error': errors.password }" v-model="form.password" type="password" placeholder="密码" @focus="clearError('password')" />
          <span class="hint" :class="{ 'hint-error': errors.password }">{{ errors.password || '6-20个数字、字母组成！' }}</span>
        </div>
        <div class="spacer-16"></div>

        <!-- 确认密码 -->
        <div class="form-row">
          <label class="form-label">确认密码</label>
          <input class="form-input" :class="{ 'input-error': errors.confirmPassword }" v-model="form.confirmPassword" type="password" placeholder="确认密码" @focus="clearError('confirmPassword')" />
          <span class="hint" :class="{ 'hint-error': errors.confirmPassword }">{{ errors.confirmPassword || '再次输入密码' }}</span>
        </div>
        <div class="spacer-16"></div>

        <!-- 学科 -->
        <div class="form-row">
          <label class="form-label">学科</label>
          <div class="select-box" :class="{ 'input-error': errors.subject }" @click="showSubjectPicker = !showSubjectPicker">
            <span :class="{ placeholder: !form.subject }">{{ form.subject || '请选择学科' }}</span>
            <i class="ri-arrow-down-s-line dropdown-icon"></i>
          </div>
          <div v-if="showSubjectPicker" class="picker-dropdown subject-picker">
            <div v-for="opt in subjectOptions" :key="opt" class="picker-item" @click="form.subject = opt; showSubjectPicker = false">{{ opt }}</div>
          </div>
          <span class="hint" :class="{ 'hint-error': errors.subject }">{{ errors.subject || '' }}</span>
        </div>
        <div class="spacer-16"></div>

        <!-- 手机 -->
        <div class="form-row">
          <label class="form-label">手机</label>
          <input class="form-input" :class="{ 'input-error': errors.phone }" v-model="form.phone" placeholder="手机" maxlength="11" @focus="clearError('phone')" />
          <span class="hint" :class="{ 'hint-error': errors.phone }">{{ errors.phone || '通过手机可以找回密码' }}</span>
        </div>
        <div class="spacer-16"></div>

        <!-- 验证码 -->
        <div class="form-row">
          <label class="form-label">验证码</label>
          <input class="form-input" :class="{ 'input-error': errors.code }" v-model="form.code" placeholder="验证码" @focus="clearError('code')" />
          <div class="code-area">
            <span class="hint-inline" v-if="errors.code">{{ errors.code }}</span>
            <button class="btn-code" @click="sendCode">{{ codeText }}</button>
          </div>
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

    <!-- ========== 学生注册表单 ========== -->
    <div class="form-wrapper" v-else>
      <div class="register-form">
        <div class="form-row">
          <label class="form-label">真实姓名</label>
          <input class="form-input" :class="{ 'input-error': errors.realName }" v-model="form.realName" placeholder="请输入真实姓名" @focus="clearError('realName')" />
          <span class="hint" :class="{ 'hint-error': errors.realName }">{{ errors.realName || '字母、数字、字符、汉字组成' }}</span>
        </div>
        <div class="spacer-16"></div>

        <div class="form-row">
          <label class="form-label">密码</label>
          <input class="form-input" :class="{ 'input-error': errors.password }" v-model="form.password" type="password" placeholder="密码" @focus="clearError('password')" />
          <span class="hint" :class="{ 'hint-error': errors.password }">{{ errors.password || '6-20个数字、字母组成！' }}</span>
        </div>
        <div class="spacer-16"></div>

        <div class="form-row">
          <label class="form-label">确认密码</label>
          <input class="form-input" :class="{ 'input-error': errors.confirmPassword }" v-model="form.confirmPassword" type="password" placeholder="确认密码" @focus="clearError('confirmPassword')" />
          <span class="hint" :class="{ 'hint-error': errors.confirmPassword }">{{ errors.confirmPassword || '再次输入密码' }}</span>
        </div>
        <div class="spacer-16"></div>

        <div class="form-row">
          <label class="form-label">手机</label>
          <input class="form-input" :class="{ 'input-error': errors.phone }" v-model="form.phone" placeholder="手机" maxlength="11" @focus="clearError('phone')" />
          <span class="hint" :class="{ 'hint-error': errors.phone }">{{ errors.phone || '通过手机可以找回密码' }}</span>
        </div>
        <div class="spacer-16"></div>

        <div class="form-row">
          <label class="form-label">验证码</label>
          <input class="form-input" :class="{ 'input-error': errors.code }" v-model="form.code" placeholder="验证码" @focus="clearError('code')" />
          <div class="code-area">
            <span class="hint-inline" v-if="errors.code">{{ errors.code }}</span>
            <button class="btn-code" @click="sendCode">{{ codeText }}</button>
          </div>
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
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authApi } from '@/api/auth'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const route = useRoute()
const toast = useToast()

const isTeacher = ref(route.path.includes('teacher'))
const jobOptions = ['老师', '年级组长', '年级大组长', '校长']
const subjectOptions = ['数学', '语文', '英语', '物理', '化学', '生物', '地理', '历史', '政治', '道德与法治']

const form = reactive({ job: '老师', realName: '', password: '', confirmPassword: '', subject: '数学', phone: '', code: '' })
const showJobPicker = ref(false)
const showSubjectPicker = ref(false)
const codeText = ref('获取验证码')
const codeSending = ref(false)
const errors = reactive({})

function switchTo(role) {
  isTeacher.value = role === 'teacher'
}

function clearError(field) {
  errors[field] = ''
}

function validate() {
  Object.keys(errors).forEach(k => errors[k] = '')
  if (!form.realName) { errors.realName = '真实姓名为空！'; return false }
  if (!/^[一-龥a-zA-Z0-9]+$/.test(form.realName)) { errors.realName = '字母、数字、字符、汉字组成'; return false }
  if (!form.password) { errors.password = '密码为空！'; return false }
  if (form.password.length < 6 || form.password.length > 20) { errors.password = '6-20个数字、字母组成！'; return false }
  if (!form.confirmPassword) { errors.confirmPassword = '请再次输入密码'; return false }
  if (form.password !== form.confirmPassword) { errors.confirmPassword = '两次密码不一致'; return false }
  if (!form.phone) { errors.phone = '手机号为空！'; return false }
  if (!/^\d{11}$/.test(form.phone)) { errors.phone = '手机号格式不正确'; return false }
  if (!form.code) { errors.code = '验证码为空！'; return false }
  return true
}

async function sendCode() {
  if (codeSending.value) return
  if (!form.phone || !/^\d{11}$/.test(form.phone)) {
    errors.phone = '手机号不合法'
    return
  }
  errors.phone = ''
  codeSending.value = true
  try {
    const res = await authApi.sendRegisterCode(form.phone)
    // 显示后端返回的验证码信息（灰色胶囊）
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
  } catch (e) {
    toast.error(e?.response?.data?.message || '发送失败，请稍后重试')
    codeText.value = '获取验证码'
    codeSending.value = false
  }
}

async function handleRegister() {
  if (!validate()) return
  try {
    if (isTeacher.value) {
      await authApi.registerTeacher({
        job: form.job,
        realName: form.realName,
        password: form.password,
        subject: form.subject,
        phone: form.phone,
        code: form.code
      })
    } else {
      await authApi.registerStudent({
        realName: form.realName,
        password: form.password,
        phone: form.phone,
        code: form.code
      })
    }
    toast.success('注册成功，请登录')
    await new Promise(r => setTimeout(r, 600))
    router.push('/auth/login')
  } catch (e) {
    toast.error(e?.response?.data?.message || '注册失败')
  }
}
</script>

<style scoped>
.register-page { min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 40px 16px 0; background: #fff; }
.page-title { font-size: 28px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; text-align: center; }
.title-divider { width: 100%; height: 1px; background: #E5E7EB; margin-top: 12px; }

.page-container {
  display: flex;
  flex-direction: column;
  /* align-items: center; */
  align-items: center;      /* 水平居中 */
  justify-content: flex-start;
}
.spacer-4 { height: 4px; }
.spacer-16 { height: 16px; }
.spacer-20 { height: 20px; }
.spacer-32 { height: 32px; }
.spacer-40 { height: 40px; }

.tab-switcher-wrapper { padding: 0 320px; margin-bottom: 8px; }
.tab-switcher { width: 768px; display: flex; border-bottom: 2px solid #E5E7EB; }
.tab { flex: 1; padding: 2px 0; text-align: center; font-size: 18px; color: #2563EB; cursor: pointer; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif; }
.tab.active { color: #F97316; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; border-bottom: 2px solid #F97316; margin-bottom: -2px; }

.form-wrapper { padding: 0 320px; }
.register-form { width: 768px; display: flex; flex-direction: column; }

.form-row { display: flex; align-items: center; position: relative; }
.form-label { width: 120px; padding-right: 16px; text-align: right; font-size: 15px; color: #374151; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif; flex-shrink: 0; }

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
.form-input:focus { border-color: #2563EB; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15); }
.form-input::placeholder { color: #9CA3AF; }
.form-input.input-error { border-color: #EF4444; }
.form-input.input-error:focus { box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15); }

.select-box {
  flex: 1; height: 40px; padding: 0 14px;
  border: 0.8px solid #D1D5DB; border-radius: 4px;
  display: flex; align-items: center; justify-content: space-between;
  font-size: 15px; color: #374151; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif;
  cursor: pointer; transition: box-shadow 0.2s, border-color 0.2s;
}
.select-box:focus { border-color: #2563EB; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15); }
.select-box.input-error { border-color: #EF4444; }
.select-box .placeholder { color: #9CA3AF; }
.dropdown-icon { font-size: 16px; color: #6B7280; }

.picker-dropdown {
  position: absolute; top: 44px; left: 136px; right: 232px;
  background: #fff; border: 0.8px solid #D1D5DB; border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1); z-index: 100; max-height: 200px; overflow-y: auto;
}
.subject-picker { display: grid; grid-template-columns: 1fr 1fr; }
.picker-item { padding: 8px 14px; font-size: 14px; color: #374151; cursor: pointer; }
.picker-item:hover { background: #EFF6FF; color: #2563EB; }
.picker-mask { position: fixed; inset: 0; z-index: 50; }

.hint { width: 200px; margin-left: 16px; font-size: 13px; color: #B0B0B0; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif; flex-shrink: 0; }
.hint.hint-error { color: #EF4444; }

/* 验证码区域：与上方 hint 左对齐 */
.code-area { width: 200px; margin-left: 16px; flex-shrink: 0; display: flex; flex-direction: column; align-items: flex-start; }
.hint-inline { font-size: 13px; color: #EF4444; font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif; margin-bottom: 4px; }
.btn-code { height: 40px; padding: 0 16px; border: none; border-radius: 4px; background: #22C55E; color: #fff; font-size: 13px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; white-space: nowrap; }
.btn-code:hover { background: #16A34A; }

.btn-wrapper { padding-left: 136px; }
.btn-register { width: calc(768px - 120px - 16px - 200px - 16px); height: 44px; border: none; border-radius: 8px; background: #2563EB; color: #fff; font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; cursor: pointer; }
.btn-register:hover { background: #3B82F6; }

.has-account { padding-left: 136px; }
.text-gray { font-size: 15px; color: #6B7280; }
.text-blue { font-size: 15px; color: #2563EB; cursor: pointer; margin-left: 8px; }
</style>
