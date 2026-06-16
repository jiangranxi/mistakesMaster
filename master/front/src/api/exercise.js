import request from './request'

export const exerciseApi = {
  // 书籍列表
  getBookList(params) {
    return request.get('/exercises/books', { params })
  },

  // 书籍详情
  getBookDetail(id) {
    return request.get(`/exercises/books/${id}`)
  },

  // 购买书籍
  purchaseBook(id) {
    return request.post(`/exercises/books/${id}/purchase`)
  },

  // 我的书籍
  getMyBooks() {
    return request.get('/exercises/my-books')
  }
}
