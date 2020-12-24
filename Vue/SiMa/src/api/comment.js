import request from '../utils/request'
// const qs = require('querystring')

const commentApi = {
  Comment: '/api/comment',
}

export function getCommentApi (table_info) {
  return request({
    url: commentApi.Comment,
    method: 'post',
    data: table_info,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  })
}

export function putCommentApi (content,table_input) {
  return request({
    url:  commentApi.Comment,
    method: 'put',
    params: content,
    data: table_input,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  })
}

export function delCommentApi (comm) {
  return request({
    url:  commentApi.Comment,
    method: 'delete',
    data: comm,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  })
}
