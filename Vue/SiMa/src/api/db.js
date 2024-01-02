import request from "../utils/request";

const database = {
  database: "/api/database/databases/"
};

export function addDBInfoApi(data) {
  console.log(data)
  return request({
    url: database.database,
    method: "post",
    data: data,
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

export function delDBInfoApi(data) {
  return request({
    url: database.database + data.id + "/",
    method: "delete",
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

export function putDBInfoApi(data) {
  return request({
    url: database.database + data.id + "/",
    method: "put",
    data: data,
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

export function getDBInfoApi() {
  return request({
    url: database.database,
    method: "get",
    headers: {
      "Content-Type": "application/json;charset=UTF-8"
    }
  });
}

