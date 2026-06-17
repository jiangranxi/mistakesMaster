import request from './request'

export const exerciseApi = {
  // 习题集书籍列表
  getBookList: (params) => request.get('/books', { params }),

  // 习题集书籍详情
  getBookDetail: (id) => request.get(`/books/${id}`)
}
