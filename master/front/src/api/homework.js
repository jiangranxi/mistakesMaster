import request from './request'

export const homeworkApi = {
  // 云作业/试卷列表
  getCloudHomework(params) {
    return request.get('/homework/cloud', { params })
  },

  // 我的组卷列表
  getMyTestPapers(params) {
    return request.get('/homework/my-papers', { params })
  },

  // 自有作业/试卷列表
  getOwnHomework(params) {
    return request.get('/homework/own', { params })
  },

  // 扩展组卷列表
  getExtendedPapers(params) {
    return request.get('/homework/extended', { params })
  },

  // 布置作业
  assignHomework(data) {
    return request.post('/homework/assign', data)
  },

  // 获取章节目录
  getChapterTree(bookId) {
    return request.get(`/homework/chapters/${bookId}`)
  }
}
