<template>
  <a-row>
    <a-col :span="8"> </a-col>
    <a-col :span="8" id="init">
      <a-form
        ref="ruleForm"
        :model="form"
        :rules="rules"
        :label-col="labelCol"
        :wrapper-col="wrapperCol"
      >
        <a-form-item
          ref="setting_es_host"
          label="ES 地址"
          name="setting_es_host"
        >
          <a-input v-model:value="form.init_data.setting_es_host" />
        </a-form-item>
        <a-form-item
          ref="setting_es_port"
          label="ES 端口"
          name="setting_es_port"
        >
          <a-input v-model:value="form.init_data.setting_es_port" />
        </a-form-item>
        <a-form-item ref="username" label="超级用户名" name="username">
          <a-input v-model:value="form.user.username" />
        </a-form-item>
        <a-form-item label="超级用户密码" name="password">
          <a-input-password
            v-model:value="form.user.password"
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
    </a-col>
    <a-col :span="8"> </a-col>
  </a-row>
</template>
<script>
import { initSuperUserApi } from "../../api/superUser";

export default {
  name: "superUser",
  data() {
    return {
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
      form: {
        init_data: {},
        user: {},
      },
      rules: {},
    };
  },
  methods: {
    onSubmit() {
      initSuperUserApi(this.form)
        .then(() => {
          this.$notification.success({
            message: "初始化",
            description: "初始化成功",
          });

          this.$router.push({
            name: "login",
          });
        })
        .catch(() => {})
        .finally(() => {});
    },
    resetForm() {
      this.$refs.ruleForm.resetFields();
    },
  },
};
</script>
<style>
#init {
  margin: 100px 2px 2px 0;
}
</style>
