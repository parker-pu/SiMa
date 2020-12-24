import request from '../utils/request'
// const qs = require('querystring')

const searchApi = {
  Search: '/api/dictionary/search',
  TableColumn: '/api/dictionary/table-column',
  GetTable:'/api/dictionary/search-table',
}

export function searchDataApi (search_data) {
  return request({
    url: searchApi.Search,
    method: 'get',
    params: {"data":search_data},
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  })
}

export function tableColumnApi (table_info) {
  return request({
    url: searchApi.TableColumn,
    method: 'post',
    data: table_info,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  })
}

export function getTableApi (table_info) {
  return request({
    url: searchApi.GetTable,
    method: 'post',
    data: table_info,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  })
}
