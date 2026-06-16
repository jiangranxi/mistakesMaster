<template>
  <div class="member-page">
    <div class="card">
      <div class="layout">
        <!-- 左侧菜单 -->
        <div class="sidebar">
          <h3 class="sidebar-title">会员中心</h3>
          <div class="menu-list">
            <div class="menu-item" :class="{ active: activeMenu === 'profile' }" @click="activeMenu = 'profile'">基本设置</div>
            <div class="menu-item" :class="{ active: activeMenu === 'security' }" @click="activeMenu = 'security'">安全设置</div>
            <div class="menu-item" :class="{ active: activeMenu === 'orders' }" @click="activeMenu = 'orders'">我的订单</div>
          </div>
        </div>

        <!-- 右侧内容 -->
        <div class="content-area">
          <!-- 基本设置 -->
          <div v-if="activeMenu === 'profile'">
            <div class="form-container">
              <div class="form-group">
                <label class="form-label">登录账号</label>
                <input :value="profile.phone" class="form-input" disabled style="width:400px" />
              </div>
              <div class="form-group">
                <label class="form-label">真实姓名</label>
                <input v-model="profile.realName" class="form-input" style="width:400px" />
              </div>
              <div class="form-group">
                <label class="form-label">出生日期</label>
                <input v-model="profile.birthday" class="form-input" type="date" style="width:400px" />
              </div>
              <div class="form-group">
                <label class="form-label">性别</label>
                <select v-model="profile.gender" class="form-input" style="width:400px">
                  <option value="">请选择</option>
                  <option value="male">男</option>
                  <option value="female">女</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">E-mail</label>
                <input v-model="profile.email" class="form-input" style="width:400px" />
              </div>
              <div class="form-group">
                <label class="form-label">手机</label>
                <input v-model="profile.phone" class="form-input" style="width:400px" />
              </div>
              <div class="form-group">
                <label class="form-label">地区</label>
                <div class="region-row">
                  <select v-model="profile.province" class="form-input" style="width:130px"><option value="">省份</option></select>
                  <select v-model="profile.city" class="form-input" style="width:130px"><option value="">城市</option></select>
                  <select v-model="profile.district" class="form-input" style="width:130px"><option value="">区县</option></select>
                </div>
              </div>
              <button class="btn btn-primary" @click="saveProfile">保存</button>
            </div>
          </div>

          <!-- 安全设置 -->
          <div v-if="activeMenu === 'security'">
            <div class="form-container">
              <div class="form-group">
                <label class="form-label">原密码</label>
                <input v-model="security.oldPassword" class="form-input" type="password" style="width:400px" />
              </div>
              <div class="form-group">
                <label class="form-label">新密码</label>
                <input v-model="security.newPassword" class="form-input" type="password" style="width:400px" />
              </div>
              <div class="form-group">
                <label class="form-label">重复密码</label>
                <input v-model="security.confirmPassword" class="form-input" type="password" style="width:400px" />
              </div>
              <button class="btn btn-primary" @click="changePassword">修改</button>
            </div>
          </div>

          <!-- 我的订单 -->
          <div v-if="activeMenu === 'orders'">
            <div class="tabs">
              <div class="tab" :class="{ active: orderTab === 'all' }" @click="orderTab = 'all'">全部</div>
              <div class="tab" :class="{ active: orderTab === 'pending' }" @click="orderTab = 'pending'">待付款</div>
              <div class="tab" :class="{ active: orderTab === 'paid' }" @click="orderTab = 'paid'">已付款</div>
              <div class="tab" :class="{ active: orderTab === 'cancelled' }" @click="orderTab = 'cancelled'">已取消</div>
            </div>
            <table class="table">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>订单号</th>
                  <th>名称</th>
                  <th>资源类型</th>
                  <th>价格</th>
                  <th>交易状态</th>
                  <th>时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="orderList.length === 0">
                  <td colspan="8" style="text-align:center;padding:40px;color:#999">暂无订单</td>
                </tr>
                <tr v-for="(order, idx) in orderList" :key="order.id">
                  <td>{{ (orderPage - 1) * orderPageSize + idx + 1 }}</td>
                  <td>{{ order.orderNo }}</td>
                  <td>{{ order.name }}</td>
                  <td>{{ order.resourceType }}</td>
                  <td>¥{{ order.price }}</td>
                  <td>{{ order.statusText }}</td>
                  <td>{{ order.time }}</td>
                  <td><button class="btn btn-sm">查看详情</button></td>
                </tr>
              </tbody>
            </table>
            <div class="pagination" v-if="orderTotal > orderPageSize">
              <button class="btn btn-sm" @click="orderPage = 1">首页</button>
              <button class="btn btn-sm" @click="orderPage--" :disabled="orderPage <= 1">上一页</button>
              <button class="btn btn-sm" @click="orderPage++" :disabled="orderPage * orderPageSize >= orderTotal">下一页</button>
              <button class="btn btn-sm" @click="orderPage = Math.ceil(orderTotal / orderPageSize)">尾页</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const activeMenu = ref('profile')
const orderTab = ref('all')
const orderList = ref([])
const orderPage = ref(1)
const orderPageSize = ref(10)
const orderTotal = ref(0)

const profile = reactive({
  phone: '', realName: '', birthday: '', gender: '',
  email: '', province: '', city: '', district: ''
})

const security = reactive({ oldPassword: '', newPassword: '', confirmPassword: '' })

function saveProfile() { alert('保存成功') }
function changePassword() { alert('修改成功') }
</script>

<style scoped>
.layout { display: flex; gap: 24px; }
.sidebar { width: 200px; border-right: 1px solid #f0f0f0; min-height: 400px; }
.sidebar-title { font-size: 16px; padding: 0 0 16px; border-bottom: 1px solid #f0f0f0; margin-bottom: 8px; }
.menu-item { padding: 10px 16px; cursor: pointer; border-radius: 4px; color: #333; }
.menu-item:hover, .menu-item.active { background: #f0f5ff; color: #4A90D9; }
.content-area { flex: 1; }
.form-container { max-width: 600px; }
.region-row { display: flex; gap: 8px; }
.tabs { margin-bottom: 16px; }
</style>
