import request from './request'

export const messageApi = {
  // 消息列表
  getMessages: (params) => request.get('/messages', { params }),

  // 标记已读
  markRead: (id) => request.put(`/messages/${id}/read`),

  // 删除消息
  deleteMessage: (id) => request.delete(`/messages/${id}`)
}
