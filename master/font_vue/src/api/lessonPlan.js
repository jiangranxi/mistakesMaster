import request from './request'

export const lessonPlanApi = {
  // 自有教案列表
  getOwnPlans: (params) => request.get('/teacher/lesson-plans/own', { params }),

  // 云教案列表
  getCloudPlans: (params) => request.get('/teacher/lesson-plans/cloud', { params })
}
