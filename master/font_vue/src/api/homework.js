import request from './request'

export const homeworkApi = {
  // === 教师端 ===
  // 自有作业/试卷列表
  getOwnHomework: (params) => request.get('/teacher/homework/own', { params }),

  // 云作业/试卷列表
  getCloudHomework: (params) => request.get('/teacher/homework/cloud', { params }),

  // 我的组卷列表
  getMyPapers: (params) => request.get('/teacher/homework/papers', { params }),

  // 章节目录
  getChapters: (homeworkId) => request.get(`/teacher/homework/${homeworkId}/chapters`),

  // 布置作业
  assignHomework: (data) => request.post('/teacher/homework/assign', data),

  // === 学生端 ===
  // 最新作业
  getLatestHomework: (params) => request.get('/student/homework/latest', { params }),

  // 历次作业
  getHistoryHomework: (params) => request.get('/student/homework/history', { params }),

  // 错题集
  getErrors: (params) => request.get('/student/homework/errors', { params }),

  // 提交作业
  submitHomework: (id, data) => request.post(`/student/homework/${id}/submit`, data),

  // 作业批改结果
  getCorrection: (id) => request.get(`/student/homework/${id}/correction`),

  // 作业报告
  getReport: (id) => request.get(`/student/homework/${id}/report`)
}
