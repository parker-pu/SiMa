import request from "../utils/request";
// const qs = require('querystring')

const Init = {
  isInit: "/api/first/is_init",
  initSuperUser: "/api/first/init-superuser"
};

export function isInitApi() {
  return request({
    url: Init.isInit,
    method: "get",
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

export function initSuperUserApi(data) {
  return request({
    url: Init.initSuperUser,
    method: "post",
    data: data,
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}
