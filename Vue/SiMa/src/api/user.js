import request from "../utils/request";
// const qs = require('querystring')

const userApi = {
  Me: "/api/user/me/",
  User: "/api/user/users/",
};

export function getMeApi() {
  return request({
    url: userApi.Me,
    method: "get",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    }
  });
}

export function putMeApi(data) {
  return request({
    url: userApi.Me,
    method: "put",
    data: data,
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

export function addUserApi(data) {
  return request({
    url: userApi.User,
    method: "post",
    data: data,
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

export function delUserApi(data) {
  return request({
    url: userApi.User + data.id + "/",
    method: "delete",
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

export function putUserApi(data) {
  return request({
    url: userApi.User + data.id + "/",
    method: "put",
    data: data,
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

export function getUserApi() {
  return request({
    url: userApi.User,
    method: "get",
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

