<template>
  <div class="member-page">
    <!-- 左侧菜单 -->
    <div class="sidebar">
      <h3 class="sidebar-title">会员中心</h3>
      <div class="menu-list">
        <div class="menu-item active">基本设置</div>
        <div class="menu-item" @click="$router.push('/teacher/member/security')">安全设置</div>
        <div class="menu-item" @click="$router.push('/teacher/member/orders')">我的订单</div>
      </div>
    </div>

    <!-- 右侧内容 -->
    <div class="main-area">
      <div class="form-container">
        <div class="form-field">
          <label class="field-label">登录账号</label>
          <div class="field-value readonly">{{ profile.accountId || '---' }}</div>
        </div>
        <div class="spacer-16"></div>

        <div class="form-field">
          <label class="field-label">真实姓名</label>
          <input class="field-input" v-model="profile.realName" />
        </div>
        <div class="spacer-16"></div>

        <div class="form-field">
          <label class="field-label">出生日期</label>
          <DatePicker v-model="profile.birthday" placeholder="请输入出生日期(2008-06-06)" style="flex: 1" />
        </div>
        <div class="spacer-16"></div>

        <div class="form-field">
          <label class="field-label">性别</label>
          <select class="field-input" v-model="profile.gender">
            <option value="男">男</option>
            <option value="女">女</option>
          </select>
        </div>
        <div class="spacer-16"></div>

        <div class="form-field">
          <label class="field-label">E-mail</label>
          <input class="field-input" v-model="profile.email" placeholder="请输入邮箱" />
        </div>
        <div class="spacer-16"></div>

        <div class="form-field">
          <label class="field-label">手机</label>
          <div class="field-value readonly">{{ profile.phone || '---' }}</div>
        </div>
        <div class="spacer-16"></div>

        <div class="form-field">
          <label class="field-label">地区</label>
          <div class="region-row">
            <select class="field-input region-select" v-model="profile.province">
              <option value="">请选择省(市)</option>
              <option v-for="p in regionTree" :key="p.n" :value="p.n">{{ p.n }}</option>
            </select>
            <span class="spacer-12"></span>
            <select class="field-input region-select" v-model="profile.city" :disabled="!profile.province">
              <option value="">请选择市县</option>
              <option v-for="c in cities" :key="c.n" :value="c.n">{{ c.n }}</option>
            </select>
            <span class="spacer-12"></span>
            <select class="field-input region-select" v-model="profile.district" :disabled="!profile.city">
              <option value="">请选择区</option>
              <option v-for="d in districts" :key="d" :value="d">{{ d }}</option>
            </select>
          </div>
        </div>
        <div class="spacer-16"></div>

        <div class="form-field">
          <label class="field-label">学科</label>
          <select class="field-input" v-model="profile.subject">
            <option v-for="s in allSubjects" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>

        <div class="spacer-24"></div>
        <button class="btn-save" @click="handleSave">保存</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, watch, ref, nextTick } from 'vue'
import { memberApi } from '@/api/member'
import { useToast } from '@/composables/useToast'
import { regionTree } from '@/data/regions'
import DatePicker from '@/components/DatePicker.vue'

const toast = useToast()

const profile = reactive({
  accountId: '', realName: '', birthday: '', gender: '男',
  email: '', phone: '', province: '', city: '', district: '', subject: '数学'
})
const loadingProfile = ref(false)

// 地区联动
const cities = computed(() => {
  if (!profile.province) return []
  const p = regionTree.find(r => r.n === profile.province)
  return p ? p.c : []
})
const districts = computed(() => {
  if (!profile.city) return []
  const c = cities.value.find(c => c.n === profile.city)
  return c ? c.d : []
})
watch(() => profile.province, () => { if (loadingProfile.value) return; profile.city = ''; profile.district = '' })
watch(() => profile.city, () => { if (loadingProfile.value) return; profile.district = '' })

const allSubjects = ['数学', '语文', '英语', '物理', '化学', '生物', '地理', '历史', '政治', '道德与法治']

async function loadProfile() {
  loadingProfile.value = true
  try { Object.assign(profile, await memberApi.getProfile()) } catch {} finally { await nextTick(); loadingProfile.value = false }
}
async function handleSave() {
  try { await memberApi.updateProfile(profile); toast.success('保存成功') } catch { toast.error('保存失败') }
}
loadProfile()
</script>

<style scoped>
.member-page { display: flex; flex: 1; min-height: 0; }
.sidebar { width: 200px; background: #EEE; padding-top: 16px; flex-shrink: 0; align-self: stretch; }
.sidebar-title { padding: 16px; font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; }
.menu-list { padding: 8px 0; }
.menu-item { padding: 8px 16px; font-size: 14px; color: #2B7CD3; cursor: pointer; }
.menu-item.active { background: #337AB7; color: #fff; }
.main-area { flex: 1; padding: 32px; }
.form-container { width: 600px; }
.form-field { display: flex; align-items: center; }
.field-label { width: 100px; text-align: right; padding-right: 16px; font-size: 14px; color: #333; flex-shrink: 0; }
.field-input { flex: 1; height: 36px; padding: 0 12px; border: 0.8px solid #E5E7EB; border-radius: 4px; font-size: 14px; outline: none; color: #333; }
.field-input::placeholder { color: #999; }
.field-value { flex: 1; height: 36px; padding: 0 12px; display: flex; align-items: center; font-size: 14px; color: #333; }
.field-value.readonly { background: #F3F4F6; border-radius: 4px; cursor: not-allowed; }
.region-row { flex: 1; display: flex; }
.region-select { width: 150px; flex: none; }
.region-select:disabled { cursor: not-allowed; }
.spacer-12 { width: 12px; flex-shrink: 0; }
.spacer-16 { height: 16px; }
.spacer-24 { height: 24px; }
.btn-save { width: 100%; height: 40px; border: none; border-radius: 4px; background: #337AB7; color: #fff; font-size: 16px; cursor: pointer; }
</style>
