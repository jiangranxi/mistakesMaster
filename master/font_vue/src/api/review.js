import request from './request'

export const reviewApi = {
  // 错题本讲评报告列表
  getErrorBookReports: (params) => request.get('/teacher/review/error-book', { params }),

  // 网络作业讲评报告列表
  getHomeworkReports: (params) => request.get('/teacher/review/homework', { params })
}
