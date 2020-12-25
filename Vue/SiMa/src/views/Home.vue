<template>
  <a-layout id="components-layout-demo-top">
    <a-layout-header>
      <!-- <a-layout-header :style="{ position: 'fixed', zIndex: 1, width: '100%' }"> -->
      <a-row>
        <a-col :span="3">
          <div class="logo" />
        </a-col>
        <a-col :span="7">
          <a-menu
            theme="dark"
            mode="horizontal"
            v-model:selectedKeys="selectedKeys"
            :style="{ lineHeight: '35px' }"
          >
            <a-menu-item key="1">
              统计
            </a-menu-item>
            <!-- <a-menu-item key="2">
              扫描记录
            </a-menu-item>
            <a-menu-item key="3">
              血缘
            </a-menu-item> -->
          </a-menu>
        </a-col>
        <a-col :span="8">
          <div class="search">
            <a-input-search
              v-model:value="searchValue"
              placeholder="input search text"
              @search="onSearch"
            />
          </div>
        </a-col>
        <a-col :span="6">
          <UserDropdown></UserDropdown>
        </a-col>
      </a-row>
    </a-layout-header>
    <a-layout-content :style="{ padding: '0 50px' }">
      <div id="body">
        <router-view />
      </div>
    </a-layout-content>
    <a-layout-footer :style="{ textAlign: 'center' }">
      Welcome to SiMa software. Contact the author: i54605@outlook.com
    </a-layout-footer>
  </a-layout>
</template>
<script>
import UserDropdown from "./user/UserDropdown";
export default {
  components: {
    UserDropdown,
  },
  name: "home",
  data() {
    return {
      selectedKeys: ["1"],
      searchValue: "",
    };
  },
  methods: {
    onSearch(value) {
      this.$router.push({
        name: "search",
        query: {
          search: value,
        },
      });
    },
  },
};
</script>
<style>
#components-layout-demo-top .logo {
  width: 120px;
  height: 31px;
  margin: 2px 2px 2px 0;
  float: left;

  background-size: 100% 100%;
  background-repeat: no-repeat;
  background-image: url(../../public/logo.png);
}

#components-layout-demo-top .search {
  margin: 2px 2px 2px 0px;
  float: left;
}

#components-layout-demo-top .user {
  margin: 2px 2px 2px 0;
  float: left;
}
#components-layout-demo-top .ant-layout-header {
  line-height: 0px;
}

#components-layout-demo-top .ant-layout-header {
  height: 35px;
}

#body {
  background: rgba(255, 255, 255, 0);
  padding: 24px;
}

.ant-layout {
  height: 100%;
}
</style>
