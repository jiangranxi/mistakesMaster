import request from './request'

export const messageApi = {
  // 消息列表
  getMessages(params) {
    return request.get('/messages', { params })
  },

  // 标记已读
  markRead(id) {
    return request.put(`/messages/${id}/read`)
  },

  // 未读消息数
  getUnreadCount() {
    return request.get('/messages/unread-count')
  }
}
