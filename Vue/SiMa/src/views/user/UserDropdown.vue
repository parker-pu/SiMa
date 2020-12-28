<template>
  <a-row>
    <a-col :span="15">
      <a-tag color="" :show-overflow-tooltip="true">
        <template #icon>
          <clock-circle-outlined />
        </template>
        {{ date }}
      </a-tag>
    </a-col>
    <a-col :span="9">
      <a-dropdown>
        <div class="user">
          <a-avatar>
            <template #icon>
              <UserOutlined />
            </template>
          </a-avatar>
        </div>
        <template #overlay>
          <a-menu @click="handleMenuClick">
            <a-menu-item key="1"><IdcardOutlined />个人信息</a-menu-item>
            <a-menu-item key="2" v-if="userInfo.is_superuser">
              <SettingFilled />设置
            </a-menu-item>
            <a-menu-item key="3"><LogoutOutlined />退出</a-menu-item>
          </a-menu>
        </template>
      </a-dropdown>
    </a-col>
  </a-row>
  <a-drawer
    title="设置"
    width="520"
    :closable="false"
    :visible="visible"
    @close="onClose"
  >
    <a-button type="primary" @click="onUser" :size="size"
      ><UserSwitchOutlined />用户操作</a-button
    >
    <br /><br />
    <a-button type="primary" @click="onDB" :size="size"
      ><DatabaseOutlined />数据库操作</a-button
    >
    <div
      :style="{
        position: 'absolute',
        bottom: 0,
        width: '100%',
        borderTop: '1px solid #e8e8e8',
        padding: '10px 16px',
        textAlign: 'right',
        left: 0,
        background: '#fff',
        borderRadius: '0 0 4px 4px'
      }"
    >
      <a-button type="primary" @click="onClose">
        关闭
      </a-button>
    </div>
  </a-drawer>

  <!-- userInfo -->
  <a-spin :spinning="spinning">
    <a-modal v-model:visible="visibleUser" title="用户" @ok="handleOk">
      <template #footer>
        <a-button key="back" @click="handleCancel">
          取消
        </a-button>
        <a-button
          key="submit"
          type="primary"
          :loading="loading"
          @click="handleOk"
        >
          提交
        </a-button>
      </template>
      <a-form :model="userInfo" :label-col="labelCol" :wrapper-col="wrapperCol">
        <a-form-item label="全名" name="full_name">
          <a-input v-model:value="userInfo.full_name"></a-input>
        </a-form-item>
        <a-form-item label="Email" name="email">
          <a-input v-model:value="userInfo.email"></a-input>
        </a-form-item>
        <a-form-item label="密码" name="password">
          <a-input v-model:value="userInfo.password"></a-input>
        </a-form-item>
      </a-form>
    </a-modal>
  </a-spin>
</template>

<script>
import {
  SettingFilled,
  IdcardOutlined,
  LogoutOutlined,
  DatabaseOutlined,
  UserSwitchOutlined,
  ClockCircleOutlined,
  UserOutlined
} from "@ant-design/icons-vue";
import { mapActions } from "vuex";
import { getUserInfoApi, putUserInfoApi } from "../../api/user";

export default {
  components: {
    SettingFilled,
    IdcardOutlined,
    LogoutOutlined,
    DatabaseOutlined,
    UserSwitchOutlined,
    ClockCircleOutlined,
    UserOutlined
  },
  data() {
    return {
      labelCol: { span: 6 },
      wrapperCol: { span: 14 },
      visible: false,
      size: "large",
      date: "",
      userInfo: {},
      spinning: false,
      visibleUser: false,
      loading: false
    };
  },
  created() {
    this.getUserInfoData();
  },
  methods: {
    ...mapActions(["Logout"]),
    editUserInfo() {},
    handleOk() {
      this.loading = true;
      putUserInfoApi(this.userInfo)
        .then(() => {
          this.$notification.success({
            message: "修改",
            description: "修改成功"
          });
        })
        .catch(() => {})
        .finally(() => {
          this.loading = false;
          this.visibleUser = false;
        });
    },
    handleCancel() {
      this.visibleUser = false;
    },
    getUserInfoData() {
      getUserInfoApi()
        .then(rsp => {
          this.userInfo = rsp;
        })
        .catch(() => {});
    },
    currentTime() {
      setInterval(this.formatDate, 500);
    },
    formatDate() {
      let date = new Date();
      let year = date.getFullYear(); // 年
      let month = date.getMonth() + 1; // 月
      let day = date.getDate(); // 日
      let week = date.getDay(); // 星期
      let weekArr = [
        "星期日",
        "星期一",
        "星期二",
        "星期三",
        "星期四",
        "星期五",
        "星期六"
      ];
      let hour = date.getHours(); // 时
      hour = hour < 10 ? "0" + hour : hour; // 如果只有一位，则前面补零
      let minute = date.getMinutes(); // 分
      minute = minute < 10 ? "0" + minute : minute; // 如果只有一位，则前面补零
      let second = date.getSeconds(); // 秒
      second = second < 10 ? "0" + second : second; // 如果只有一位，则前面补零
      this.date = `${year}/${month}/${day} ${hour}:${minute}:${second} ${weekArr[week]}`;
    },

    padaDate(value) {
      return value < 10 ? "0" + value : value;
    },
    handleMenuClick(e) {
      console.log("click", e.key);
      switch (e.key) {
        case "1":
          this.visibleUser = true;
          break;
        case "2":
          this.visible = true;
          break;
        case "3":
          this.Logout();
          this.$router.push({ name: "login" });
          break;
        default:
          console.log("click", e.key);
      }
    },
    onClose() {
      this.visible = false;
    },
    onUser() {
      this.$router.push({
        name: "user"
      });
      this.visible = false;
    },
    onDB() {
      this.$router.push({
        name: "db"
      });
      this.visible = false;
    }
  },
  mounted() {
    this.currentTime();
  },
  beforeUnmount() {
    if (this.date) {
      clearInterval(this.date); // 在Vue实例销毁前，清除我们的定时器
    }
  }
};
</script>
<style scoped>
.ant-tag {
  color: rgba(255, 249, 249, 0.82);
  background: #fafafa00;
  border: 1px solid #fffefe00;
  font-size: 15px;
  padding: 6px 7px;
}

#components-layout-demo-top .ant-row .ant-col-6 .ant-row {
  line-height: 25px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
