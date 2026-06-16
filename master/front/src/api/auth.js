import request from './request'

export const authApi = {
  // 手机号+密码登录
  login(data) {
    return request.post('/auth/login', data)
  },

  // 老师注册
  registerTeacher(data) {
    return request.post('/auth/register/teacher', data)
  },

  // 学生注册
  registerStudent(data) {
    return request.post('/auth/register/student', data)
  },

  // 发送验证码
  sendVerifyCode(phone) {
    return request.post('/auth/verify-code', { phone })
  },

  // 忘记密码 - 验证用户身份
  verifyUser(data) {
    return request.post('/auth/forgot/verify', data)
  },

  // 忘记密码 - 重置密码
  resetPassword(data) {
    return request.post('/auth/forgot/reset', data)
  },

  // 获取当前用户信息
  getUserInfo() {
    return request.get('/auth/userinfo')
  },

  // 更新用户信息
  updateUserInfo(data) {
    return request.put('/auth/userinfo', data)
  },

  // 修改密码
  changePassword(data) {
    return request.put('/auth/password', data)
  }
}
