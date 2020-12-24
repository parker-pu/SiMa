<template>
  <a-spin :spinning="spinning" tip="Loading...">
    <div
      id="tableList"
      v-for="line in search_result_data"
      :key="line.table_name"
    >
      <a-collapse>
        <a-collapse-panel
          :header="
            line.table_name +
              ' -> [' +
              line.db_type +
              '].[' +
              line.db_host +
              '].[' +
              line.db_name +
              '] -> [最近一次更新时间: ' +
              line.update_time +
              ']'
          "
        >
          <p style="white-space: pre-wrap;">
            {{ line.data }}
          </p>
          <template #extra>
            <RightCircleOutlined @click="tableInfo(line)" />
          </template>
        </a-collapse-panel>
      </a-collapse>
    </div>
  </a-spin>
</template>
<script>
import { searchDataApi } from "../../api/search";
import { RightCircleOutlined } from "@ant-design/icons-vue";

export default {
  name: "newTable",
  components: {
    RightCircleOutlined,
  },
  props: {
    new_search_data: String,
  },
  data() {
    return {
      search_data: "",
      search_result_data: [],
      spinning: false,
    };
  },
  created() {
    this.search_data = this.$route.query.search;
    this.searchData();
  },
  updated() {
    this.updateHandel();
  },
  methods: {
    tableInfo(data) {
      this.$router.push({
        name: "tableInfo",
        query: {
          db_host: data.db_host,
          db_port: data.db_port,
          db_type: data.db_type,
          db_name: data.db_name,
          table_name: data.table_name,
        },
      });
    },
    updateHandel() {
      if (this.search_data != this.new_search_data) {
        this.search_data = this.new_search_data;
        this.searchData();
      }
    },
    searchData() {
      this.spinning = true;
      searchDataApi(this.search_data)
        .then((res) => this.searchSuccess(res))
        .catch((err) => this.searchFailed(err))
        .finally(() => {});
      setTimeout(() => {
        this.spinning = false;
      }, 1000);
    },
    searchSuccess(res) {
      // 延迟 1 秒显示欢迎信息
      setTimeout(() => {
        this.$notification.success({
          message: "成功",
          description: "搜索成功",
        });
        this.search_result_data = res.data;
      }, 1000);
    },
    searchFailed(err) {
      this.$notification["error"]({
        message: "错误",
        description:
          ((err.response || {}).data || {}).message ||
          "请求出现错误，请稍后再试",
        duration: 4,
      });
    },
  },
};
</script>
<style>
.ant-list-bordered.ant-list-sm .ant-list-header,
.ant-list-bordered.ant-list-sm .ant-list-footer {
  padding: 8px 0px;
}
</style>
