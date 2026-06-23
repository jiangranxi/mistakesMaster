import request from './request'

export const classApi = {
  // 我创建的班级列表（教师端）
  getCreatedClasses: () => request.get('/teacher/classes/created'),

  // 我加入的班级列表（教师端）
  getJoinedClasses: () => request.get('/teacher/classes/joined'),

  // 创建班级（教师端）
  createClass: (data) => request.post('/teacher/classes', data),

  // 加入班级（教师端）
  joinClass: (code, message) => request.post('/teacher/classes/join', { code, message }),

  // 班级详情（教师端）
  getClassDetail: (id) => request.get(`/teacher/classes/${id}`),

  // 班级学生列表（教师端）
  getClassStudents: (id) => request.get(`/teacher/classes/${id}/students`),

  // 我加入的班级列表（学生端）
  getStudentJoined: () => request.get('/student/classes/joined'),

  // 加入班级（学生端）
  studentJoin: (code, message) => request.post('/student/classes/join', { code, message })
}
