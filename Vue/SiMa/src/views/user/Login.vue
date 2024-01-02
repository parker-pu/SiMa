<template>
  <div>
    <a-row>
      <a-col :span="10" :offset="7">
        <a-tabs>
          <a-tab-pane key="1" tab="登录">
            <a-form
              :model="loginForm"
              :rules="rules"
              ref="refLoginForm"
              labelAlign="left"
              :label-col="labelCol"
              :wrapper-col="wrapperCol"
            >
              <a-form-item label="用户名" name="username">
                <a-input v-model:value="loginForm.username"></a-input>
              </a-form-item>
              <a-form-item label="密码" name="password">
                <a-input-password
                  v-model:value="loginForm.password"
                  type="password"
                  autocomplete="off"
                ></a-input-password>
              </a-form-item>
              <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
                <a-button type="primary" @click="onSubmit">
                  提交
                </a-button>
                <a-button style="margin-left: 10px;" @click="resetForm">
                  重置
                </a-button>
              </a-form-item>
            </a-form>
          </a-tab-pane>
          <a-tab-pane key="2" tab="注册" force-render>
            暂无注册
          </a-tab-pane>
        </a-tabs>
      </a-col>
    </a-row>
  </div>
</template>
<script>
import { mapActions } from "vuex";
import { timeFix } from "../../utils/util";

export default {
  name: "login",
  // store,
  data() {
    let validatePass = async (rule, value) => {
      if (value === "") {
        return Promise.reject("Please input the password");
      } else {
        return Promise.resolve();
      }
    };

    return {
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
      activeName: "login", // 选项卡
      loginForm: {
        // 表单v-moda的值
        username: "",
        password: "",
        grant_type: "password",
        scope: "me"
      },
      rules: {
        username: [
          {
            required: true,
            message: "Please input user name",
            trigger: "blur"
          },
          {
            min: 1,
            max: 50,
            message: "Length should be 1 to 50",
            trigger: "blur"
          }
        ],
        password: [
          { required: true, validator: validatePass, trigger: "change" }
        ]
      }
    };
  },
  created() {},
  methods: {
    ...mapActions(["Login", "Logout"]),
    onSubmit() {
      this.$refs.refLoginForm
        .validate()
        .then(() => {
          this.Login(this.loginForm)
            .then(res => this.loginSuccess(res))
            .catch(err => this.requestFailed(err))
            .finally(() => {});
        })
        .catch(error => {
          console.log("error", error);
        });
    },
    resetForm() {
      this.$refs.refLoginForm.resetFields();
    },
    loginSuccess() {
      let redirectUrl = decodeURIComponent(this.$route.query.redirect || "/");
      // 跳转到指定的路由
      this.$router.push({
        path: redirectUrl
      });
      // 延迟 1 秒显示欢迎信息
      setTimeout(() => {
        this.$notification.success({
          message: "欢迎",
          description: `${timeFix()}，欢迎回来`
        });
      }, 1000);
    },
    requestFailed() {}
  }
};
</script>
<style scoped></style>
