import request from './request'

export const studentApi = {
  // 最新作业列表
  getLatestHomework(params) {
    return request.get('/student/homework/latest', { params })
  },

  // 历次作业列表
  getHistoryHomework(params) {
    return request.get('/student/homework/history', { params })
  },

  // 错题集列表
  getErrorBook(params) {
    return request.get('/student/homework/errors', { params })
  },

  // 提交作业
  submitHomework(id, data) {
    return request.post(`/student/homework/${id}/submit`, data)
  },

  // 批改详情
  getCorrectionDetail(id) {
    return request.get(`/student/homework/${id}/correction`)
  },

  // 分析报告
  getReport(id) {
    return request.get(`/student/homework/${id}/report`)
  }
}
