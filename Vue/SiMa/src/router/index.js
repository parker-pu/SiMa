import { createRouter, createWebHistory } from "vue-router";
import store from '../store'
import storage from 'store'
import { ACCESS_TOKEN } from '../store/mutation-types'
import {routes} from './routerList'

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
