import request from './request'

export const classApi = {
  // 我创建的班级列表
  getCreatedClasses: () => request.get('/teacher/classes/created'),

  // 我加入的班级列表
  getJoinedClasses: () => request.get('/teacher/classes/joined'),

  // 创建班级
  createClass: (data) => request.post('/teacher/classes', data),

  // 加入班级
  joinClass: (code, message) => request.post('/teacher/classes/join', { code, message }),

  // 班级详情
  getClassDetail: (id) => request.get(`/teacher/classes/${id}`),

  // 班级学生列表
  getClassStudents: (id) => request.get(`/teacher/classes/${id}/students`)
}
