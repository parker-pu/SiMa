import request from "../utils/request";
const qs = require("querystring");

const userApi = {
  Login: "/api/token",
  Logout: "/api/token",
  UserInfo: "/api/user/me/"
};

export function login(parameter) {
  return request({
    url: userApi.Login,
    method: "post",
    data: qs.stringify(parameter)
  });
}

export function getInfo() {
  return request({
    url: userApi.UserInfo,
    method: "get",
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

export function logout() {
  return request({
    url: userApi.Logout,
    method: "post",
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}
