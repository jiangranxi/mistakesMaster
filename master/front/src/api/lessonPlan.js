import request from './request'

export const lessonPlanApi = {
  // 云教案列表
  getCloudPlans(params) {
    return request.get('/lesson-plans/cloud', { params })
  },

  // 自有教案列表
  getOwnPlans(params) {
    return request.get('/lesson-plans/own', { params })
  },

  // 上传教案
  uploadPlan(data) {
    return request.post('/lesson-plans', data)
  },

  // 删除教案
  deletePlan(id) {
    return request.delete(`/lesson-plans/${id}`)
  },

  // 下载教案
  downloadPlan(id) {
    return request.get(`/lesson-plans/${id}/download`, { responseType: 'blob' })
  }
}
