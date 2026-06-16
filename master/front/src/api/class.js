import request from './request'

export const classApi = {
  // 我创建的班级列表
  getMyCreatedClasses() {
    return request.get('/classes/my-created')
  },

  // 我加入的班级列表
  getMyJoinedClasses() {
    return request.get('/classes/my-joined')
  },

  // 创建班级
  createClass(data) {
    return request.post('/classes', data)
  },

  // 加入班级
  joinClass(classCode) {
    return request.post('/classes/join', { classCode })
  },

  // 班级详情
  getClassDetail(id) {
    return request.get(`/classes/${id}`)
  },

  // 获取班级学生列表
  getClassStudents(id) {
    return request.get(`/classes/${id}/students`)
  }
}
