import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/user/Login.vue";
import store from '../store'
import storage from 'store'
import { ACCESS_TOKEN } from '../store/mutation-types'

const routes = [
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/",
    name: "Home",
    component: Home,
    hidden: true,
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: "search",
        name: "search",
        component: () => import("@/views/search/Search"),
        meta: {
          requiresAuth: true
        },
      },
      {
        path: "tableInfo",
        name: "tableInfo",
        component: () => import("@/views/search/TableInfo"),
        meta: {
          requiresAuth: true
        },
      },
      {
        path: "user",
        name: "user",
        component: () => import("@/views/user/UserInfo"),
        meta: {
          requiresAuth: true
        },
      },
      {
        path: "db",
        name: "db",
        component: () => import("@/views/setting/DataBase"),
        meta: {
          requiresAuth: true
        },
      },
    ]
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

// 注册全局钩子用来拦截导航
router.beforeEach((to, from, next) => {
  // 获取store里面的token
  let token = store.state.userInfo.token || storage.get(ACCESS_TOKEN)
  // 判断要去的路由有没有requiresAuth
  if (to.meta.requiresAuth) {
    if (token) {
      next()
    } else {
      next({
        name: 'login',
        query: {redirect: to.fullPath}
        // 将刚刚要去的路由path（却无权限）作为参数，方便登录成功后直接跳转到该路由
      })
    }
  } else {
    next()// 如果无需token,那么随它去吧
  }
})

export default router;
