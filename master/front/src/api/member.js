import request from './request'

export const memberApi = {
  // 获取个人信息
  getProfile() {
    return request.get('/member/profile')
  },

  // 更新个人信息
  updateProfile(data) {
    return request.put('/member/profile', data)
  },

  // 修改密码
  changePassword(data) {
    return request.put('/member/password', data)
  },

  // 订单列表
  getOrders(params) {
    return request.get('/member/orders', { params })
  },

  // 订单详情
  getOrderDetail(id) {
    return request.get(`/member/orders/${id}`)
  }
}
