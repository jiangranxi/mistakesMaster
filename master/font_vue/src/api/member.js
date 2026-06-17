import request from './request'

export const memberApi = {
  // 获取会员信息
  getProfile: () => request.get('/member/profile'),

  // 更新基本设置
  updateProfile: (data) => request.put('/member/profile', data),

  // 修改密码
  changePassword: (data) => request.put('/member/password', data),

  // 我的订单
  getOrders: (params) => request.get('/member/orders', { params })
}
