<template>
  <a-spin :spinning="useSpinning">
    <a-button class="editable-add-btn" @click="handleAdd">
      增加
    </a-button>
    <a-table bordered :data-source="dataSource" :columns="columns">
      <template #disabled="{ text }">
        <span>
          <CloseCircleOutlined
            v-if="text === false"
            :style="{ fontSize: '16px', color: '#FF0000' }"
          />
          <CheckOutlined
            v-if="text === true"
            :style="{ fontSize: '16px', color: '#00FF00' }"
          />
        </span>
      </template>
      <template #superuser="{ text }">
        <span>
          <CloseCircleOutlined
            v-if="text === false"
            :style="{ fontSize: '16px', color: '#FF0000' }"
          />
          <CheckOutlined
            v-if="text === true"
            :style="{ fontSize: '16px', color: '#00FF00' }"
          />
        </span>
      </template>
      <template #operation="{ record  }">
        <a-space size="small">
          <!-- del -->
          <a-popconfirm
            v-if="count"
            title="确定删除吗?"
            ok-text="是"
            cancel-text="否"
            @confirm="onDelete(record)"
          >
            <a-button type="danger" size="default"><ClearOutlined /> 删除</a-button>
          </a-popconfirm>
          <!-- edit -->
          <a-button size="default" @click="editUser(record)"><EditOutlined />编辑</a-button>
        </a-space>
      </template>
    </a-table>
  </a-spin>

  <!-- user -->
  <a-spin :spinning="spinning">
    <a-modal v-model:visible="visible" :title="edidTitle" @ok="handleOk">
      <template #footer>
        <a-button key="back" @click="handleCancel">
          取消
        </a-button>
        <a-button key="back" @click="resetCancel">
          重置
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
      <a-form :model="addUser" :label-col="labelCol" :wrapper-col="wrapperCol">
        <a-form-item label="用户名" name="username">
          <a-input v-model:value="addUser.username"></a-input>
        </a-form-item>
        <a-form-item label="Email" name="email">
          <a-input v-model:value="addUser.email"></a-input>
        </a-form-item>
        <a-form-item label="全名" name="full_name">
          <a-input v-model:value="addUser.full_name"></a-input>
        </a-form-item>
        <a-form-item label="失效" name="disabled">
          <a-switch v-model:checked="addUser.disabled" />
        </a-form-item>
        <a-form-item label="超级用户" name="superuser">
          <a-switch v-model:checked="addUser.superuser" />
        </a-form-item>
        <a-form-item label="密码" name="password">
          <a-input-password
            v-model:value="addUser.password"
            type="password"
            autocomplete="off"
          ></a-input-password>
        </a-form-item>
      </a-form>
    </a-modal>
  </a-spin>
</template>

<script>
import { getUserApi, putUserApi,addUserApi, delUserApi } from "../../api/user";
import {
  CloseCircleOutlined,
  EditOutlined,
  CheckOutlined,
  ClearOutlined
} from "@ant-design/icons-vue";
export default {
  components: {
    CloseCircleOutlined,
    EditOutlined,
    ClearOutlined,
    CheckOutlined
  },
  data() {
    return {
      labelCol: { span: 6 },
      wrapperCol: { span: 14 },
      count: null,
      useSpinning: false,
      spinning: false,
      visible: false,
      loading: false,
      addUser: {},
      edidTitle: "新增",
      dataSource: [],
      columns: [
        {
          title: "用户名",
          dataIndex: "username",
          width: "10%",
          slots: { title: "customTitle", customRender: "username" }
        },
        {
          title: "Email",
          dataIndex: "email"
        },
        {
          title: "全名",
          dataIndex: "full_name"
        },
        {
          title: "失效",
          dataIndex: "disabled",
          slots: { customRender: "disabled" }
        },
        {
          title: "超级用户",
          dataIndex: "superuser",
          slots: { customRender: "superuser" }
        },
        {
          title: "更新时间",
          dataIndex: "update_time"
        },
        {
          title: "操作",
          dataIndex: "operation",
          slots: { customRender: "operation" }
        }
      ]
    };
  },
  created() {
    this.getUserList();
  },
  methods: {
    handleAdd() {
      this.edidTitle= "新增"
      this.visible = true;
      this.addUser = {}
    },
    onDelete(line) {
      this.useSpinning = true;
      delUserApi(line)
        .then(res => this.delSuccess(res))
        .catch(err => this.delFailed(err))
        .finally(() => {});
    },
    delSuccess() {
      // 延迟 1 秒显示欢迎信息
      setTimeout(() => {
        this.$notification.success({
          message: "删除",
          description: "删除成功"
        });

        // off
        this.useSpinning = false;
        this.getUserList();
      }, 1000);
    },
    delFailed(err) {
      this.$notification["error"]({
        message: "错误",
        description:
          ((err.response || {}).data || {}).message ||
          "请求出现错误，请稍后再试",
        duration: 4
      });

      // off
      this.useSpinning = false;
    },
    editUser(record) {
      this.edidTitle = "编辑";
      this.addUser = record;
      this.visible = true;
    },
    handleOk() {
      this.loading = true;
      var pa = putUserApi
      if(this.edidTitle == "新增"){pa = addUserApi}
      pa(this.addUser)
        .then(() => this.getUserList())
        .catch()
        .finally(() => {
          setTimeout(() => {
            this.visible = false;
            this.loading = false;
          }, 500);
        });
    },
    handleCancel() {
      this.visible = false;
    },
    resetCancel() {
      this.addUser = {};
    },
    getUserList() {
      this.useSpinning = true;
      setTimeout(() => {
        getUserApi()
          .then(rsp => {
            this.dataSource = rsp.data;
            this.count = this.dataSource.length;
          })
          .catch(() => {})
          .finally(() => {
            this.useSpinning = false;
          });
      }, 1000);
    }
  },
  mounted() {},
  beforeUnmount() {}
};
</script>
<style scoped></style>
