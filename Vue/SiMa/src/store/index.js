import { createStore } from "vuex";
import { login, getInfo } from "../api/login"
import storage from 'store'
import { ACCESS_TOKEN } from '../store/mutation-types'

export default createStore({
  state: {
    userInfo:{
      "token": "",
      "name": "",
      "token_type":""
    }
  },
  mutations: {
    SET_TOKEN: (state, token) => {
      state.userInfo.token = token
    },
    SET_TOKEN_TYPE: (state, token_type) => {
      state.userInfo.token_type = token_type
    },
    SET_NAME: (state, name) => {
      state.userInfo.name = name
    }
  },
  actions: {
    // 登录
    Login ({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        login(userInfo).then(response => {
          storage.set(ACCESS_TOKEN, response.access_token, 1 * 12 * 60 * 60);
          commit("SET_TOKEN", response.access_token);
          commit("SET_TOKEN_TYPE", response.token_type);
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetInfo ({ commit }) {
      return new Promise((resolve, reject) => {
        getInfo().then(response => {
          const result = response.result

          if (result.role && result.role.permissions.length > 0) {
            const role = result.role
            role.permissions = result.role.permissions
            role.permissions.map(per => {
              if (per.actionEntitySet != null && per.actionEntitySet.length > 0) {
                const action = per.actionEntitySet.map(action => { return action.action })
                per.actionList = action
              }
            })
            role.permissionList = role.permissions.map(permission => { return permission.permissionId })
            commit("SET_ROLES", result.role)
            commit("SET_INFO", result)
          } else {
            reject(new Error("getInfo: roles must be a non-null array !"))
          }

          commit("SET_NAME", { name: result.name })
          commit("SET_AVATAR", result.avatar)

          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // // 登出
    // Logout ({ commit, state }) {
    //   return new Promise((resolve) => {
    //     logout(state.token).then(() => {
    //       commit("SET_TOKEN", "")
    //       // commit("SET_ROLES", [])
    //       storage.remove(ACCESS_TOKEN)
    //       resolve()
    //     }).catch(() => {
    //       resolve()
    //     }).finally(() => {
    //     })
    //   })
    // },
  // 登出
  Logout ({ commit }) {
    return new Promise((resolve) => {
      commit("SET_TOKEN", "")
      // commit("SET_ROLES", [])
      storage.remove(ACCESS_TOKEN)
      resolve()
    })
  }
  },
  modules: {}
});
