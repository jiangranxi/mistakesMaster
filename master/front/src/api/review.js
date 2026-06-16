import request from './request'

export const reviewApi = {
  // 讲评报告列表
  getReportList(params) {
    return request.get('/reviews/reports', { params })
  },

  // 讲评报告详情
  getReportDetail(id) {
    return request.get(`/reviews/reports/${id}`)
  },

  // 获取筛选条件选项
  getFilterOptions() {
    return request.get('/reviews/filter-options')
  },

  // 导出讲评报告
  exportReport(id) {
    return request.get(`/reviews/reports/${id}/export`, { responseType: 'blob' })
  }
}
