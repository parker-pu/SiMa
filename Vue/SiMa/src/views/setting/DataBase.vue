<template>
  <a-button class="editable-add-btn" @click="handleAdd">
    增加
  </a-button>
  <a-table bordered :data-source="dataSource" :columns="columns">
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
          <a-button type="danger" size="default"
            ><ClearOutlined /> 删除</a-button
          >
        </a-popconfirm>
        <!-- edit -->
        <a-button size="default" @click="editDBConn(record)"
          ><EditOutlined />编辑</a-button
        >
      </a-space>
    </template>
  </a-table>

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
      <a-form
        :model="addDBForm"
        :label-col="labelCol"
        :wrapper-col="wrapperCol"
      >
        <a-form-item label="主机地址" name="db_host">
          <a-input v-model:value="addDBForm.db_host"></a-input>
        </a-form-item>
        <a-form-item label="数据库名称" name="db_name">
          <a-input v-model:value="addDBForm.db_name"></a-input>
        </a-form-item>
        <a-form-item label="端口" name="db_port">
          <a-input v-model:value="addDBForm.db_port"></a-input>
        </a-form-item>
        <a-form-item label="数据库类型" name="db_type">
          <div>
            <a-select
              v-model:value="addDBForm.db_type"
              style="width: 120px"
              ref="select"
              @change="handleChange"
            >
              <a-select-option value="mysql">
                mysql
              </a-select-option>
              <a-select-option value="es" disabled>
                es
              </a-select-option>
            </a-select>
          </div>
        </a-form-item>
        <a-form-item label="用户名" name="username">
          <a-input v-model:value="addDBForm.username"></a-input>
        </a-form-item>
        <a-form-item label="数据库密码" name="password">
          <a-input-password
            v-model:value="addDBForm.password"
            type="password"
            autocomplete="off"
          ></a-input-password>
        </a-form-item>
      </a-form>
    </a-modal>
  </a-spin>
</template>
<script>
import { getDBConnApi, addDBConnApi, delDBConnApi } from "../../api/db";
import { ClearOutlined, EditOutlined } from "@ant-design/icons-vue";
export default {
  components: {
    ClearOutlined,
    EditOutlined,
  },
  data() {
    return {
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
      loading: false,
      visible: false,
      spinning: false,
      addDBForm: {},
      dataSource: [],
      count: null,
      edidTitle: "新增",
      columns: [
        {
          title: "主机地址",
          dataIndex: "db_host",
          width: "10%",
          slots: { customRender: "db_host" },
        },
        {
          title: "数据库名称",
          dataIndex: "db_name",
        },
        {
          title: "端口",
          dataIndex: "db_port",
        },
        {
          title: "数据库类型",
          dataIndex: "db_type",
          slots: { customRender: "db_type" },
        },
        {
          title: "用户名",
          dataIndex: "username",
        },
        {
          title: "更新时间",
          dataIndex: "update_time",
        },
        {
          title: "操作",
          dataIndex: "operation",
          slots: { customRender: "operation" },
        },
      ],
    };
  },
  created() {
    this.getDBConnList();
  },
  methods: {
    getDBConnList() {
      getDBConnApi()
        .then((rsp) => {
          // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
          this.dataSource = rsp.data;
          this.count = rsp.total_nums;
        })
        .catch((error) => {
          // catch 指请求出错的处理
          console.log(error);
        });
    },
    onDelete(line) {
      this.spinning = true;
      delDBConnApi(line)
        .then((res) => this.delSuccess(res))
        .catch((err) => this.delFailed(err))
        .finally(() => {});
    },
    delSuccess() {
      // 延迟 1 秒显示欢迎信息
      setTimeout(() => {
        this.$notification.success({
          message: "删除",
          description: "删除成功",
        });

        // off
        this.spinning = false;
        this.getDBConnList();
      }, 1000);
    },
    delFailed(err) {
      this.$notification["error"]({
        message: "错误",
        description:
          ((err.response || {}).data || {}).message ||
          "请求出现错误，请稍后再试",
        duration: 4,
      });

      // off
      this.spinning = false;
    },
    handleAdd() {
      this.visible = true;
    },
    resetCancel() {
      this.addDBForm = {};
    },
    handleOk() {
      this.loading = true;
      this.addDB();
    },
    handleCancel() {
      this.visible = false;
    },
    addDB() {
      addDBConnApi(this.addDBForm)
        .then((res) => this.addSuccess(res))
        .catch((err) => this.addFailed(err))
        .finally(() => {});
    },
    addSuccess() {
      // 延迟 1 秒显示欢迎信息
      setTimeout(() => {
        this.$notification.success({
          message: "成功",
          description: "添加成功",
        });

        // off
        this.visible = false;
        this.loading = false;
        this.getDBConnList();
      }, 1000);
    },
    addFailed(err) {
      this.$notification["error"]({
        message: "错误",
        description:
          ((err.response || {}).data || {}).message ||
          "请求出现错误，请稍后再试",
        duration: 4,
      });

      // off
      this.visible = false;
      this.loading = false;
    },
    editDBConn(line) {
      this.visible = true;
      this.edidTitle = "编辑";
      this.addDBForm = line;
    },
  },
};
</script>
<style lang="less">
.editable-cell {
  position: relative;
  .editable-cell-input-wrapper,
  .editable-cell-text-wrapper {
    padding-right: 24px;
  }

  .editable-cell-text-wrapper {
    padding: 5px 24px 5px 5px;
  }

  .editable-cell-icon,
  .editable-cell-icon-check {
    position: absolute;
    right: 0;
    width: 20px;
    cursor: pointer;
  }

  .editable-cell-icon {
    line-height: 18px;
    display: none;
  }

  .editable-cell-icon-check {
    line-height: 28px;
  }

  .editable-cell-icon:hover,
  .editable-cell-icon-check:hover {
    color: #108ee9;
  }

  .editable-add-btn {
    margin-bottom: 8px;
  }
}
.editable-cell:hover .editable-cell-icon {
  display: inline-block;
}
</style>
