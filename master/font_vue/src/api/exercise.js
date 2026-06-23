import request from './request'

export const exerciseApi = {
  // 习题集书籍列表
  getBookList: (params) => request.get('/books', { params }),

  // 习题集书籍详情
  getBookDetail: (id) => request.get(`/books/${id}`),

  // 上传封面图片
  uploadCover: (file) => {
    const fd = new FormData()
    fd.append('file', file)
    return request.post('/upload/image', fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 更新习题集信息
  updateBook: (id, data) => request.put(`/books/${id}`, data)
}
