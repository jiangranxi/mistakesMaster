import request from './request'

export const authApi = {
  // 登录 - 学生和教师共用同一入口，通过手机号区分
  login: (data) => request.post('/auth/login', data),

  // 老师注册
  registerTeacher: (data) => request.post('/auth/register/teacher', data),

  // 学生注册
  registerStudent: (data) => request.post('/auth/register/student', data),

  // 发送验证码(注册)
  sendRegisterCode: (phone) => request.post('/auth/send-code', { phone, type: 'register' }),

  // 忘记密码 - 发送验证码
  sendForgotCode: (phone) => request.post('/auth/send-code', { phone, type: 'forgot' }),

  // 忘记密码 - 验证用户
  verifyUser: (data) => request.post('/auth/forgot/verify', data),

  // 忘记密码 - 重置密码
  resetPassword: (data) => request.post('/auth/forgot/reset', data),

  // 获取当前用户信息
  getUserInfo: () => request.get('/auth/userinfo')
}
