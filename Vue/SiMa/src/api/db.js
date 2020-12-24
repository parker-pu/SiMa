import request from '../utils/request'
// const qs = require('querystring')

const dictionary = {
  dbConn: 'api/dictionary/db-conn',
}

export function getDBConnApi () {
  return request({
    url: dictionary.dbConn,
    method: 'get',
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  })
}

export function addDBConnApi (parameter) {
  return request({
    url: dictionary.dbConn,
    method: 'put',
    data: parameter,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  })
}

export function delDBConnApi (parameter) {
  return request({
    url: dictionary.dbConn,
    method: 'delete',
    data: parameter,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  })
}
