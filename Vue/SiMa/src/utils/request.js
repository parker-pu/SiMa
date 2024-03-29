import axios from "axios";
import store from "../store";
import storage from "store";
import notification from "ant-design-vue/es/notification";
import { VueAxios } from "./axios";
import { ACCESS_TOKEN } from "../store/mutation-types";
import router from "../router";

// 创建 axios 实例
const request = axios.create({
  // API 请求的默认前缀
  baseURL: process.env.VUE_APP_API_BASE_URL,
  timeout: 6000 // 请求超时时间
});

// 异常拦截处理器
const errorHandler = error => {
  if (error.response) {
    const data = error.response.data;
    // 从 localstorage 获取 token
    const token = storage.get(ACCESS_TOKEN);
    if (error.response.status === 403) {
      notification.error({
        message: "Forbidden",
        description: data.message
      });
    } else if (
      error.response.status === 401 &&
      !(data.result && data.result.isLogin)
    ) {
      notification.error({
        message: "Unauthorized",
        description: "Authorization verification failed"
      });

      if (token) {
        store.dispatch("Logout").then(() => {
          setTimeout(() => {
            window.location.reload();
          }, 1500);
        });
      }

      router.push({
        // 跳转到登录页面
        name: "login",
        query: { redirect: router.currentRoute.fullPath }
        // 将跳转的路由path作为参数，登录成功后跳转到该路由
      })
    } else {
      notification.error({
        message: "错误",
        description: data.message || "请检查输入或者联系管理员"
      });
    }
  }
  return Promise.reject(error);
};

// request interceptor
request.interceptors.request.use(config => {
  const token = storage.get(ACCESS_TOKEN);
  // const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInNjb3BlcyI6WyJtZSJdLCJleHAiOjE3MDM3NDk4NTd9.wrHsLJSfc1Mi8Y8F07wDufuDrA5MMASvVT-TXVONC1M";
  // 如果 token 存在
  // 让每个请求携带自定义 token 请根据实际情况自行修改
  if (token) {
    console.log(token)
    config.headers.Authorization = "bearer" + " " + token.replace(/'|"/g, ""); // 把token加入到默认请求参数中
  }
  return config;
}, errorHandler);

// response interceptor
request.interceptors.response.use(response => {
  return response.data;
}, errorHandler);

const installer = {
  vm: {},
  install(Vue) {
    Vue.use(VueAxios, request);
  }
};

export default request;

export { installer as VueAxios, request as axios };
