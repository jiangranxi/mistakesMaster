<template>
  <div class="message-page">
    <div class="card">
      <h3 class="page-title">消息管理</h3>

      <table class="table">
        <thead>
          <tr>
            <th>序号</th>
            <th>来自</th>
            <th>身份</th>
            <th>消息内容</th>
            <th>时间</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="messageList.length === 0">
            <td colspan="7" style="text-align:center;padding:40px;color:#999">暂无消息</td>
          </tr>
          <tr v-for="(msg, idx) in messageList" :key="msg.id">
            <td>{{ (page - 1) * pageSize + idx + 1 }}</td>
            <td>{{ msg.from }}</td>
            <td>{{ msg.role }}</td>
            <td>{{ msg.content }}</td>
            <td>{{ msg.time }}</td>
            <td><span :class="msg.read ? 'read' : 'unread'">{{ msg.read ? '已读' : '未读' }}</span></td>
            <td>
              <button v-if="!msg.read" class="btn btn-sm" @click="markRead(msg)">标为已读</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="pagination" v-if="total > pageSize">
        <button class="btn btn-sm" @click="page = 1">首页</button>
        <button class="btn btn-sm" @click="page--" :disabled="page <= 1">上一页</button>
        <button class="btn btn-sm" @click="page++" :disabled="page * pageSize >= total">下一页</button>
        <button class="btn btn-sm" @click="page = Math.ceil(total / pageSize)">尾页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const messageList = ref([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

function markRead(msg) { msg.read = true }
</script>

<style scoped>
.page-title { font-size: 18px; margin-bottom: 16px; }
.unread { color: #FF4D4F; font-weight: 500; }
.read { color: #999; }
</style>
