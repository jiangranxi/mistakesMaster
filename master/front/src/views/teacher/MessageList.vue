<template>
  <div class="message-page">
    <div class="card">
      <div class="page-header">
        <h3 class="page-title">消息管理</h3>
        <div class="msg-tabs">
          <button class="btn btn-sm">📬 消息</button>
        </div>
      </div>

      <table class="table">
        <thead>
          <tr>
            <th>来自</th>
            <th>身份</th>
            <th>消息内容</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="messageList.length === 0">
            <td colspan="5" style="text-align:center;padding:40px;color:#999">暂无消息</td>
          </tr>
          <tr v-for="msg in messageList" :key="msg.id">
            <td>{{ msg.from }}</td>
            <td>{{ msg.role }}</td>
            <td>{{ msg.content }}</td>
            <td><span :class="msg.read ? 'read' : 'unread'">{{ msg.read ? '已读' : '未读' }}</span></td>
            <td>
              <button v-if="!msg.read" class="btn btn-sm" @click="markRead(msg)">标为已读</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="pagination" v-if="total > pageSize">
        <button class="btn btn-sm">首页</button>
        <button class="btn btn-sm">上一页</button>
        <button class="btn btn-sm">下一页</button>
        <button class="btn btn-sm">尾页</button>
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
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.page-title { font-size: 18px; }
.unread { color: #FF4D4F; font-weight: 500; }
.read { color: #999; }
</style>
