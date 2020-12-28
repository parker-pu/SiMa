import request from "../utils/request";
// const qs = require('querystring')

const statisApi = {
  statis: "/api/dashboard/static"
};

export function getStatisApi() {
  return request({
    url: statisApi.statis,
    method: "get",
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}
