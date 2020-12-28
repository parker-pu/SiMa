import request from "../utils/request";
// const qs = require('querystring')

const userApi = {
  UserInfo: "/api/user/me",
  UserList: "/api/user/user-info"
};

export function getUserInfoApi() {
  return request({
    url: userApi.UserInfo,
    method: "get",
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

export function putUserInfoApi(data) {
  return request({
    url: userApi.UserInfo,
    method: "put",
    data: data,
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

export function delUserInfoApi(data) {
  return request({
    url: userApi.UserList,
    method: "delete",
    data: data,
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

export function getUserListApi() {
  return request({
    url: userApi.UserList,
    method: "get",
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}
