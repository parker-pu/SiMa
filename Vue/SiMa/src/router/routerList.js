import Home from "../views/Home.vue";
import Login from "../views/user/Login.vue";
export const BASE_PATH = "/";

export const routes = [
  {
    path: "/login",
    name: "login",
    component: Login,
    breadcrumbName: "Login"
  },
  {
    path: "/isInit",
    name: "isInit",
    component: () => import("@/views/first/SuperUser"),
    breadcrumbName: "isInit"
  },
  {
    path: BASE_PATH,
    name: "Home",
    component: Home,
    hidden: true,
    breadcrumbName: "Home",
    redirect: "/static",
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: "static",
        name: "static",
        component: () => import("@/views/dashBoard/Static"),
        breadcrumbName: "Static",
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "search",
        name: "search",
        component: () => import("@/views/search/Search"),
        breadcrumbName: "Search",
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "tableInfo",
        name: "tableInfo",
        component: () => import("@/views/search/TableInfo"),
        breadcrumbName: "TableInfo",
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "user",
        name: "user",
        component: () => import("@/views/user/UserInfo"),
        breadcrumbName: "User",
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "db",
        name: "db",
        component: () => import("@/views/setting/DataBase"),
        breadcrumbName: "DB",
        meta: {
          requiresAuth: true
        }
      }
    ]
  }
];
